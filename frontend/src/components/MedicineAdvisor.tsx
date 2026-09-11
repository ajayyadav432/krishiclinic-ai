"use client";

import { useState, useEffect } from "react";
import { getMedicineDiseases, getMedicineTreatment } from "@/lib/api";
import { useApp } from "@/context/AppContext";

interface TreatmentDetail {
  chemical: string;
  fungicide: string;
  organic: string;
  dose: string;
  frequency: string;
  notes: string;
}

interface AllStagesTreatment {
  sowing?: TreatmentDetail;
  mid_season?: TreatmentDetail;
  pre_harvest?: TreatmentDetail;
}

interface MedicineAdvisorProps {
  cropType: string;
  detectedDisease?: string;
  onApply?: (text: string) => void;
}

const STAGE_LABELS: Record<string, string> = {
  sowing: "🌱 Sowing Stage",
  mid_season: "🌿 Mid-Season",
  pre_harvest: "🌾 Pre-Harvest",
};

const STAGE_COLORS: Record<string, string> = {
  sowing: "#dcfce7",
  mid_season: "#dbeafe",
  pre_harvest: "#fef3c7",
};

const STAGE_BORDER_COLORS: Record<string, string> = {
  sowing: "#86efac",
  mid_season: "#93c5fd",
  pre_harvest: "#fcd34d",
};

export default function MedicineAdvisor({
  cropType,
  detectedDisease,
  onApply,
}: MedicineAdvisorProps) {
  const { t } = useApp();
  const [diseases, setDiseases] = useState<string[]>([]);
  const [selectedDisease, setSelectedDisease] = useState(detectedDisease || "");
  const [treatment, setTreatment] = useState<AllStagesTreatment | null>(null);
  const [activeStage, setActiveStage] = useState<string>("mid_season");
  const [loading, setLoading] = useState(false);
  const [loadingDiseases, setLoadingDiseases] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load diseases for the crop
  useEffect(() => {
    if (!cropType) return;
    setLoadingDiseases(true);
    getMedicineDiseases(cropType)
      .then((data) => {
        setDiseases(data.diseases || []);
      })
      .catch(() => {
        setDiseases([]);
      })
      .finally(() => setLoadingDiseases(false));
  }, [cropType]);

  // Auto-select detected disease when diseases load
  useEffect(() => {
    if (detectedDisease && diseases.length > 0) {
      const match = diseases.find(
        (d) => d.toLowerCase() === detectedDisease.toLowerCase()
      );
      if (match) setSelectedDisease(match);
      else setSelectedDisease(diseases[0]);
    } else if (diseases.length > 0 && !selectedDisease) {
      setSelectedDisease(diseases[0]);
    }
  }, [diseases, detectedDisease]);

  // Load treatment when disease changes
  useEffect(() => {
    if (!selectedDisease || !cropType) return;
    setLoading(true);
    setError(null);
    setTreatment(null);
    getMedicineTreatment(cropType, selectedDisease)
      .then((data) => {
        if (data.all_stages) setTreatment(data.all_stages);
        else setError("No treatment data available for this combination.");
      })
      .catch(() => {
        setError("Treatment data not found. Please consult an agronomist manually.");
      })
      .finally(() => setLoading(false));
  }, [selectedDisease, cropType]);

  const activeData =
    treatment && activeStage
      ? (treatment as any)[activeStage]
      : null;

  const handleApplyTreatment = () => {
    if (!activeData || !onApply) return;
    const stage = STAGE_LABELS[activeStage] || activeStage;
    const text = `[${stage} Treatment for ${selectedDisease}]

🧪 Chemical: ${activeData.chemical}
🍄 Fungicide/Bactericide: ${activeData.fungicide}
🌿 Organic Option: ${activeData.organic}
💊 Dose: ${activeData.dose}
📅 Frequency: ${activeData.frequency}
📝 Notes: ${activeData.notes}`;
    onApply(text);
  };

  if (!cropType) return null;

  return (
    <div
      style={{
        background: "linear-gradient(135deg, #f0fdf4, #eff6ff)",
        border: "1px solid #bbf7d0",
        borderRadius: "var(--radius-lg)",
        padding: "1.25rem",
        marginBottom: "1.25rem",
      }}
    >
      {/* Header */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "0.625rem",
          marginBottom: "1rem",
        }}
      >
        <span style={{ fontSize: "1.25rem" }}>💊</span>
        <div>
          <h4
            style={{
              fontSize: "0.9375rem",
              fontWeight: 700,
              color: "var(--color-primary-dark)",
              margin: 0,
            }}
          >
            {t("Medicine Advisor")}
          </h4>
          <p
            style={{
              fontSize: "0.75rem",
              color: "var(--color-text-muted)",
              margin: 0,
            }}
          >
            {t("Stage-wise treatment recommendations for")} {cropType}
          </p>
        </div>
      </div>

      {/* Disease selector */}
      <div style={{ marginBottom: "1rem" }}>
        <label
          style={{
            display: "block",
            fontSize: "0.75rem",
            fontWeight: 600,
            color: "var(--color-text-secondary)",
            marginBottom: "0.375rem",
          }}
        >
          {t("Select Disease")}
        </label>
        {loadingDiseases ? (
          <div className="skeleton" style={{ height: "38px", borderRadius: "var(--radius-sm)" }} />
        ) : diseases.length === 0 ? (
          <p style={{ fontSize: "0.8125rem", color: "var(--color-text-muted)", fontStyle: "italic" }}>
            {t("No disease data available for this crop.")}
          </p>
        ) : (
          <select
            value={selectedDisease}
            onChange={(e) => setSelectedDisease(e.target.value)}
            style={{
              width: "100%",
              padding: "0.6rem 0.75rem",
              borderRadius: "var(--radius-sm)",
              border: "1px solid var(--color-border)",
              fontSize: "0.875rem",
              background: "var(--color-bg)",
              cursor: "pointer",
            }}
          >
            {diseases.map((d) => (
              <option key={d} value={d}>
                {d}
              </option>
            ))}
          </select>
        )}
      </div>

      {/* Stage tabs */}
      {!loading && !error && treatment && (
        <>
          <div
            style={{
              display: "flex",
              gap: "0.375rem",
              marginBottom: "1rem",
              flexWrap: "wrap",
            }}
          >
            {(["sowing", "mid_season", "pre_harvest"] as const).map((stage) => {
              const hasData = !!(treatment as any)[stage];
              return (
                <button
                  key={stage}
                  onClick={() => setActiveStage(stage)}
                  disabled={!hasData}
                  style={{
                    padding: "0.4rem 0.875rem",
                    borderRadius: "var(--radius-sm)",
                    border: `1px solid ${
                      activeStage === stage
                        ? STAGE_BORDER_COLORS[stage]
                        : "var(--color-border)"
                    }`,
                    background:
                      activeStage === stage
                        ? STAGE_COLORS[stage]
                        : "transparent",
                    fontSize: "0.75rem",
                    fontWeight: activeStage === stage ? 700 : 500,
                    cursor: hasData ? "pointer" : "not-allowed",
                    opacity: hasData ? 1 : 0.45,
                    transition: "all 0.15s",
                  }}
                >
                  {STAGE_LABELS[stage]}
                </button>
              );
            })}
          </div>

          {/* Treatment details */}
          {activeData && (
            <div
              style={{
                background: STAGE_COLORS[activeStage],
                border: `1px solid ${STAGE_BORDER_COLORS[activeStage]}`,
                borderRadius: "var(--radius-md)",
                padding: "1rem",
              }}
            >
              <div
                className="medicine-fields-grid"
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr",
                  gap: "0.75rem",
                  marginBottom: "0.75rem",
                }}
              >
                <TreatmentField
                  icon="🧪"
                  label={t("Chemical")}
                  value={activeData.chemical}
                />
                <TreatmentField
                  icon="🍄"
                  label={t("Fungicide / Bactericide")}
                  value={activeData.fungicide}
                />
                <TreatmentField
                  icon="🌿"
                  label={t("Organic Option")}
                  value={activeData.organic}
                />
                <TreatmentField
                  icon="💊"
                  label={t("Dose")}
                  value={activeData.dose}
                />
              </div>

              <TreatmentField
                icon="📅"
                label={t("Application Frequency")}
                value={activeData.frequency}
              />
              <div style={{ marginTop: "0.5rem" }}>
                <TreatmentField
                  icon="📝"
                  label={t("Agronomist Notes")}
                  value={activeData.notes}
                  highlight
                />
              </div>

              {onApply && (
                <button
                  onClick={handleApplyTreatment}
                  className="btn btn-primary"
                  style={{
                    marginTop: "1rem",
                    width: "100%",
                    justifyContent: "center",
                    fontSize: "0.875rem",
                    padding: "0.6rem",
                  }}
                >
                  ✨ {t("Auto-Fill Treatment Notes")}
                </button>
              )}
            </div>
          )}
        </>
      )}

      {/* Loading state */}
      {loading && (
        <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <div className="skeleton" style={{ height: "38px", borderRadius: "var(--radius-sm)" }} />
          <div className="skeleton" style={{ height: "140px", borderRadius: "var(--radius-md)" }} />
        </div>
      )}

      {/* Error state */}
      {error && !loading && (
        <div
          style={{
            background: "#fef2f2",
            border: "1px solid #fca5a5",
            borderRadius: "var(--radius-sm)",
            padding: "0.75rem",
            fontSize: "0.8125rem",
            color: "#991b1b",
          }}
        >
          ⚠️ {error}
        </div>
      )}
    </div>
  );
}

function TreatmentField({
  icon,
  label,
  value,
  highlight,
}: {
  icon: string;
  label: string;
  value: string;
  highlight?: boolean;
}) {
  return (
    <div
      style={{
        background: highlight ? "rgba(255,255,255,0.7)" : "rgba(255,255,255,0.5)",
        borderRadius: "var(--radius-sm)",
        padding: "0.5rem 0.625rem",
        border: highlight ? "1px solid #fde68a" : "none",
      }}
    >
      <div
        style={{
          fontSize: "0.6875rem",
          fontWeight: 700,
          color: "var(--color-text-muted)",
          textTransform: "uppercase",
          letterSpacing: "0.04em",
          marginBottom: "0.25rem",
        }}
      >
        {icon} {label}
      </div>
      <div style={{ fontSize: "0.8125rem", color: "var(--color-text)", lineHeight: 1.5 }}>
        {value}
      </div>
    </div>
  );
}
