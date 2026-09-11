import pytest
from unittest.mock import MagicMock, patch
from app.ai.local_provider import LocalPyTorchProvider
from app.ai.base import PredictionResult

def test_local_provider_name():
    provider = LocalPyTorchProvider()
    assert provider.provider_name == "local"

@pytest.mark.asyncio
@patch("huggingface_hub.hf_hub_download")
@patch("timm.create_model")
@patch("torch.load")
async def test_local_provider_initialize_and_predict(mock_torch_load, mock_create_model, mock_hf_download):
    mock_hf_download.return_value = "/tmp/dummy_path"

    mock_model = MagicMock()
    mock_logits = MagicMock()
    mock_model.return_value = mock_logits
    mock_create_model.return_value = mock_model

    mock_torch_load.return_value = {}

    provider = LocalPyTorchProvider()
    provider._class_names = ["bacterial_blight", "healthy", "soybean_rust"]
    provider._weights_dir = MagicMock()

    from PIL import Image
    import io
    import torch

    img = Image.new("RGB", (100, 100), color="green")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="JPEG")
    img_bytes = img_byte_arr.getvalue()

    provider._transform = MagicMock()
    mock_tensor = MagicMock()
    provider._transform.return_value = mock_tensor

    provider._device = torch.device("cpu")

    provider._model = mock_model

    with patch("torch.softmax") as mock_softmax, patch("torch.max") as mock_max:
        mock_probs = MagicMock()
        mock_softmax.return_value = mock_probs
        
        mock_max_val = MagicMock()
        mock_max_idx = MagicMock()
        mock_max_val.item.return_value = 0.95
        mock_max_idx.item.return_value = 2
        mock_max.return_value = (mock_max_val, mock_max_idx)

        result = await provider.analyze(img_bytes, "Soybean", "yellow spots")

        assert isinstance(result, PredictionResult)
        assert result.predicted_disease == "Soybean Rust"
        assert result.confidence == 0.95
        assert result.severity == "High"
        assert "Tebuconazole" in result.recommendation
