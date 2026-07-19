"""Dashboard theme: palette, global CSS, floating motion, and UI fragments."""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

COLORS = {
    "bg_deep": "#060912",
    "bg_panel": "rgba(14, 22, 42, 0.82)",
    "border": "rgba(99, 179, 237, 0.18)",
    "border_strong": "rgba(99, 179, 237, 0.35)",
    "accent": "#63b3ed",
    "accent_soft": "rgba(99, 179, 237, 0.12)",
    "violet": "#a78bfa",
    "magenta": "#f472b6",
    "text": "#f1f5f9",
    "muted": "#94a3b8",
    "danger": "#fb7185",
    "warning": "#fbbf24",
    "success": "#34d399",
}

PLOTLY_TEMPLATE = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(10, 16, 30, 0.65)",
    "font": {"family": "IBM Plex Sans, system-ui, sans-serif", "color": COLORS["text"], "size": 12},
    "xaxis": {
        "gridcolor": "rgba(148, 163, 184, 0.08)",
        "linecolor": "rgba(148, 163, 184, 0.25)",
        "zerolinecolor": "rgba(148, 163, 184, 0.15)",
    },
    "yaxis": {
        "gridcolor": "rgba(148, 163, 184, 0.08)",
        "linecolor": "rgba(148, 163, 184, 0.25)",
        "zerolinecolor": "rgba(148, 163, 184, 0.15)",
    },
    "legend": {"bgcolor": "rgba(0,0,0,0)", "bordercolor": "rgba(0,0,0,0)"},
    "margin": {"l": 8, "r": 8, "t": 40, "b": 8},
}

HORIZON_LABELS = {
    "5m": "5 min",
    "15m": "15 min",
    "60m": "1 hour",
    "1d": "1 day",
}


def horizon_label(horizon: str) -> str:
    return HORIZON_LABELS.get(horizon, horizon)


_FLOATING_CSS = """
            @keyframes aegis-float-y {
                0%, 100% { transform: translateY(0) translateX(0); }
                50% { transform: translateY(-12px) translateX(5px); }
            }
            @keyframes aegis-float-y-slow {
                0%, 100% { transform: translateY(0) rotate(0deg); }
                50% { transform: translateY(-18px) rotate(1.5deg); }
            }
            @keyframes aegis-float-orb {
                0%, 100% {
                    transform: translate(0, 0) scale(1);
                    opacity: 0.35;
                }
                33% {
                    transform: translate(28px, -36px) scale(1.06);
                    opacity: 0.5;
                }
                66% {
                    transform: translate(-18px, -22px) scale(0.94);
                    opacity: 0.3;
                }
            }
            @keyframes aegis-float-glow {
                0%, 100% { box-shadow: 0 0 20px rgba(99, 179, 237, 0.08); }
                50% { box-shadow: 0 0 32px rgba(99, 179, 237, 0.18); }
            }
            @keyframes aegis-badge-float {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-4px); }
            }
            .aegis-float-layer {
                position: fixed;
                inset: 0;
                pointer-events: none;
                z-index: 0;
                overflow: hidden;
            }
            [data-testid="stAppViewContainer"],
            [data-testid="stMain"],
            [data-testid="stSidebar"],
            [data-testid="stHeader"],
            [data-testid="stBottom"],
            [data-testid="stBottomBlockContainer"],
            .block-container {
                position: relative;
                z-index: 1;
            }
            [data-testid="stMarkdownContainer"] h1,
            [data-testid="stMarkdownContainer"] h2,
            [data-testid="stMarkdownContainer"] h3,
            [data-testid="stMarkdownContainer"] p,
            [data-testid="stWidgetLabel"],
            [data-testid="stCaptionContainer"],
            label[data-testid="stWidgetLabel"],
            .stTextInput label,
            .stSelectbox label,
            .stMultiSelect label,
            .stSlider label,
            .stToggle label {
                color: var(--aegis-text) !important;
            }
            [data-testid="stMarkdownContainer"] .aegis-login-brand p,
            [data-testid="stMarkdownContainer"] .aegis-topbar-sub,
            [data-testid="stMarkdownContainer"] .aegis-pred-label,
            [data-testid="stMarkdownContainer"] .aegis-empty {
                color: var(--aegis-muted) !important;
            }
            [data-baseweb="tab-list"] button,
            [data-baseweb="tab"] {
                color: var(--aegis-muted) !important;
            }
            [data-baseweb="tab"][aria-selected="true"] {
                color: var(--aegis-accent) !important;
            }
            .aegis-orb {
                position: absolute;
                border-radius: 50%;
                filter: blur(40px);
                animation: aegis-float-orb ease-in-out infinite;
            }
            .aegis-orb-1 {
                width: 280px; height: 280px;
                top: 8%; left: -4%;
                background: rgba(99, 179, 237, 0.22);
                animation-duration: 14s;
            }
            .aegis-orb-2 {
                width: 220px; height: 220px;
                top: 55%; right: -2%;
                background: rgba(167, 139, 250, 0.2);
                animation-duration: 18s;
                animation-delay: -4s;
            }
            .aegis-orb-3 {
                width: 160px; height: 160px;
                bottom: 12%; left: 35%;
                background: rgba(244, 114, 182, 0.14);
                animation-duration: 16s;
                animation-delay: -7s;
            }
            .aegis-orb-4 {
                width: 120px; height: 120px;
                top: 22%; right: 28%;
                background: rgba(52, 211, 153, 0.12);
                animation-duration: 12s;
                animation-delay: -2s;
            }
            .aegis-float,
            .aegis-pred-card,
            .aegis-panel,
            .aegis-empty {
                animation: aegis-float-y 5.5s ease-in-out infinite,
                           aegis-float-glow 5.5s ease-in-out infinite;
            }
            .aegis-pred-grid .aegis-pred-card:nth-child(1) { animation-delay: 0s, 0s; }
            .aegis-pred-grid .aegis-pred-card:nth-child(2) { animation-delay: 0.4s, 0.4s; }
            .aegis-pred-grid .aegis-pred-card:nth-child(3) { animation-delay: 0.8s, 0.8s; }
            .aegis-pred-grid .aegis-pred-card:nth-child(4) { animation-delay: 1.2s, 1.2s; }
            .aegis-login-brand {
                animation: aegis-float-y-slow 7s ease-in-out infinite;
            }
            .aegis-topbar-meta .aegis-badge {
                animation: aegis-badge-float 4s ease-in-out infinite;
            }
            .aegis-topbar-meta .aegis-badge:nth-child(2) { animation-delay: 0.35s; }
            .aegis-topbar-meta .aegis-badge:nth-child(3) { animation-delay: 0.7s; }
            .aegis-chip {
                animation: aegis-badge-float 5s ease-in-out infinite;
            }
            @media (prefers-reduced-motion: reduce) {
                .aegis-orb, .aegis-float, .aegis-pred-card, .aegis-panel,
                .aegis-empty, .aegis-login-brand,
                .aegis-topbar-meta .aegis-badge, .aegis-chip {
                    animation: none !important;
                }
            }
"""


def inject_futuristic_theme() -> None:
    st.markdown(
        f"""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <style>
            :root {{
                --aegis-accent: {COLORS["accent"]};
                --aegis-text: {COLORS["text"]};
                --aegis-muted: {COLORS["muted"]};
                --aegis-border: {COLORS["border"]};
            }}
            {_FLOATING_CSS}
            .stApp {{
                position: relative;
                overflow-x: hidden;
                background:
                    radial-gradient(ellipse 70% 45% at 0% 0%, rgba(99, 179, 237, 0.12), transparent 50%),
                    radial-gradient(ellipse 50% 35% at 100% 0%, rgba(167, 139, 250, 0.14), transparent 45%),
                    linear-gradient(180deg, #03050b 0%, #07111e 48%, #060912 100%);
                color: var(--aegis-text);
                font-family: 'IBM Plex Sans', system-ui, sans-serif;
                scroll-behavior: smooth;
            }}
            .stApp ::selection {{
                background: rgba(99, 179, 237, 0.25);
                color: {COLORS["text"]};
            }}
            #MainMenu, footer, header[data-testid="stHeader"] {{
                background: transparent !important;
                box-shadow: none !important;
            }}
            .block-container {{
                padding-top: 1.5rem;
                padding-bottom: 2rem;
                max-width: 1320px;
            }}
            [data-testid="stSidebar"] > div {{
                position: relative;
                z-index: 1;
            }}
            [data-testid="stSidebar"] {{
                background: linear-gradient(180deg, rgba(6, 9, 18, 0.96), rgba(8, 12, 23, 0.95)) !important;
                border-right: 1px solid {COLORS["border"]};
                box-shadow: inset -1px 0 0 rgba(99, 179, 237, 0.06);
            }}
            [data-testid="stSidebar"] .block-container {{ padding-top: 1rem; }}
            h1, h2, h3 {{
                font-family: 'IBM Plex Sans', sans-serif !important;
                letter-spacing: -0.02em;
            }}
            span[data-testid="stIconMaterial"] {{
                font-family: 'Material Icons' !important;
                font-weight: normal !important;
                font-style: normal !important;
                font-size: inherit !important;
                line-height: 1 !important;
                letter-spacing: normal !important;
                text-transform: none !important;
                display: inline-block !important;
                word-wrap: normal !important;
                white-space: nowrap !important;
                direction: ltr !important;
                -webkit-font-feature-settings: 'liga' !important;
                -webkit-font-smoothing: antialiased !important;
            }}
            h1 {{
                font-size: 1.9rem !important;
                font-weight: 700 !important;
                color: {COLORS["text"]} !important;
                letter-spacing: -0.04em;
            }}
            h2 {{
                font-size: 1.1rem !important;
                font-weight: 600 !important;
                color: {COLORS["text"]} !important;
                margin-bottom: 0.75rem !important;
            }}
            h3 {{
                font-size: 0.98rem !important;
                color: {COLORS["muted"]} !important;
            }}
            p, label, .stMarkdown, span {{
                font-family: 'IBM Plex Sans', sans-serif !important;
            }}
            [data-testid="stSidebar"] {{
                background: linear-gradient(180deg, #0a1020 0%, #060912 100%) !important;
                border-right: 1px solid {COLORS["border"]};
            }}
            [data-testid="stSidebar"] .block-container {{ padding-top: 1rem; }}
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3 {{
                font-size: 0.7rem !important;
                font-weight: 600 !important;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: {COLORS["muted"]} !important;
            }}
            [data-testid="stMetric"] {{
                background: {COLORS["bg_panel"]};
                border: 1px solid {COLORS["border"]};
                border-radius: 12px;
                padding: 0.85rem 1rem;
                animation: aegis-float-y 6s ease-in-out infinite;
            }}
            [data-testid="stMetricLabel"] {{
                color: var(--aegis-muted) !important;
                font-size: 0.7rem !important;
                letter-spacing: 0.06em;
                text-transform: uppercase;
            }}
            [data-testid="stMetricValue"] {{
                color: var(--aegis-text) !important;
                font-family: 'IBM Plex Mono', monospace !important;
                font-size: 1.2rem !important;
            }}
            .aegis-mono, .aegis-pred-value, .aegis-pred-cell {{
                font-family: 'IBM Plex Mono', monospace !important;
            }}
            .aegis-pred-label {{
                font-size: 0.68rem !important;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                color: var(--aegis-muted);
                font-weight: 500;
            }}
            .aegis-pred-value {{
                font-size: 1.35rem;
                font-weight: 500;
                line-height: 1.25;
            }}
            .aegis-pred-value-lg {{
                font-size: 1.65rem;
                font-family: 'IBM Plex Mono', monospace !important;
            }}
            .aegis-pred-card {{
                background: linear-gradient(180deg, rgba(14, 24, 48, 0.95), rgba(9, 16, 30, 0.96));
                border: 1px solid rgba(99, 179, 237, 0.16);
                border-radius: 18px;
                padding: 1rem 1.05rem;
                min-height: 88px;
                box-shadow: 0 18px 35px rgba(0, 0, 0, 0.14);
                transition: transform 0.18s ease, border-color 0.18s ease;
            }}
            .aegis-pred-card:hover {{
                transform: translateY(-2px);
                border-color: rgba(99, 179, 237, 0.26);
            }}
            .aegis-pred-grid {{
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 0.75rem;
                margin-bottom: 1rem;
            }}

            @media (max-width: 1100px) {{
                .aegis-pred-grid {{ grid-template-columns: repeat(2, 1fr); }}
            }}
            @media (max-width: 520px) {{
                .aegis-pred-grid {{ grid-template-columns: 1fr; }}
            }}
            .aegis-pred-table {{
                width: 100%;
                border-collapse: separate;
                border-spacing: 0 5px;
                font-family: 'IBM Plex Mono', monospace !important;
                font-size: 0.85rem;
                min-width: 100%;
            }}
            .aegis-pred-table th {{
                font-size: 0.68rem;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: {COLORS["muted"]};
                text-align: left;
                padding: 0.55rem 0.85rem;
                border-bottom: 1px solid rgba(99, 179, 237, 0.12);
                font-weight: 600;
            }}
            .aegis-pred-table td {{
                padding: 0.65rem 0.85rem;
                color: {COLORS["text"]};
                background: rgba(13, 24, 42, 0.85);
                transition: background 0.18s ease;
            }}
            .aegis-pred-table tr:hover td {{
                background: rgba(99, 179, 237, 0.08);
            }}
            .aegis-pred-table tr td:first-child {{ border-radius: 10px 0 0 10px; }}
            .aegis-pred-table tr td:last-child {{ border-radius: 0 10px 10px 0; }}
            .aegis-telemetry-strip {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 0.85rem;
                margin-bottom: 0.85rem;
            }}
            @media (max-width: 900px) {{
                .aegis-telemetry-strip {{ grid-template-columns: 1fr; }}
            }}
            .aegis-forecast-compact .aegis-compact-row {{
                display: flex;
                justify-content: space-between;
                align-items: baseline;
                gap: 0.75rem;
                padding: 0.4rem 0;
                border-bottom: 1px solid rgba(148, 163, 184, 0.1);
            }}
            .aegis-forecast-compact .aegis-compact-row:last-child {{ border-bottom: none; }}
            .aegis-forecast-compact .aegis-compact-value {{
                font-family: 'IBM Plex Mono', monospace !important;
                font-size: 0.95rem;
                text-align: right;
            }}
            .stTabs [data-baseweb="tab-list"] {{
                gap: 4px;
                background: rgba(10, 16, 30, 0.7);
                border-radius: 10px;
                padding: 4px;
                border: 1px solid {COLORS["border"]};
            }}
            .stTabs [data-baseweb="tab"] {{
                font-size: 0.8rem !important;
                font-weight: 500 !important;
                color: var(--aegis-muted) !important;
                border-radius: 8px;
                padding: 0.45rem 0.9rem;
            }}
            .stTabs [aria-selected="true"] {{
                background: {COLORS["accent_soft"]} !important;
                color: {COLORS["accent"]} !important;
                border: 1px solid {COLORS["border_strong"]} !important;
            }}
            .stButton > button {{
                font-weight: 600 !important;
                font-size: 0.88rem !important;
                border-radius: 999px !important;
                border: 1px solid transparent !important;
                background: linear-gradient(135deg, rgba(99, 179, 237, 0.22), rgba(167, 139, 250, 0.20)) !important;
                color: {COLORS["text"]} !important;
                box-shadow: inset 0 0 0 1px rgba(99, 179, 237, 0.10);
                transition: transform 0.18s ease, background 0.18s ease, border-color 0.18s ease;
            }}
            .stButton > button:hover {{
                background: linear-gradient(135deg, rgba(99, 179, 237, 0.35), rgba(167, 139, 250, 0.25)) !important;
                color: {COLORS["text"]} !important;
                transform: translateY(-1px);
            }}
            .stDownloadButton > button {{
                border-radius: 999px !important;
                background: linear-gradient(135deg, rgba(99, 179, 237, 0.16), rgba(167, 139, 250, 0.16)) !important;
                color: {COLORS["text"]} !important;
            }}
            [data-testid="stFormSubmitButton"] > button {{
                background: {COLORS["accent"]} !important;
                color: #060912 !important;
                font-weight: 600 !important;
                border: none !important;
            }}
            .stTextInput input,
            .stTextArea textarea,
            .stSelectbox div[data-baseweb="select"] > div,
            .stMultiSelect div[data-baseweb="select"] > div,
            .stNumberInput input,
            .stSlider > div[role="slider"] {{
                background: rgba(10, 16, 30, 0.92) !important;
                border-color: rgba(99, 179, 237, 0.18) !important;
                color: var(--aegis-text) !important;
                border-radius: 12px !important;
                box-shadow: inset 0 1px 2px rgba(255,255,255,0.04);
            }}
            .stTextInput input:focus,
            .stTextArea textarea:focus,
            .stSelectbox div[data-baseweb="select"] > div:focus,
            .stMultiSelect div[data-baseweb="select"] > div:focus {{
                border-color: {COLORS["accent"]} !important;
                outline: none !important;
                box-shadow: 0 0 0 4px rgba(99, 179, 237, 0.12) !important;
            }}
            [data-testid="stDataFrame"] {{
                border: 1px solid rgba(99, 179, 237, 0.12);
                border-radius: 14px;
                overflow: hidden;
                background: rgba(10, 16, 30, 0.9);
            }}

            .aegis-topbar {{
                display: flex;
                flex-wrap: wrap;
                align-items: flex-end;
                justify-content: space-between;
                gap: 1rem;
                margin-bottom: 1.25rem;
                padding-bottom: 1rem;
                border-bottom: 1px solid {COLORS["border"]};
            }}
            .aegis-topbar-title {{
                margin: 0;
                font-size: 1.5rem !important;
                font-weight: 700 !important;
                color: {COLORS["text"]} !important;
            }}
            .aegis-topbar-sub {{
                margin: 0.25rem 0 0;
                color: {COLORS["muted"]};
                font-size: 0.9rem;
            }}
            .aegis-topbar-meta {{
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
                align-items: center;
            }}
            .aegis-badge {{
                display: inline-flex;
                align-items: center;
                gap: 0.35rem;
                padding: 0.2rem 0.65rem;
                border-radius: 999px;
                font-size: 0.72rem;
                font-weight: 500;
                border: 1px solid {COLORS["border"]};
                background: rgba(10, 16, 30, 0.6);
                color: {COLORS["muted"]};
            }}
            .aegis-badge-live {{
                border-color: rgba(52, 211, 153, 0.35);
                color: {COLORS["success"]};
                background: rgba(52, 211, 153, 0.08);
            }}
            .aegis-badge-live::before {{
                content: "";
                width: 6px;
                height: 6px;
                border-radius: 50%;
                background: {COLORS["success"]};
                box-shadow: 0 0 8px {COLORS["success"]};
                animation: aegis-badge-float 2.5s ease-in-out infinite;
            }}
            .aegis-badge-offline {{
                border-color: rgba(251, 113, 133, 0.35);
                color: {COLORS["danger"]};
                background: rgba(251, 113, 133, 0.08);
            }}
            .aegis-panel {{
                background: linear-gradient(180deg, rgba(14, 22, 42, 0.94), rgba(9, 14, 28, 0.98));
                border: 1px solid rgba(99, 179, 237, 0.16);
                border-radius: 18px;
                padding: 1.1rem 1.2rem;
                margin-bottom: 1rem;
                box-shadow: 0 18px 36px rgba(0, 0, 0, 0.12);
            }}
            .aegis-advice-buy {{
                border-left: 4px solid {COLORS["success"]};
                background: rgba(52, 211, 153, 0.1);
            }}
            .aegis-advice-sell {{
                border-left: 3px solid {COLORS["danger"]};
                background: rgba(251, 113, 133, 0.06);
            }}
            .aegis-advice-hold {{
                border-left: 3px solid {COLORS["warning"]};
                background: rgba(251, 191, 36, 0.06);
            }}
            .aegis-advice-title {{
                font-size: 1rem;
                font-weight: 600;
                margin-bottom: 0.3rem;
            }}
            .aegis-login-brand {{
                text-align: center;
                margin-bottom: 1.75rem;
                pointer-events: none;
            }}
            .aegis-login-brand h1 {{
                font-size: 1.65rem !important;
                margin: 0.5rem 0 0.35rem !important;
            }}
            .aegis-login-brand p {{
                color: {COLORS["muted"]};
                font-size: 0.9rem;
                margin: 0;
            }}
            .aegis-chip {{
                display: inline-block;
                margin: 0.2rem 0.3rem 0.2rem 0;
                padding: 0.15rem 0.55rem;
                border: 1px solid {COLORS["border"]};
                border-radius: 6px;
                font-family: 'IBM Plex Mono', monospace !important;
                font-size: 0.72rem;
                color: {COLORS["accent"]};
            }}
            .aegis-empty {{
                text-align: center;
                padding: 2rem 1rem;
                color: {COLORS["muted"]};
                border: 1px dashed {COLORS["border"]};
                border-radius: 12px;
                background: rgba(10, 16, 30, 0.4);
            }}
            .aegis-empty-title {{
                font-weight: 600;
                color: {COLORS["text"]};
                margin-bottom: 0.35rem;
            }}
            .stAlert {{ border-radius: 10px !important; }}
            div[data-testid="stVerticalBlockBorderWrapper"] {{ border-radius: 12px; }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    render_floating_background()


def render_floating_background() -> None:
    st.markdown(
        """
        <div class="aegis-float-layer" aria-hidden="true">
            <span class="aegis-orb aegis-orb-1"></span>
            <span class="aegis-orb aegis-orb-2"></span>
            <span class="aegis-orb aegis-orb-3"></span>
            <span class="aegis-orb aegis-orb-4"></span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_topbar(
    *,
    title: str,
    subtitle: str,
    symbol: str,
    company_name: str | None,
    horizon: str,
    api_online: bool,
) -> None:
    status_class = "aegis-badge-live" if api_online else "aegis-badge-offline"
    status_text = "API connected" if api_online else "API offline"
    company_badge = f'<span class="aegis-badge">{company_name}</span>' if company_name else ""
    st.markdown(
        f"""
        <div class="aegis-topbar">
            <div>
                <h1 class="aegis-topbar-title">{title}</h1>
                <p class="aegis-topbar-sub">{subtitle}</p>
            </div>
            <div class="aegis-topbar-meta">
                <span class="aegis-badge">{symbol}</span>
                {company_badge}
                <span class="aegis-badge">{horizon_label(horizon)}</span>
                <span class="aegis-badge {status_class}">{status_text}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_login_brand() -> None:
    st.markdown(
        f"""
        <div class="aegis-login-brand aegis-float">
            <span class="aegis-badge aegis-badge-live">Analytics platform</span>
            <h1>Aegis Analytics</h1>
            <p>ML forecasts, risk bands, and India stock dashboards</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(title: str, detail: str) -> None:
    st.markdown(
        f"""
        <div class="aegis-empty">
            <div class="aegis-empty-title">{title}</div>
            <p style="margin:0;font-size:0.88rem;">{detail}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_advice_panel(label: str, reason: str) -> None:
    css_class = "aegis-advice-hold"
    color = COLORS["warning"]
    if label == "Buy":
        css_class = "aegis-advice-buy"
        color = COLORS["success"]
    elif label == "Sell / Reduce":
        css_class = "aegis-advice-sell"
        color = COLORS["danger"]

    st.markdown(
        f"""
        <div class="aegis-panel {css_class}">
            <div class="aegis-advice-title" style="color:{color}">{label}</div>
            <p style="margin:0;color:{COLORS['muted']};font-size:0.9rem;line-height:1.5;">{reason}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _value_color(value: float, *, positive_good: bool = True) -> str:
    if value > 0:
        return COLORS["success"] if positive_good else COLORS["danger"]
    if value < 0:
        return COLORS["danger"] if positive_good else COLORS["success"]
    return COLORS["muted"]


def render_prediction_metrics(
    *,
    expected_return: float,
    expected_price: float,
    p_up: float | None,
    downside_risk: float,
) -> None:
    ret_color = _value_color(expected_return)
    conf_text = "N/A" if p_up is None else f"{p_up * 100:.1f}%"
    conf_color = COLORS["muted"] if p_up is None else _value_color(float(p_up) - 0.5)
    risk_color = (
        COLORS["danger"]
        if downside_risk >= 0.35
        else COLORS["warning"]
        if downside_risk >= 0.2
        else COLORS["success"]
    )

    st.markdown(
        f"""
        <div class="aegis-pred-grid">
            <div class="aegis-pred-card">
                <div class="aegis-pred-label">Expected return</div>
                <div class="aegis-pred-value aegis-mono" style="color:{ret_color}">{expected_return * 100:+.3f}%</div>
            </div>
            <div class="aegis-pred-card">
                <div class="aegis-pred-label">Expected price</div>
                <div class="aegis-pred-value aegis-mono" style="color:{COLORS['accent']}">${expected_price:,.2f}</div>
            </div>
            <div class="aegis-pred-card">
                <div class="aegis-pred-label">P(up)</div>
                <div class="aegis-pred-value aegis-mono" style="color:{conf_color}">{conf_text}</div>
            </div>
            <div class="aegis-pred-card">
                <div class="aegis-pred-label">Downside (&lt; −2%)</div>
                <div class="aegis-pred-value aegis-mono" style="color:{risk_color}">{downside_risk * 100:.1f}%</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_future_outlook_panel(
    *,
    symbol: str,
    horizon: str,
    timeframe: str,
    last_close: float,
    expected_return: float,
    expected_price: float,
    interval_low: float,
    interval_high: float,
    p_up: float | None,
    last_timestamp: str,
) -> None:
    future_label = "Future outlook"
    low_price = last_close * (1.0 + interval_low)
    high_price = last_close * (1.0 + interval_high)
    conf = "—" if p_up is None else f"{p_up * 100:.1f}%"
    conf_color = COLORS["muted"] if p_up is None else _value_color(float(p_up) - 0.5)
    ret_color = _value_color(expected_return)
    next_date = last_timestamp

    st.markdown(
        f"""
        <div class="aegis-panel">
            <div class="aegis-pred-label" style="margin-bottom:0.55rem;">{future_label} · {symbol}</div>
            <div class="aegis-forecast-compact">
                <div class="aegis-compact-row">
                    <span class="aegis-pred-label">Target date</span>
                    <span class="aegis-compact-value">{next_date}</span>
                </div>
                <div class="aegis-compact-row">
                    <span class="aegis-pred-label">Target price</span>
                    <span class="aegis-compact-value" style="color:{COLORS['magenta']}">${expected_price:,.2f}</span>
                </div>
                <div class="aegis-compact-row">
                    <span class="aegis-pred-label">Expected return</span>
                    <span class="aegis-compact-value" style="color:{ret_color}">{expected_return * 100:+.3f}%</span>
                </div>
                <div class="aegis-compact-row">
                    <span class="aegis-pred-label">Confidence</span>
                    <span class="aegis-compact-value" style="color:{conf_color}">{conf}</span>
                </div>
                <div class="aegis-compact-row">
                    <span class="aegis-pred-label">Price band</span>
                    <span class="aegis-compact-value" style="color:{COLORS['violet']}">${low_price:,.2f} – ${high_price:,.2f}</span>
                </div>
                <div class="aegis-compact-row">
                    <span class="aegis-pred-label">Horizon</span>
                    <span class="aegis-compact-value">{horizon_label(horizon)} · {timeframe}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_forecast_summary_compact(
    *,
    symbol: str,
    company_name: str | None,
    horizon: str,
    timeframe: str,
    last_close: float,
    expected_return: float,
    expected_price: float,
    interval_low: float,
    interval_high: float,
    p_up: float | None,
    model_version: str | None,
    model_trained_at: str | None = None,
) -> None:
    low_price = last_close * (1.0 + interval_low)
    high_price = last_close * (1.0 + interval_high)
    conf = "—" if p_up is None else f"{p_up * 100:.1f}%"
    conf_color = COLORS["muted"] if p_up is None else _value_color(float(p_up) - 0.5)
    ret_color = _value_color(expected_return)
    trained = str(model_trained_at)[:19].replace("T", " ") if model_trained_at else "—"

    def row(label: str, value: str, color: str) -> str:
        return (
            f'<div class="aegis-compact-row">'
            f'<span class="aegis-pred-label">{label}</span>'
            f'<span class="aegis-compact-value" style="color:{color}">{value}</span>'
            f"</div>"
        )

    rows = [
        row("Last close", f"${last_close:,.2f}", COLORS["text"]),
        row("Target price", f"${expected_price:,.2f}", COLORS["magenta"]),
        row("Expected return", f"{expected_return * 100:+.3f}%", ret_color),
        row("P(up)", conf, conf_color),
        row("Return band", f"{interval_low * 100:+.2f}% to {interval_high * 100:+.2f}%", COLORS["violet"]),
        row("Price band", f"${low_price:,.2f} – ${high_price:,.2f}", COLORS["violet"]),
    ]

    company_display = f"<div class=\"aegis-pred-label\" style=\"margin-bottom:0.35rem;color:{COLORS['accent']};\">{company_name}</div>" if company_name else ""
    st.markdown(
        f"""
        <div class="aegis-panel aegis-forecast-compact">
            {company_display}
            <div class="aegis-pred-label" style="margin-bottom:0.5rem;">
                {symbol} · {horizon_label(horizon)} · {timeframe}
            </div>
            {"".join(rows)}
            <p style="margin:0.6rem 0 0;font-family:'IBM Plex Mono',monospace;font-size:0.68rem;color:{COLORS['muted']};">
                Model {model_version or '—'} · trained {trained}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_forecast_telemetry(
    *,
    symbol: str,
    horizon: str,
    timeframe: str,
    last_close: float,
    expected_return: float,
    expected_price: float,
    interval_low: float,
    interval_high: float,
    p_up: float | None,
    model_version: str | None,
) -> None:
    low_price = last_close * (1.0 + interval_low)
    high_price = last_close * (1.0 + interval_high)
    conf = "—" if p_up is None else f"{p_up * 100:.1f}%"

    st.markdown(
        f"""
        <div class="aegis-panel">
            <div class="aegis-pred-label" style="margin-bottom:0.65rem;">
                Forecast · {symbol} · {horizon_label(horizon)}
            </div>
            <div class="aegis-telemetry-strip">
                <div>
                    <div class="aegis-pred-label">Last close</div>
                    <div class="aegis-pred-value-lg aegis-mono" style="color:{COLORS['text']}">${last_close:,.2f}</div>
                </div>
                <div>
                    <div class="aegis-pred-label">Target price</div>
                    <div class="aegis-pred-value-lg aegis-mono" style="color:{COLORS['magenta']}">${expected_price:,.2f}</div>
                </div>
                <div>
                    <div class="aegis-pred-label">P(up)</div>
                    <div class="aegis-pred-value-lg aegis-mono" style="color:{COLORS['accent']}">{conf}</div>
                </div>
            </div>
            <div class="aegis-telemetry-strip">
                <div>
                    <div class="aegis-pred-label">Return forecast</div>
                    <div class="aegis-pred-value aegis-mono" style="color:{_value_color(expected_return)}">{expected_return * 100:+.4f}%</div>
                </div>
                <div>
                    <div class="aegis-pred-label">Return interval</div>
                    <div class="aegis-pred-value aegis-mono" style="color:{COLORS['violet']}">
                        {interval_low * 100:+.3f}% to {interval_high * 100:+.3f}%
                    </div>
                </div>
                <div>
                    <div class="aegis-pred-label">Price band</div>
                    <div class="aegis-pred-value aegis-mono" style="color:{COLORS['violet']};font-size:1rem;">
                        ${low_price:,.2f} – ${high_price:,.2f}
                    </div>
                </div>
            </div>
            <p style="margin:0.4rem 0 0;font-family:'IBM Plex Mono',monospace;font-size:0.72rem;color:{COLORS['muted']};">
                {model_version or '—'} · {timeframe} · {horizon_label(horizon)}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_raw_data_summary(df: pd.DataFrame, *, symbol: str, timeframe: str) -> None:
    if df.empty:
        render_empty_state("No market data", f"No bars loaded for {symbol} ({timeframe}).")
        return

    last = df.iloc[-1]
    last_close = float(last.get("close", 0))
    period_high = float(df["high"].max()) if "high" in df.columns else last_close
    period_low = float(df["low"].min()) if "low" in df.columns else last_close
    bar_count = len(df)
    vol = last.get("volume")
    vol_txt = "—" if vol is None or (isinstance(vol, float) and pd.isna(vol)) else f"{int(vol):,}"

    st.markdown(
        f"""
        <div class="aegis-panel">
            <div class="aegis-pred-label" style="margin-bottom:0.65rem;">Market feed · {symbol} · {timeframe}</div>
            <div class="aegis-pred-grid">
                <div class="aegis-pred-card">
                    <div class="aegis-pred-label">Bars</div>
                    <div class="aegis-pred-value aegis-mono" style="color:{COLORS['accent']}">{bar_count:,}</div>
                </div>
                <div class="aegis-pred-card">
                    <div class="aegis-pred-label">Last close</div>
                    <div class="aegis-pred-value aegis-mono" style="color:{COLORS['text']}">${last_close:,.2f}</div>
                </div>
                <div class="aegis-pred-card">
                    <div class="aegis-pred-label">Period high</div>
                    <div class="aegis-pred-value aegis-mono" style="color:{COLORS['success']}">${period_high:,.2f}</div>
                </div>
                <div class="aegis-pred-card">
                    <div class="aegis-pred-label">Period low</div>
                    <div class="aegis-pred-value aegis-mono" style="color:{COLORS['danger']}">${period_low:,.2f}</div>
                </div>
            </div>
            <p style="margin:0;font-family:'IBM Plex Mono',monospace;font-size:0.72rem;color:{COLORS['muted']};">
                Last volume {vol_txt} · range ${period_low:,.2f} – ${period_high:,.2f}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_raw_data_table(df: pd.DataFrame, *, limit: int = 100) -> None:
    if df.empty:
        render_empty_state("No rows", "Load price data from the API to populate this table.")
        return

    view = df.tail(limit).copy()
    if "ts_utc" in view.columns:
        view["ts_utc"] = pd.to_datetime(view["ts_utc"]).dt.strftime("%Y-%m-%d %H:%M")

    col_defs: list[tuple[str, str, str | None]] = [
        ("ts_utc", "Time", COLORS["muted"]),
        ("open", "Open", COLORS["text"]),
        ("high", "High", COLORS["success"]),
        ("low", "Low", COLORS["danger"]),
        ("close", "Close", COLORS["accent"]),
        ("volume", "Volume", COLORS["violet"]),
    ]
    optional = [
        ("ma_fast", "MA fast", COLORS["magenta"]),
        ("ma_slow", "MA slow", COLORS["violet"]),
        ("ret_1", "Ret 1", None),
        ("ret_5", "Ret 5", None),
    ]
    for col, label, _ in optional:
        if col in view.columns:
            col_defs.append((col, label, _))

    headers = "".join(f"<th>{label}</th>" for _, label, _ in col_defs)
    body: list[str] = []
    for _, row in view.iterrows():
        cells = []
        for col, _, default_color in col_defs:
            val = row.get(col)
            if val is None or (isinstance(val, float) and pd.isna(val)):
                txt, color = "—", COLORS["muted"]
            elif col == "ts_utc":
                txt, color = str(val), COLORS["muted"]
            elif col in {"ret_1", "ret_5"}:
                fval = float(val)
                txt, color = f"{fval * 100:+.3f}%", _value_color(fval)
            elif col == "volume":
                txt, color = f"{int(val):,}", default_color or COLORS["violet"]
            elif col in {"open", "high", "low", "close", "ma_fast", "ma_slow"}:
                txt, color = f"{float(val):,.4f}", default_color or COLORS["text"]
            else:
                txt, color = str(val), default_color or COLORS["text"]
            cells.append(f"<td style='color:{color}'>{txt}</td>")
        body.append(f"<tr>{''.join(cells)}</tr>")

    st.markdown(
        f"""
        <div class="aegis-panel" style="padding:0.75rem 1rem;overflow-x:auto;">
            <div class="aegis-pred-label" style="margin-bottom:0.55rem;">
                OHLCV · {len(view)} of {len(df)} rows
            </div>
            <table class="aegis-pred-table">
                <thead><tr>{headers}</tr></thead>
                <tbody>{"".join(body)}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_prediction_history_table(rows: list[dict[str, Any]]) -> None:
    if not rows:
        render_empty_state("No history yet", "Predictions are logged when you load a symbol and horizon.")
        return

    body = []
    for row in rows:
        exp_ret = float(row.get("expected_return", 0))
        exp_price = float(row.get("expected_price", 0))
        p_up = row.get("p_up")
        p_up_txt = "—" if p_up is None else f"{float(p_up) * 100:.1f}%"
        ret_color = _value_color(exp_ret)
        created = str(row.get("created_at", ""))[:19].replace("T", " ")
        body.append(
            f"<tr>"
            f"<td>{row.get('symbol', '')}</td>"
            f"<td>{horizon_label(str(row.get('horizon', '')))}</td>"
            f"<td style='color:{ret_color}'>{exp_ret * 100:+.3f}%</td>"
            f"<td style='color:{COLORS['accent']}'>${exp_price:,.2f}</td>"
            f"<td style='color:{COLORS['violet']}'>{p_up_txt}</td>"
            f"<td style='color:{COLORS['muted']};font-size:0.75rem;'>{created}</td>"
            f"</tr>"
        )

    st.markdown(
        f"""
        <table class="aegis-pred-table">
            <thead>
                <tr>
                    <th>Symbol</th>
                    <th>Horizon</th>
                    <th>Return</th>
                    <th>Price</th>
                    <th>P(up)</th>
                    <th>When</th>
                </tr>
            </thead>
            <tbody>{"".join(body)}</tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )


def render_profile_panel(
    *,
    username: str,
    favorite_symbol: str | None,
    favorite_horizon: str | None,
    watchlist: list[str],
    current_symbol: str,
    current_horizon: str,
) -> None:
    watchlist_html = "".join(f'<span class="aegis-chip">{s}</span>' for s in watchlist)
    if not watchlist_html:
        watchlist_html = f'<span style="color:{COLORS["muted"]};font-size:0.85rem;">Add symbols in the sidebar</span>'

    st.markdown(
        f"""
        <div class="aegis-panel">
            <div class="aegis-pred-label">Account</div>
            <p style="margin:0.35rem 0 0.85rem;font-size:1rem;font-weight:600;color:{COLORS['text']};">{username}</p>
            <div class="aegis-pred-label">Saved defaults</div>
            <p style="margin:0.25rem 0 0.65rem;color:{COLORS['muted']};font-size:0.88rem;">
                {favorite_symbol or current_symbol} · {horizon_label(favorite_horizon or current_horizon)}
            </p>
            <div class="aegis-pred-label">Watchlist</div>
            <div style="margin-top:0.35rem;">{watchlist_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_market_stats_strip(
    *,
    period_return: float,
    volatility: float,
    avg_volume: float | None,
    bar_count: int,
) -> None:
    ret_color = _value_color(period_return)
    vol_color = COLORS["warning"] if volatility >= 0.015 else COLORS["success"] if volatility <= 0.008 else COLORS["muted"]
    vol_txt = f"{volatility * 100:.2f}%" if volatility == volatility else "—"
    avg_vol_txt = "—" if avg_volume is None else f"{int(avg_volume):,}"

    st.markdown(
        f"""
        <div class="aegis-pred-grid">
            <div class="aegis-pred-card">
                <div class="aegis-pred-label">Period return</div>
                <div class="aegis-pred-value aegis-mono" style="color:{ret_color}">{period_return * 100:+.2f}%</div>
            </div>
            <div class="aegis-pred-card">
                <div class="aegis-pred-label">Volatility (1-bar)</div>
                <div class="aegis-pred-value aegis-mono" style="color:{vol_color}">{vol_txt}</div>
            </div>
            <div class="aegis-pred-card">
                <div class="aegis-pred-label">Avg volume</div>
                <div class="aegis-pred-value aegis-mono" style="color:{COLORS['violet']}">{avg_vol_txt}</div>
            </div>
            <div class="aegis-pred-card">
                <div class="aegis-pred-label">Bars loaded</div>
                <div class="aegis-pred-value aegis-mono" style="color:{COLORS['accent']}">{bar_count:,}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_horizon_comparison_table(rows: list[dict[str, Any]], *, current_horizon: str) -> None:
    if not rows:
        render_empty_state("No horizon data", "Predictions across horizons will appear once the API responds.")
        return

    body = []
    for row in rows:
        horizon = str(row.get("horizon", ""))
        exp_ret = float(row.get("expected_return", 0))
        p_up = row.get("p_up")
        p_up_txt = "—" if p_up is None else f"{float(p_up) * 100:.1f}%"
        active = " · active" if horizon == current_horizon else ""
        body.append(
            f"<tr>"
            f"<td>{horizon_label(horizon)}{active}</td>"
            f"<td style='color:{_value_color(exp_ret)}'>{exp_ret * 100:+.3f}%</td>"
            f"<td style='color:{COLORS['accent']}'>${float(row.get('expected_price', 0)):,.2f}</td>"
            f"<td style='color:{COLORS['violet']}'>{p_up_txt}</td>"
            f"<td style='color:{COLORS['muted']}'>{float(row.get('interval_low', 0)) * 100:+.2f}% to {float(row.get('interval_high', 0)) * 100:+.2f}%</td>"
            f"</tr>"
        )

    st.markdown(
        f"""
        <div class="aegis-panel" style="padding:0.75rem 1rem;overflow-x:auto;">
            <div class="aegis-pred-label" style="margin-bottom:0.55rem;">Horizon comparison</div>
            <table class="aegis-pred-table">
                <thead>
                    <tr>
                        <th>Horizon</th>
                        <th>Return</th>
                        <th>Target</th>
                        <th>P(up)</th>
                        <th>Band</th>
                    </tr>
                </thead>
                <tbody>{"".join(body)}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_watchlist_snapshot(rows: list[dict[str, Any]], *, current_symbol: str, horizon: str) -> None:
    if not rows:
        render_empty_state("Watchlist empty", "Add symbols in the sidebar to compare forecasts here.")
        return

    body = []
    for row in rows:
        sym = str(row.get("symbol", ""))
        exp_ret = float(row.get("expected_return", 0))
        p_up = row.get("p_up")
        advice = str(row.get("advice", "Hold"))
        advice_color = COLORS["success"] if advice == "Buy" else COLORS["danger"] if "Sell" in advice else COLORS["warning"]
        active = " · selected" if sym == current_symbol else ""
        body.append(
            f"<tr>"
            f"<td>{sym}{active}</td>"
            f"<td style='color:{_value_color(exp_ret)}'>{exp_ret * 100:+.3f}%</td>"
            f"<td style='color:{COLORS['accent']}'>${float(row.get('expected_price', 0)):,.2f}</td>"
            f"<td style='color:{COLORS['violet']}'>{'—' if p_up is None else f'{float(p_up) * 100:.1f}%'}</td>"
            f"<td style='color:{advice_color}'>{advice}</td>"
            f"</tr>"
        )

    st.markdown(
        f"""
        <div class="aegis-panel" style="padding:0.75rem 1rem;overflow-x:auto;">
            <div class="aegis-pred-label" style="margin-bottom:0.55rem;">Watchlist · {horizon_label(horizon)}</div>
            <table class="aegis-pred-table">
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Return</th>
                        <th>Target</th>
                        <th>P(up)</th>
                        <th>Signal</th>
                    </tr>
                </thead>
                <tbody>{"".join(body)}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_risk_summary_panel(
    *,
    last_close: float,
    expected_return: float,
    expected_price: float,
    interval_low: float,
    interval_high: float,
    p_down_1: float,
    p_down_2: float,
    p_up: float | None,
) -> None:
    band_width = interval_high - interval_low
    low_price = last_close * (1.0 + interval_low)
    high_price = last_close * (1.0 + interval_high)
    conf = "—" if p_up is None else f"{float(p_up) * 100:.1f}%"

    st.markdown(
        f"""
        <div class="aegis-panel">
            <div class="aegis-pred-label" style="margin-bottom:0.65rem;">Risk summary</div>
            <div class="aegis-telemetry-strip">
                <div>
                    <div class="aegis-pred-label">Expected move</div>
                    <div class="aegis-pred-value aegis-mono" style="color:{_value_color(expected_return)}">{expected_return * 100:+.3f}%</div>
                </div>
                <div>
                    <div class="aegis-pred-label">Band width</div>
                    <div class="aegis-pred-value aegis-mono" style="color:{COLORS['violet']}">{band_width * 100:.2f}%</div>
                </div>
                <div>
                    <div class="aegis-pred-label">Direction confidence</div>
                    <div class="aegis-pred-value aegis-mono" style="color:{COLORS['accent']}">{conf}</div>
                </div>
            </div>
            <div class="aegis-telemetry-strip">
                <div>
                    <div class="aegis-pred-label">Price band</div>
                    <div class="aegis-pred-value aegis-mono" style="color:{COLORS['violet']};font-size:1rem;">
                        ${low_price:,.2f} – ${high_price:,.2f}
                    </div>
                </div>
                <div>
                    <div class="aegis-pred-label">Target price</div>
                    <div class="aegis-pred-value aegis-mono" style="color:{COLORS['magenta']}">${expected_price:,.2f}</div>
                </div>
                <div>
                    <div class="aegis-pred-label">Tail risk</div>
                    <div class="aegis-pred-value aegis-mono" style="color:{COLORS['danger']}">
                        {p_down_1 * 100:.1f}% / {p_down_2 * 100:.1f}%
                    </div>
                </div>
            </div>
            <p style="margin:0.35rem 0 0;font-size:0.82rem;color:{COLORS['muted']};">
                Tail risk shows P(return &lt; −1%) / P(return &lt; −2%) from the conformal interval.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_footer(*, symbol_count: int, api_base: str) -> None:
    st.markdown(
        f"""
        <div class="aegis-panel" style="padding:0.75rem 0.9rem;margin-top:0.5rem;">
            <div class="aegis-pred-label">System</div>
            <p style="margin:0.35rem 0 0.5rem;font-size:0.82rem;color:{COLORS['muted']};">
                {symbol_count} trained symbol{"s" if symbol_count != 1 else ""} · API online
            </p>
            <span class="aegis-chip">{api_base}</span>
            <span class="aegis-chip">/docs</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def apply_plotly_theme(fig, *, height: int | None = None, title: str | None = None):
    layout = dict(PLOTLY_TEMPLATE)
    if height is not None:
        layout["height"] = height
    if title:
        layout["title"] = {
            "text": title,
            "font": {"family": "IBM Plex Sans, sans-serif", "size": 13, "color": COLORS["text"]},
            "x": 0,
            "xanchor": "left",
        }
    fig.update_layout(**layout)
    fig.update_xaxes(showgrid=True, gridwidth=1)
    fig.update_yaxes(showgrid=True, gridwidth=1)
    return fig
