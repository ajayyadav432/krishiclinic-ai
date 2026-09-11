"use client";

import { useState, useEffect } from "react";

interface AudioPlayerProps {
  text: string;
  language?: string;
  label?: string;
}

export default function AudioPlayer({ text, language = "en", label = "Listen Advisory" }: AudioPlayerProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isSupported, setIsSupported] = useState(false);

  useEffect(() => {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      setIsSupported(true);
    }
  }, []);

  const getLanguageCode = (lang: string) => {
    switch (lang) {
      case "hi":
        return "hi-IN";
      case "te":
        return "te-IN";
      case "mr":
        return "mr-IN";
      case "es":
        return "es-ES";
      default:
        return "en-IN";
    }
  };

  const handleTogglePlay = () => {
    if (!isSupported || !text) return;

    if (isPlaying) {
      window.speechSynthesis.cancel();
      setIsPlaying(false);
      return;
    }

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = getLanguageCode(language);
    utterance.rate = 0.95;

    utterance.onend = () => {
      setIsPlaying(false);
    };

    utterance.onerror = () => {
      setIsPlaying(false);
    };

    window.speechSynthesis.speak(utterance);
    setIsPlaying(true);
  };

  if (!isSupported) {
    return null;
  }

  return (
    <button
      type="button"
      onClick={handleTogglePlay}
      className={`audio-player-btn ${isPlaying ? "playing" : ""}`}
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "0.5rem",
        padding: "0.45rem 0.85rem",
        borderRadius: "9999px",
        fontSize: "0.8125rem",
        fontWeight: 600,
        cursor: "pointer",
        border: "1px solid var(--color-border, #d1d5db)",
        background: isPlaying ? "var(--color-primary, #16a34a)" : "var(--color-surface, #ffffff)",
        color: isPlaying ? "#ffffff" : "var(--color-text, #1f2937)",
        transition: "all 0.2s ease"
      }}
    >
      <svg
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
        <path d="M15.54 8.46a5 5 0 0 1 0 7.07" />
        <path d="M19.07 4.93a10 10 0 0 1 0 14.14" />
      </svg>
      <span>{isPlaying ? "Pause Audio" : label}</span>
      {isPlaying && (
        <span
          style={{
            display: "inline-block",
            width: "6px",
            height: "6px",
            borderRadius: "50%",
            background: "#ffffff"
          }}
        />
      )}
    </button>
  );
}
