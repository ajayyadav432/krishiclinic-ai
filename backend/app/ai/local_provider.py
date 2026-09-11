import io
import os
import json
import logging
from pathlib import Path
from app.ai.base import AIProvider, PredictionResult

logger = logging.getLogger(__name__)

HF_REPO_ID = "the-harsh-vardhan/krishiclinic-crop-disease-v0-1-baseline-bmd"
MODEL_FILENAME = "model.pt"
METADATA_FILENAME = "metadata.json"

ADVISORY_LOOKUP = {
    "bacterial_blight": {
        "disease_name": "Bacterial Blight",
        "severity": "Medium",
        "recommendation": "Avoid overhead irrigation to reduce humidity. Spray Copper Oxychloride at 2g/L or streptocycline at 100ppm if infection is severe. Implement crop rotation with non-legumes next season.",
        "possible_reasons": "High leaf wetness, persistent warm temperatures, splashing rain, or use of infected seeds."
    },
    "cercospora_leaf_blight": {
        "disease_name": "Cercospora Leaf Blight",
        "severity": "Medium",
        "recommendation": "Apply foliar fungicides such as strobilurins (e.g. Pyraclostrobin) or triazoles at early bloom (R1-R3 stage). Use certified disease-free seeds and plow under crop residue.",
        "possible_reasons": "Warm weather (25-30°C) combined with high relative humidity and extended periods of dew."
    },
    "downey_mildew": {
        "disease_name": "Downy Mildew",
        "severity": "Low",
        "recommendation": "Maintain wider row spacing to improve air circulation. Apply metalaxyl or mancozeb fungicide at 2g/L if infection spreads rapidly. Plant resistant varieties.",
        "possible_reasons": "Cool, humid weather conditions and persistent leaf wetness."
    },
    "frogeye": {
        "disease_name": "Frogeye Leaf Spot",
        "severity": "Medium",
        "recommendation": "Apply quinone outside inhibitor (QoI) or methyl benzimidazole carbamate (MBC) fungicides. Plant resistant cultivars and practice crop rotation.",
        "possible_reasons": "Warm, humid weather conditions (25-30°C) and infected crop residues left on the soil surface."
    },
    "healthy": {
        "disease_name": "Healthy",
        "severity": "Low",
        "recommendation": "No disease detected. Continue normal agronomic practices: ensure proper irrigation, balanced N-P-K fertilization, and conduct regular field scouting.",
        "possible_reasons": "Favorable growing conditions, proper nutrition, and robust crop resistance."
    },
    "potassium_deficiency": {
        "disease_name": "Potassium Deficiency",
        "severity": "Low",
        "recommendation": "Apply potassium-rich fertilizers (such as Muriate of Potash, K2O) based on soil test recommendations. Ensure soil compaction is minimized to promote root health.",
        "possible_reasons": "Low soil potassium levels, poor root development due to soil compaction, or dry soil conditions limiting nutrient uptake."
    },
    "soybean_rust": {
        "disease_name": "Soybean Rust",
        "severity": "High",
        "recommendation": "Immediately spray triazole or strobilurin-based fungicides (e.g., Tebuconazole at 1ml/L or Propiconazole). Monitor field daily as the disease spreads rapidly.",
        "possible_reasons": "Prolonged leaf wetness (6-12 hours), moderate temperatures (15-28°C), and airborne spores carried from infected regions."
    },
    "target_spot": {
        "disease_name": "Target Spot",
        "severity": "Medium",
        "recommendation": "Apply fluxapyroxad or prothioconazole fungicides if disease reaches lower canopy early. Practice crop rotation with corn or wheat, and manage weeds.",
        "possible_reasons": "High humidity (>80%) and warm temperatures (25-33°C) combined with susceptible crop varieties."
    }
}

class LocalPyTorchProvider(AIProvider):

    def __init__(self):
        self._model = None
        self._class_names = None
        self._transform = None
        self._device = None
        self._weights_dir = Path(__file__).resolve().parent / "weights"
        self._weights_dir.mkdir(exist_ok=True)

    @property
    def provider_name(self) -> str:
        return "local"

    def _initialize_model(self):
        if self._model is not None:
            return

        try:
            import torch
            import timm
            from torchvision import transforms
            from PIL import Image
            from huggingface_hub import hf_hub_download
        except ImportError as e:
            logger.error("Failed to import PyTorch, torchvision, timm, or huggingface_hub", exc_info=True)
            raise RuntimeError(
                f"Local PyTorch provider dependencies are missing: {e}. "
                "Ensure torch, torchvision, timm, and huggingface_hub are installed."
            ) from e

        if torch.cuda.is_available():
            self._device = torch.device("cuda")
        else:
            self._device = torch.device("cpu")
        logger.info(f"Using device for local PyTorch inference: {self._device}")

        model_path = self._weights_dir / MODEL_FILENAME
        metadata_path = self._weights_dir / METADATA_FILENAME

        if not model_path.exists() or not metadata_path.exists():
            logger.info(f"Downloading model weights and metadata from Hugging Face: {HF_REPO_ID}")
            try:
                hf_hub_download(repo_id=HF_REPO_ID, filename=MODEL_FILENAME, local_dir=str(self._weights_dir))
                hf_hub_download(repo_id=HF_REPO_ID, filename=METADATA_FILENAME, local_dir=str(self._weights_dir))
            except Exception as e:
                logger.error(f"Failed to download model weights from Hugging Face Hub: {e}", exc_info=True)
                raise RuntimeError(
                    f"Model weights not found in {self._weights_dir} and offline fallback download failed: {e}. "
                    "Ensure weights (model.pt and metadata.json) are bundled in app/ai/weights at build time for zero-network operation."
                ) from e

        with open(metadata_path, encoding="utf-8") as f:
            metadata = json.load(f)
            self._class_names = metadata["class_names"]

        logger.info("Initializing EfficientNetV2-S model and loading weights...")
        self._model = timm.create_model(
            "tf_efficientnetv2_s",
            pretrained=False,
            num_classes=len(self._class_names)
        )
        state_dict = torch.load(model_path, map_location=self._device)
        self._model.load_state_dict(state_dict)
        self._model.to(self._device)
        self._model.eval()

        self._transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        logger.info("Local PyTorch model initialized successfully.")

    async def analyze(
        self,
        image: bytes,
        crop_type: str,
        farmer_notes: str | None = None,
    ) -> PredictionResult:
        self._initialize_model()

        import torch
        from PIL import Image

        try:
            pil_image = Image.open(io.BytesIO(image)).convert("RGB")
            tensor = self._transform(pil_image).unsqueeze(0).to(self._device)

            with torch.no_grad():
                logits = self._model(tensor)
                probs = torch.softmax(logits, dim=1)[0]

            top_prob, top_idx = torch.max(probs, dim=0)
            confidence = float(top_prob.item())
            predicted_class = self._class_names[top_idx.item()]

            advisory = ADVISORY_LOOKUP.get(
                predicted_class,
                {
                    "disease_name": predicted_class.replace("_", " ").title(),
                    "severity": "Medium",
                    "recommendation": "Scout the field regularly. Consult an agronomist for detailed treatment options.",
                    "possible_reasons": "Environmental stressors or crop pathogens."
                }
            )

            if predicted_class == "healthy":
                return PredictionResult(
                    predicted_disease="Healthy",
                    confidence=confidence,
                    severity="Low",
                    recommendation=advisory["recommendation"],
                    possible_reasons=advisory["possible_reasons"]
                )

            return PredictionResult(
                predicted_disease=advisory["disease_name"],
                confidence=confidence,
                severity=advisory["severity"],
                recommendation=advisory["recommendation"],
                possible_reasons=advisory["possible_reasons"]
            )

        except Exception as e:
            logger.error(f"Local PyTorch inference failed: {e}", exc_info=True)
            raise RuntimeError(f"Local AI model inference failed: {e}") from e
