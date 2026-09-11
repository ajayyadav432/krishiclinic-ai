"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { getPrediction, getImageUrl, downloadPdf, uploadFollowup } from "@/lib/api";
import type { Prediction } from "@/lib/types";
import { useApp } from "@/context/AppContext";
import AuthPage from "@/components/AuthPage";
import AudioPlayer from "@/components/AudioPlayer";

function SeverityBadge({ severity, t }: { severity: string | null; t: any }) {
  if (!severity) return null;
  const translated = t(severity);
  const cls =
    severity === "High"
      ? "badge-high"
      : severity === "Medium"
      ? "badge-medium"
      : "badge-low";
  return <span className={`badge ${cls}`}>{translated}</span>;
}

function ConfidenceBar({ confidence, t }: { confidence: number; t: any }) {
  const percentage = Math.round(confidence * 100);
  const cls =
    confidence >= 0.85
      ? "confidence-high"
      : confidence >= 0.65
      ? "confidence-medium"
      : "confidence-low";

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.375rem" }}>
        <span style={{ fontSize: "0.8125rem", color: "var(--color-text-muted)" }}>
          {t("Confidence")}
        </span>
        <span style={{ fontSize: "0.875rem", fontWeight: 700, color: "var(--color-primary)" }}>
          {percentage}%
        </span>
      </div>
      <div className="confidence-bar">
        <div className={`confidence-fill ${cls}`} style={{ width: `${percentage}%` }} />
      </div>
    </div>
  );
}

export default function PredictionDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;
  const { user, isInitialized, t, translateDynamic, language } = useApp();

  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [transDisease, setTransDisease] = useState("");
  const [transRecommendation, setTransRecommendation] = useState("");
  const [transNotes, setTransNotes] = useState("");
  const [transReasons, setTransReasons] = useState("");
  const [pdfLoading, setPdfLoading] = useState(false);

  const [followupFile, setFollowupFile] = useState<File | null>(null);
  const [followupNotes, setFollowupNotes] = useState("");
  const [followupLoading, setFollowupLoading] = useState(false);
  const [followupError, setFollowupError] = useState<string | null>(null);

  const handleFollowupSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!followupFile) return;
    setFollowupLoading(true);
    setFollowupError(null);
    try {
      const updated = await uploadFollowup(id, followupFile, followupNotes);
      setPrediction(updated);
      setFollowupFile(null);
      setFollowupNotes("");
    } catch (err: any) {
      setFollowupError(err?.detail?.message || err?.message || "Failed to upload follow-up image");
    } finally {
      setFollowupLoading(false);
    }
  };

  useEffect(() => {
    async function fetchPrediction() {
      if (!user) return;
      try {
        const data = await getPrediction(id);
        setPrediction(data);
        
        const [d, r, n, pr] = await Promise.all([
          translateDynamic(data.predicted_disease),
          translateDynamic(data.recommendation || ""),
          translateDynamic(data.farmer_notes || ""),
          translateDynamic(data.possible_reasons || ""),
        ]);
        setTransDisease(d);
        setTransRecommendation(r);
        setTransNotes(n);
        setTransReasons(pr);
      } catch (err) {
        setError(err instanceof Error ? err.message : t("Failed to load prediction."));
      } finally {
        setLoading(false);
      }
    }
    
    if (user) {
      fetchPrediction();
    }
  }, [id, user, language]);

  if (!isInitialized) {
    return (
      <div className="page-container">
        <div style={{ maxWidth: "800px", margin: "0 auto" }}>
          <div className="skeleton" style={{ height: "32px", width: "200px", marginBottom: "1.5rem" }} />
          <div className="card" style={{ padding: "2rem" }}>
            <div className="skeleton" style={{ height: "300px", marginBottom: "1.5rem", borderRadius: "var(--radius-md)" }} />
          </div>
        </div>
      </div>
    );
  }

  if (!user) {
    return <AuthPage />;
  }

  if (loading) {
    return (
      <div className="page-container">
        <div style={{ maxWidth: "800px", margin: "0 auto" }}>
          <div className="skeleton" style={{ height: "32px", width: "200px", marginBottom: "1.5rem" }} />
          <div className="card" style={{ padding: "2rem" }}>
            <div className="skeleton" style={{ height: "300px", marginBottom: "1.5rem", borderRadius: "var(--radius-md)" }} />
            <div className="skeleton" style={{ height: "20px", width: "60%", marginBottom: "0.75rem" }} />
            <div className="skeleton" style={{ height: "20px", width: "40%", marginBottom: "0.75rem" }} />
            <div className="skeleton" style={{ height: "20px", width: "80%" }} />
          </div>
        </div>
      </div>
    );
  }

  if (error || !prediction) {
    return (
      <div className="page-container">
        <div className="empty-state">
          <div className="empty-state-icon"></div>
          <h2 style={{ fontWeight: 600, marginBottom: "0.5rem" }}>{t("Prediction Not Found")}</h2>
          <p>{error || t("The prediction you're looking for doesn't exist.")}</p>
          <Link href="/history" className="btn btn-primary" style={{ marginTop: "1rem" }}>
            ← {t("Back to History")}
          </Link>
        </div>
      </div>
    );
  }

  const formattedDate = new Date(prediction.created_at).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  const isPending = prediction.status === "PENDING_REVIEW";

  return (
    <div className="page-container">
      <div style={{ maxWidth: "800px", margin: "0 auto" }}>
        <div className="breadcrumb-row" style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.5rem", flexWrap: "wrap", gap: "0.75rem" }}>
          <Link href="/history" style={{ color: "var(--color-primary)", textDecoration: "none", fontSize: "0.875rem", fontWeight: 600 }}>
            ← {t("Back to History")}
          </Link>
          <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
            <AudioPlayer
              text={
                language === "hi"
                  ? `फसल: ${t(prediction.crop_type)}। निदान: ${transDisease || t(prediction.predicted_disease)}। तीव्रता: ${t(prediction.severity || "")}। उपचार सलाह: ${transRecommendation || prediction.recommendation || "विशेषज्ञ से परामर्श करें"}।`
                  : language === "te"
                  ? `పంట: ${t(prediction.crop_type)}. నిర్ధారణ: ${transDisease || t(prediction.predicted_disease)}. తీవ్రత: ${t(prediction.severity || "")}. చికిత్స సలహా: ${transRecommendation || prediction.recommendation || "నిపుణులను సంప్రదించండి"}.`
                  : language === "mr"
                  ? `पीक: ${t(prediction.crop_type)}. निदान: ${transDisease || t(prediction.predicted_disease)}. तीव्रता: ${t(prediction.severity || "")}. उपचार सल्ला: ${transRecommendation || prediction.recommendation || "तज्ज्ञांचा सल्ला घ्या"}.`
                  : language === "es"
                  ? `Cultivo: ${t(prediction.crop_type)}. Diagnóstico: ${transDisease || t(prediction.predicted_disease)}. Severidad: ${t(prediction.severity || "")}. Recomendación: ${transRecommendation || prediction.recommendation || "Consulte a un especialista"}.`
                  : `Crop: ${prediction.crop_type}. Diagnosis: ${transDisease || prediction.predicted_disease}. Severity: ${prediction.severity || "Standard"}. Treatment recommendation: ${transRecommendation || prediction.recommendation || "Consult local specialist"}.`
              }
              language={language}
              label={t("Voice Advisory")}
            />
            <button
              onClick={async () => {
                setPdfLoading(true);
                try {
                  await downloadPdf(id);
                } catch (e) {
                  alert(t("Failed to download PDF advisory card"));
                } finally {
                  setPdfLoading(false);
                }
              }}
              disabled={pdfLoading}
              className="btn btn-primary"
              style={{ padding: "0.5rem 1rem", fontSize: "0.8125rem" }}
            >
              {pdfLoading ? t("Exporting...") : t("Export PDF Advisory")}
            </button>
          </div>
        </div>

        {isPending && user.role !== "AGRONOMIST" && (
          <div
            style={{
              background: "#fffbeb",
              border: "1px solid #fef3c7",
              color: "#b45309",
              padding: "1rem 1.25rem",
              borderRadius: "var(--radius-md)",
              marginBottom: "1.5rem",
              fontSize: "0.875rem",
              display: "flex",
              alignItems: "center",
              gap: "0.75rem",
            }}
          >
            <span style={{ fontSize: "1.25rem" }}>ℹ️</span>
            <div>
              <strong>{t("Pending Review")}:</strong> {t("Our agronomist is currently reviewing this prediction. The diagnosis below is locked until verified.")}
            </div>
          </div>
        )}

        <div className="page-header">
          <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", flexWrap: "wrap" }}>
            <h1 className="page-title">{transDisease || t(prediction.predicted_disease)}</h1>
            <SeverityBadge severity={prediction.severity} t={t} />
            <span
              className={`badge`}
              style={{
                background: isPending ? "#fef3c7" : "#dcfce7",
                color: isPending ? "#b45309" : "#15803d",
                fontSize: "0.75rem",
                fontWeight: 600,
              }}
            >
              {isPending ? t("Pending Review") : t("Verified")}
            </span>
          </div>
          <p className="page-subtitle">
            {t(prediction.crop_type)} · {t("Analyzed on")} {formattedDate}
            {prediction.location && ` ·  ${prediction.location}`}
            {prediction.language && ` ·  ${prediction.language}`}
          </p>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr", gap: "1.5rem" }}>
          {prediction.image_filename && (
            prediction.after_image_filename ? (
              <div className="card" style={{ padding: "1.25rem" }}>
                <h3 style={{ fontWeight: 600, marginBottom: "1rem", fontSize: "1rem", display: "flex", alignItems: "center", gap: "0.5rem" }}>
                   {t("Recovery Tracker (Before vs After)")}
                </h3>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1.25rem" }} className="results-grid">
                  <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                    <span style={{ fontSize: "0.75rem", fontWeight: 700, color: "var(--color-danger)", textTransform: "uppercase" }}>
                       {t("Before Treatment")}
                    </span>
                    <div style={{ overflow: "hidden", borderRadius: "var(--radius-md)", border: "1px solid var(--color-border)" }}>
                      <img
                        src={getImageUrl(prediction.image_filename)}
                        alt="Before treatment"
                        style={{ width: "100%", height: "240px", objectFit: "cover", background: "#f8f9fa" }}
                      />
                    </div>
                  </div>

                  <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                    <span style={{ fontSize: "0.75rem", fontWeight: 700, color: "var(--color-success)", textTransform: "uppercase" }}>
                       {t("After Treatment")}
                    </span>
                    <div style={{ overflow: "hidden", borderRadius: "var(--radius-md)", border: "1px solid var(--color-border)" }}>
                      <img
                        src={getImageUrl(prediction.after_image_filename)}
                        alt="After treatment"
                        style={{ width: "100%", height: "240px", objectFit: "cover", background: "#f8f9fa" }}
                      />
                    </div>
                  </div>
                </div>

                {prediction.after_notes && (
                  <div style={{ marginTop: "1rem", background: "var(--color-bg-secondary)", padding: "1rem", borderRadius: "var(--radius-md)", border: "1px solid var(--color-border-light)" }}>
                    <strong style={{ fontSize: "0.8125rem", color: "var(--color-text-secondary)", display: "block" }}>
                       {t("Farmer Recovery Notes:")}
                    </strong>
                    <p style={{ fontSize: "0.875rem", color: "var(--color-text)", marginTop: "0.25rem", fontStyle: "italic" }}>
                      &ldquo;{prediction.after_notes}&rdquo;
                    </p>
                  </div>
                )}
              </div>
            ) : (
              <div className="card" style={{ overflow: "hidden" }}>
                <img
                  src={getImageUrl(prediction.image_filename)}
                  alt={`${prediction.crop_type} sample`}
                  style={{
                    width: "100%",
                    maxHeight: "400px",
                    objectFit: "contain",
                    background: "#f8f9fa",
                  }}
                  onError={(e) => {
                    (e.target as HTMLImageElement).style.display = "none";
                  }}
                />
              </div>
            )
          )}

          <div className="results-grid" style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "1rem" }}>
            <div className="card" style={{ padding: "1.25rem" }}>
              <ConfidenceBar confidence={prediction.confidence} t={t} />
            </div>

            <div className="stat-card">
              <div className="stat-label">{t("Crop Type")}</div>
              <div style={{ fontSize: "1.25rem", fontWeight: 700, color: "var(--color-text)", marginTop: "0.25rem" }}>
                {t(prediction.crop_type)}
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-label">{t("AI Provider")}</div>
              <div style={{ fontSize: "1.25rem", fontWeight: 700, color: "var(--color-text)", marginTop: "0.25rem", textTransform: "capitalize" }}>
                {prediction.ai_provider === "Hidden" ? t("Pending Review") : t(prediction.ai_provider)}
              </div>
            </div>
          </div>

          {(prediction.possible_reasons || transReasons) && prediction.possible_reasons !== "Pending Review" && (
            <div className="card" style={{ padding: "1.5rem", borderLeft: "4px solid #ffba08" }}>
              <h3 style={{ fontWeight: 600, marginBottom: "0.75rem", display: "flex", alignItems: "center", gap: "0.5rem", color: "#92400e" }}>
                 {t("Possible Reasons")}
              </h3>
              <p style={{ color: "var(--color-text-secondary)", lineHeight: 1.7 }}>
                {transReasons || prediction.possible_reasons}
              </p>
            </div>
          )}

          {(prediction.recommendation || transRecommendation) && (
            <div className="card" style={{ padding: "1.5rem" }}>
              <h3 style={{ fontWeight: 600, marginBottom: "0.75rem", display: "flex", alignItems: "center", gap: "0.5rem" }}>
                 {prediction.status === "REVIEWED" ? t("Verified Advisory") : t("Treatment Recommendation")}
              </h3>
              <p style={{ color: "var(--color-text-secondary)", lineHeight: 1.7 }}>
                {transRecommendation || prediction.recommendation}
              </p>
            </div>
          )}

          {(prediction.farmer_notes || transNotes) && (
            <div className="card" style={{ padding: "1.5rem" }}>
              <h3 style={{ fontWeight: 600, marginBottom: "0.75rem", display: "flex", alignItems: "center", gap: "0.5rem" }}>
                 {t("Farmer Notes")}
              </h3>
              <p style={{ color: "var(--color-text-secondary)", lineHeight: 1.7, fontStyle: "italic" }}>
                &ldquo;{transNotes || prediction.farmer_notes}&rdquo;
              </p>
            </div>
          )}

          {user.role === "FARMER" && prediction.farmer_id === user.id && !prediction.after_image_filename && (
            <div className="card" style={{ padding: "1.5rem", border: "1px dashed var(--color-primary-light)", background: "rgba(76, 175, 80, 0.03)" }}>
              <h3 style={{ fontWeight: 700, marginBottom: "0.5rem", display: "flex", alignItems: "center", gap: "0.5rem", color: "var(--color-primary-dark)" }}>
                 {t("Track Treatment Success")}
              </h3>
              <p style={{ fontSize: "0.8125rem", color: "var(--color-text-secondary)", marginBottom: "1rem" }}>
                {t("Have you applied the recommended treatment? Upload a follow-up photo to track recovery progress and see before-vs-after status.")}
              </p>

              <form onSubmit={handleFollowupSubmit} style={{ display: "flex", flexDirection: "column", gap: "0.875rem" }}>
                <div>
                  <label className="label">{t("Follow-up Image")}</label>
                  <input
                    type="file"
                    accept="image/jpeg,image/png,image/webp"
                    onChange={(e) => setFollowupFile(e.target.files?.[0] || null)}
                    className="input"
                    required
                    style={{ background: "white" }}
                  />
                </div>
                <div>
                  <label className="label">{t("Recovery Observations")}</label>
                  <textarea
                    value={followupNotes}
                    onChange={(e) => setFollowupNotes(e.target.value)}
                    placeholder={t("Describe the crop health now (e.g., spots disappearing, new leaves sprouting, yellowing reduced)")}
                    className="textarea"
                    rows={3}
                    style={{ background: "white" }}
                  />
                </div>

                {followupError && (
                  <div style={{ color: "var(--color-danger)", fontSize: "0.8125rem", fontWeight: 600 }}>
                     {followupError}
                  </div>
                )}

                <button
                  type="submit"
                  disabled={followupLoading || !followupFile}
                  className="btn btn-primary"
                  style={{ alignSelf: "flex-start", marginTop: "0.5rem" }}
                >
                   {followupLoading ? t("Uploading...") : t("Update Recovery Status")}
                </button>
              </form>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
