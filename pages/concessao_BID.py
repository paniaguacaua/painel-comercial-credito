import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import base64
from pathlib import Path
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Concessão BID",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

COR_TEAL   = "#00AE9D"
COR_VERDE  = "#7DB61C"
COR_ROXO   = "#49479D"
COR_ESCURO = "#003641"
COR_TEXTO  = "#F0FAF9"
COR_MUTED  = "#9ECFCA"
COR_CARD   = "#00485A"
COR_BORDER = "#006B80"
COR_BG     = "#002B36"
COR_LABEL  = "#C8E8E5"
COR_AXIS   = "#D4EEEB"

def _b64_font(path):
    p = Path(path)
    if p.exists():
        data = p.read_bytes()
        ext  = p.suffix.lstrip(".")
        fmt  = "woff2" if ext == "woff2" else "woff" if ext == "woff" else "truetype"
        mime = "font/woff2" if ext == "woff2" else "font/woff" if ext == "woff" else "font/truetype"
        return f"data:{mime};base64,{base64.b64encode(data).decode()}", fmt
    return None, None

_SICOOB_PATHS = {
    "400": ["static/SicoobSans-Regular.woff2","static/SicoobSans-Regular.woff","static/SicoobSans-Regular.ttf"],
    "600": ["static/SicoobSans-SemiBold.woff2","static/SicoobSans-SemiBold.woff","static/SicoobSans-SemiBold.ttf"],
    "700": ["static/SicoobSans-Bold.woff2","static/SicoobSans-Bold.woff","static/SicoobSans-Bold.ttf"],
    "800": ["static/SicoobSans-ExtraBold.woff2","static/SicoobSans-ExtraBold.woff","static/SicoobSans-ExtraBold.ttf"],
}

_font_face_blocks = []
_sicoob_available = False
for weight, candidates in _SICOOB_PATHS.items():
    for candidate in candidates:
        data_uri, fmt = _b64_font(candidate)
        if data_uri:
            _font_face_blocks.append(f"""
@font-face {{
    font-family: 'Sicoob Sans';
    src: url('{data_uri}') format('{fmt}');
    font-weight: {weight};
    font-style: normal;
    font-display: swap;
}}""")
            _sicoob_available = True
            break

_FONT_IMPORT = ""
if not _sicoob_available:
    _FONT_IMPORT = "@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@300;400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');"

_PRIMARY_FONT = "'Sicoob Sans', 'Nunito Sans', 'DM Sans', sans-serif" if _sicoob_available else "'Nunito Sans', 'DM Sans', sans-serif"
_HEADING_FONT = _PRIMARY_FONT
_font_faces_css = "\n".join(_font_face_blocks)

st.markdown(f"""
<style>
{_FONT_IMPORT}
{_font_faces_css}

:root {{
    --bg:      {COR_BG};
    --card:    {COR_CARD};
    --border:  {COR_BORDER};
    --teal:    {COR_TEAL};
    --verde:   {COR_VERDE};
    --roxo:    {COR_ROXO};
    --escuro:  {COR_ESCURO};
    --text:    {COR_TEXTO};
    --muted:   {COR_MUTED};
    --label:   {COR_LABEL};
    --axis:    {COR_AXIS};
    --font:    {_PRIMARY_FONT};
    --heading: {_HEADING_FONT};
}}

html, body, [class*="css"] {{
    font-family: var(--font) !important;
    background-color: var(--bg);
    color: var(--text);
    -webkit-font-smoothing: antialiased;
}}
.stApp {{ background-color: var(--bg); }}

/* ── SIDEBAR ─────────────────────────────── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {COR_ESCURO} 0%, #001F28 100%) !important;
    border-right: 1px solid var(--border);
    width: 300px !important;
}}
[data-testid="stSidebar"] * {{
    font-family: var(--font) !important;
    color: var(--text) !important;
}}
[data-testid="stSidebar"] label {{
    color: var(--label) !important;
    font-size: 0.76rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {{
    color: var(--text) !important;
}}
[data-testid="stSidebar"] .stCaption {{
    color: var(--muted) !important;
    font-size: 0.76rem !important;
}}

/* Selectbox e Multiselect */
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="select"] > div:hover {{
    background-color: #005570 !important;
    border: 1px solid {COR_BORDER} !important;
    border-radius: 8px !important;
}}
[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="select"] div,
[data-testid="stSidebar"] [data-baseweb="select"] input {{
    color: {COR_TEXTO} !important;
    background-color: transparent !important;
    font-size: 0.88rem !important;
}}
/* Placeholder */
[data-testid="stSidebar"] [data-baseweb="select"] [aria-placeholder],
[data-testid="stSidebar"] [data-baseweb="select"] .placeholder {{
    color: {COR_MUTED} !important;
    opacity: 1 !important;
}}
/* Dropdown list */
[data-baseweb="popover"] [data-baseweb="menu"],
[data-baseweb="popover"] ul {{
    background-color: #004A5E !important;
    border: 1px solid {COR_BORDER} !important;
}}
[data-baseweb="popover"] li,
[data-baseweb="popover"] [role="option"] {{
    color: {COR_TEXTO} !important;
    background-color: transparent !important;
    font-size: 0.88rem !important;
}}
[data-baseweb="popover"] li:hover,
[data-baseweb="popover"] [role="option"]:hover {{
    background-color: {COR_TEAL}33 !important;
}}
/* Tags multiselect */
[data-testid="stSidebar"] [data-baseweb="tag"] {{
    background-color: {COR_TEAL}44 !important;
    border: 1px solid {COR_TEAL} !important;
    border-radius: 6px !important;
}}
[data-testid="stSidebar"] [data-baseweb="tag"] span {{
    color: {COR_TEXTO} !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
}}

/* ── SIDEBAR NAVIGATION overhaul ─────────────────────────── */
[data-testid="stSidebarNavItems"] {{
    padding-top: 1.5rem !important;
}}
[data-testid="stSidebarNavItems"]::before {{
    margin-left: 1.25rem;
    margin-bottom: 0.75rem;
    font-size: 1.1rem;
    font-weight: 500;
    color: rgba(255,255,255,0.7);
    display: block;
    font-family: var(--font) !important;
}}
/* Links individuais */
[data-testid="stSidebarNavItem"] a {{
    background-color: transparent !important;
    border-radius: 12px !important;
    margin: 4px 12px !important;
    padding: 8px 16px !important;
    transition: all 0.2s ease !important;
}}
/* Efeito de hover */
[data-testid="stSidebarNavItem"] a:hover {{
    background-color: rgba(255,255,255,0.06) !important;
}}
/* Item de página ATIVO */
[data-testid="stSidebarNavItem"] a[aria-current="page"] {{
    background-color: rgba(255,255,255,0.12) !important;
}}
/* Texto do link */
[data-testid="stSidebarNavItem"] span {{
    color: white !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
}}
/* Esconder ícones padrão para um look mais clean */
[data-testid="stSidebarNavItem"] [data-testid="stIconMaterial"] {{
    display: none !important;
}}

/* ── HEADER ──────────────────────────────── */
.main-header {{
    background: linear-gradient(135deg, {COR_ESCURO} 0%, #005A6E 55%, {COR_ESCURO} 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 40px 20px;
    margin-bottom: 22px;
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}}
.main-header::before {{
    content: '';
    position: absolute;
    top: -40%; right: -5%;
    width: 380px; height: 380px;
    background: radial-gradient(circle, rgba(0,174,157,0.22) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}}
.main-header h1 {{
    font-family: var(--heading) !important;
    font-size: 2.6rem;
    font-weight: 800;
    margin: 15px 0 0;
    background: white;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    position: relative; z-index: 1;
    letter-spacing: -0.01em;
    line-height: 1.2;
}}
.main-header p {{ color: var(--muted); font-size: 0.92rem; margin: 8px 0 0; font-weight: 400; position: relative; z-index: 1; }}

/* ── SECTION TITLE ──────────────────────── */
.section-title {{
    font-family: var(--heading) !important;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: {COR_TEAL};
    margin: 28px 0 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}}
.section-title::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}}

/* ── MÉTRICAS ────────────────────────────── */
[data-testid="stMetric"] {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px 24px !important;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}}
[data-testid="stMetric"]:hover {{
    border-color: {COR_TEAL} !important;
}}
[data-testid="stMetric"]::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, {COR_TEAL}, {COR_VERDE});
    border-radius: 14px 0 0 14px;
}}
/* Label da métrica — era quase invisível */
[data-testid="stMetric"] label,
[data-testid="stMetricLabel"] {{
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--label) !important;    /* #C8E8E5 — bem mais legível */
    font-family: var(--font) !important;
}}
/* Valor principal da métrica */
[data-testid="stMetricValue"] {{
    font-family: var(--heading) !important;
    font-size: 1.65rem !important;
    font-weight: 800 !important;
    color: {COR_TEXTO} !important;    /* branco quase puro */
    letter-spacing: -0.02em !important;
    line-height: 1.1 !important;
}}
/* Delta da métrica */
[data-testid="stMetricDelta"] {{
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    color: {COR_MUTED} !important;     /* #9ECFCA — visível */
    font-family: var(--font) !important;
}}
[data-testid="stMetricDelta"] svg {{ display: none; }}

/* ── DATAFRAME ───────────────────────────── */
[data-testid="stDataFrame"] {{
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border);
}}
[data-testid="stDataFrame"] tr:hover td {{
    background-color: #005570 !important;
}}

/* ── PLOTLY TRANSPARENT ──────────────────── */
.js-plotly-plot .plotly {{ background: transparent !important; }}

/* ── TÍTULOS DE GRÁFICO ──────────────────── */
.chart-title {{
    font-family: var(--heading) !important;
    font-size: 0.98rem;
    font-weight: 700;
    color: {COR_TEXTO};
    margin: 0 0 6px 4px;
    letter-spacing: -0.01em;
}}

/* ── SCROLLBAR ───────────────────────────── */
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: var(--bg); }}
::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}

/* ── LAYOUT ──────────────────────────────── */
.block-container {{ padding-top: 1.4rem !important; }}

/* ── SIDEBAR HELPERS ─────────────────────── */
.sb-divider {{ height: 1px; background: var(--border); margin: 14px 0; }}
.sb-logo {{
    font-family: var(--heading) !important;
    font-size: 1.5rem; font-weight: 800;
    color: {COR_TEAL}; padding-bottom: 2px; letter-spacing: 0.02em;
}}

/* ── NO-DATA ─────────────────────────────── */
.no-data {{
    text-align: center; padding: 54px 20px;
    background: var(--card);
    border: 1px dashed var(--border);
    border-radius: 14px;
    color: var(--muted); font-size: 0.9rem;
    font-family: var(--font) !important;
}}

/* ── LOGIN ───────────────────────────────── */
div[data-testid="stTextInput"] input {{
    background: {COR_CARD} !important;
    border: 1px solid {COR_BORDER} !important;
    border-radius: 10px !important;
    color: {COR_TEXTO} !important;
    font-size: 0.95rem !important;
    padding: 12px 16px !important;
    font-family: var(--font) !important;
}}
div[data-testid="stTextInput"] input:focus {{
    border-color: {COR_TEAL} !important;
    box-shadow: 0 0 0 3px rgba(0,174,157,0.2) !important;
}}
div[data-testid="stTextInput"] input::placeholder {{
    color: {COR_MUTED} !important;
    opacity: 1 !important;
}}
.stButton > button {{
    background: linear-gradient(135deg, {COR_TEAL}, {COR_VERDE}) !important;
    color: #001E26 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 8px 20px !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.04em !important;
    font-family: var(--font) !important;
    transition: opacity 0.2s !important;
    min-height: 38px !important;
}}
.stButton > button:hover {{ opacity: 0.88 !important; }}

/* ── FILTROS ATIVOS (markdown inline) ────── */
.filtros-ativos {{
    background: {COR_CARD};
    border: 1px solid {COR_BORDER};
    border-radius: 10px;
    padding: 10px 18px;
    font-size: 0.84rem;
    color: {COR_LABEL};
    margin-bottom: 6px;
    font-family: var(--font) !important;
}}
.filtros-ativos strong {{
    color: {COR_TEXTO};
}}

/* ── PLOTLY TOOLBAR ──────────────────────── */
.modebar-btn[data-title="Zoom in"],
.modebar-btn[data-title="Zoom out"],
.modebar-btn[data-title="Reset axes"],
.modebar-btn[data-title="Autoscale"],
.modebar-btn[data-title="Lasso Select"],
.modebar-btn[data-title="Box Select"],
.modebar-btn[data-title="Toggle Spike Lines"],
.modebar-btn[data-title="Show closest data on hover"],
.modebar-btn[data-title="Compare data on hover"] {{
    display: none !important;
}}
.modebar {{ opacity: 1 !important; display: flex !important; }}

/* ── FULLSCREEN ──────────────────────────── */
:-webkit-full-screen  {{ background-color: {COR_BG} !important; }}
:-moz-full-screen     {{ background-color: {COR_BG} !important; }}
:fullscreen           {{ background-color: {COR_BG} !important; }}

/* ── BOTÃO ABRIR (collapsedControl — sidebar fechada) ─────────────── */
[data-testid="collapsedControl"] {{
    background: linear-gradient(180deg, #003641 0%, #001F28 100%) !important;
    border-right: 1px solid #006B80 !important;
    border-bottom: 1px solid #006B80 !important;
    border-radius: 0 0 12px 0 !important;
    width: auto !important;
    min-width: 52px !important;
    padding: 14px 10px !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    gap: 10px !important;
}}
[data-testid="collapsedControl"]::before {{
    content: "FILTROS" !important;
    font-size: 0.6rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.14em !important;
    color: #9ECFCA !important;
    writing-mode: vertical-rl !important;
    text-orientation: mixed !important;
    transform: rotate(180deg) !important;
    margin-bottom: 4px !important;
}}
[data-testid="collapsedControl"] button {{
    background: rgba(0,174,157,0.13) !important;
    border: 1px solid rgba(0,174,157,0.4) !important;
    border-radius: 8px !important;
    width: 36px !important;
    height: 36px !important;
    padding: 0 !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: background 0.2s !important;
}}
[data-testid="collapsedControl"] button:hover {{
    background: rgba(0,174,157,0.28) !important;
}}
/* Mostra o ícone Material nativo keyboard_double_arrow_right */
[data-testid="collapsedControl"] button span[data-testid="stIconMaterial"] {{
    font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    font-size: 1.3rem !important;
    color: #00AE9D !important;
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
}}

/* ── BOTÃO FECHAR (dentro da sidebar) ───────────────────────── */
[data-testid="stSidebarCollapseButton"] {{
    display: flex !important;
    align-items: center !important;
    justify-content: flex-end !important;
    padding-right: 8px !important;
}}
[data-testid="stSidebarCollapseButton"] button {{
    background: transparent !important;
    border: none !important;
    width: 36px !important;
    height: 36px !important;
    padding: 0 !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: opacity 0.2s !important;
}}
[data-testid="stSidebarCollapseButton"] button:hover {{
    opacity: 0.7 !important;
}}
/* Mostra o ícone Material nativo keyboard_double_arrow_left — branco sem estilo extra */
[data-testid="stSidebarCollapseButton"] button span[data-testid="stIconMaterial"] {{
    font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    font-size: 1.3rem !important;
    color: #FFFFFF !important;
    display: block !important;
    visibility: visible !important;
    opacity: 0.85 !important;
}}

/* ── RESPONSIVO MOBILE ───────────────────── */
@media (max-width: 900px) {{
    .block-container {{ padding: 0.8rem 0.5rem 2rem !important; }}
    .main-header {{ 
        padding: 30px 15px !important; 
        border-radius: 12px !important; 
        margin-bottom: 16px !important;
    }}
    .main-header img {{
        height: 60px !important;
    }}
    .main-header h1 {{ 
        font-size: 1.6rem !important; 
        margin-top: 10px !important;
    }}
    .main-header p  {{ font-size: 0.8rem !important; }}
    .section-title  {{ font-size: 0.65rem !important; margin: 18px 0 10px !important; }}
    
    /* Métricas em lista no mobile */
    [data-testid="stMetric"] {{ 
        padding: 14px 16px !important; 
        border-radius: 10px !important; 
        margin-bottom: 10px !important; 
    }}
    [data-testid="stMetricValue"] {{ font-size: 1.4rem !important; }}
    [data-testid="stMetric"] label {{ font-size: 0.64rem !important; }}
    
    /* Forçar colunas a ocuparem 100% no mobile */
    [data-testid="stHorizontalBlock"] {{ 
        flex-direction: column !important; 
        gap: 0 !important; 
    }}
    [data-testid="stHorizontalBlock"] > div {{ 
        width: 100% !important; 
        min-width: 100% !important; 
        flex: 1 1 100% !important; 
        margin-bottom: 10px !important;
    }}
    
    [data-testid="stSidebar"] {{ width: 85vw !important; }}
    
    [data-testid="stDataFrame"] {{ overflow-x: auto !important; font-size: 0.75rem !important; }}
    .no-data {{ padding: 30px 16px !important; font-size: 0.82rem !important; }}
    .footer {{ font-size: 0.68rem !important; margin-top: 24px !important; }}
}}

/* ── FOOTER ──────────────────────────────── */
.footer {{
    text-align: center; margin-top: 46px; padding: 18px;
    color: #3A7080; font-size: 0.76rem;
    border-top: 1px solid var(--border);
    font-family: var(--font) !important;
    letter-spacing: 0.02em;
}}
</style>
""", unsafe_allow_html=True)

ARQUIVO_BID = "concessão_BID.xlsx"
ARQUIVO_GIRO = "concessão_BID_capital_giro.xlsx"
SENHA_CORRETA = "sicoob123"

LOGO_B64 = "data:image/png;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCAGQA+gDASIAAhEBAxEB/8QAHQABAAIDAQEBAQAAAAAAAAAAAAcIBQYJBAMCAf/EAFMQAAEDAgMEBAYOCAQFAgcBAAABAgMEBQYHEQgSITFBUWGBExQiMnGRFRYjN0JSYnOCk6GxstE1VnJ1kpSzwTNUVaIXGEN00pXwJERTY4PD4fH/xAAbAQEAAgMBAQAAAAAAAAAAAAAABAUCAwYBB//EADcRAQACAQIDBQQIBwEBAQAAAAABAgMEEQUhMRITMkFRFHGBkQYiM1JTscHRFTRCYZKh4fBUYv/aAAwDAQACEQMRAD8AuWAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANDzKxvJY5UtdrRi1ytR0kjk1SFF5Jp0uXnx6NOepGj8W4le9Xre65FXqlVE9SH0zCSZMa3Xw+u94ddNfi6Ju/ZoYE4XX67Pkz2jtTERMxEOc1OpyXyTz2iGZ9tWJP9cr/rlHtqxJ/rlf9cphgQvaM335+co/e3+9LM+2rEn+uV/1yj21Yk/1yv8ArlMMB7Rm+/Pzk72/3pZn21Yk/wBcr/rlHtqxJ/rlf9cphgPaM335+cne3+9LM+2rEn+uV/1yj21Yk/1yv+uUwwHtGb78/OTvb/el/b9ivF0D2zw4jubY3cFRKh2iKYr28Yw/WW6fzLvzMhUwsngfC/zXJp6DUaiJ8Ez4npo5q6H0D6NcQrqsHc5Odq/7j/nT5OL4/Gq0+bvaZLdm3955T/7mz3t4xh+st0/mXfmPbxjD9Zbp/Mu/M14HTd3X0c/7fqvxbfOWw+3jGH6y3T+Zd+Y9vGMP1lun8y78zXgO7r6Ht+q/Ft85bD7eMYfrLdP5l35j28Yw/WW6fzLvzNeA7uvoe36r8W3zlsPt4xh+st0/mXfmPbxjD9Zbp/Mu/M14Du6+h7fqvxbfOWw+3jGH6y3T+Zd+Y9vGMP1lun8y78zXgO7r6Ht+q/Ft85bD7eMYfrLdP5l35nts+ZOM7bVtnS91FU1F8qKqXwjHJ1LrxTuVDUQeTjpPkypxLWUtFq5bb++VtMvsVUmL8PMuVOzwMzXeDqIFXVY3p96KioqL/dFNiIT2YGz79+dx8AqQJ2b3l/2/sTYU+ekUyTWH2bgWtya7QY8+XxTvv8JmN/jsAA0rcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEZ504e8JDHiClj8uPSOqROlvwXd3JfSnURUWdqoIaqmlpqhiSRSsVj2ryVFTRUK74tss1gvtRbpdVY1d6J6/DjXzV/svainJcd0Xd5O/r0nr7/wDqk4jp+zbvI6T+bFAA59WAAAAAAAABiMQ0m/GlUxPKZwf2p1mXP45qOarXJqipoqEzh+svotRXNXy/3HnCJrdLXV4bYref+paWD13Silop0a9j0jeiuicqcHN104L06LqnceQ+vYctM2OuSk8pjeHzLLithvNLxtMAANrWAAAAAAAAH7p4ZaieOCFjpJZHIxjGpqrnKuiIh+CWtnnCfj10fiasj1p6Nyspkcnny6cXfRRfWvYa8uSMdZtKfwzQX4hqqaenn1/tHnKV8tsMx4UwrTW7Rq1Tvdap6cd6VU48epOCJ2IbKAUVrTad5fddPgpp8VcWONq1jaAAHjcA8F8vVnsdJ43errQ22n/+rV1DYm+tyoRvfdofKe1PdGmIn18jebaOlkkTucqI1e5TKKzPSGu+WlPFMQlcEBzbV+XDJFa21YolRPhNpYdF9cyKfyLavy4fIjXWnFEaLzc6lg0T1TKpl3V/Rq9swfehPoItw3tAZVXuRsTcSst8zuTLhC6BE9L1TcT+Ik2kqaespo6qkniqIJW70csT0cx6daKnBUMJrNesN1MlL+Gd31AB4zADWsRY9wZh26exl+xNbLZWeDbL4GpnSNysVVRFTXnyU9iJno8taKxvMtlBqVHmbl1Vu3YMdYbc7XRGrcomqq9iK5NTZaCuorhAk9BWU9XEvKSGRHtXvRRMTHV5W9bdJegAHjIAAAAAAAABhMS4twvhpm9iDENrtmqao2pqWMe70NVdV7kI9vO0flPb3OZFfam4PbzbSUUi+pXI1q9y9JlFLT0hrvmx08VohLoICk2sMuGPVrbTiiRE5ObSwaL65kU/VPtXZbyyox9sxNA1fhvpIVRP4ZVX7DLur+jV7Zg+9CewR5hHOvLLE8zKe34ppYKl+iJBWo6ncqr0Ir0Rrl7EVSQ0VFTVF1Qwmsx1b6XreN6zuAA8ZAAAAHivN2tVlonVt4uVHbqVvOaqnbExO9yogJnZ7QRPiHaIyps73RtxA+5St5soaZ8idz1RGL3ONTqtrPAbJN2msOI5mpzc6KFnq90X+xsjFefJHtq8NetoWEBXmHa0wMr9JsPYjYzrZHC5fUsiGyWPaTypuUiRz3WttjncvHKJ6Jr6WbyJ3roJxXjyeV1eC3S0JiBicN4mw9iSnWosF8t10jb5y0tQ2Td/aRF1TvMsa+iRExMbwAAPQAAAAAAAAH8keyNjpJHNYxqKrnOXREROlTQMUZ0ZY4de6K4YvoJZm8Fio96pdr1L4NHIi+lUPYiZ6MbXrSN7TskAECXLasy6p3ObS27ENaqcnMpo2MXvdIi/YeD/AJtcF/q3iD1Q/wDmZ9zf0R51uCP6ligQbatqXLGsejall9tya6b1RRtcnp9ze5fsJDwlmbgDFcjYrDiu2VU7/NgdJ4KZ3ojfo5fUeTjtHWGymoxX5VtDbwAYNwAAAB+JpYoInSzSMjjbzc9yIid6gfsGt3HH+BbdqlfjLD1M5PgyXKJHdyb2q80MDWZ2ZVUqqkuNrY7RdPclfL+FqmUVtPk1zlxx1tCQgRXNtDZPxK9q4vR7m68GW+qXX0L4PT7Tyf8AMllJ/rtX/wCnzf8Aie93f0Ye04fvx80vgiD/AJkspP8AXav/ANPm/wDE9lLtC5QVCtRMXJG5ya6SUFS3T0r4PT7R3d/Q9pwz/XHzSmDTLPmrlvdnNZRY2sbnu81ktW2Jy+hH6KpuFPNDUQtmglZLE9NWvY5HNcnYqczGYmOrbW9beGd37AB4yAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADTM2MPey9iWup496sokV7dE4vj+E3+6ehes3MGnUYK58c47dJa8uOMlJrPmq8DaczMPewWIHOgZu0VVrJBonBvxmdy/YqGrHz3PhthyTjt1hzGTHOO01nyAAamAAAAAAHusNsqLzd6e20ye6TP016Gp0uXsRNVPCTFk5h7xC1uvVSzSorG6RIqcWxdf0l4+hEJ3D9JOqzRTy8/ckaXBObJFfLzfLNXAtPc8CxU9rg0q7TGr6VETypGonls7VXTXtVO0raXWK1Z5YT9r2KHV9JHu2+4qsrNE4RyfDZ611TsXToPp2gyRWO68vJQ/TTg8bRrcUdOVv0n9Pkj4AFm+cgAAAAAAAPfh+1Vd8vVJaaFm9PUyIxvU1Oly9iJqq9iFt8OWmksVjpLTRN0gpo0YirzcvS5e1V1VfSRns74T8TtsmKK2LSerRY6VHJxZFrxd9JU9SdpLhU6zN27dmOkPrP0P4R7JpvackfXv/qvl8+vyADz3KtpLbb6i4V87KekponSzSvXRrGNTVVX0IhDdi+GILzasP2eou96r4KGgpm70s0ztGtT+6ryRE4qvBCp2bW1Hd7hNNbcv6f2NouLfZGojR1RJ2saurWJ6dXdPkrwI5z+zYueZeJX+DkmpsP0j1Sho95UR2mqeFkTkr1RfopwTpVYyJuLBEc7KHV8QtaezjnaPV7b1drpe699feLjV3Crf501TM6R697l1PEASVZM79QAB4G95SZp4oy4vEdRa6uSe2ufrVW2V6+Bmb06J8B3U5OPXqmqLogPJiJjaWdL2pParO0unmDMRW3FmF7fiK0SLJRV0KSx6+c1eTmr8prkVq9qKZcr1sKXOapy1u1slc5zaK5q6LXk1skbV3U+kjl+kWFK29ezaYdTgyd7ji/qFIdt/35Yf3RB+OQu8Uh23/flh/dEH45DZpvGi8T+w+KCj12q53K01bau13CroKhvmy00zo3p3tVFPICe56J2WayA2jbvHeaTDeP6ptbRVMiRQ3N6I2WBy8GpIqJo5irom8vFNdVVU5W5OVh0gyPvU2IMo8M3apesk8tAxkr111c9nkOVe1VaqkLUY4rzhecN1Nsm9LTvs3MAEZagP45zWtVzlRrUTVVVdERCpW0XtEVFXPVYUy/rFhpG6x1d2ido+ZelsKp5rflpxXo0TiudMc3naGjPqKYK9qyYs2s9cF5fvloHzOvF6ZwWgpHJ7m7qlfyZ6OLvklWswNoPMbFckkUF0Ww0Dl8mmtqrG7T5Uvnr26KiL1ETOc5zlc5yucq6qqrqqqfwnUwVqoc+uy5fPaP7P3PLLPM+aeR8sr11c97lVzl61VeZ+ADahAAAE67Nmd9zwheKTDeJK2Srw1UvbEx8z1VaBVXRHNVf+n1t5JzTpRYKB5asWjaW3Fltit2qy6pg0/JS6TXnKTC1xqHOdNJbIWyOdzc5rUaq96tVe83Aq5jadnV1t2qxPqHhvt3tlitU91vFdBQ0NO3elnmfutan59Sc1PFjjFNmwbhmrxBfapIKOmbrpw35XfBjYnS5eSJ9yIqlBs5s1MQ5l3tai4SLS2uFy+J2+Ny+DiT4zvjPVObl7tE4GzFim8/2RdVq66ePWUv5sbU1dUSzW3LykbSwJq32Uq496R3bHGvBqdrtV7EK5Ygvt6xDXur77day5VTv+rUzOkcidSa8k7E4GOBPpjrTooM2oyZp3vIADJoAAB6LdXVturI6y31dRR1Ma6xzQSLG9i9aOTihPOVe07iexSQ0GMolv9tRUatQiI2rjTr14Nk9DtFX4xX4GNqVt1bcWfJinek7OnGCsWYfxlY47zhy5RV1I/gqt4Ojd0te1eLXdi+nkZs5q5ZY8xBl9iSK9WGpVq6olRTPVfBVLPiPTp6dF5pzQv/lXj2yZiYUhv1mkVqr5FTTPVFkppdOLHfei9KaL2EHLhmnPyX+k1lc8bTys2sAGlOAAqoiarwQAQTnJtH4dwjLPaMMRxX+8xqrXvR//AMLA5Ohzk4vVOpve5F4Ea7TOfct3mqMH4HrnR2xirHXXGF2i1S8ljjVOUfW5PO6PJ86thLxaffnZT6viO09jF824Y/zMxtjmd7sQ32pmp3O1bRxO8HTs6tI28F0611XtNPAJcREcoU9rWtO9p3AAGIAAJLy2zvx/giWKKmu0lztjF8qgr3LKzTqa5fKZ9FdOtFLeZN50YVzIhbTUz1tt7a3WW3VD03l61jdwSRvo0VOlEOfB9qKqqaGrirKOolpqmF6PilierXscnFFRU4opqyYa396bp9dkwzt1h1NBBOzJncmOqdMM4mlijxHAzWKVE3W1zETi7TkkidKJz5p0ok7EC1ZrO0uhxZa5a9qoVN2+3O9ksJN1Xd8DUrprw13oy2RUzb7/AErhL5iq/FGbMHjhG4h/L2+H5qvgAsHNAAAAAAZnC+K8S4XqvGcPX24WyTXVUp53Na79pvJydiophgJjd7EzE7ws9lZtU18E0VvzCoWVUC6N9kqONGyM7Xxp5Lk6VVumnQ1S1Fiu1svtpp7tZ66Cuoalm/FPC/ea5PzReCpzRU0U5cks7N2a1Xl3iuOkrp3vw5cJGsrYlVVSBV4JM1OhU+Fpzb2omkbLgiY3qtNJxC1ZiuWd49V+gfyN7JI2yMcjmOTVrkXVFTrP6Ql6AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwWObCzEGH5qNETxhnulO5eh6ck9C8u8r7Kx8UjopGqx7FVrmqmioqc0LPkQZyYe8TuLb5TM0gq3bs6JybLpz+kn2ovWc7x3RdusZ69Y6+5V8S0/ajvI8uqPQAcopQAAAAiKqoiJqq8kAz+AbA7EGIIqZzV8Vi90qHfIReXpVeH/+FgWNaxjWMajWtTRERNERDWsuMPJYMPsbKzSsqdJahelF6G9yfaqmzHc8J0Xs2He3itzn9nRaLT9zj59ZDA4+w5BinDFVapUakrk36eRU/wAOVPNX+y9iqZ4FrW01neG/Phpnx2xZI3iY2lS6spp6OrmpKmN0U8L1jkY7m1yLoqHyJj2isJ+Aqo8V0UfucypFWo1PNfya/vTgvaidZDheYskZKRaHwvivD78O1VsF/LpPrHlP/vMABtVwAABseXOGZcVYqprYiOSnRfC1T0+BEnPvXgidqmuFmslMJ+1vCrKiqi3bjXoks2qcWN+AzuRdV7VUj6nL3dN46r/6OcJniWsito+pXnb3enx/LdvNPDFT08dPBG2OKJiMYxqaI1qJoiJ3H7AKV9qiIiNoCuW3FjSW14Ut2DaKZWS3d6z1e6vHwEapo1exz/wKWNKKbZ1yfXZ41lK52qW+ip6dqa8kVnhf/wBpuwV3uhcQyTTBO3nyQuACwc2H0p4ZqidkFPFJNNI5GsjY1XOcq8kRE5qfMvBsf4Dslmy2oMWLSwT3q7JJI6qciOdDHvK1sbF+CmjdV04qqqi8k0wyZIpG6TpdPOov2YnZV615MZpXKnSemwTdWsVNU8OxsC+qRWqfWsyRzWpY9+XBNxcnH/CVki+prlU6Hgi+1W9Fr/CsfrLmDfcN4hsL9y+WK6Wx2umlXSPi1/iRDFHVGaKOaJ0U0bJI3po5r01RU6lRSN8b5GZaYrY91Rh2G21Tv/mbbpTvRetWtTccva5qmddVHnDRk4VaPBZpmw1an0eVVdcpGbq3C6SOjXTzmMYxqf7keT6YPAOGaHBuDrZhm2ue+moIfBte9ERz1VVc5y6cNVcqr3mcI17dq0ytcGPu8daz5BSHbf8Aflh/dEH45C7xSHbf9+WH90QfjkNmm8aLxP7D4oKABPc6HQjZe94bC3zEv9aQ57nQjZe94bC3zEv9aQj6rwwtOFfaz7v2SWAabnTjWLAGXNzxEu66qYzwNFG7ij538GJp0onFy9jVIURvO0Ly9opWbT0hBW2Jm5LFJLlzhyqViq1PZiojdx48Up0VOzi70o34yFUz7VtVUVtbPW1cz5qieR0ssj11c97l1Vyr1qqqp8SypSKRtDltRntmvNpAAZtAfuCKWeZkMMb5ZHro1jGqrnL1Iicybcg8gLnjyKK/4hlntWHlXWLdbpPWJ8jVNGs+WuuvQi80t/gjAmEcF0iU+GrFR0C7u6+ZrN6aT9qRdXO71NOTPWvKOaw0/D8mWO1PKFBbVlPmVdI2yUmCL5uO03XS0rokXXpRX6cO099XkjmtSs35cE3FyaKvuSskXh2Ncp0PBo9qt6J0cKx7c7S5j33CGK7EjnXrDV4tzW831NFJG31qmimEOqaoipovFDTcRZW5f364U9wuGFrd47TzsnbUQxJE9zmuRyb6s0304aKjteBnGq9Yab8Jn+iz3ZWWd+H8t8OWaVm5NSW2COZummkm4m//ALtTY3uaxjnvcjWtTVVVdEROs/pCm2Djl+FMs1tFDOsVyvznUzFaujmQIiLK5PSitZ9PsIsRN7beq1veuHHvPSFcdpnNGbMPGT6W3zu9rtse6OiYi6JM7k6ZevX4PU3TkqqRKAWdaxWNoctkyWyWm1usgBkMN2a44hv1FZLRTOqa6tlSKGNvSq9K9SImqqvJERVPWERMztDzUNJV19ZFR0NLPVVMzt2KGGNXvevUjU4qvoJXw9s45qXembUSWemtbHpq3x6qaxyp2tbvOb6FRFLYZJZTWDLWyRtghjq73NGiVtwc3Vzl6Ws181iLyTp0RV1UkUiX1M7/AFVzg4XG2+Seag+I9nXNSzU76htkhucbOLvEKhsju5i6OXuRSKaymqaKqkpaynlp6iJytkilYrHsVOhUXiinU4i/PfJ+y5k2aSaOOGhxFCzWlr0bpv6Jwjl085i9fNvNOlFU1M7/AFjPwuIjfHPP0c/Aey9Wyus12qrTc6Z9NW0kroZ4npxY5q6Kh4yWppjYJDyDzHqst8cwXFz5H2mqVIblAnHej189E+M3XVO9OkjwHkxFo2llS80tFq9YdTqSogq6SGrpZmTQTMbJFIx2rXtVNUVF6UVD6kC7FmNX3/LyfDVZMr6ywyJHHvLxdTP1WP8AhVHt7ERpPRWXr2bTDqsOWMtIvHmFctsjNN9jtSYCsdSrLjXxb1xlYvGGBeUfY5/T8n9onrFV7osN4auN+uL92loKd88nHiqNTXRO1V4J2qhzVxhf6/FGKLjiG5v36uvqHTSceDdV4NTsRNETsRDdp8fanefJD4jqJx07Fes/kxIAJzngAtfss5F0i0FJjrGdGyoknaktst8zNWMbzbNIi81Xm1OSJoq8VTTG94pG8t+DBbPfs1QhgnJrMfF9NHWWnDc7KKRNWVNW5sEbk6276ork7Woptddsw5p09P4WGmtFY/TXwUNciO9Hlo1PtL0IiImiJoiAhzqbeS4rwvFEc5lzFxbhXEeE7h4hiSzVlsqF13Unj0a9E6Wu81ydqKqGGOneMMM2PFtinsuILfDXUcycWvTixehzXc2uToVOJQbPfLOvyzxg63vV9RaqrWW3VTv+pHrxa7o328EX0ovSSMWaL8p6q/V6GcH1o5wj0AG5Aeq03CttNzprnbamSlrKWVssE0a6OY9q6oqHRDI/H9LmNgGkvjEZHXR+4V8Df+nO1E10+S5FRydi6c0U5yk2bHeNX4azQjslTMrbffmpTOarvJbOmqxO9Krqz6Zpz07Vd/RP4fqJxZOzPSV5ypm33+lcJfMVX4oy2ZUzb7/SuEvmKr8UZFweOFtxH+Xt8PzVfABYOaCZ8m8gLrmNhVuI4sRUVupXTPhRjoHSP1bzXTVE07yGC9Gxb7yUH/f1H3oas15rXeE3Q4aZsvZv02R47ZAqPAIrcfxLLw1atpVG+vwv9jTca7MOYFjpJKy0y0GIIY0Vyx0rlZPonPRjk0X0I5VXqLwAixqLwtrcNwTHKNvi5XzxS088kE8T4pY3Kx7HtVHNci6KiovJUPwWF248N0Fqx7a77RRMhku9K5alrU035I1RN9e1Wuan0SvRNpbtViVDnxTiyTSfIABk1Ogmy5iKXEmStknqZFkqaJrqGVVXVfcl3Wa9u5uEnkF7ELHNyalc5qoj7rOrVXpTdjT70UnQrMkbXl1eltNsNZn0AAYN4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHivltp7vaai3VSe5zs3ddOLV6HJ2oui9x7QY2rFoms9JeTETG0q0XegqLXc6i31Td2aB6sd29Sp2Kmi955SWs58PeMUjL/AErPdYERlQifCZrwd3KvqXsIlOA1+knS5px+Xl7nM6nDOHJNQAENoDd8osPeyl69k6lmtJQuRyIvJ8vwU7ufq6zS4InzTNijTVzl0Qm7DF3w5Y7JT22Cpevg26vf4F3lvXzncuv7NCdw6dNGeLai8ViOfOYjdP0Gn72/anpDcAYH23WL/Mv+qd+Q9t1i/wAy/wCqd+R1v8Y4f+NX/KF/szwMD7brF/mX/VO/Ie26xf5l/wBU78h/GOH/AI1f8oNmTvVupLvaqm2V0aSU9TGscjexelOpU5ovWhUjFdkqsO4gq7RWJ7pTv0a/TRJG82uTsVNFLSe26xf5l/1TvyI4zqorVimlpa+0Sb10p18GrXMVqSRL0ar0ovFPSpL0nHuH47bTnrtP/wCocn9LOC21+njLirvkp85jzj9Y+Pqg4Ge9qN9/yzPrW/mPajff8sz61v5ll/H+F/8A0U/yj93zX+CcR/Av/jP7MCDPe1G+/wCWZ9a38z9RYNxBLKyKOka573I1rUlbqqryTmexx7hkztGop/lH7n8E4j+Bf/Gf2Z/I/CftixSlZVx71vtypLJqnCR/wGetNV7E06Sy5r+X2G4cK4XprVHuumRPCVMifDlXzl9HJE7EQ2A1ajL3l9/J9Z+j3CY4bo4paPr2529/p8P3AAaF6FC9sOikpc+bxO9HI2sgppmapzRIWR8O9il9Cr23Xg6WoorRjmkiVyUqeIVqonmsVyuicvYjlenpc036e210DiNJvgnby5qmgAnucCwWzVn1T4Ht0eEsVxTSWRJHOpauJu++k3l1c1zebmaqruHFFVeC68K+gxvSLxtLbhzWw27VXT/DOIrFia3NuGH7vR3OlXT3SnlR+6q9DkTi1exdFMocu7DerxYLg24WS6Vltq28pqWZ0btOrVF4p2ciccBbU2MrR4OmxRQ0mIKZNEWVNKeoRP2mpuu726r1kS+mtHhXOHilLcskbLpgjbLbO3L/ABy6KlobqlvuUmiJQV+kUrnL0MXXdevY1VXsQkkjzWa8pWNMlbxvWdwAHjMKQ7b/AL8sP7og/HIXeKQ7b/vyw/uiD8chv03jV/E/sPigoAE9zodCNl73hsLfMS/1pDnudCNl73hsLfMS/wBaQj6rwwtOFfaz7v2SWVE27sUOqcQ2TCEEvuVHAtbUtReCySKrWIvajWqvokLdnOraIu7r3nXiqsV++2OvdSsVF4bsKJEmn8Bp01d77pvE8nZw9mPNoIAJznglTZmy2bmJj5rbhGrrJbEbUV/VJx8iLX5SouvyWu6dCKy9exvhuOyZN01ycxEqrzUSVciqnFGIvg2N9Gjd5P21NWa/ZryTNDhjLliJ6RzTLTww08EdPTxMihiajI42NRrWNRNERETkiJ0H7AK50wAAAAAFEdsTEr77nJV0DJFdS2aFlHGiLw39N+RfTvOVv0UL3OVGoqqqIicVVeg5gYuuj75iu7Xl7lc6urZqlVX5b1d/ck6aN7TKr4rfbHFfX9GLABNUIWq2F8ExObc8e1sSOka5aCg3k83giyvTt4tai/tp0lVToxs+2VthyZwtQI1GufQMqZNPjze6u19Cv07jRqLbV29Vjw3FF828+TewAQHQgAAqTtz4Kjpbla8dUUCNSsXxKvVqcFka3WNy9qtRzfoIViOhO07ZWXzJDEcSs3pKSBK2NdNVasTkeq/wo5PQqnPYn6e29Pc53iWKKZt48wAG9Xph2QMROsWdNBSuk3ae7wyUUqKvDVU32cOvfY1PpKXyOYmB7k6zY0sl3a/cWiuEFRr1bkjXf2OnaciFqY2tEr7hV98c19JV+24sSvteXFBh6CRWyXmr1kRF5ww6Ocn8bo/UUtLAbc91dV5o261o5VioLYxd3qkke9VX+FGeor+SMFdqQrtfft55/tyAAbUJv2z/AIMbjrNO1WWpiWSgjctVXJ0eBj4qi9jl3WfSOikbGxsaxjUa1qaNaiaIidRVjYIsjNzE+I5Gav1hooXack4venf7n6i1BA1Ft77ejouG4orh7XnIADQsAjXaTwVDjXKq507IUfcbfG6uoXInlb7EVXMT9pu83TrVF6CSgqIqaLxQ9rPZneGGSkXrNZ83KwGx5oWVmHcxcQ2SJu7DR3GaKFNNPc0eu5/t0NcLWJ3jdyVqzWZiQ+9vq6i319PX0kixVFNK2aJ6c2vaqKi9yoh8AHjp/hK7w4gwtar7AmkVwo4qlqdSPYjtO7UrBt9/pXCXzFV+KMl7ZNuS3HIiw77t6Sl8NTO7EbK/dT+FWkQ7ff6Vwl8xVfijIOKNsuzoNXft6Tteu36KvgAnOeC9Gxb7yUH/AH9R96FFyUMt88saYBwy3D9jitLqNsr5UWop3PfvO58Ucn3GrNSb12hM0WauHJ2rdNnQM+NdV0tDRy1lbURU1NCxXyyyvRrGNTmqqvBEKN1203mpUI7wNba6TXl4Ghau76N/e+0jzGWYGNMYqiYlxHX3CNHbyQvfuwovWkbdGovboR401vOVlfiuOI+rEy3TakzEoswMwWus8iyWi1w+LU0vRM7eVXyIi8kVdETsai9JEoBMrWKxtClyZJyXm9ush+4IpJ5mQwxuklkcjWMamquVV0RETrEMck0zIYY3ySPcjWMYmrnKvBERE5qW02Xsh6qz1tPjbG1IsNbF5dut0ieVCvRLInQ5Pgt6Oa8dNMb3ikbyz0+ntnt2apryVwo7BWWFjw9M1EqYKffquOvuz1V7016dHOVE7EQ3EArZned3U1rFaxWPIAB4yAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAfiohiqIJIJmI+KRqse1eTkVNFQr1jOxy4fv89A7VYtd+B6/CjXl+S9qFiDUM08PezdgWop496to9ZI0ROL2/Cb6uKdqdpU8Y0XtGHtV8Vf/AEwha7T97j3jrCDQD0W6mdV1TYk13ebl6kOGvaKVm09Ic/Ss3tFY6yy2HKTdYtU9OLuDPR1mYP4xrWMRjURGomiInQf05XPmnNkm8uqwYYw44pAADU3AAAAAAAABuGXdp8JO66zt8iPyYUXpd0r3f++RrFropbhXw0cKeVI7TXqTpXuQlyhpoqOjipYG6RxNRqfmdd9EuFe06j2nJH1adP72/wCdfk8mX2AB9QYgAAHhxBaLffrJWWa60zamhrInQzxO+E1U+xelF6F4nuAeTG/KXOzO/K+8ZZ4mdR1LX1FpqHOdb67TyZWfFd0I9E01TvTgpH51AxRYLNieyVFlv1vhr6CoTSSKRPUqKnFqp0Kmip0FQs39mbENgkmueCVlvts1Vy0vDxuFOpE5Sp+z5XyeknYs8W5W6qHV8PtSe1j5x+SvgPpUwT01RJT1MMkM0bla+ORqtc1U5oqLxRT5khWgADwRVRdU4KTfkxtEYmwdNBbMRyT36wou6qSO3qmnb1xvVfKRPiuXToRWkIA8tWLRtLZiy3xW7VJ2dPsJ4is2KrDTXyw10dbQVLdY5GcNF6Wqi8WuTkqLxQypz72eM063LbFsfjEskuH656MuFNqqo3oSZifHb9qap1KnQGCWKeCOeCRskUjUex7V1RzVTVFReor8uOaS6TSaqNRTfzjq/ZSHbf8Aflh/dEH45C7xSHbf9+WH90QfjkMtN42nif2HxQUACe50OhGy97w2FvmJf60hz3OhGy97w2FvmJf60hH1XhhacK+1n3fsks5fYqqXVmJ7rVv13562aR2q6rq56rz6eZ1BOXF7RW3quRUVFSokRUXo8pTDS+bdxbpT4vGACWpQ6VZQ0jKHKrCdKxE9zs1Lrp0uWJqqveuqnNU6U5PVba7KjCdU1Wqr7NS727yRyRNRydyopG1XSFtwnx29zagAQl4AAAAAMVjGp8Twjeave3PAUE8m9prpuxuXXTuOYK8zp1juBarBF+pkVUWW21EeqJqvGJyHMVeZM0vSVLxbxV+IACUpw6j2Sm8Ts1FR7u54Cnjj3dddN1qJpr3HLg6lWmp8ctVJV7zXeHgZJq3ku81F4esi6ryXHCet/h+r0gAhroAAGEx/Tsq8CYgpZNNya2VMbtU1TRYnIvDp5nMc6cY/qGUmBMQVUmm5DbKmR2q6JokTlXj0cjmOTNL0lScW8VfiAAlKgOpdslfPbaaaTTfkhY52nWqIpy1a1znI1qK5yroiInFVOplFClPRQU6O3kijazXTnomhE1XkueE/1/D9VC9rqV8mf+IWO00jZStb6PFol+9VImJV2tYvBZ/4k0j3Gv8AFnpw0RdaaLVfXqRUScfghW6n7a/vkABk0Ls7DcMceUFZK1PKlvEznL6I4k/sT0QPsOSMfk7VNa7VY7xM1yacl8HEv3KhPBW5fHLqdH9hX3AANaSAADn7tWQMps/cTRx8lfTyLw6XU8Tl+1VIuJR2rZ2VGfuJpGckfTs7208TV+1CLi0x+GHJ6j7W3vkABk0rv7EL3Oyala5yqjLrOjUXoTdjX71U0Db7/SuEvmKr8UZIWxLC6LJdZHKmk1zne30aMb97VI92+/0rhL5iq/FGQ6/bLzL/ACEe6PzVfABMUYAAAAAAACw+zlmVlDhOSCK74Vmtd2XyVvUrvHE16+SLF1eQ1e1S4VpuNBd7dDcbXWQVtHO3fingej2PTrRUOWxIWS2a1/y0vjZqSWSqtEz08dtz3+RInS5vxXp0KnPTRdUI+XB2ucdVppOId3tS8cnREGLwliC14pw5RX+y1KVFDWxJJE9OadCtVOhyKioqdCoqGUIPRexMTG8AAD0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEGZpYe9hL+6enj3aKsVZI9E4Md8Jvr4p2L2HnsdJ4tS7700kk4r2J0ITNiqzU98tD6OZjVe1UkhVfgvTl3LyXsUiuWN8UropGq17FVrmrzRUPmX0s09tLkiKR9S/P8A5+qJh0dceacnyfkAHHJwAAAAAAAAAZXC9rddrqyBUXwLPLmX5KdHfyN2n099RlrixxvNp2gbZl7afFqJbjM33WoTSPX4LP8A+/dobUfxrUa1GtREaiaIidB/T7Xw/RU0Onrgp5f7nzlgAAmgAAAAAAADUcf5a4JxzEvtjsNNUVG7utq2J4Oobpy0kboqonUuqdhX3HWyXUxpJU4LxGyZOKtpLk3ddp1JKxNFX0tT0lsAbK5bV6Sj5dLiy+KObmfjfA2LMFVjabE9jq7cr10jke1HRSfsyN1a7uU1w6k3e22+726a3XSip62jnbuywTxo9j07UUo3tTZVUWXOJKOtsavSyXZHrDC9yuWnkZpvM1XirdHIqa8eacdNVl4s/bnaeqm1egnDHbrO8IaABvVwXw2PsTy4iycpaWpk36izTut6qq8VjaiOj7ka5Gp+yUPLX7AVS91FjGkX/Djko5G8elyTIv4ENOojem6w4bea54j1WkKQ7b/vyw/uiD8chd4pDtv+/LD+6IPxyEbTeNZcT+w+KCgAT3Oh0I2XveGwt8xL/WkOe50I2XveGwt8xL/WkI+q8MLThX2s+79klnNPNm3OtGaGJ7crVakF1qEZrrxZ4RytXj1oqKdLCjm2lh11ozfddmR6U95pI6hHInDwjE8G9PT5LVX9o1aadrbJfFKb4ot6Sg8AE1QBefYyxLHesn4rU+VHVVlqH0z2qvleDcqyRu9HlK1P2FKMEn7N2ZH/AA5x8yorXu9hbi1Ke4NTjupr5EunSrFVe5XdZqzU7deSZoc0YcsTPSeToID5UlRBV0sVXSzRz08zGyRSxuRzXtVNUcipwVFRddT6lc6YAAAAAfmaNk0L4pE3mParXJrzReCnLm9UMlsvNbbZv8SkqJIH8Oljlav3HUg5/bVOHnYeztviJHuQXFzbhCunnJKmr1+sSRO4laWecwquK03pW3oi0AExRB0eyKvLL9k/ha4tk8I5bdFDI7XnJEng3/7mKc4S2ewtjSOW23TAlXLpNC9a6hRy+cx2iSNT0O3XafLd1GjUV3rv6LHhmWKZezPmtAACA6EAAEc7S94bZcj8TTq/dfUUvibERdFcszkjVP4XOX0IpzyLS7deMopZrTgWklRzoXeP1yNXzXKitiavbor3adStUq0T9PXam7neJZIvm2jyAAb1e2DLW2Lesw8O2pG7yVVzp4ndjVkbvL3Jqp0zTkUW2M8OuvOckFxexVgs9LJVOXThvuTwbE9Plq5P2S9JC1M72iF9wqm2ObesqQ7btsdR5xRVu75FfbIZd5PjNV8ap6dGJ60IKLf7d+HHVWF7FiiGNVWgqX0s6p8SVEVqr2I5mn0yoBIwzvSFbrqdjPb+/MABtQ1sdgi8sdb8T4fe9EfHLDWRt6XI5FY9e7dZ6y0Rz02bsaR4HzXttxq5kit1XrRVzlXg2ORU0cvUjXoxy9iKdC0VFRFRdUUgaiu19/V0XDckXw9nzgABoWAAR9tC4ziwRlXdrk2ZGV1TGtHQoi6OWaRFRFT9lN5/0T2I3naGN7xSs2nyUTzVvLcQ5k4jvMbkdFV3GZ8Souvue+qM/wBqIayAWsRtGzkbWm0zMgB67Lbqq73iitVEzwlVW1DKeFvW97kaietQ8iN1+9lu2OtWRWG4nt0fPDJVO7Ukkc9v+1WkM7ff6Vwl8xVfijLS4fttPZbFb7PSJpT0NNHTRJ8ljUan2IVa2+/0rhL5iq/FGQMU75d3QaynY0nZ9Nv0VfABPc8F0tkHDOG7pk5BV3PD9prqha6dqy1FHHI/RFTRNXIq6FLS9Gxb7yUH/f1H3oaNR4FjwyInNz9EkzYDwPNGscuDMOyMXm11shVF7t00bGWzvljiGnf4vZnWSqVPJnt0isRF6NY11YqdyL2oS2CFF7R0leWw47xtasOdGc+V98yxxA2huLkq6Cp1dRV0bN1k7U5oqcd1yapq3VeacVRdTQy+O2LaqWvyMulZOxFlttRT1EDtOKOdK2Jf9silDifhvN67y53W4IwZezXoAA2oizmwvjOaG8XPA1XMq09RGtbRNcvmyN0SRqftNVHfQXrLbnPLZoq5aPPPC0sS6K+qdEva18b2r9inQ0gaiu193Q8MyTbDtPlIADQsQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADQ8xLT4Kdt0gb5Eq7syJ0O6F7/wD3zN8PjX0sVbRy0s7d6OVu6v5+kq+McOrxHS2wz16xPpP/ALkQhoHpulFLb6+WjmTy43aa9adC96HmPi+THbHaaWjaY5SzAAYgAAAAAEpYPtPsVampI3Som8uXrTqb3ffqalgK0+PXLxyZusFMqKmvwn9Cd3P1EjH0L6HcK7NZ1uSOc8q/rP6fN5MgAO8YgAAAAAannDiuTBOWt6xNAyF9RRwJ4u2VFVjpXORjNURUVU3nJqiKhthXrbqviUWXNqsbHbslzuHhHJ1xxNVVT+J8fqM8de1aIaNTk7vFaz55e7VOFrnHHTYxt9RY6rgjqiBqz0y9uieW30aO9JOGGcV4ZxNAk2H79bbm1U1VKaoa9zf2mourV7FRDmKfqKSSKRskT3RvaurXNXRUXsUl201Z6clPi4pkryvG7qiDm1aMzsxLSxI6DGt+jjamjY3Vr3sanY1yqiGcTPjNtE09udX9RD/4GqdLb1S44rj86y6EuVGoqqqIicVVegphtm5iWfFV8tmG7DVx1tPaFkfU1MTt6N8z91N1qpwXdRq6qnDV2nQpEmJsxMdYlhfT3zFd2rad/nwOqXNid6WN0avqNWNuLB2J3mUTVcQ76nYrG0AAJCsC32wTbHw4UxLeFbo2qrYqdq6c/BMVy/1SocTHyyNjjY573qjWtamquVeSIh0ZyIwg7A+VtmsU7EbWpF4et6/DSLvORevd1RuvU1DRqbbU29VlwzHNs3a9G8FIdt/35Yf3RB+OQu8Uh23/AH5Yf3RB+OQj6bxrDif2HxQUACe50OhGy97w2FvmJf60hz3OhGy97w2FvmJf60hH1XhhacK+1n3fskshna8wO/FuWD7nRxb9xsLnVcaImquh00manciO+hp0kzH8e1r2OY9qOa5NFRU1RU6iHW3ZneF1lxxkpNJ83K0Et7TOVsuXuMX1dvgd7Xbm90lE9E4Qu5ugX0dHW3TmqKRIWdbRaN4crkx2x2mtusAAPWtNGQ+fV5y+bHZbxFLd8O6+TFv+7UvWsSrwVvyF0TXkqcdbfYEzJwTjaBj8PYgo6idyarSPf4Oob16xu0d3oip2nNk/rXOa5HNVWuRdUVF0VFNOTBW/NP0/EMmGOzPOHVIHNW05jY+tUaRW/Gd/giTlGlfIrE+iq6GTnzjzRmZuPxxeUTXXyJ9xfWmimn2W3qnRxXH51l0XMDdMZYTtl1pbTXYitkNxqp2QQUi1DVmfI9yNaiMRd7iqomumhzovGM8X3hrmXbFV8r2O5sqK+WRvo0V2mnEx1guElpvtvusWvhKKqjqGac9WORyfcexpfWWFuLc/q1dRiu+2/gt12wZRYwood6ps8ngqrdTitPIqcfov07nuXoLC000dRTxzwvR8cjEexydKKmqKfG6UNJdLbU22vgZUUlVE6GeJ6atexyaORfSikaluzbdZ58UZsc0nzctQbvnXl/XZc46q7JUNfJRPVZrfUKnCaFV4cfjJ5qp1p1KhpBZxMTG8OUvSaWmtusBlcJYgumFsSUOILNP4CuopUkid0L0K1ydLVRVRU6UVTFA96vImYneHRbJzNPDuZVjZU2+ZlNdI2ItZbnvTwsK8lVPjM15OTrTXReBvpy1tlfXWuvir7bWVFFVwu3op6eRY5GL1o5OKEs2DaTzUtVM2nludFdGtTRrq2ka56elzN1V9K6kO+mnf6q6w8UrttkjmviR7nVmtYMtLE+aqljqrxMxfErc1/lyL0Od8ViLzVeemiaqVQv20nmpdKZ1PFc6K2NcmjnUVI1r1+k/eVPSmhEtyrq2510tdcayorKqZ29JNPIr3vXrVy8VPaaad/rGfildtscc3pxLerjiK/Vt8u9Q6orq2VZZpF6VXoROhE5InQiIhjgCWpZmZneQAkzZ2y1nzGx1DBURPSx0CtnuUvFEVuvCJF+M9U07E3l6Dy1orG8ssdLZLRWvWVmNjfBT8M5ZLe6yJY66/vbU6KmipTtRUiTv1c/0PQm8/EEUcELIYY2RxRtRrGMTRrUTgiIickP2Vl7dqZl1eHHGKkUjya5mbheDGmArxhmdWt8eplbE93JkqeVG7uejV7jmtcaOqt9fUUFbA+CqppXRTRPTRzHtXRUXtRUOphUfbSyxfR3FMxbNTqtLUq2O6sYn+FLwayX0O4NX5SJ0uN+nvtPZlX8T083rGSPL8lZAATVCFvtlnPGhrrVSYIxhXsp7jTokNurJ3aMqWImjY3uXgkickVfOTRPO51BBhkxxeNpb9PqLYL9qrqmDnjgnOzMnCVKyituIpZ6KNNGU1axs7Gp0I1XeU1OxFRDa6najzPlgdHH7BwOVOEkdEqub6N5yp60Ik6a/kua8UwzHOJXSxJfLThyzVF4vlfBQ0NO3ekmldoididKqvQicV6ChO0HmnVZm4qbPCyWmstDvR0FM9eOirxkd0bztE4dCIicea6njTGmKsZViVeJ75WXKRqqrGyO0jj157rG6Nb3Ihr5vxYYpznqr9Xrpzx2axtAADerwnjYwwS+/5iuxNVRa2+xN32qqcH1D0VGJ3JvO7FRvWQrYbTcL7eqSz2qmfVV1ZK2KGJicXOX7k6VXkiIqnRTJzA1Hl5gKhw9TKySdqeFrZ2pp4ad2m870cEanY1DRnv2a7eqw4fp5yZO1PSG4lTNvv9K4S+YqvxRlsypm33+lcJfMVX4oyNg8cLXiP8vb4fmq+ACwc0F6Ni33koP8Av6j70KLk75H7QUeXODI8MzYUfcWNqJJvGWV/g18rjpuLGvVz3jVnrNq7Qm6DLTFl7V52jZdwFXKja+pEj1p8Bzvf1PuiNT1pEpo2NNqLHt6pX0llpqDD8T0VFlgRZZ9F6Ee7gnpRqL2kSNPefJb24jgrHKd0i7buPaCHD1PgGhqGS19TMyor2tVF8DE3ixrupznbrtOpvahUM+tZU1FZVS1dXUS1FRM9XyyyvVz3uXiqqq8VVes+RNx07FdlFqc858k3kABm0JM2XrdLcs9MNRxou7BM+okd8VrI3O4+lURO86DlWthfBMsUVzx7Wwq1szVoberk85qORZXp2ao1qKnU9C0pA1Ft7ui4bjmmHefPmAA0LAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAarmFafGaJLlC33WBNJNE4uZ1933akfE1Oa17Va5Ec1U0VF5KhFWKLW603V8LUXwL/AC4V+SvR3cj5z9MOFd3eNZjjlPK3v8p+P5+9lEsUADh3oAAB9KaGSpqI4IWq6SRyNanWqnzN1y5tPnXaZvWyDX/c7+3rLHhXD78Q1VcFek9Z9I8//epLabJb47ZbYqOPRd1NXu+M7pU9oB9pxYqYqRjpG0RyhgAA2AAAAAAFLNua9+PZnW+zRv1jtluar06pJXK5f9qRl0ynG0fkvmPccfXjGFvoG3yjrpfCNbRu3pomNajGtdGuiqqNaieTvG/TzEX3lA4jF7YdqxurmD0XCirLfVvpK+kqKSojXR8U8ase1e1F4oecnudAAHgAAANkwVgTF+M6psGGrBW16Kujpms3YWftSO0anepaXJnZmtdhmgvWOZoLvcGKj46CNFWmidz8pV4yKnVojex3M13y1p1ScGlyZp+rHL1alsk5MVFVXUmYOKaRY6OFUltNLImjpn9E7k6Gpzb1rovJE1tufxrWtajWtRrUTRERNERD+kDJebzvLotPgrgp2ahSHbf9+WH90QfjkLvFIdt/35Yf3RB+OQ2abxo3E/sPigoAE9zodCNl73hsLfMS/wBaQ57nQjZe94bC3zEv9aQj6rwwtOFfaz7v2SWACCvmHxphmzYww3V4fv1KlTQ1TdHJro5jk5PavQ5F4ov9ihmdmUOIstLq51RG+uscz1SkuMbPJXqZInwH6dC8F46Kui6dCzzXSgobpb57fcqSCso52KyaCZiPY9vUqLwU24ss0n+yJqtJXUR6T6uWoLbZq7LFHVyTXLL+vbRSO1d7GVblWJeyOTirfQ7X0ohW7GeAsY4OndHiTD1fQNauiTOj3oXL8mRurF7lJ1Mtb9JUGbS5cM/Wjk1oAGaOAAAAf1qK5UREVVXgiJ0gdIMkLr7NZQ4VuDnK97rZDHI5ebnsbuOX+Jqm5EQbIMd3pslqOhu9urKB1NVztp21MLo1kic7wiPRHJqrVV7tF7FJfKu8bWmHW4LdrFWZ9GlZxZdWfMrCb7PcvcKmJVkoqxrUV9PJpz7WrwRzelOpURUoDj/B1+wPiOexYho3U9RGusb04xzs10R7HfCaun9l0VFQ6Zmt5hYHw3jyxraMSW9tTEmqwyt8mWBy/CY7m1eXYunFFNuLNNOU9EbWaKM/1q8rOaAJyzT2a8ZYYklrcNtdiS1pxRIGaVUadTo/helmuvUhCNTBPTTvp6mGSGaNd18cjVa5q9SovFCbW8WjeFBkw3xTteNnzABk1AAAA9lntVzvNcyhtFuq7hVP82GmhdI9e5qKpYHKrZcvt0liuGO6j2HofO8Sge19TInUqpq2NP4l7E5mNr1r1bsWDJlnakIiypy6xFmNiFtrslOrYGKi1da9PcqZirzcvSvU1OK+hFVL/Za4KsuAcKU2HrJFpFH5U0zkTwlRIvnSPVOar9iIickPfhPDlkwrZYbNh+3QUFFCnkxxN85elzl5ucvSq6qpliDlyzf3L/SaOuCN55yAA0poee50NJc7dUW64U8dTSVMbopoZG6texyaKip1Kh6ABQvaGyWueXd0kulsjlrMMTye4zp5TqZV5RyfcjuS8OngRAdTa2lpq6jlo6yniqaaZislilYjmPavBUVF4KhWHOHZdZPLNd8uZmQud5TrTUyaN1/+1IvL9l3D5SciZi1ETyspNXw6YntYunoqgDLYow1iDC9wWgxDZ622VCcmVESt3k62rycnamqGJJXVUzExO0gADwAP6iK5UREVVXgiIB/D1Wm3112uVPbbZSTVdZUvSOGGJque9y9CIhJuWuQWP8ZyRzy291itjuK1dwYrFVPkR+c7s5J2lu8ososJ5bUm9a6dau6SN3ZrjUIiyuTpa3oY3sTvVdDTkz1r707T6HJlneeUNW2a8lafL6gS/X1kdRiaqj0dpo5tExecbF6XL8JyehOGqumoAg2tNp3l0GLFXFWK16BUzb7/AErhL5iq/FGWzKmbff6Vwl8xVfijNmDxwjcR/l7fD81XwAWDmgAAAAAANlwjgLGeLZGtw7hu417XLp4ZkSthT0yO0YneomYjqyrWbTtENaJHyLyovOZeIWMZHLS2KnkTx+v3dEROCrGxV4LIqdHRrqvQizBlhsqS+Gir8wbmzwaKjvY2geqq7sfLw07Uai9jkLP2O02yxWqC1Wehp6Gip27sUEDEa1qehOnpVeaqRsmoiOVVnpeHWtPay8o9Cw2m32KzUlntVMymoqOJsMETeTWomieleteaqe0AhL2I25QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGGxfaUutqckbdaiHV8XWvW3v+/QzII+q02PVYbYckcrRsIUBsuPbT4lcfHIW6QVKqq6cmv6U7+frNaPimu0eTRai2DJ1j/fpPxZgAIg9lloJbncoqOLhvr5Tvit6VJbpYIqanjp4Wo2ONqNaidCIa9gK0+JW7x2Zuk9Smqa/BZ0J38/UbKfVvotwr2PS97ePr35+6PKP1n/jGZAAdQ8AAAAAAAAAABj75YrLfafxa9WiguUPxKunZK1O5yKR5e9n3Ke6vdIuGG0UrvhUdTLEiehqO3U9RKYMotMdJa74qX8URKAq7ZRy7mVzqa64jpXLyRKiJzU49Sx6/aeL/AJSsF/rJiD1w/wDgWKBl31/VpnRYJ/pQRb9lbLWmejp6zENb1tlq42p/sjav2m64cyUytsMjZaLB1vmlT4dZvVS69ekquRF9CISEDycl56yzrpsNelYfiCKKCFkMEbIo2Jo1jGojWp1Iicj9gGDeAAAarirLrBGKbmlzxDhuhuNYkaRJNM1VduIqqicF7V9ZtQPYmY6MbVi0bTG6P/8AgtlX+pFq/gd+Y/4LZV/qRav4HfmSAD3t29WHc4/ux8kf/wDBbKv9SLV/A78zcrDaLbYbRT2mz0cVFQ06K2GCNPJYiqqrp3qp7geTaZ6yyrjpXnWNgAHjMAAA/MsccsTopWNkjemjmuTVFTqVD9ADQ8R5OZY39zn3DBtsbI7i6SlatM5V61WJW6r6TSblstZY1T1dA+/UCL8GnrGqifWMcTkDOMlo6S0202K3WsK7ybJWCFeqx4jxC1mvBHOhVUT0+DQ+1Jsm4AYqLU3zEsyo7XRs0LEVOpfclX7ULBA976/q1+xYPuodtGzXlRQua6e0VtxVvFPGq6TT1MVqKb/hjAmDMMua+w4XtNBK3gk0VM3wve9U3l9ZsYMZvaesttMGOnhrEAAMW0AAAwGK8F4TxVHu4iw7bbk7TdSSeBqyNT5L/Ob3KZ8HsTt0eTWLRtKFL1sw5W171dS093tWvRSVquRPrUea3U7JGE3Kni2Kb3GnHXwjIn69XJELHgzjLePNHnR4J/phXaj2SsFN3fG8R4hl4cfBOhj1XvY42yxbOOVNrcj5bJU3KRq6o6trHuT+FqtavehLoE5bz5va6TBXpWGPsNjstho/E7HaaG2U/THSU7Ymr2qjUTVe0yABrb4iI5QAAPQAAAAAAAHlultt11o3Ud0oKWupn+dDUwtkYvpa5FQjLEezzlVeZHSph91tldzfQVD4k7maqxO5pK4MotNektd8VL+KN1eK3ZLwQ9XLR4hxDBqnBJHwyIi9zE4Hnp9kjCjVXxjFV6kTo3I4maetFLHgz76/q0+xYPuoQs+y7lfQvR1U29XPTm2prUai/VNYv2kj4Ty8wRhVzZLBhe2UMzeU7YUdMn/5Hau+02gGM3tPWWymDFTw1gABg3AAAGExVhDC+Ko42YjsFuungkVInVMDXujRee65eLddE5L0IZsCJ2eTEWjaUV3DZ6yirF3lwokD+uCtnZ9m/p9hhqnZfyulT3OK80/HX3Ot17vKapNoM+8v6tM6XDP9MfJA1Rsp5bStRGV+JIdOllXEuv8AFEp849k/Llr0ct3xS9EXi11VBovqh1J9B73t/Vj7Hg+7CDoNlvLCN+89b5MmnmvrURPsYimZt2zrlHSaK7DMlU9E86eunXo6keifYSwDzvb+rKNLhj+mPk1ax5c4CsjmyWvB1jppW+bKlEx0ifTVFd9ptDURrUa1ERE4IidB/QYzMz1ba1ivKIAAeMgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB471QRXO2y0cvDfTyXaea7oUiSqglpqiSnmarZI3K1ydSoTOYDEuGae7P8Yjk8XqtNFdpqj/Sn9zlPpNwO/EKVzYI+vX/AHH7w9iUZmZwhaVut2a2RutPDo+XtTob3/dqZOHA1esuk1ZTMj15s3nLp6FRPvNys1rpbVRpTUzV56ve7znr1qc5wX6ManJqK31VOzSvPn5/2/d7MvaiIiaJwQAH05iAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//9k="

# ─────────────────────────────────────────────
# FUNÇÕES AUXILIARES
# ─────────────────────────────────────────────

def fmt_moeda(v: float) -> str:
    if v >= 1_000_000_000:
        return f"R$ {v/1_000_000_000:.2f} B".replace(".", ",")
    if v >= 1_000_000:
        return f"R$ {v/1_000_000:.2f} M".replace(".", ",")
    if v >= 1_000:
        return f"R$ {v/1_000:.1f} K".replace(".", ",")
    return f"R$ {v:.2f}".replace(".", ",")

def fmt_moeda_full(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

def fmt_abrev(v: float) -> str:
    if abs(v) >= 1_000_000_000:
        return f"{v/1_000_000_000:.2f} Bi".replace(".", ",")
    if abs(v) >= 1_000_000:
        return f"{v/1_000_000:.2f} Mi".replace(".", ",")
    if abs(v) >= 1_000:
        return f"{v/1_000:.2f} K".replace(".", ",")
    return f"{v:.0f}"

def gerar_tickvals(series, n_ticks=6):
    max_v = series.max() if not series.empty else 1
    vals = np.linspace(0, max_v * 1.05, n_ticks)
    texts = [fmt_abrev(v) for v in vals]
    return list(vals), texts


@st.cache_data
def carregar_dados():
    dfs = []
    
    # 1. Base Principal BID
    try:
        df_bid = pd.read_excel(ARQUIVO_BID)
        # Adicionar categoria para o grupo BID (Cooperados)
        df_bid["Categoria Linha"] = "SICOOB VERDE · ASSOCIADO"
        dfs.append(df_bid)
    except Exception as e:
        st.error(f"Erro ao carregar '{ARQUIVO_BID}': {e}")

    # 2. Base Capital de Giro
    try:
        if Path(ARQUIVO_GIRO).exists():
            df_giro = pd.read_excel(ARQUIVO_GIRO)
            
            # Mapeamento de colunas divergentes detectado na análise
            mapeamento = {
                "Data Movimento Entrada": "Data Movimento",
                "Número Central Local Negócio": "Número Central",
                "Número Cooperativa Local Negócio": "Número Cooperativa",
                "Sigla Cooperativa Local Negócio": "Sigla Cooperativa",
            }
            df_giro = df_giro.rename(columns=mapeamento)
            
            # Inferência de Sigla Tipo Pessoa (ausente no Giro)
            if "Sigla Tipo Pessoa" not in df_giro.columns and "Número CPF/CNPJ" in df_giro.columns:
                df_giro["Sigla Tipo Pessoa"] = df_giro["Número CPF/CNPJ"].apply(
                    lambda x: "PJ" if len(str(x).strip()) >= 12 else "PF"
                )
            
            # Adicionar categoria para o grupo Giro (Cooperativa)
            df_giro["Categoria Linha"] = "CAPITAL DE GIRO · COOPERATIVA"
            
            dfs.append(df_giro)
    except Exception as e:
        st.warning(f"Aviso ao carregar '{ARQUIVO_GIRO}': {e}")

    if not dfs:
        return pd.DataFrame()

    df_raw = pd.concat(dfs, ignore_index=True)

    df = pd.DataFrame()

    # Datas
    df["data_movimento"] = pd.to_datetime(df_raw["Data Movimento"], dayfirst=True, errors="coerce")

    # Identificação
    df["central"]         = df_raw["Número Central"].astype(str).str.strip()
    df["cooperativa_num"] = df_raw["Número Cooperativa"].astype(str).str.strip()
    df["cooperativa_nom"] = df_raw["Sigla Cooperativa"].astype(str).str.strip()
    df["tipo_pessoa"]     = df_raw["Sigla Tipo Pessoa"].astype(str).str.upper().str.strip()

    # Financeiro
    df["valor_contrato"]  = pd.to_numeric(df_raw["Valor Contrato"], errors="coerce").fillna(0.0)
    df["taxa_operacao"]   = pd.to_numeric(df_raw["% Taxa Operação"], errors="coerce").fillna(0.0)
    df["num_contrato"]    = df_raw["Número Contrato Crédito"].astype(str)
    df["num_proposta"]    = df_raw["Número Proposta"].astype(str)

    # Indexador
    df["indexador"] = df_raw["Índice Correção"].astype(str).replace({
        "CERTIFICADO DEPOSITO INTERBANCÁRIO": "CDI",
        "CERTIFICADO DEPÓSITO INTERBANCÁRIO": "CDI",
        "NAO INFORMADO": "PREFIXADO",
        "NÃO INFORMADO": "PREFIXADO",
        "TAXA SELIC": "SELIC",
    }, regex=False)
    df["pre_pos"] = np.where(df["indexador"] == "PREFIXADO", "PRÉ", "PÓS")

    # Linha de crédito
    df["linha_credito"]   = df_raw["Linha Crédito"].astype(str).str.strip()
    df["categoria_linha"] = df_raw["Categoria Linha"].astype(str).str.strip()

    # Ano Mes para filtro
    df["ano_mes"] = df["data_movimento"].dt.to_period("M").astype(str)

    return df


def aplicar_filtros(df, central_sel, coop_sel, tp_sel, ano_mes_sel, indexador_sel, categoria_linha_sel):
    dff = df.copy()
    if central_sel:
        dff = dff[dff["central"].isin(central_sel)]
    if coop_sel:
        dff = dff[dff["cooperativa_num"].isin(coop_sel)]
    if tp_sel:
        dff = dff[dff["tipo_pessoa"].isin(tp_sel)]
    if ano_mes_sel:
        dff = dff[dff["ano_mes"].isin(ano_mes_sel)]
    if indexador_sel:
        dff = dff[dff["indexador"].isin(indexador_sel)]
    if categoria_linha_sel:
        dff = dff[dff["categoria_linha"].isin(categoria_linha_sel)]
    return dff


BASE_LAYOUT = dict(
    paper_bgcolor=COR_BG,
    plot_bgcolor =COR_BG,
    font=dict(family="'Sicoob Sans', 'Nunito Sans', 'DM Sans', sans-serif", color=COR_AXIS, size=12),
    separators=".,",
    dragmode=False,
)

PLOTLY_CFG = dict(
    modeBarButtonsToRemove=[
        "zoom2d","zoomIn2d","zoomOut2d","resetScale2d",
        "lasso2d","select2d","toggleSpikelines",
        "hoverClosestCartesian","hoverCompareCartesian","pan2d","autoScale2d"
    ],
    displayModeBar=True, displaylogo=False, responsive=True,
    toImageButtonOptions=dict(format="png", scale=2),
)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    if not st.session_state.get("autenticado", False):
        st.switch_page("menu.py")

    if st.session_state.pop("force_collapse", False):
        import streamlit.components.v1 as components
        components.html(
            """
            <script>
            setTimeout(function() {
                const btn = window.parent.document.querySelector('[data-testid="stSidebarCollapseButton"] button');
                if (btn) { btn.click(); }
            }, 50);
            </script>
            """,
            height=0, width=0,
        )

    # ── Tela de Carregamento (Splash Screen) ──
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(f"""
            <style>
            .splash-container {{
                position: fixed;
                top: 0; left: 0; width: 100vw; height: 100vh;
                background-color: {COR_BG};
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                z-index: 999999;
                font-family: {_PRIMARY_FONT};
            }}
            .splash-logo {{
                height: 100px;
                margin-bottom: 24px;
                border-radius: 10px;
                animation: pulse 2s infinite ease-in-out;
            }}
            .loader {{
                width: 48px; height: 48px;
                border: 5px solid {COR_BORDER};
                border-bottom-color: {COR_TEAL};
                border-radius: 50%;
                display: inline-block;
                box-sizing: border-box;
                animation: rotation 1s linear infinite;
            }}
            .loading-text {{
                color: {COR_TEXTO};
                margin-top: 16px;
                font-size: 1.1rem;
                font-weight: 600;
                letter-spacing: 0.05em;
            }}
            @keyframes rotation {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
            @keyframes pulse {{
                0% {{ transform: scale(1); opacity: 0.8; }}
                50% {{ transform: scale(1.05); opacity: 1; }}
                100% {{ transform: scale(1); opacity: 0.8; }}
            }}
            [data-testid="stStatusWidget"] {{ display: none !important; }}
            </style>
            <div class="splash-container">
                <img src="{LOGO_B64}" class="splash-logo">
                <span class="loader"></span>
                <div class="loading-text">Carregando Concessão BID...</div>
            </div>
        """, unsafe_allow_html=True)
        
        df = carregar_dados()
    
    placeholder.empty()

    if df.empty:
        st.warning("Nenhum dado carregado. Verifique o arquivo concessão_BID.xlsx.")
        st.stop()

    # Mapa de siglas das centrais (usado nos filtros ativos e nas tabelas)
    _sigla_central_map_preview = {
        "1001": "SICOOB CENTRAL ES",
        "1002": "SICOOB CENTRAL BA",
        "1003": "SICOOB CENTRAL CREDIMINAS",
        "1004": "SICOOB NOVA CENTRAL",
        "1005": "SICOOB CENTRAL SC/RS",
        "1006": "SICOOB CENTRAL SÃO PAULO",
        "1007": "SICOOB CENTRAL NORTE",
        "2003": "SICOOB CENTRAL CECREMGE",
        "2007": "SICOOB CENTRAL CECRESP",
        "2008": "SICOOB CENTRAL RONDON",
        "2009": "SICOOB CENTRAL UNICOOB",
        "2015": "SICOOB UNI",
        "2016": "SICOOB UNIMAIS RIO",
    }

    # Contador para reset de filtros
    if "bid_reset" not in st.session_state:
        st.session_state["bid_reset"] = 0
    _r = st.session_state["bid_reset"]

    # ── Sidebar ──────────────────────────────
    with st.sidebar:
        st.markdown(f"""
        <div class="sb-logo">Filtros</div>
        <div class="sb-divider"></div>
        """, unsafe_allow_html=True)

        st.markdown(f"<p style='color:{COR_LABEL};font-size:0.78rem;font-weight:700;"
                    f"letter-spacing:0.06em;text-transform:uppercase;margin:0 0 8px;'>"
                    f"🏦 Central / Cooperativa</p>", unsafe_allow_html=True)

        centrais = sorted(df["central"].unique().tolist())
        st.markdown(f"<p style='color:{COR_MUTED};font-size:0.8rem;font-weight:100;"
                    f"letter-spacing:0.04em;margin:0 0 4px;'>CENTRAL</p>", unsafe_allow_html=True)
        central_sel = st.multiselect("Central", centrais, placeholder="Todas",
                                     label_visibility="collapsed", key=f"bid_central_{_r}")

        if not central_sel:
            coops_disp = sorted(df["cooperativa_num"].unique().tolist())
        else:
            coops_disp = sorted(df[df["central"].isin(central_sel)]["cooperativa_num"].unique().tolist())

        st.markdown(f"<p style='color:{COR_MUTED};font-size:0.8rem;font-weight:100;"
                    f"letter-spacing:0.04em;margin:6px 0 4px;'>COOPERATIVA</p>", unsafe_allow_html=True)
        coop_sel = st.multiselect("Cooperativa", coops_disp, placeholder="Todas",
                                  label_visibility="collapsed", key=f"bid_coop_{_r}")

        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

        st.markdown(f"<p style='color:{COR_LABEL};font-size:0.78rem;font-weight:700;"
                    f"letter-spacing:0.06em;text-transform:uppercase;margin:0 0 8px;'>"
                    f"🔎 Filtros Adicionais</p>", unsafe_allow_html=True)

        meses = sorted(df["ano_mes"].unique().tolist(), reverse=True)
        ano_mes_sel = st.multiselect("Mês-Ano", meses,
                                      format_func=lambda x: f"{x[5:7]}/{x[0:4]}",
                                      placeholder="Todos os períodos",
                                      key=f"ano_mes_sel_{_r}")

        tp_sel = st.multiselect("Tipo de Pessoa", ["PF", "PJ"], placeholder="PF / PJ", key=f"bid_tp_{_r}")

        indexadores = sorted(df["indexador"].unique().tolist())
        indexador_sel = st.multiselect("Tipo de Indexador", indexadores,
                                 placeholder="Todos",
                                 key=f"indexador_sel_{_r}")

        st.markdown(f"<p style='color:{COR_MUTED};font-size:0.8rem;font-weight:100;"
                    f"letter-spacing:0.04em;margin:6px 0 4px;'>LINHA DE CRÉDITO</p>", unsafe_allow_html=True)
        categorias_credito = sorted(df["categoria_linha"].unique().tolist())
        categoria_linha_sel = st.multiselect("Linha de Crédito", categorias_credito,
                                           placeholder="Todas",
                                           label_visibility="collapsed",
                                           key=f"cat_linha_sel_{_r}")

        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background: rgba(0,174,157,0.1); border: 1px solid {COR_BORDER}44; 
                    border-radius: 10px; padding: 10px; margin-top: 5px;">
            <p style="color: {COR_MUTED}; font-size: 0.74rem; margin: 0; line-height: 1.3;">
                📦 Base: {f'{len(df):,}'.replace(',', '.')} contratos carregados.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ── Aplica filtros ───────────────────────
    dff = aplicar_filtros(df, central_sel, coop_sel, tp_sel, ano_mes_sel, indexador_sel, categoria_linha_sel)

    # ── Header ───────────────────────────────
    data_base_str = df["data_movimento"].max().strftime("%d/%m/%Y") if not df.empty else "N/A"
    
    st.markdown(f"""
    <div class="main-header">
        <img src="{LOGO_B64}" style="height:80px;object-fit:contain;background:#FFFFFF;border-radius:10px;padding:8px 14px;" alt="Sicoob" />
        <h1>Concessão BID</h1>
        <p style="color: white; font-size: 0.9rem; margin-top: 5px; opacity: 0.9; font-weight: 600;">Data Base: {data_base_str}</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Tags de filtros ativos ───────────────
    tags = []
    if central_sel:
        if len(central_sel) == 1:
            _sigla = _sigla_central_map_preview.get(central_sel[0], central_sel[0])
            tags.append(f"Central: <strong>{central_sel[0]} – {_sigla}</strong>")
        else:
            tags.append(f"Central: <strong>{len(central_sel)} selecionadas</strong>")
    if coop_sel:
        if len(coop_sel) == 1:
            tags.append(f"Cooperativa: <strong>{coop_sel[0]}</strong>")
        else:
            tags.append(f"Cooperativa: <strong>{len(coop_sel)} selecionadas</strong>")
    if tp_sel:
        tags.append(f"Tipo Pessoa: <strong>{', '.join(tp_sel)}</strong>")
    if ano_mes_sel:
        tags.append(f"Mês/Ano: <strong>{', '.join(ano_mes_sel)}</strong>")
    if indexador_sel:
        tags.append(f"Indexador: <strong>{', '.join(indexador_sel)}</strong>")
    if categoria_linha_sel:
        tags.append(f"Linha de Crédito: <strong>{', '.join(categoria_linha_sel)}</strong>")
    if tags:
        c_filt, c_reset = st.columns([0.82, 0.18])
        with c_filt:
            st.markdown(
                f"<div class='filtros-ativos'>🔍 Filtros ativos: &nbsp;"
                + " &nbsp;·&nbsp; ".join(tags) + "</div>",
                unsafe_allow_html=True,
            )
        with c_reset:
            def _limpar_filtros_bid():
                st.session_state["bid_reset"] += 1

            st.button("Limpar", use_container_width=True,
                      on_click=_limpar_filtros_bid)

    # ── KPIs ─────────────────────────────────
    st.markdown('<div class="section-title">Indicadores Principais</div>', unsafe_allow_html=True)

    valor_total  = dff["valor_contrato"].sum()
    taxa_media   = dff["taxa_operacao"].mean() if not dff.empty else 0
    qtd_contratos = len(dff)
    pf_count = (dff["tipo_pessoa"] == "PF").sum()
    pj_count = (dff["tipo_pessoa"] == "PJ").sum()
    total_pp = (pf_count + pj_count) or 1

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(
            label="Valor Total Liberado",
            value=fmt_moeda(valor_total),
            delta=f"{f'{qtd_contratos:,}'.replace(',', '.')} contratos",
        )
    with c2:
        st.metric(
            label="Taxa Média (% a.m.)",
            value=f"{taxa_media:.2f}%",
            delta=f" - ",
        )
    with c3:
        st.metric(
            label="Contratos (PF / PJ)",
            value=f"{pf_count} / {pj_count}",
            delta=f"PF {pf_count/total_pp*100:.0f}%  ·  PJ {pj_count/total_pp*100:.0f}%",
        )

    if dff.empty:
        st.markdown("""
        <div class="no-data">
            🔎 Nenhum contrato encontrado para os filtros selecionados.<br>
            Ajuste os filtros na barra lateral para ver os dados.
        </div>
        """, unsafe_allow_html=True)
    else:
        # ── Tabela por Central ───────────────────
        st.markdown('<div class="section-title">Operações por Central</div>', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">📋 Valor Contratado, Ticket Médio, Taxa e Volume por Central</p>',
                    unsafe_allow_html=True)

        df_central = dff.groupby("central").agg(
            Valor_Contratado=("valor_contrato", "sum"),
            Qtd_Contratos   =("num_proposta",   "count"),
            Taxa_Utilizada  =("taxa_operacao",  "mean"),
        ).reset_index()
        df_central["Ticket_Medio"] = df_central["Valor_Contratado"] / df_central["Qtd_Contratos"]
        df_central["Central"] = df_central["central"].apply(
            lambda x: f"{x} - {_sigla_central_map_preview[x]}" if x in _sigla_central_map_preview else x
        )

        df_central_disp = df_central.drop(columns=["central"]).rename(columns={
            "Valor_Contratado":"Valor Contratado (R$)",
            "Ticket_Medio":    "Ticket Médio (R$)",
            "Taxa_Utilizada":  "Taxa Média (% a.m.)",
            "Qtd_Contratos":   "Qtd Contratos",
        })[["Central", "Valor Contratado (R$)", "Ticket Médio (R$)", "Taxa Média (% a.m.)", "Qtd Contratos"]]

        st.dataframe(
            df_central_disp.style.format({
                "Valor Contratado (R$)": lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "Ticket Médio (R$)":    lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "Taxa Média (% a.m.)": "{:.2f}%",
                "Qtd Contratos": lambda x: f"{x:,.0f}".replace(",", "."),
            }),
            use_container_width=True,
            hide_index=True,
        )

        # ── Tabela de Operações por Cooperativa ──
        st.markdown('<div class="section-title">Operações por Cooperativa</div>', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">📋 Detalhamento das Operações Contratadas por Cooperativa</p>',
                    unsafe_allow_html=True)

        df_coop_ops = dff.groupby(["central", "cooperativa_num", "cooperativa_nom", "linha_credito"]).agg(
            Valor_Contratado=("valor_contrato", "sum"),
            Contagem        =("num_proposta",   "count"),
        ).reset_index()

        df_coop_ops = df_coop_ops.sort_values("Valor_Contratado", ascending=False).reset_index(drop=True)

        # Coluna combinada Central: nº + sigla
        df_coop_ops["Central"] = df_coop_ops["central"].apply(
            lambda x: f"{x} - {_sigla_central_map_preview[x]}" if x in _sigla_central_map_preview else x
        )
        # Coluna combinada Cooperativa: nº + sigla
        df_coop_ops["Cooperativa"] = df_coop_ops["cooperativa_num"] + " - " + df_coop_ops["cooperativa_nom"]

        df_coop_ops_disp = df_coop_ops.rename(columns={
            "Valor_Contratado": "Valor Contratado (R$)",
            "Contagem":         "Qtd. Contratos",
        })

        st.dataframe(
            df_coop_ops_disp[["Central","Cooperativa","Valor Contratado (R$)","Qtd. Contratos"]].style.format({
                "Valor Contratado (R$)": lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "Qtd. Contratos": lambda x: f"{x:,.0f}".replace(",", "."),
            }),
            use_container_width=True,
            hide_index=True,
        )

        # ── Gráficos PF/PJ + Valor Diário ────────
        st.markdown('<div class="section-title">Análise Visual</div>', unsafe_allow_html=True)

        col_g1, col_g2 = st.columns(2)

        # Donut PF/PJ
        with col_g1:
            st.markdown('<p class="chart-title">👤 Distribuição PF / PJ</p>', unsafe_allow_html=True)
            df_tp = dff.groupby("tipo_pessoa")["valor_contrato"].sum().reset_index().sort_values("tipo_pessoa")
            fig_tp = go.Figure(go.Pie(
                labels=df_tp["tipo_pessoa"],
                values=df_tp["valor_contrato"],
                hole=0.50,
                marker=dict(colors=[COR_VERDE, COR_TEAL], line=dict(color=COR_BG, width=3)),
                textinfo="percent",
                textfont=dict(size=14, family="'Sicoob Sans','Nunito Sans',sans-serif", weight="bold"),
                textposition="outside",
                hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>",
            ))
            fig_tp.update_layout(
                **BASE_LAYOUT,
                legend=dict(
                    bgcolor="rgba(0,0,0,0)",
                    orientation="h",
                    x=0.5, xanchor="center",
                    y=-0.12, yanchor="top",
                    font=dict(color=COR_TEXTO, size=13,
                              family="'Sicoob Sans','Nunito Sans',sans-serif"),
                ),
                height=340,
                margin=dict(l=60, r=60, t=80, b=60),
            )
            st.plotly_chart(fig_tp, use_container_width=True, config=PLOTLY_CFG)

        # Donut Pré/Pós
        with col_g2:
            st.markdown('<p class="chart-title">📈 Pré / Pós Fixado</p>', unsafe_allow_html=True)
            df_pp = dff.groupby("pre_pos")["valor_contrato"].sum().reset_index().sort_values("pre_pos")
            fig_pp = go.Figure(go.Pie(
                labels=df_pp["pre_pos"],
                values=df_pp["valor_contrato"],
                hole=0.50,
                marker=dict(colors=[COR_VERDE, COR_TEAL], line=dict(color=COR_BG, width=3)),
                textinfo="percent",
                textfont=dict(size=14, family="'Sicoob Sans','Nunito Sans',sans-serif", weight="bold"),
                textposition="outside",
                hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>",
            ))
            fig_pp.update_layout(
                **BASE_LAYOUT,
                legend=dict(
                    bgcolor="rgba(0,0,0,0)",
                    orientation="h",
                    x=0.5, xanchor="center",
                    y=-0.12, yanchor="top",
                    font=dict(color=COR_TEXTO, size=13,
                              family="'Sicoob Sans','Nunito Sans',sans-serif"),
                ),
                height=340,
                margin=dict(l=60, r=60, t=80, b=60),
            )
            st.plotly_chart(fig_pp, use_container_width=True, config=PLOTLY_CFG)

        # Valor Diário últimos 14 dias
        st.markdown('<p class="chart-title">📅 Valor Diário — Últimos 14 Dias</p>', unsafe_allow_html=True)
        data_ref = dff["data_movimento"].max()
        data_ini_14 = data_ref - timedelta(days=13)
        df_14 = dff[dff["data_movimento"] >= data_ini_14].copy()
        df_diario = df_14.groupby("data_movimento")["valor_contrato"].sum().reset_index()
        df_diario = df_diario.sort_values("data_movimento")
        df_diario["label"] = df_diario["data_movimento"].dt.strftime("%d/%m")

        fig_diario = go.Figure()
        fig_diario.add_trace(go.Bar(
            x=df_diario["label"],
            y=df_diario["valor_contrato"],
            marker=dict(
                color=df_diario["valor_contrato"],
                colorscale=[[0, "#003D4D"], [0.4, COR_TEAL], [1, COR_VERDE]],
                showscale=False,
                line=dict(color="rgba(0,0,0,0)", width=0),
            ),
            text=df_diario["valor_contrato"].apply(lambda v: fmt_abrev(v)),
            textposition="auto",
            textfont=dict(color="white", weight="bold"),
            hovertemplate="<b>%{x}</b><br><span style='color:#00AE9D'>R$ %{text}</span><extra></extra>",
        ))
        tv, tt = gerar_tickvals(df_diario["valor_contrato"])
        fig_diario.update_layout(
            **BASE_LAYOUT,
            xaxis=dict(gridcolor=COR_BORDER, tickangle=-40,
                       tickfont=dict(size=11, color=COR_AXIS), linecolor=COR_BORDER, showline=True),
            yaxis=dict(gridcolor=COR_BORDER, gridwidth=0.5, tickvals=tv, ticktext=tt,
                       title=dict(text="R$", font=dict(color=COR_LABEL, size=12)),
                       tickfont=dict(size=11, color=COR_AXIS), linecolor=COR_BORDER, showline=True),
            height=340,
            bargap=0.2,
            margin=dict(l=60, r=30, t=30, b=70),
        )
        st.plotly_chart(fig_diario, use_container_width=True, config=PLOTLY_CFG)

    # ── Rodapé ───────────────────────────────
    st.markdown("""
    <div class="footer">
        Concessão BID &nbsp;|&nbsp;
        Desenvolvido com Streamlit &amp; Python &nbsp;|&nbsp;
        Sicoob
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
