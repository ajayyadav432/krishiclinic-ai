"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useApp } from "@/context/AppContext";

export default function Navbar() {
  const pathname = usePathname();
  const { user, logout, language, setLanguage, t } = useApp();

  const navItems = [
    { href: "/", label: "Upload" },
    { href: "/history", label: "History" },
    { href: "/outbreak", label: "Outbreak Radar" },
    { href: "/analytics", label: "Analytics" },
  ];

  if (user && user.role === "AGRONOMIST") {
    navItems.push({ href: "/agronomist", label: "Agronomist Portal" });
  }

  return (
    <nav className="nav">
      <div
        className="nav-mobile-wrap"
        style={{
          maxWidth: "1280px",
          margin: "0 auto",
          padding: "0 1.5rem",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          height: "64px",
        }}
      >
        <Link
          href="/"
          style={{
            display: "flex",
            alignItems: "center",
            gap: "0.5rem",
            textDecoration: "none",
            flexShrink: 0,
          }}
        >
          <span
            style={{
              fontSize: "1.125rem",
              fontWeight: 800,
              color: "var(--color-primary-dark, #15803d)",
              letterSpacing: "-0.025em",
              whiteSpace: "nowrap",
            }}
          >
            KrishiClinic AI
          </span>
          <span
            style={{
              fontSize: "0.625rem",
              fontWeight: 700,
              color: "var(--color-primary, #16a34a)",
              background: "rgba(22, 163, 74, 0.1)",
              padding: "0.125rem 0.45rem",
              borderRadius: "9999px",
              border: "1px solid rgba(22, 163, 74, 0.2)",
              flexShrink: 0,
              textTransform: "uppercase"
            }}
          >
            Pro
          </span>
        </Link>

        <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", flexShrink: 0 }}>
          <div style={{ display: "flex", alignItems: "center", gap: "0.25rem" }}>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              style={{
                fontSize: "0.75rem",
                fontWeight: 600,
                padding: "0.25rem 0.5rem",
                borderRadius: "var(--radius-sm, 6px)",
                border: "1px solid var(--color-border, #d1d5db)",
                background: "var(--color-bg, #ffffff)",
                cursor: "pointer",
                outline: "none",
              }}
            >
              <option value="en">English</option>
              <option value="hi">Hindi</option>
              <option value="te">Telugu</option>
              <option value="mr">Marathi</option>
              <option value="es">Spanish</option>
            </select>
          </div>

          {user && (
            <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
              <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end" }}>
                <span style={{ fontSize: "0.75rem", fontWeight: 700, lineHeight: 1.2 }}>
                  {user.username}
                </span>
                <span
                  style={{
                    fontSize: "0.625rem",
                    fontWeight: 600,
                    color: "white",
                    background:
                      user.role === "AGRONOMIST"
                        ? "#0f766e"
                        : user.role === "ADMIN"
                        ? "#7c3aed"
                        : "#0284c7",
                    padding: "0.0625rem 0.35rem",
                    borderRadius: "3px",
                    textTransform: "uppercase",
                  }}
                >
                  {user.role}
                </span>
              </div>
              <button
                onClick={logout}
                style={{
                  fontSize: "0.75rem",
                  fontWeight: 600,
                  color: "#b91c1c",
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                  padding: "0.25rem",
                  whiteSpace: "nowrap",
                }}
              >
                {t("Logout")}
              </button>
            </div>
          )}
        </div>
      </div>

      {user && (
        <div
          className="nav-links-mobile"
          style={{
            maxWidth: "1280px",
            margin: "0 auto",
            padding: "0 1rem 0.5rem",
            display: "flex",
            gap: "0.25rem",
            borderTop: "1px solid var(--color-border-light, #f3f4f6)",
          }}
        >
          {navItems.map((item) => {
            const isActive =
              item.href === "/"
                ? pathname === "/"
                : pathname.startsWith(item.href);

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`nav-link ${isActive ? "nav-link-active" : ""}`}
                style={{ whiteSpace: "nowrap", fontSize: "0.8125rem" }}
              >
                {t(item.label)}
              </Link>
            );
          })}
        </div>
      )}
    </nav>
  );
}
