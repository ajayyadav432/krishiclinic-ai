"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useApp } from "@/context/AppContext";

const NAV_ITEMS = [
  { href: "/", label: "Dashboard" },
  { href: "/history", label: "My Reports" },
  { href: "/outbreak", label: "Outbreak Radar" },
  { href: "/analytics", label: "Analytics" },
  { href: "/calendar", label: "Crop Calendar" },
];

const AGRO_ITEMS = [
  { href: "/agronomist", label: "Agro Portal" },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { user, logout, language, setLanguage, t } = useApp();
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => { setMobileOpen(false); }, [pathname]);

  const isActive = (href: string) =>
    href === "/" ? pathname === "/" : pathname.startsWith(href);

  const navLinks = [
    ...NAV_ITEMS,
    ...(user?.role === "AGRONOMIST" || user?.role === "ADMIN" ? AGRO_ITEMS : []),
  ];

  if (!user) {
    return (
      <style dangerouslySetInnerHTML={{ __html: `
        .app-main {
          margin-left: 0 !important;
        }
        .mobile-topbar {
          display: none !important;
        }
      `}} />
    );
  }

  return (
    <>
      <div className="mobile-topbar">
        <button
          className="mobile-menu-btn"
          onClick={() => setMobileOpen(!mobileOpen)}
          aria-label="Open menu"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
            <line x1="3" y1="6" x2="21" y2="6"/>
            <line x1="3" y1="12" x2="21" y2="12"/>
            <line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
        </button>
        <span className="mobile-topbar-brand">KrishiClinic AI</span>
        {user && (
          <div className="sidebar-avatar" style={{ width: 28, height: 28, fontSize: "0.75rem", marginLeft: "auto" }}>
            {user.username?.[0]?.toUpperCase() ?? "U"}
          </div>
        )}
      </div>

      {mobileOpen && (
        <div
          className="sidebar-overlay"
          onClick={() => setMobileOpen(false)}
        />
      )}

      <aside className={`app-sidebar ${mobileOpen ? "mobile-open" : ""}`}>
        <div className="sidebar-brand">
          <div className="sidebar-brand-name">
            <span>KrishiClinic AI</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          <span className="sidebar-nav-label">Navigation</span>
          {navLinks.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`sidebar-link ${isActive(item.href) ? "active" : ""}`}
            >
              {t(item.label)}
            </Link>
          ))}
        </nav>

        {user && (
          <div className="sidebar-footer">
            <div style={{ paddingBottom: "0.5rem" }}>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="lang-select"
                style={{ width: "100%" }}
              >
                <option value="en">English</option>
                <option value="hi">Hindi</option>
                <option value="te">Telugu</option>
                <option value="mr">Marathi</option>
                <option value="es">Spanish</option>
              </select>
            </div>
            <div className="sidebar-user">
              <div className="sidebar-avatar">
                {user.username?.[0]?.toUpperCase() ?? "U"}
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div className="sidebar-user-name"
                  style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                  {user.username}
                </div>
                <div className="sidebar-user-role">{user.role.toLowerCase()}</div>
              </div>
              <button
                onClick={logout}
                title="Logout"
                style={{
                  background: "none", border: "none", cursor: "pointer",
                  fontSize: "0.8125rem", color: "var(--color-text-muted)",
                  padding: "0.25rem", borderRadius: "6px", flexShrink: 0,
                }}
              >
                Sign out
              </button>
            </div>
          </div>
        )}
      </aside>
    </>
  );
}
