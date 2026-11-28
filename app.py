import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import math
import os
import datetime
import re
import base64
import requests
from io import BytesIO

# =========================================================
# 🔗 CONFIGURAZIONE CLOUD: LINK GOOGLE FOGLI GIÀ INSERITO
# =========================================================
URL_PARTE_1 = "https://docs.google.com/spreadsheets/d/"
URL_PARTE_2 = "1jggdGzGzv30wBWrCn1JhQGjBvU3op0fr-UEpsZ1SJ2I"
URL_PARTE_3 = "/edit?usp=sharing"

LINK_GOOGLE_FOGLI_26_27 = URL_PARTE_1 + URL_PARTE_2 + URL_PARTE_3
LINK_GOOGLE_FOGLI_25_26 = ""

# =============================================================
# 1. IMPOSTAZIONI GENERALI E TEMA OBSIDIAN CARBON & NEON EMERALD
# =============================================================
st.set_page_config(
    page_title="Dashboard Betting", 
    layout="wide", 
    initial_sidebar_state="auto"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Outfit:wght@300;400;600;800&display=swap');

    /* Polyfill Font Bandiere a Colori per Windows (inclusa bandiera Inghilterra) */
    @font-face {
        font-family: 'Twemoji Country Flags';
        unicode-range: U+1F1E6-1F1FF, U+1F3F4, U+E0061-E007A, U+E007F;
        src: url('https://cdn.jsdelivr.net/npm/country-flag-emoji-polyfill@0.1/dist/TwemojiCountryFlags.woff2') format('woff2');
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stHeader"] { background-color: transparent; }
    
    html, body, [class*="css"],
    div[data-baseweb="select"], div[data-baseweb="select"] *,
    div[data-baseweb="popover"], div[data-baseweb="popover"] *,
    ul[data-baseweb="menu"], ul[data-baseweb="menu"] * {
        font-family: 'Twemoji Country Flags', 'Outfit', sans-serif !important;
    }

    @keyframes slideUpFade {
        0% { opacity: 0; transform: translateY(12px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .main .block-container { 
        padding-top: 1.5rem; 
        animation: slideUpFade 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    /* Intestazioni pulite stile default su sfondo carbonio */
    h1 {
        color: #ffffff !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    h2, h3, h4 {
        color: #f3f4f6 !important;
        font-weight: 700 !important;
    }
    
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
        color: #ffffff !important;
    }

    /* Sfondo Obsidian Carbon opaco */
    .stApp {
        background: radial-gradient(circle at 12% 10%, rgba(0, 230, 118, 0.045), transparent 34%),
                    radial-gradient(circle at 88% 88%, rgba(16, 185, 129, 0.03), transparent 36%);
        background-color: #0a0c0f !important;
        color: #e5e7eb;
    }

    /* Sidebar Grafite Scura */
    [data-testid="stSidebar"] {
        background-color: #101317 !important;
        border-right: 1px solid #1d2229 !important;
    }
    [data-testid="stSidebar"] h1 {
        color: #00e676 !important;
        font-size: 1.55rem !important;
    }

    /* Menu a tendina e input: Antracite puro opaco (zero marroncino) */
    div[data-baseweb="select"] > div,
    div[data-baseweb="base-input"] > div,
    div[data-baseweb="input"] > div {
        background-color: #161a20 !important;
        border: 1px solid #2b313a !important;
        color: #f3f4f6 !important;
        border-radius: 10px !important;
        transition: border-color 0.25s ease, box-shadow 0.25s ease;
    }
    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="base-input"] > div:hover,
    div[data-baseweb="input"] > div:hover {
        border-color: rgba(0, 230, 118, 0.55) !important;
    }
    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="base-input"] > div:focus-within,
    div[data-baseweb="input"] > div:focus-within {
        border-color: #00e676 !important;
        box-shadow: 0 0 0 1px rgba(0, 230, 118, 0.25) !important;
    }
    div[data-baseweb="popover"] > div,
    ul[data-baseweb="menu"] {
        background-color: #161a20 !important;
        border: 1px solid #2b313a !important;
        border-radius: 10px !important;
    }
    ul[data-baseweb="menu"] li:hover {
        background-color: #202630 !important;
    }
    /* Tag del multiselect (Coppe) */
    span[data-baseweb="tag"] {
        background-color: rgba(0, 230, 118, 0.16) !important;
        border: 1px solid rgba(0, 230, 118, 0.4) !important;
        color: #e5e7eb !important;
        border-radius: 6px !important;
    }

    hr {
        border-color: #1d2229 !important;
    }
    
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0a0c0f; }
    ::-webkit-scrollbar-thumb { background: #262c36; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #36404f; }

    /* Schede Tab */
    .stTabs [data-baseweb="tab-list"] { gap: 2rem; border-bottom: 1px solid #1d2229; }
    .stTabs [data-baseweb="tab"] { height: 48px; font-weight: 600; font-size: 1.02rem; color: #8b949e; padding-bottom: 10px; transition: color 0.25s ease; }
    .stTabs [data-baseweb="tab"]:hover { color: #e5e7eb; }
    .stTabs [aria-selected="true"] { color: #00e676 !important; border-bottom-color: #00e676 !important; }
    
    /* Pulsanti Neon Emerald */
    .stButton>button, div[data-testid="stFormSubmitButton"]>button, a[data-testid="stLinkButton"] { 
        border-radius: 10px !important; 
        background: rgba(0, 230, 118, 0.13) !important; 
        color: #00e676 !important; 
        font-weight: 700 !important; 
        border: 1px solid rgba(0, 230, 118, 0.42) !important; 
        box-shadow: 0 4px 14px rgba(0, 230, 118, 0.08) !important;
        transition: all 0.25s ease !important;
    }
    .stButton>button:hover, div[data-testid="stFormSubmitButton"]>button:hover, a[data-testid="stLinkButton"]:hover { 
        background: #00e676 !important; 
        color: #0a0c0f !important;
        border-color: #00e676 !important;
        box-shadow: 0 6px 20px rgba(0, 230, 118, 0.35) !important;
        transform: translateY(-1px);
    }
    
    /* Metriche Carbon */
    div[data-testid="metric-container"] {
        background: #13171d !important;
        border: 1px solid #222831 !important;
        padding: 15% 10% !important;
        border-radius: 14px !important;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.25) !important;
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        border-color: rgba(0, 230, 118, 0.38) !important;
        box-shadow: 0 10px 28px rgba(0, 230, 118, 0.08) !important;
    }
    div[data-testid="metric-container"] label {
        color: #9ca3af !important;
        font-size: 0.92rem !important;
        font-weight: 600 !important;
    }
    
    /* Card Obsidian Matte */
    .glass-box {
        background: #13171d;
        border: 1px solid #222831;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 8px 28px rgba(0, 0, 0, 0.28);
        margin-bottom: 22px;
        transition: border-color 0.25s ease;
    }
    .glass-box:hover { border-color: #2f3845; }
    
    [data-testid="stTable"] table { width: 100% !important; background: transparent !important; color: #e5e7eb; border-collapse: collapse; }
    [data-testid="stTable"] tbody tr { transition: background-color 0.2s ease; }
    [data-testid="stTable"] tbody tr:hover { background-color: rgba(255, 255, 255, 0.04) !important; }
    [data-testid="stTable"] th {
        background-color: #161a20 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border-bottom: 1px solid #262c36 !important;
        text-transform: uppercase;
        font-size: 0.85em;
        letter-spacing: 1px;
    }
    [data-testid="stTable"] th, [data-testid="stTable"] td { 
        text-align: center !important; 
        border-color: #1d2229 !important;
        padding: 12px 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🔒 0. SISTEMA DI SICUREZZA E LOGIN
# ==========================================
if 'autenticato' not in st.session_state:
    st.session_state.autenticato = False

if not st.session_state.autenticato:
    col_l1, col_l2, col_l3 = st.columns([1, 1.5, 1])
    with col_l2:
        st.markdown("""
        <div class="glass-box" style="text-align: center; margin-top: 12vh; border-top: 4px solid #00e676;">
            <h1 style="margin:0; font-size: 3em;">🔒</h1>
            <h2 style="color: #fff; margin-top: 10px;">Accesso Riservato</h2>
            <p style="color: #9ca3af; font-size: 0.9em; margin-bottom: 0;">Inserisci la password per sbloccare la Dashboard Betting.</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            pwd_inserita = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Inserisci la password...")
            submit_login = st.form_submit_button("🔓 Sblocca Dashboard", use_container_width=True)
            
            if submit_login:
                if pwd_inserita == "Mamma&Papa":
                    st.session_state.autenticato = True
                    st.rerun()
                else:
                    st.error("❌ Password errata. Accesso negato.")
    st.stop()

# =========================================================
# 🏳️ MOTORE GRAFICO BANDIERE E STEMMI SERIE A (CDN UFFICIALE)
# =========================================================
MAPPA_BANDIERE_URL = {
    'Serie A': 'https://flagcdn.com/w40/it.png',
    'La Liga': 'https://flagcdn.com/w40/es.png',
    'Premier League': 'https://flagcdn.com/w40/gb-eng.png'
}

STEMMI_SERIE_A_ID = [
    ('internazionale', 505), ('inter', 505),
    ('hellas verona', 504), ('verona', 504),
    ('atalanta', 499), ('bologna', 500), ('cagliari', 490), ('como', 895),
    ('cremonese', 520), ('empoli', 511), ('fiorentina', 502), ('frosinone', 512),
    ('genoa', 495), ('juventus', 496), ('juve', 496), ('lazio', 487),
    ('lecce', 867), ('milan', 489), ('monza', 1579), ('napoli', 492),
    ('parma', 523), ('pisa', 506), ('roma', 497), ('salernitana', 514),
    ('sassuolo', 488), ('spezia', 515), ('torino', 503), ('udinese', 494),
    ('venezia', 517), ('sampdoria', 498), ('bari', 508), ('palermo', 522),
    ('catanzaro', 1687), ('cesena', 509), ('modena', 524), ('brescia', 518)
]

def ottieni_bandiera_html(campionato, width=22):
    lega_pulita = campionato.replace('🇮🇹 ', '').replace('🏴󠁧󠁢󠁥󠁮󠁧󠁿 ', '').replace('🇪🇸 ', '').strip()
    url = MAPPA_BANDIERE_URL.get(lega_pulita, '')
    if url:
        return f'<img src="{url}" width="{width}" style="vertical-align: middle; margin-right: 6px; border-radius: 3px; box-shadow: 0 1px 4px rgba(0,0,0,0.4);">'
    return ''

@st.cache_data
def ottieni_src_stemma(squadra, campionato):
    lega_pulita = campionato.replace('🇮🇹 ', '').replace('🏴󠁧󠁢󠁥󠁮󠁧󠁿 ', '').replace('🇪🇸 ', '').strip()
    if lega_pulita != 'Serie A':
        return ""
    percorso_locale = f"Stemmi/{squadra}.png"
    if os.path.exists(percorso_locale):
        try:
            with open(percorso_locale, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            return f"data:image/png;base64,{b64}"
        except Exception:
            pass
    sq_norm = str(squadra).lower().strip()
    for chiave, team_id in STEMMI_SERIE_A_ID:
        if chiave == sq_norm or chiave in sq_norm:
            return f"https://media.api-sports.io/football/teams/{team_id}.png"
    return ""

def ottieni_stemma_html(squadra, campionato, size=26):
    src = ottieni_src_stemma(squadra, campionato)
    if src:
        return f'<img src="{src}" style="width:{size}px; height:{size}px; object-fit:contain; vertical-align:middle; margin-right:7px; filter: drop-shadow(0 2px 3px rgba(0,0,0,0.5));">'
    return ""

# ==========================================
# 2. FUNZIONI DI CARICAMENTO E CALCOLO
# ==========================================
def estrai_id_google_sheet(url):
    if not url or "INCOLLA_QUI" in url:
        return None
    match = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
    if match:
        return match.group(1)
    return url.strip() if len(url.strip()) > 20 else None

def pulisci_e_normalizza_df(df):
    if df is None or df.empty: return df
    df = df.dropna(how='all')
    df.columns = [str(col).strip() for col in df.columns]
    mappa_correzioni = {
        'Titi Totali Casa': 'Tiri totali Casa', 'Titi Totali Trasferta': 'Tiri totali Trasferta',
        'Titi Totali trasferta': 'Tiri totali Trasferta', 'Tiri Totali trasferta': 'Tiri totali Trasferta',
        'xG casa': 'xG Casa', 'xG trasferta': 'xG Trasferta',
        'xGA casa': 'xGA Casa', 'xGA trasferta': 'xGA Trasferta',
        'Falli commessi Casa': 'Falli Commessi Casa', 'Falli commessi Trasferta': 'Falli Commessi Trasferta',
        'Parate casa': 'Parate Casa', 'parate casa': 'Parate Casa', 'Parate effettuate Casa': 'Parate Casa',
        'Parate trasferta': 'Parate Trasferta', 'parate trasferta': 'Parate Trasferta', 'Parate effettuate Trasferta': 'Parate Trasferta',
        'XGOT Casa': 'xGOT Casa', 'xGOT casa': 'xGOT Casa', 'xgot casa': 'xGOT Casa', 'XGOT casa': 'xGOT Casa',
        'XGOT Trasferta': 'xGOT Trasferta', 'xGOT trasferta': 'xGOT Trasferta', 'xgot trasferta': 'xGOT Trasferta', 'XGOT trasferta': 'xGOT Trasferta'
    }
    df = df.rename(columns=mappa_correzioni)
    return df

@st.cache_data(ttl=300)
def load_data(stagione, custom_url=""):
    url_scelto = custom_url if custom_url else (LINK_GOOGLE_FOGLI_26_27 if stagione == "2026-2027" else LINK_GOOGLE_FOGLI_25_26)
    sheet_id = estrai_id_google_sheet(url_scelto)
    
    xls = None
    modalita_fonte = ""
    errore_dettaglio = ""
    
    if sheet_id:
        try:
            export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
            response = requests.get(export_url, timeout=20)
            if response.status_code == 200 and not response.content[:15].startswith(b'<!DOCTYPE html'):
                xls = pd.ExcelFile(BytesIO(response.content))
                ora_sync = datetime.datetime.now().strftime('%d/%m/%Y alle %H:%M')
                modalita_fonte = f"☁️ Google Fogli ({ora_sync})"
            else:
                errore_dettaglio = f"Il file su Google Drive è impostato su 'Con restrizioni' oppure non è stato convertito in Fogli Google (Codice HTTP {response.status_code}). Vai su Google Fogli -> Condividi -> Chiunque abbia il link."
        except Exception as e:
            errore_dettaglio = f"Errore tecnico durante la lettura del foglio: {str(e)}"

    if xls is None:
        local_path = f"Statistiche Campionati {stagione}.xlsx"
        if os.path.exists(local_path):
            xls = pd.ExcelFile(local_path)
            timestamp = os.path.getmtime(local_path)
            ora_sync = datetime.datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y alle %H:%M')
            modalita_fonte = f"💻 File Locale ({ora_sync})"
        else:
            return {"Errore": errore_dettaglio} if errore_dettaglio else None

    dati = {}
    for sheet in ['Serie A', 'La Liga', 'Premier League', 'Partite']:
        if sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet)
            dati[sheet] = pulisci_e_normalizza_df(df).fillna(0)
        else:
            dati[sheet] = pd.DataFrame()
            
    if 'Palinsesto' in xls.sheet_names:
        df_pal = pd.read_excel(xls, sheet_name='Palinsesto').dropna(how='all')
        df_pal.columns = [str(col).strip() for col in df_pal.columns]
        dati['Palinsesto'] = df_pal.fillna(0)
    elif 'Palinsesto Serie A' in xls.sheet_names:
        df_pal = pd.read_excel(xls, sheet_name='Palinsesto Serie A').dropna(how='all')
        df_pal.columns = [str(col).strip() for col in df_pal.columns]
        dati['Palinsesto'] = df_pal.fillna(0)
    else:
        dati['Palinsesto'] = pd.DataFrame()
        
    dati['Ultimo_Aggiornamento'] = modalita_fonte
    return dati

def formatta_numero(val):
    if isinstance(val, (int, float)) and not pd.isna(val): return f"{math.ceil(val * 100) / 100:.2f}"
    return val

def calcola_forma(team, df_part):
    if df_part is None or df_part.empty: return "N/D"
    df_team = df_part[(df_part['Squadra Casa'] == team) | (df_part['Squadra Trasferta'] == team)].copy()
    if df_team.empty: return "Nessun dato recente"
    if 'Data' in df_team.columns:
        df_team['Data'] = pd.to_datetime(df_team['Data'], errors='coerce')
        df_team = df_team.sort_values(by='Data')
    ultime_5 = df_team.tail(5)
    forma = []
    for _, row in ultime_5.iterrows():
        gf = row.get('Gol Casa') if row.get('Squadra Casa') == team else row.get('Gol Trasferta')
        gs = row.get('Gol Trasferta') if row.get('Squadra Casa') == team else row.get('Gol Casa')
        if pd.isna(gf) or pd.isna(gs): continue
        if gf > gs: forma.append("🟢")
        elif gf == gs: forma.append("⚪")
        else: forma.append("🔴")
    return " ".join(forma) if forma else "N/D"

def calcola_mercati_betting(team, df_part, modalita="globale", ruolo="casa"):
    if df_part is None or df_part.empty: return 0, 0, 0
    
    if modalita == "globale":
        df_team = df_part[(df_part['Squadra Casa'] == team) | (df_part['Squadra Trasferta'] == team)]
    elif modalita == "specifico" and ruolo == "casa":
        df_team = df_part[df_part['Squadra Casa'] == team]
    elif modalita == "specifico" and ruolo == "trasferta":
        df_team = df_part[df_part['Squadra Trasferta'] == team]
        
    tot_partite = len(df_team)
    if tot_partite == 0: return 0, 0, 0
    
    over_25 = 0
    goal = 0
    
    for _, row in df_team.iterrows():
        try:
            gf_casa = float(row.get('Gol Casa', 0))
            gf_trasf = float(row.get('Gol Trasferta', 0))
            if math.isnan(gf_casa) or math.isnan(gf_trasf): continue
            
            if (gf_casa + gf_trasf) > 2.5: over_25 += 1
            if gf_casa > 0 and gf_trasf > 0: goal += 1
        except:
            pass
        
    perc_over = (over_25 / tot_partite) * 100
    perc_goal = (goal / tot_partite) * 100
    
    return tot_partite, perc_over, perc_goal

# =========================================================================
# 🔬 MOTORE AVANZATO: SPRECONI/CINICI + QUALITÀ TIRO + xGOT + PARATE + FORMA
# =========================================================================
def analizza_dna_squadra(team, df_part, xg_att, tt_att, xg_stag_medio, xgot_att=0.0):
    """Calcola Momentum ultime 5, Cinismo (Gol Reali vs xG), Qualità Tiro (xG/Tiro) e Qualità Conclusione (xGOT vs xG)."""
    res = {
        'n_part': 0, 'n_5': 0, 'gf_5': None, 'gs_5': None, 'punti_5': None,
        'momentum_label': '➡️ N/D',
        'delta_cinismo': 0.0, 'stato_cinismo': '⚖️ In Linea', 'mult_cin_stat': 1.00,
        'xg_per_tiro': 0.11, 'stato_tiro': '⚖️ Mix Bilanciato',
        'mult_cor_tiro': 1.00, 'mult_par_tiro': 1.00,
        'has_xgot': False, 'delta_xgot': 0.0, 'stato_xgot': '', 'mult_par_xgot': 1.00
    }
    
    if tt_att and tt_att > 0:
        xgt = float(xg_att) / float(tt_att)
        res['xg_per_tiro'] = xgt
        if xgt < 0.095 and tt_att >= 11.0:
            res['stato_tiro'] = '🚀 Da Fuori (+Corner/Parate)'
            res['mult_cor_tiro'] = 1.06
            res['mult_par_tiro'] = 1.08
        elif xgt > 0.135:
            res['stato_tiro'] = '🎯 In Area (-Corner, +Gol)'
            res['mult_cor_tiro'] = 0.94
            res['mult_par_tiro'] = 0.95

    if xgot_att and float(xgot_att) > 0 and xg_att and float(xg_att) > 0:
        res['has_xgot'] = True
        d_xgot = float(xgot_att) - float(xg_att)
        res['delta_xgot'] = d_xgot
        if d_xgot <= -0.15:
            res['stato_xgot'] = f'🧤 Tiri Parabili ({d_xgot:+.2f} xGOT)'
            res['mult_par_xgot'] = 1.08
        elif d_xgot >= 0.15:
            res['stato_xgot'] = f'🎯 Finalizz. Top ({d_xgot:+.2f} xGOT)'
            res['mult_par_xgot'] = 0.93
        else:
            res['stato_xgot'] = f'⚖️ xGOT Neutro ({d_xgot:+.2f})'
            res['mult_par_xgot'] = 1.00
            
    if df_part is not None and not df_part.empty and 'Squadra Casa' in df_part.columns and 'Squadra Trasferta' in df_part.columns:
        df_t = df_part[(df_part['Squadra Casa'] == team) | (df_part['Squadra Trasferta'] == team)].copy()
        if not df_t.empty:
            if 'Data' in df_t.columns:
                df_t['Data'] = pd.to_datetime(df_t['Data'], errors='coerce')
                df_t = df_t.sort_values(by='Data')
            gf_all, gs_all, pts_all = [], [], []
            for _, r in df_t.iterrows():
                try:
                    gf = float(r.get('Gol Casa')) if r.get('Squadra Casa') == team else float(r.get('Gol Trasferta'))
                    gs = float(r.get('Gol Trasferta')) if r.get('Squadra Casa') == team else float(r.get('Gol Casa'))
                    if math.isnan(gf) or math.isnan(gs):
                        continue
                    gf_all.append(gf)
                    gs_all.append(gs)
                    pts_all.append(3 if gf > gs else (1 if gf == gs else 0))
                except Exception:
                    continue
                    
            n_tot = len(gf_all)
            res['n_part'] = n_tot
            if n_tot >= 4 and xg_stag_medio > 0:
                media_gf_reale = sum(gf_all) / n_tot
                delta = media_gf_reale - xg_stag_medio
                res['delta_cinismo'] = delta
                if delta <= -0.22:
                    res['stato_cinismo'] = f'🔥 Sprecona ({delta:+.2f} vs xG)'
                    res['mult_cin_stat'] = 1.06
                elif delta >= 0.22:
                    res['stato_cinismo'] = f'🎯 Iper-Cinica ({delta:+.2f} vs xG)'
                    res['mult_cin_stat'] = 0.95
                else:
                    res['stato_cinismo'] = f'⚖️ In Linea ({delta:+.2f} vs xG)'
                    
            if n_tot >= 3:
                ult5_gf = gf_all[-5:]
                ult5_gs = gs_all[-5:]
                ult5_pts = pts_all[-5:]
                res['n_5'] = len(ult5_gf)
                res['gf_5'] = sum(ult5_gf) / len(ult5_gf)
                res['gs_5'] = sum(ult5_gs) / len(ult5_gs)
                p5 = sum(ult5_pts)
                res['punti_5'] = p5
                p5_norm = (p5 / len(ult5_pts)) * 5.0
                if p5_norm >= 10.5:
                    res['momentum_label'] = f'📈 Hot ({p5} pt/5G)'
                elif p5_norm <= 4.5:
                    res['momentum_label'] = f'📉 Cold ({p5} pt/5G)'
                else:
                    res['momentum_label'] = f'➡️ Stabile ({p5} pt/5G)'
    return res

def calcola_game_state(p_win, p_lose):
    """Restituisce moltiplicatore volumi e badge in base alla probabilità 1X2 di Poisson."""
    if p_win >= 64.0:
        return 0.92, "🧊 Rischio Gestione (-8%)"
    elif 44.0 <= p_win <= 58.0:
        return 1.04, "🔥 Spinta Costante (+4%)"
    elif 48.0 <= p_lose < 64.0:
        return 1.04, "⚡ Spinta Rincorsa (+4%)"
    return 1.00, "⚖️ Game State Neutro"

def calcola_poisson_match(xg_att_1, xg_att_2, xga_def_1, xga_def_2, tp_1, tp_2, media_tp_1, media_tp_2, dna_1, dna_2, coppe_1=False, coppe_2=False, xgot_1=0.0, xgot_2=0.0):
    """Calcola xG calibrati con xGOT (se presente in Serie A), Tiri in Porta, Momentum Ultime 5 e Affaticamento Coppe + distribuzione 1X2."""
    att_eff_1 = (xg_att_1 * 0.70 + xgot_1 * 0.30) if (xgot_1 and xgot_1 > 0) else xg_att_1
    att_eff_2 = (xg_att_2 * 0.70 + xgot_2 * 0.30) if (xgot_2 and xgot_2 > 0) else xg_att_2

    xg_base_1 = (att_eff_1 + xga_def_2) / 2.0
    xg_base_2 = (att_eff_2 + xga_def_1) / 2.0

    fattore_tp_1 = max(0.85, min(1.18, tp_1 / media_tp_1)) if media_tp_1 > 0 else 1.0
    fattore_tp_2 = max(0.85, min(1.18, tp_2 / media_tp_2)) if media_tp_2 > 0 else 1.0

    gol_base_1 = ((xg_base_1 * 0.85) + (xg_base_1 * fattore_tp_1 * 0.15)) * 1.06
    gol_base_2 = ((xg_base_2 * 0.85) + (xg_base_2 * fattore_tp_2 * 0.15)) * 0.94

    gol_sq1 = gol_base_1
    gol_sq2 = gol_base_2
    if dna_1['n_5'] >= 3 and dna_2['n_5'] >= 3:
        rec_1 = (dna_1['gf_5'] + dna_2['gs_5']) / 2.0
        rec_2 = (dna_2['gf_5'] + dna_1['gs_5']) / 2.0
        gol_blend_1 = (gol_base_1 * 0.82) + (rec_1 * 0.18)
        gol_blend_2 = (gol_base_2 * 0.82) + (rec_2 * 0.18)
        gol_sq1 = max(gol_base_1 * 0.85, min(gol_base_1 * 1.15, gol_blend_1))
        gol_sq2 = max(gol_base_2 * 0.85, min(gol_base_2 * 1.15, gol_blend_2))

    if coppe_1:
        gol_sq1 *= 0.90
        gol_sq2 *= 1.05
    if coppe_2:
        gol_sq2 *= 0.90
        gol_sq1 *= 1.05

    l1 = max(0.1, gol_sq1)
    l2 = max(0.1, gol_sq2)
    probs_1 = [(math.exp(-l1) * (l1**k)) / math.factorial(k) for k in range(7)]
    probs_2 = [(math.exp(-l2) * (l2**k)) / math.factorial(k) for k in range(7)]

    p_1, p_x, p_2 = 0.0, 0.0, 0.0
    risultati_esatti = []
    for i in range(7):
        for j in range(7):
            p_ij = probs_1[i] * probs_2[j]
            if i > j: p_1 += p_ij
            elif i == j: p_x += p_ij
            else: p_2 += p_ij
            if i <= 4 and j <= 4:
                risultati_esatti.append((f"{i}-{j}", p_ij * 100))

    tot_p = p_1 + p_x + p_2
    if tot_p > 0:
        p_1, p_x, p_2 = (p_1 / tot_p) * 100, (p_x / tot_p) * 100, (p_2 / tot_p) * 100

    risultati_esatti.sort(key=lambda x: x[1])
    return l1, l2, p_1, p_x, p_2, risultati_esatti

def calcola_parate_portiere(parate_reali, proj_tp_avv, xga_dif, media_xga_lega, dna_avv):
    """Combina Parate Reali (se presenti in Serie A) con Tiri in Porta e xGOT dell'avversario."""
    molt_dif = (xga_dif / media_xga_lega) if (media_xga_lega and media_xga_lega > 0) else 1.0
    molt_dif = max(0.80, min(1.25, molt_dif))
    tiri_subiti = proj_tp_avv * molt_dif

    mult_qualita = dna_avv['mult_par_xgot'] if dna_avv.get('has_xgot', False) else dna_avv['mult_par_tiro']
    mult_sprec = 1.05 if "Sprecona" in dna_avv['stato_cinismo'] else 1.0
    parate_da_avv = tiri_subiti * 0.725 * mult_qualita * mult_sprec

    if parate_reali and float(parate_reali) > 0:
        parate_finali = (float(parate_reali) * 0.55) + (parate_da_avv * 0.45)
        badge_fonte = "✅ Dati Reali Parate + xGOT" if dna_avv.get('has_xgot', False) else "✅ Dati Reali Parate"
    else:
        parate_finali = parate_da_avv
        badge_fonte = "📐 Stima IA (xGOT)" if dna_avv.get('has_xgot', False) else "📐 Stima IA"

    return float(parate_finali), float(tiri_subiti), badge_fonte

def stima_stat_subita(df_lega, dati_difesa, ruolo_difesa, col_stat_attacco, col_stat_difesa):
    media_attacco_lega = df_lega[col_stat_attacco].mean() if col_stat_attacco in df_lega.columns else 0
    if media_attacco_lega <= 0:
        return 0.0, "⚪ N/D"

    if "Falli" in col_stat_attacco:
        val_avv = dati_difesa.get(col_stat_difesa, media_attacco_lega)
        media_dif_lega = df_lega[col_stat_difesa].mean() if col_stat_difesa in df_lega.columns else media_attacco_lega
        ratio = val_avv / media_dif_lega if media_dif_lega > 0 else 1.0
        if ratio >= 1.08:
            stato = "🟢 Gara Fisica"
        elif ratio <= 0.92:
            stato = "🔴 Gara Corretta"
        else:
            stato = "⚪ Ritmo Medio"
        return float(val_avv), stato

    col_xga = 'xGA Casa' if ruolo_difesa == 'Casa' else 'xGA Trasferta'
    media_xga = df_lega[col_xga].mean() if col_xga in df_lega.columns else 1.25
    xga_squadra = dati_difesa.get(col_xga, media_xga)
    ratio_xga = (xga_squadra / media_xga) if media_xga > 0 else 1.0

    media_fatti_dif = df_lega[col_stat_difesa].mean() if col_stat_difesa in df_lega.columns else 1.0
    fatti_dif = dati_difesa.get(col_stat_difesa, media_fatti_dif)
    ratio_passivita = (media_fatti_dif / fatti_dif) if fatti_dif > 0 else 1.0
    ratio_passivita = max(0.75, min(1.30, ratio_passivita))

    moltiplicatore_vulnerabilita = (0.70 * ratio_xga) + (0.30 * ratio_passivita)
    subiti_stimati = media_attacco_lega * moltiplicatore_vulnerabilita

    if moltiplicatore_vulnerabilita >= 1.08:
        stato = "🟢 Concede Molto"
    elif moltiplicatore_vulnerabilita <= 0.92:
        stato = "🔴 Difesa Solida"
    else:
        stato = "⚪ Difesa Media"

    return float(subiti_stimati), stato

def calcola_linea_statistica(proiezione, cuscinetto_base, stato_difesa=""):
    """Calcola la linea .5 consigliata garantendo un cuscinetto reale sopra il target intero di cassa."""
    if proiezione <= 0:
        return "N/D", 0, 0.0, "#888"
    is_muro = ("Solida" in stato_difesa) or ("Chiuse" in stato_difesa)
    cuscinetto = cuscinetto_base * 1.35 if is_muro else cuscinetto_base
    target_cassa = int(math.floor(proiezione - cuscinetto))
    if target_cassa < 1:
        return "NO BET (Linea bassa)", 0, 0.0, "#888"
    linea_consigliata = target_cassa - 0.5
    margine = proiezione - target_cassa
    colore = "#ffb703" if is_muro else ("#00e676" if "Concede" in stato_difesa or "Permessive" in stato_difesa else "#38bdf8")
    return f"OVER {linea_consigliata:.1f}", target_cassa, margine, colore

def genera_html_scanner(perc_over, perc_goal, tot_partite, color_accent="#00e676"):
    if perc_over > 0:
        quota_over = 100 / perc_over
        testo_q_over = f"<span style='color:#9ca3af; font-size:0.85em;'>Quota Fair:</span> <b style='color:#fff; font-family: JetBrains Mono, monospace;'>{quota_over:.2f}</b>"
    else:
        testo_q_over = "<span style='color:#9ca3af; font-size:0.85em;'>Quota Fair:</span> <b style='color:#fff; font-family: JetBrains Mono, monospace;'>N/D</b>"

    if perc_goal > 0:
        quota_goal = 100 / perc_goal
        testo_q_goal = f"<span style='color:#9ca3af; font-size:0.85em;'>Quota Fair:</span> <b style='color:#fff; font-family: JetBrains Mono, monospace;'>{quota_goal:.2f}</b>"
    else:
        testo_q_goal = "<span style='color:#9ca3af; font-size:0.85em;'>Quota Fair:</span> <b style='color:#fff; font-family: JetBrains Mono, monospace;'>N/D</b>"

    return f"""
    <div class="glass-box">
        <p style="margin:0; font-size:12px; color:#8b949e; text-align: right; text-transform: uppercase; letter-spacing: 1px;">Match Storici Analizzati: {tot_partite}</p>
        <div style="margin-top: 5px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <strong style="color: #fff; font-size: 1.1em;">🔥 OVER 2.5</strong>
                <div style="text-align: right;">
                    <span style="margin-right: 12px; background: #0d1014; border: 1px solid #222831; padding: 3px 8px; border-radius: 6px;">{testo_q_over}</span>
                    <span style="font-weight:800; font-size: 1.1em; color: {color_accent}; font-family: 'JetBrains Mono', monospace;">{perc_over:.1f}%</span>
                </div>
            </div>
            <div style="background: #0d1014; border-radius: 12px; width: 100%; height: 14px; overflow: hidden; border: 1px solid #222831;">
                <div style="background: linear-gradient(90deg, #123c2f, {color_accent}); border-radius: 12px; width: {perc_over}%; height: 100%; box-shadow: 0 0 12px {color_accent}; transition: width 1s ease-in-out;"></div>
            </div>
        </div>
        <div style="margin-top: 28px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <strong style="color: #fff; font-size: 1.1em;">⚽ GOAL (GG)</strong>
                <div style="text-align: right;">
                    <span style="margin-right: 12px; background: #0d1014; border: 1px solid #222831; padding: 3px 8px; border-radius: 6px;">{testo_q_goal}</span>
                    <span style="font-weight:800; font-size: 1.1em; color: {color_accent}; font-family: 'JetBrains Mono', monospace;">{perc_goal:.1f}%</span>
                </div>
            </div>
            <div style="background: #0d1014; border-radius: 12px; width: 100%; height: 14px; overflow: hidden; border: 1px solid #222831;">
                <div style="background: linear-gradient(90deg, #123c2f, {color_accent}); border-radius: 12px; width: {perc_goal}%; height: 100%; box-shadow: 0 0 12px {color_accent}; transition: width 1s ease-in-out;"></div>
            </div>
        </div>
    </div>
    """

# ==========================================
# 3. GESTIONE INTERFACCIA E SIDEBAR
# ==========================================
if 'pagina_impostazioni' not in st.session_state:
    st.session_state.pagina_impostazioni = False
if 'custom_gsheet_url' not in st.session_state:
    st.session_state.custom_gsheet_url = ""

st.sidebar.title("Dashboard Betting")

if st.sidebar.button("🔄 Sincronizza Google Fogli", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

if not st.session_state.pagina_impostazioni:
    st.sidebar.subheader("⚙️ Filtri Analisi")
    stagione_scelta = st.sidebar.selectbox("📅 Seleziona la Stagione:", ["2026-2027", "2025-2026"])
    
    opzioni_campionato = {
        "🇮🇹 Serie A": "Serie A",
        "🇪🇸 La Liga": "La Liga",
        "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League": "Premier League"
    }
    label_campionato = st.sidebar.selectbox("🏆 Seleziona il Campionato:", list(opzioni_campionato.keys()))
    campionato_scelto = opzioni_campionato[label_campionato]

    dati_campionati = load_data(stagione_scelta, st.session_state.custom_gsheet_url)

    if dati_campionati is None or "Errore" in dati_campionati:
        msg_err = dati_campionati.get("Errore", "") if isinstance(dati_campionati, dict) else ""
        st.error(f"⚠️ Impossibile leggere il database da Google Fogli. {msg_err}")
        if st.sidebar.button("⚙️ Apri Impostazioni"):
            st.session_state.pagina_impostazioni = True
            st.rerun()
    else:
        df_selezionato = dati_campionati.get(campionato_scelto, pd.DataFrame())
        df_partite = dati_campionati.get('Partite', pd.DataFrame())
        data_aggiornamento = dati_campionati.get('Ultimo_Aggiornamento', 'Sconosciuta')
        
        if df_selezionato.empty or 'Squadra' not in df_selezionato.columns:
            st.warning(f"⚠️ Il foglio '{campionato_scelto}' non contiene dati validi o la colonna 'Squadra'. Verifica il tuo Google Fogli.")
        else:
            lista_squadre_pure = sorted(df_selezionato['Squadra'].dropna().unique().tolist())
            
            st.sidebar.divider()
            modalita_confronto = st.sidebar.checkbox("⚔️ Attiva Modalità Confronto")
            
            coppe_casa = False
            coppe_ospite = False
            if modalita_confronto:
                st.sidebar.markdown("**Seleziona le squadre:**")
                squadra_1 = st.sidebar.selectbox("🏠 Prima Squadra (Casa):", lista_squadre_pure)
                squadra_2 = st.sidebar.selectbox("✈️ Seconda Squadra (Ospite):", lista_squadre_pure, index=1 if len(lista_squadre_pure)>1 else 0)
                simula_reale = st.sidebar.checkbox("🏟️ Usa Dati Reali (Solo Casa vs Trasferta)", value=True)
                st.sidebar.markdown("**🇪🇺 Affaticamento Coppe (-10%):**")
                coppe_casa = st.sidebar.checkbox(f"🇪🇺 Coppe in settimana: {squadra_1}")
                coppe_ospite = st.sidebar.checkbox(f"🇪🇺 Coppe in settimana: {squadra_2}")
            else:
                lista_squadre = ["Tutte le squadre"] + lista_squadre_pure
                squadra_scelta = st.sidebar.selectbox("🔎 Seleziona la Squadra:", lista_squadre)

            st.sidebar.divider()
            col_txt_ingr, col_btn_ingr = st.sidebar.columns([4, 1])
            with col_txt_ingr:
                st.markdown("<p style='font-size: 0.85em; color: #8b949e; margin-top: 8px;'>Impostazioni Cloud</p>", unsafe_allow_html=True)
            with col_btn_ingr:
                if st.button("⚙️", help="Gestisci il collegamento Cloud"):
                    st.session_state.pagina_impostazioni = not st.session_state.pagina_impostazioni
                    st.rerun()

            flag_header = ottieni_bandiera_html(campionato_scelto, width=34)

            if modalita_confronto:
                stemma_1_hdr = ottieni_stemma_html(squadra_1, campionato_scelto, size=42)
                stemma_2_hdr = ottieni_stemma_html(squadra_2, campionato_scelto, size=42)
                badge_c1 = " <span style='font-size:0.45em; background:rgba(255,183,3,0.18); color:#ffb703; padding:2px 6px; border-radius:4px; vertical-align:middle;'>🇪🇺 COPPE</span>" if coppe_casa else ""
                badge_c2 = " <span style='font-size:0.45em; background:rgba(255,183,3,0.18); color:#ffb703; padding:2px 6px; border-radius:4px; vertical-align:middle;'>🇪🇺 COPPE</span>" if coppe_ospite else ""
                col_t1, col_vs, col_t2 = st.columns([2, 1, 2])
                with col_t1:
                    st.markdown(f"<h2 style='text-align: right; color: #00e676 !important; text-shadow: 0 0 20px rgba(0,230,118,0.28);'>{stemma_1_hdr}{squadra_1}{badge_c1}</h2>", unsafe_allow_html=True)
                with col_vs:
                    st.markdown(f"<h3 style='text-align: center; color: #6b7280 !important; margin-top: 8px;'>{flag_header} vs</h3>", unsafe_allow_html=True)
                with col_t2:
                    st.markdown(f"<h2 style='text-align: left; color: #ff4b4b !important; text-shadow: 0 0 20px rgba(255,75,75,0.28);'>{stemma_2_hdr}{squadra_2}{badge_c2}</h2>", unsafe_allow_html=True)
            else:
                col_titolo, col_data = st.columns([3, 1])
                with col_titolo:
                    st.markdown(f"<h1>{flag_header} Statistiche {campionato_scelto}</h1>", unsafe_allow_html=True)
                with col_data:
                    st.markdown(f"<p style='text-align: right; color: #8b949e; font-size: 0.85em; margin-top: 1.5em;'>⏱️ Fonte Dati:<br><b style='color:#00e676;'>{data_aggiornamento}</b></p>", unsafe_allow_html=True)
            
            st.markdown(f"<p style='color:#8b949e;'>Stagione sportiva {stagione_scelta}</p>", unsafe_allow_html=True)
            st.divider()

            if modalita_confronto:
                dati_sq1 = df_selezionato[df_selezionato['Squadra'] == squadra_1].iloc[0]
                dati_sq2 = df_selezionato[df_selezionato['Squadra'] == squadra_2].iloc[0]
                stemma_sq1 = ottieni_stemma_html(squadra_1, campionato_scelto, size=24)
                stemma_sq2 = ottieni_stemma_html(squadra_2, campionato_scelto, size=24)

                has_parate_col = ('Parate Casa' in df_selezionato.columns) and ('Parate Trasferta' in df_selezionato.columns)
                has_xgot_col = ('xGOT Casa' in df_selezionato.columns) and ('xGOT Trasferta' in df_selezionato.columns)
                
                tab_radar, tab_pronostici_ia, tab_scanner = st.tabs(["🕸️ Radar e Tiro alla Fune", "🧠 Pronostici IA & Gol", "📊 Scanner Mercati"])
                
                with tab_radar:
                    categorie_radar = ['xG Fatti', 'Tiri Totali', 'Tiri in Porta', 'Corner', 'Gol Subiti (xGA)']
                    
                    if simula_reale:
                        v1_raw = [dati_sq1.get('xG Casa', 0), dati_sq1.get('Tiri totali Casa', 0), dati_sq1.get('Tiri in porta Casa', 0), dati_sq1.get('Corner Casa', 0), dati_sq1.get('xGA Casa', 0)]
                        v2_raw = [dati_sq2.get('xG Trasferta', 0), dati_sq2.get('Tiri totali Trasferta', 0), dati_sq2.get('Tiri in porta Trasferta', 0), dati_sq2.get('Corner Trasferta', 0), dati_sq2.get('xGA Trasferta', 0)]
                        nome_1 = f"{squadra_1} (Casa)"; nome_2 = f"{squadra_2} (Trasferta)"
                    else:
                        v1_raw = [dati_sq1.get('xG Casa',0)+dati_sq1.get('xG Trasferta',0), dati_sq1.get('Tiri totali Casa',0)+dati_sq1.get('Tiri totali Trasferta',0), dati_sq1.get('Tiri in porta Casa',0)+dati_sq1.get('Tiri in porta Trasferta',0), dati_sq1.get('Corner Casa',0)+dati_sq1.get('Corner Trasferta',0), dati_sq1.get('xGA Casa',0)+dati_sq1.get('xGA Trasferta',0)]
                        v2_raw = [dati_sq2.get('xG Casa',0)+dati_sq2.get('xG Trasferta',0), dati_sq2.get('Tiri totali Casa',0)+dati_sq2.get('Tiri totali Trasferta',0), dati_sq2.get('Tiri in porta Casa',0)+dati_sq2.get('Tiri in porta Trasferta',0), dati_sq2.get('Corner Casa',0)+dati_sq2.get('Corner Trasferta',0), dati_sq2.get('xGA Casa',0)+dati_sq2.get('xGA Trasferta',0)]
                        nome_1 = squadra_1; nome_2 = squadra_2

                    if 'Falli Commessi Casa' in dati_sq1 and 'Falli Commessi Trasferta' in dati_sq2:
                        categorie_radar.append('Falli Commessi')
                        if simula_reale:
                            v1_raw.append(dati_sq1.get('Falli Commessi Casa', 0))
                            v2_raw.append(dati_sq2.get('Falli Commessi Trasferta', 0))
                        else:
                            v1_raw.append(dati_sq1.get('Falli Commessi Casa', 0) + dati_sq1.get('Falli Commessi Trasferta', 0))
                            v2_raw.append(dati_sq2.get('Falli Commessi Casa', 0) + dati_sq2.get('Falli Commessi Trasferta', 0))

                    v1_norm, v2_norm = [], []
                    for i in range(len(categorie_radar)):
                        max_val = max(v1_raw[i], v2_raw[i])
                        if max_val == 0: max_val = 1
                        is_inverted = 'xGA' in categorie_radar[i] or 'Falli' in categorie_radar[i]
                        if is_inverted:
                            min_val = min(v1_raw[i], v2_raw[i])
                            v1_norm.append(100 if v1_raw[i] == min_val else (min_val/v1_raw[i]*100 if v1_raw[i]>0 else 0))
                            v2_norm.append(100 if v2_raw[i] == min_val else (min_val/v2_raw[i]*100 if v2_raw[i]>0 else 0))
                        else:
                            v1_norm.append((v1_raw[i]/max_val)*100)
                            v2_norm.append((v2_raw[i]/max_val)*100)
                            
                    v1_norm.append(v1_norm[0]); v2_norm.append(v2_norm[0]); categorie_radar.append(categorie_radar[0])
                    
                    fig_radar = go.Figure()
                    fig_radar.add_trace(go.Scatterpolar(r=v1_norm, theta=categorie_radar, fill='toself', name=nome_1, line_color='#00e676', line_width=3))
                    fig_radar.add_trace(go.Scatterpolar(r=v2_norm, theta=categorie_radar, fill='toself', name=nome_2, line_color='#ff4b4b', line_width=3))
                    fig_radar.update_layout(
                        template="plotly_dark",
                        polar=dict(
                            bgcolor='rgba(19, 23, 29, 0.7)',
                            radialaxis=dict(visible=False, range=[0, 100]),
                            angularaxis=dict(gridcolor='#222831', linecolor='#2b313a')
                        ),
                        showlegend=True,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        height=420,
                        margin=dict(t=30, b=30),
                        font=dict(family='Outfit', size=13, color='#e5e7eb')
                    )
                    st.plotly_chart(fig_radar, use_container_width=True)

                    st.markdown(f"### 🪢 Tiro alla Fune (Rapporto di Forza)")
                    colonne_numeriche = df_selezionato.select_dtypes(include=['number']).columns.tolist()
                    
                    if simula_reale:
                        lista_stats = [
                            ('🎯 xG', dati_sq1.get('xG Casa', 0), dati_sq2.get('xG Trasferta', 0)), 
                            ('🛡️ xGA Subiti', dati_sq1.get('xGA Casa', 0), dati_sq2.get('xGA Trasferta', 0)), 
                            ('👟 Tiri totali', dati_sq1.get('Tiri totali Casa', 0), dati_sq2.get('Tiri totali Trasferta', 0)), 
                            ('🥅 Tiri in porta', dati_sq1.get('Tiri in porta Casa', 0), dati_sq2.get('Tiri in porta Trasferta', 0)), 
                            ('🚩 Corner', dati_sq1.get('Corner Casa', 0), dati_sq2.get('Corner Trasferta', 0)),
                            ('🛑 Falli Commessi', dati_sq1.get('Falli Commessi Casa', 0), dati_sq2.get('Falli Commessi Trasferta', 0))
                        ]
                        if has_xgot_col and (dati_sq1.get('xGOT Casa', 0) > 0 or dati_sq2.get('xGOT Trasferta', 0) > 0):
                            lista_stats.insert(1, ('🔥 xGOT', dati_sq1.get('xGOT Casa', 0), dati_sq2.get('xGOT Trasferta', 0)))
                        if has_parate_col and (dati_sq1.get('Parate Casa', 0) > 0 or dati_sq2.get('Parate Trasferta', 0) > 0):
                            lista_stats.append(('🧤 Parate Portiere', dati_sq1.get('Parate Casa', 0), dati_sq2.get('Parate Trasferta', 0)))
                    else:
                        lista_stats = [(col, dati_sq1[col], dati_sq2[col]) for col in colonne_numeriche]
                    
                    html_content = '<div style="background: #13171d; border: 1px solid #222831; border-radius: 14px; padding: 28px; color: #e5e7eb;">'
                    for nome_stat, v1, v2 in lista_stats:
                        tot = v1 + v2
                        p1 = 50 if tot == 0 else (v1 / tot) * 100
                        p2 = 50 if tot == 0 else (v2 / tot) * 100
                        v1_str = formatta_numero(v1)
                        v2_str = formatta_numero(v2)
                        html_content += f"""
                        <div style="margin-bottom: 22px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; font-weight: 600; font-size: 0.95em; color: #e5e7eb; font-family: 'Outfit', sans-serif;">
                                <span style="color: #00e676; width: 30%; text-align: left; font-family: 'JetBrains Mono', monospace; font-size: 1.1em;">{v1_str}</span>
                                <span style="width: 40%; text-align: center; font-size: 0.92em; text-transform: uppercase; letter-spacing: 1px; color: #d1d5db;">{nome_stat}</span>
                                <span style="color: #ff4b4b; width: 30%; text-align: right; font-family: 'JetBrains Mono', monospace; font-size: 1.1em;">{v2_str}</span>
                            </div>
                            <div style="display: flex; width: 100%; height: 10px; border-radius: 5px; overflow: hidden; background: #0d1014; border: 1px solid #222831;">
                                <div style="width: {p1}%; background-color: #00e676; box-shadow: 0 0 10px rgba(0,230,118,0.45);"></div>
                                <div style="width: {p2}%; background-color: #ff4b4b; box-shadow: 0 0 10px rgba(255,75,75,0.45);"></div>
                            </div>
                        </div>
                        """
                    html_content += "</div>"
                    st.components.v1.html(html_content, height=480, scrolling=True)

                with tab_pronostici_ia:
                    mod_testo = "Dati Reali (Casa vs Trasferta)" if simula_reale else "Media Stagionale Globale"
                    st.markdown("### 🧠 Centrale Pronostici IA: 1X2, Multigol & Bussola Tattica")
                    st.markdown(f"<p style='color:#9ca3af; font-size:0.9em;'>Motore calibrato con <b>Poisson + xGOT + Parate Reali + Forma 5G + Game State + Cinismo + Coppe</b> (Modalità: <b>{mod_testo}</b>).</p>", unsafe_allow_html=True)

                    xg_stag_1 = (dati_sq1.get('xG Casa', 0) + dati_sq1.get('xG Trasferta', 0)) / 2.0
                    xg_stag_2 = (dati_sq2.get('xG Casa', 0) + dati_sq2.get('xG Trasferta', 0)) / 2.0

                    if simula_reale:
                        xg_att_1 = dati_sq1.get('xG Casa', 1.0)
                        xg_att_2 = dati_sq2.get('xG Trasferta', 1.0)
                        xga_def_1 = dati_sq1.get('xGA Casa', 1.0)
                        xga_def_2 = dati_sq2.get('xGA Trasferta', 1.0)
                        xgot_1 = float(dati_sq1.get('xGOT Casa', 0.0)) if has_xgot_col else 0.0
                        xgot_2 = float(dati_sq2.get('xGOT Trasferta', 0.0)) if has_xgot_col else 0.0
                        par_real_1 = float(dati_sq1.get('Parate Casa', 0.0)) if has_parate_col else 0.0
                        par_real_2 = float(dati_sq2.get('Parate Trasferta', 0.0)) if has_parate_col else 0.0
                        tp_1 = dati_sq1.get('Tiri in porta Casa', 4.0)
                        tp_2 = dati_sq2.get('Tiri in porta Trasferta', 3.5)
                        tt_1 = dati_sq1.get('Tiri totali Casa', 12.0)
                        tt_2 = dati_sq2.get('Tiri totali Trasferta', 10.0)
                        cor_1 = dati_sq1.get('Corner Casa', 5.0)
                        cor_2 = dati_sq2.get('Corner Trasferta', 4.0)
                        fal_1 = dati_sq1.get('Falli Commessi Casa', 12.0)
                        fal_2 = dati_sq2.get('Falli Commessi Trasferta', 12.0)
                        media_tp_1 = df_selezionato['Tiri in porta Casa'].mean() if 'Tiri in porta Casa' in df_selezionato.columns else 4.2
                        media_tp_2 = df_selezionato['Tiri in porta Trasferta'].mean() if 'Tiri in porta Trasferta' in df_selezionato.columns else 3.6
                        media_xga_1 = df_selezionato['xGA Casa'].mean() if 'xGA Casa' in df_selezionato.columns else 1.25
                        media_xga_2 = df_selezionato['xGA Trasferta'].mean() if 'xGA Trasferta' in df_selezionato.columns else 1.25
                    else:
                        xg_att_1 = xg_stag_1
                        xg_att_2 = xg_stag_2
                        xga_def_1 = (dati_sq1.get('xGA Casa',0)+dati_sq1.get('xGA Trasferta',0))/2.0
                        xga_def_2 = (dati_sq2.get('xGA Casa',0)+dati_sq2.get('xGA Trasferta',0))/2.0
                        xgot_1 = (float(dati_sq1.get('xGOT Casa',0)) + float(dati_sq1.get('xGOT Trasferta',0)))/2.0 if has_xgot_col else 0.0
                        xgot_2 = (float(dati_sq2.get('xGOT Casa',0)) + float(dati_sq2.get('xGOT Trasferta',0)))/2.0 if has_xgot_col else 0.0
                        par_real_1 = (float(dati_sq1.get('Parate Casa',0)) + float(dati_sq1.get('Parate Trasferta',0)))/2.0 if has_parate_col else 0.0
                        par_real_2 = (float(dati_sq2.get('Parate Casa',0)) + float(dati_sq2.get('Parate Trasferta',0)))/2.0 if has_parate_col else 0.0
                        tp_1 = (dati_sq1.get('Tiri in porta Casa', 0) + dati_sq1.get('Tiri in porta Trasferta', 0)) / 2.0
                        tp_2 = (dati_sq2.get('Tiri in porta Casa', 0) + dati_sq2.get('Tiri in porta Trasferta', 0)) / 2.0
                        tt_1 = (dati_sq1.get('Tiri totali Casa', 0) + dati_sq1.get('Tiri totali Trasferta', 0)) / 2.0
                        tt_2 = (dati_sq2.get('Tiri totali Casa', 0) + dati_sq2.get('Tiri totali Trasferta', 0)) / 2.0
                        cor_1 = (dati_sq1.get('Corner Casa', 0) + dati_sq1.get('Corner Trasferta', 0)) / 2.0
                        cor_2 = (dati_sq2.get('Corner Casa', 0) + dati_sq2.get('Corner Trasferta', 0)) / 2.0
                        fal_1 = (dati_sq1.get('Falli Commessi Casa', 0) + dati_sq1.get('Falli Commessi Trasferta', 0)) / 2.0
                        fal_2 = (dati_sq2.get('Falli Commessi Casa', 0) + dati_sq2.get('Falli Commessi Trasferta', 0)) / 2.0
                        media_tp_1 = 4.0
                        media_tp_2 = 4.0
                        media_xga_1 = 1.25
                        media_xga_2 = 1.25

                    dna_1 = analizza_dna_squadra(squadra_1, df_partite, xg_att_1, tt_1, xg_stag_1, xgot_1)
                    dna_2 = analizza_dna_squadra(squadra_2, df_partite, xg_att_2, tt_2, xg_stag_2, xgot_2)

                    l1, l2, p_1, p_x, p_2, risultati_esatti = calcola_poisson_match(
                        xg_att_1, xg_att_2, xga_def_1, xga_def_2, tp_1, tp_2, media_tp_1, media_tp_2,
                        dna_1, dna_2, coppe_casa, coppe_ospite, xgot_1, xgot_2
                    )
                    xg_totali_match = l1 + l2

                    mult_gs_1, label_gs_1 = calcola_game_state(p_1, p_2)
                    mult_gs_2, label_gs_2 = calcola_game_state(p_2, p_1)

                    p_1x = p_1 + p_x
                    p_x2 = p_x + p_2
                    qf_1 = 100 / p_1 if p_1 > 0 else 99.0
                    qf_x = 100 / p_x if p_x > 0 else 99.0
                    qf_2 = 100 / p_2 if p_2 > 0 else 99.0
                    qf_1x = 100 / p_1x if p_1x > 0 else 99.0
                    qf_x2 = 100 / p_x2 if p_x2 > 0 else 99.0
                    top_2_ris = f"{risultati_esatti[-1][0]} ({risultati_esatti[-1][1]:.1f}%)  |  {risultati_esatti[-2][0]} ({risultati_esatti[-2][1]:.1f}%)"

                    if p_1 >= 56:
                        esito_consigliato = f"1 FISSO ({squadra_1})"
                        prob_esito = p_1; qf_esito = qf_1; col_esito = "#00e676"
                    elif p_2 >= 56:
                        esito_consigliato = f"2 FISSO ({squadra_2})"
                        prob_esito = p_2; qf_esito = qf_2; col_esito = "#ff4b4b"
                    elif p_1 >= 44:
                        esito_consigliato = f"DOPPIA CHANCE 1X ({squadra_1} o Pareggio)"
                        prob_esito = p_1x; qf_esito = qf_1x; col_esito = "#00e676"
                    elif p_2 >= 44:
                        esito_consigliato = f"DOPPIA CHANCE X2 ({squadra_2} o Pareggio)"
                        prob_esito = p_x2; qf_esito = qf_x2; col_esito = "#ff4b4b"
                    else:
                        esito_consigliato = "GARA IN EQUILIBRIO (Meglio Mercati Gol / Statistiche)"
                        prob_esito = max(p_1x, p_x2)
                        qf_esito = 100 / prob_esito if prob_esito > 0 else 1.50
                        col_esito = "#ffb703"

                    st.markdown(f"""
                    <div class="glass-box" style="border-top: 4px solid {col_esito}; padding: 20px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                            <div>
                                <p style="margin:0; font-size:0.75em; color:#8b949e; text-transform:uppercase; letter-spacing:1px;">Esito Principale Consigliato dall'IA</p>
                                <h2 style="margin: 4px 0; color: {col_esito} !important; font-family: 'JetBrains Mono', monospace;">🏆 {esito_consigliato}</h2>
                                <p style="margin:0; font-size:0.85em; color:#d1d5db;">Probabilità Stimata: <b>{prob_esito:.1f}%</b> | Quota Fair: <b>{qf_esito:.2f}</b> &nbsp;•&nbsp; 🎯 Risultati più probabili: <b>{top_2_ris}</b></p>
                            </div>
                            <div style="display: flex; gap: 15px; margin-top: 10px;">
                                <div style="background: rgba(0,230,118,0.08); border: 1px solid rgba(0,230,118,0.3); padding: 8px 14px; border-radius: 10px; text-align: center;">
                                    <span style="font-size:0.75em; color:#9ca3af;">SEGNO 1</span><br>
                                    <b style="color:#00e676; font-family:'JetBrains Mono', monospace; font-size:1.15em;">{p_1:.1f}%</b><br>
                                    <span style="font-size:0.7em; color:#8b949e;">Fair: {qf_1:.2f}</span>
                                </div>
                                <div style="background: #161a20; border: 1px solid #2b313a; padding: 8px 14px; border-radius: 10px; text-align: center;">
                                    <span style="font-size:0.75em; color:#9ca3af;">SEGNO X</span><br>
                                    <b style="color:#fff; font-family:'JetBrains Mono', monospace; font-size:1.15em;">{p_x:.1f}%</b><br>
                                    <span style="font-size:0.7em; color:#8b949e;">Fair: {qf_x:.2f}</span>
                                </div>
                                <div style="background: rgba(255,75,75,0.08); border: 1px solid rgba(255,75,75,0.3); padding: 8px 14px; border-radius: 10px; text-align: center;">
                                    <span style="font-size:0.75em; color:#9ca3af;">SEGNO 2</span><br>
                                    <b style="color:#ff4b4b; font-family:'JetBrains Mono', monospace; font-size:1.15em;">{p_2:.1f}%</b><br>
                                    <span style="font-size:0.7em; color:#8b949e;">Fair: {qf_2:.2f}</span>
                                </div>
                            </div>
                        </div>
                        <div style="margin-top: 14px; display: flex; width: 100%; height: 10px; border-radius: 6px; overflow: hidden;">
                            <div style="width: {p_1}%; background: #00e676;" title="1: {p_1:.1f}%"></div>
                            <div style="width: {p_x}%; background: #6b7280;" title="X: {p_x:.1f}%"></div>
                            <div style="width: {p_2}%; background: #ff4b4b;" title="2: {p_2:.1f}%"></div>
                        </div>
                        <div style="display:flex; justify-content:space-between; font-size:0.78em; color:#9ca3af; margin-top:8px; font-family:'JetBrains Mono', monospace;">
                            <span>Doppia Chance 1X: <b style="color:#fff;">{p_1x:.1f}%</b> (Fair {qf_1x:.2f})</span>
                            <span>Gol Totali Attesi nel Match: <b style="color:#00e676;">{xg_totali_match:.2f} xG</b></span>
                            <span>Doppia Chance X2: <b style="color:#fff;">{p_x2:.1f}%</b> (Fair {qf_x2:.2f})</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # PANNELLO DNA TATTICO
                    st.markdown("#### 🔬 DNA Tattico & Correttori Attivi (Game State • Cinismo • Qualità Tiro / xGOT • Forma)")
                    col_dna1, col_dna2 = st.columns(2)
                    with col_dna1:
                        coppe_txt_1 = "<span style='color:#ffb703; font-weight:700;'>🇪🇺 Freno Coppe (-10%)</span>" if coppe_casa else "<span style='color:#8b949e;'>Riposata</span>"
                        lbl_q1 = f"xGOT ({xgot_1:.2f})" if dna_1['has_xgot'] else f"Qualità ({dna_1['xg_per_tiro']:.3f} xG/T)"
                        val_q1 = dna_1['stato_xgot'] if dna_1['has_xgot'] else dna_1['stato_tiro']
                        st.markdown(f"""
                        <div class="glass-box" style="border-left: 4px solid #00e676; padding: 14px 16px; margin-bottom: 16px;">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                                <b style="color:#00e676; font-size:0.95em;">🏠 {stemma_sq1}{squadra_1}</b>
                                <span style="font-size:0.75em; background:#0d1014; border:1px solid #222831; padding:2px 8px; border-radius:6px;">{dna_1['momentum_label']} • {coppe_txt_1}</span>
                            </div>
                            <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:8px; font-size:0.76em;">
                                <div style="background:#0d1014; border:1px solid #1e232a; padding:7px; border-radius:6px;">
                                    <span style="color:#8b949e; display:block;">Game State</span>
                                    <b style="color:#fff;">{label_gs_1}</b>
                                </div>
                                <div style="background:#0d1014; border:1px solid #1e232a; padding:7px; border-radius:6px;">
                                    <span style="color:#8b949e; display:block;">Cinismo (Gol/xG)</span>
                                    <b style="color:#fff;">{dna_1['stato_cinismo']}</b>
                                </div>
                                <div style="background:#0d1014; border:1px solid #1e232a; padding:7px; border-radius:6px;">
                                    <span style="color:#8b949e; display:block;">{lbl_q1}</span>
                                    <b style="color:#fff;">{val_q1}</b>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col_dna2:
                        coppe_txt_2 = "<span style='color:#ffb703; font-weight:700;'>🇪🇺 Freno Coppe (-10%)</span>" if coppe_ospite else "<span style='color:#8b949e;'>Riposata</span>"
                        lbl_q2 = f"xGOT ({xgot_2:.2f})" if dna_2['has_xgot'] else f"Qualità ({dna_2['xg_per_tiro']:.3f} xG/T)"
                        val_q2 = dna_2['stato_xgot'] if dna_2['has_xgot'] else dna_2['stato_tiro']
                        st.markdown(f"""
                        <div class="glass-box" style="border-left: 4px solid #ff4b4b; padding: 14px 16px; margin-bottom: 16px;">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                                <b style="color:#ff4b4b; font-size:0.95em;">✈️ {stemma_sq2}{squadra_2}</b>
                                <span style="font-size:0.75em; background:#0d1014; border:1px solid #222831; padding:2px 8px; border-radius:6px;">{dna_2['momentum_label']} • {coppe_txt_2}</span>
                            </div>
                            <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:8px; font-size:0.76em;">
                                <div style="background:#0d1014; border:1px solid #1e232a; padding:7px; border-radius:6px;">
                                    <span style="color:#8b949e; display:block;">Game State</span>
                                    <b style="color:#fff;">{label_gs_2}</b>
                                </div>
                                <div style="background:#0d1014; border:1px solid #1e232a; padding:7px; border-radius:6px;">
                                    <span style="color:#8b949e; display:block;">Cinismo (Gol/xG)</span>
                                    <b style="color:#fff;">{dna_2['stato_cinismo']}</b>
                                </div>
                                <div style="background:#0d1014; border:1px solid #1e232a; padding:7px; border-radius:6px;">
                                    <span style="color:#8b949e; display:block;">{lbl_q2}</span>
                                    <b style="color:#fff;">{val_q2}</b>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    def analizza_squadra_ia(lmbda, tiri_tot, dna_sq):
                        probs = {k: (math.exp(-lmbda) * (lmbda**k)) / math.factorial(k) for k in range(7)}
                        mg_1_2 = (probs[1] + probs[2]) * 100
                        mg_1_3 = (probs[1] + probs[2] + probs[3]) * 100
                        mg_2_3 = (probs[2] + probs[3]) * 100
                        mg_2_4 = (probs[2] + probs[3] + probs[4]) * 100
                        zero_gol = probs[0] * 100

                        if lmbda < 0.65:
                            consiglio = "Under 1.5 Squadra (0-1 Gol)"
                            prob_scelta = zero_gol + (probs[1] * 100)
                        elif lmbda < 1.35:
                            consiglio = "Multigol 1-2"
                            prob_scelta = mg_1_2
                        elif lmbda <= 2.15:
                            consiglio = "Multigol 1-3"
                            prob_scelta = mg_1_3
                        else:
                            consiglio = "Multigol 2-4"
                            prob_scelta = mg_2_4

                        quota_fair = 100 / prob_scelta if prob_scelta > 0 else 0

                        if "Iper-Cinica" in dna_sq['stato_cinismo'] or "Finalizz. Top" in dna_sq['stato_xgot'] or dna_sq['xg_per_tiro'] > 0.135:
                            bussola = "🎯 <b>PROFILO CINICO / PRECISO:</b> Calcia con alta qualità nello specchio. <b>Meglio Multigol / 1X2</b> rispetto a Corner o Parate Avversario."
                        elif "Sprecona" in dna_sq['stato_cinismo'] or "Tiri Parabili" in dna_sq['stato_xgot'] or dna_sq['xg_per_tiro'] < 0.095:
                            bussola = "🔥 <b>PROFILO D'ASSEDIO / PARABILE:</b> Alto volume ma tiri leggibili o imprecisi. Scenario <b>TOP per Over Tiri, Corner e Parate Avversario</b>."
                        else:
                            bussola = "⚖️ <b>PRODUZIONE BILANCIATA:</b> Equilibrio tra occasioni e volume di tiro. Valido sia il <b>Multigol</b> sia le <b>Statistiche</b>."

                        return consiglio, prob_scelta, quota_fair, mg_1_2, mg_1_3, mg_2_3, bussola

                    cons_1, prob_1, qf_1_mg, m12_1, m13_1, m23_1, buss_1 = analizza_squadra_ia(l1, tt_1, dna_1)
                    cons_2, prob_2, qf_2_mg, m12_2, m13_2, m23_2, buss_2 = analizza_squadra_ia(l2, tt_2, dna_2)

                    col_mg1, col_mg2 = st.columns(2)
                    
                    with col_mg1:
                        st.markdown(f"""
                        <div class="glass-box" style="border-left: 5px solid #00e676;">
                            <h4 style="margin:0; color:#00e676 !important;">🏠 {stemma_sq1}{squadra_1} (xG Calibrati: {l1:.2f})</h4>
                            <p style="margin: 8px 0 4px 0; font-size: 0.82em; color: #9ca3af;">Multigol Squadra Consigliato:</p>
                            <h2 style="margin:0; color:#fff !important; font-family:'JetBrains Mono', monospace;">⚽ {cons_1}</h2>
                            <p style="margin: 4px 0 12px 0; font-size: 0.85em; color: #00e676;">Probabilità: <b>{prob_1:.1f}%</b> | Quota Fair: <b>{qf_1_mg:.2f}</b></p>
                            <div style="background: #0d1014; border: 1px solid #1e232a; padding: 10px; border-radius: 8px; font-size: 0.8em; color: #d1d5db; margin-bottom: 12px;">
                                {buss_1}
                            </div>
                            <div style="display:flex; justify-content:space-between; font-size:0.8em; color:#9ca3af; font-family:'JetBrains Mono', monospace;">
                                <span>MG 1-2: <b style="color:#fff;">{m12_1:.1f}%</b></span>
                                <span>MG 1-3: <b style="color:#fff;">{m13_1:.1f}%</b></span>
                                <span>MG 2-3: <b style="color:#fff;">{m23_1:.1f}%</b></span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col_mg2:
                        st.markdown(f"""
                        <div class="glass-box" style="border-left: 5px solid #ff4b4b;">
                            <h4 style="margin:0; color:#ff4b4b !important;">✈️ {stemma_sq2}{squadra_2} (xG Calibrati: {l2:.2f})</h4>
                            <p style="margin: 8px 0 4px 0; font-size: 0.82em; color: #9ca3af;">Multigol Squadra Consigliato:</p>
                            <h2 style="margin:0; color:#fff !important; font-family:'JetBrains Mono', monospace;">⚽ {cons_2}</h2>
                            <p style="margin: 4px 0 12px 0; font-size: 0.85em; color: #ff4b4b;">Probabilità: <b>{prob_2:.1f}%</b> | Quota Fair: <b>{qf_2_mg:.2f}</b></p>
                            <div style="background: #0d1014; border: 1px solid #1e232a; padding: 10px; border-radius: 8px; font-size: 0.8em; color: #d1d5db; margin-bottom: 12px;">
                                {buss_2}
                            </div>
                            <div style="display:flex; justify-content:space-between; font-size:0.8em; color:#9ca3af; font-family:'JetBrains Mono', monospace;">
                                <span>MG 1-2: <b style="color:#fff;">{m12_2:.1f}%</b></span>
                                <span>MG 1-3: <b style="color:#fff;">{m13_2:.1f}%</b></span>
                                <span>MG 2-3: <b style="color:#fff;">{m23_2:.1f}%</b></span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown("#### 🌡️ Proiezione Reti Totali del Match")
                    if xg_totali_match < 2.2:
                        st.info(f"🧊 **TREND UNDER ({xg_totali_match:.2f} xG Totali):** Partita potenzialmente bloccata. Favorito il **Multigol 1-3 Totale** o **Under 2.5**.")
                    elif xg_totali_match > 2.8:
                        st.error(f"🔥 **TREND OVER ({xg_totali_match:.2f} xG Totali):** Le difese concedono e gli attacchi producono. Favorito **Over 2.5** o **Multigol 2-5 Totale**.")
                    else:
                        st.warning(f"⚖️ **RITMO MEDIO ({xg_totali_match:.2f} xG Totali):** Match equilibrato, ottimo per **Multigol 2-4 Totale**.")

                    # CALCOLO CENTRALIZZATO PROIEZIONI INCROCIATE + CORRETTORI TATTICI
                    m_coppe_1 = 0.90 if coppe_casa else 1.00
                    m_coppe_2 = 0.90 if coppe_ospite else 1.00

                    mult_tt_1 = max(0.80, min(1.15, mult_gs_1 * dna_1['mult_cin_stat'] * m_coppe_1))
                    mult_tt_2 = max(0.80, min(1.15, mult_gs_2 * dna_2['mult_cin_stat'] * m_coppe_2))

                    mult_tp_1 = max(0.82, min(1.12, mult_gs_1 * m_coppe_1))
                    mult_tp_2 = max(0.82, min(1.12, mult_gs_2 * m_coppe_2))

                    mult_cor_1 = max(0.80, min(1.16, mult_gs_1 * dna_1['mult_cin_stat'] * dna_1['mult_cor_tiro'] * m_coppe_1))
                    mult_cor_2 = max(0.80, min(1.16, mult_gs_2 * dna_2['mult_cin_stat'] * dna_2['mult_cor_tiro'] * m_coppe_2))

                    sub_tt_2, stato_tt_2 = stima_stat_subita(df_selezionato, dati_sq2, 'Trasferta', 'Tiri totali Casa', 'Tiri totali Trasferta')
                    sub_tt_1, stato_tt_1 = stima_stat_subita(df_selezionato, dati_sq1, 'Casa', 'Tiri totali Trasferta', 'Tiri totali Casa')
                    proj_tt_1 = ((tt_1 + sub_tt_2) / 2.0 if sub_tt_2 > 0 else tt_1) * mult_tt_1
                    proj_tt_2 = ((tt_2 + sub_tt_1) / 2.0 if sub_tt_1 > 0 else tt_2) * mult_tt_2

                    sub_tp_2, stato_tp_2 = stima_stat_subita(df_selezionato, dati_sq2, 'Trasferta', 'Tiri in porta Casa', 'Tiri in porta Trasferta')
                    sub_tp_1, stato_tp_1 = stima_stat_subita(df_selezionato, dati_sq1, 'Casa', 'Tiri in porta Trasferta', 'Tiri in porta Casa')
                    proj_tp_1 = ((tp_1 + sub_tp_2) / 2.0 if sub_tp_2 > 0 else tp_1) * mult_tp_1
                    proj_tp_2 = ((tp_2 + sub_tp_1) / 2.0 if sub_tp_1 > 0 else tp_2) * mult_tp_2

                    sub_cor_2, stato_cor_2 = stima_stat_subita(df_selezionato, dati_sq2, 'Trasferta', 'Corner Casa', 'Corner Trasferta')
                    sub_cor_1, stato_cor_1 = stima_stat_subita(df_selezionato, dati_sq1, 'Casa', 'Corner Trasferta', 'Corner Casa')
                    proj_cor_1 = ((cor_1 + sub_cor_2) / 2.0 if sub_cor_2 > 0 else cor_1) * mult_cor_1
                    proj_cor_2 = ((cor_2 + sub_cor_1) / 2.0 if sub_cor_1 > 0 else cor_2) * mult_cor_2

                    # 📏 LINEE STATISTICHE PREVISTE
                    st.markdown("<h4 style='margin-top: 30px;'>📏 Linee Statistiche Previste (Calibrate con Game State, Cinismo, Qualità Tiro & Coppe)</h4>", unsafe_allow_html=True)
                    st.markdown("<p style='color:#9ca3af; font-size:0.85em;'>Incrocia i dati prodotti dalla squadra con quelli concessi dall'avversario applicando tutti i correttori tattici e il cuscinetto sul Target Reale di Cassa.</p>", unsafe_allow_html=True)

                    def genera_riga_linea_html(icona, etichetta, media_fatti, subiti_avv, stato_dif, proj_reale, cuscinetto, mult_appl):
                        linea_txt, target_int, marg, col_badge = calcola_linea_statistica(proj_reale, cuscinetto, stato_dif)
                        extra_target = f"Servono <b>{target_int}</b> (+{marg:.2f})" if target_int > 0 else "Dati bassi"
                        delta_pct = (mult_appl - 1.0) * 100
                        tag_corr = f"<span style='color:{'#00e676' if delta_pct > 0.5 else ('#ffb703' if delta_pct < -0.5 else '#8b949e')};'>({delta_pct:+.0f}% IA)</span>" if abs(delta_pct) >= 1.0 else ""
                        return f"""
                        <div style="background: #0d1014; border: 1px solid #1e232a; border-radius: 10px; padding: 10px 12px; margin-bottom: 10px;">
                            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
                                <div>
                                    <span style="font-size:0.85em; font-weight:700; color:#fff;">{icona} {etichetta} {tag_corr}</span>
                                    <div style="font-size:0.74em; color:#9ca3af; margin-top:2px;">
                                        Media: <b style="color:#e5e7eb;">{media_fatti:.2f}</b> &nbsp;|&nbsp; Concessi Avv: <b style="color:#e5e7eb;">{subiti_avv:.2f}</b> <span style="font-size:0.95em;">({stato_dif})</span>
                                    </div>
                                </div>
                                <div style="text-align:right;">
                                    <span style="background: #161a20; border: 1px solid {col_badge}; color: {col_badge}; padding: 3px 9px; border-radius: 6px; font-family:'JetBrains Mono', monospace; font-weight:800; font-size:0.92em;">{linea_txt}</span>
                                    <div style="font-size:0.72em; color:#9ca3af; margin-top:3px; font-family:'JetBrains Mono', monospace;">
                                        Proiez: <b style="color:#fff;">{proj_reale:.2f}</b> • {extra_target}
                                    </div>
                                </div>
                            </div>
                        </div>
                        """

                    col_lin1, col_lin2 = st.columns(2)
                    with col_lin1:
                        r1_tt = genera_riga_linea_html("👟", "Tiri Totali", tt_1, sub_tt_2, stato_tt_2, proj_tt_1, 1.1, mult_tt_1)
                        r1_tp = genera_riga_linea_html("🥅", "Tiri in Porta", tp_1, sub_tp_2, stato_tp_2, proj_tp_1, 0.6, mult_tp_1)
                        r1_cor = genera_riga_linea_html("🚩", "Corner", cor_1, sub_cor_2, stato_cor_2, proj_cor_1, 0.7, mult_cor_1)
                        st.markdown(f"""
                        <div class="glass-box" style="border-top: 3px solid #00e676; padding: 16px; margin-bottom: 14px;">
                            <h4 style="margin:0 0 12px 0; color:#00e676 !important;">🏠 Linee {stemma_sq1}{squadra_1} <span style="font-size:0.72em; color:#8b949e; font-weight:400;">vs difesa {squadra_2}</span></h4>
                            {r1_tt}
                            {r1_tp}
                            {r1_cor}
                        </div>
                        """, unsafe_allow_html=True)

                    with col_lin2:
                        r2_tt = genera_riga_linea_html("👟", "Tiri Totali", tt_2, sub_tt_1, stato_tt_1, proj_tt_2, 1.1, mult_tt_2)
                        r2_tp = genera_riga_linea_html("🥅", "Tiri in Porta", tp_2, sub_tp_1, stato_tp_1, proj_tp_2, 0.6, mult_tp_2)
                        r2_cor = genera_riga_linea_html("🚩", "Corner", cor_2, sub_cor_1, stato_cor_1, proj_cor_2, 0.7, mult_cor_2)
                        st.markdown(f"""
                        <div class="glass-box" style="border-top: 3px solid #ff4b4b; padding: 16px; margin-bottom: 14px;">
                            <h4 style="margin:0 0 12px 0; color:#ff4b4b !important;">✈️ Linee {stemma_sq2}{squadra_2} <span style="font-size:0.72em; color:#8b949e; font-weight:400;">vs difesa {squadra_1}</span></h4>
                            {r2_tt}
                            {r2_tp}
                            {r2_cor}
                        </div>
                        """, unsafe_allow_html=True)

                    proj_tot_tt = proj_tt_1 + proj_tt_2
                    proj_tot_tp = proj_tp_1 + proj_tp_2
                    proj_tot_cor = proj_cor_1 + proj_cor_2

                    stato_tot_tt = "🔴 Difese Chiuse" if ("Solida" in stato_tt_1 and "Solida" in stato_tt_2) else ("🟢 Difese Permessive" if ("Concede" in stato_tt_1 and "Concede" in stato_tt_2) else "⚪ Difese Medie")
                    stato_tot_tp = "🔴 Difese Chiuse" if ("Solida" in stato_tp_1 and "Solida" in stato_tp_2) else ("🟢 Difese Permessive" if ("Concede" in stato_tp_1 and "Concede" in stato_tp_2) else "⚪ Difese Medie")
                    stato_tot_cor = "🔴 Difese Chiuse" if ("Solida" in stato_cor_1 and "Solida" in stato_cor_2) else ("🟢 Difese Permessive" if ("Concede" in stato_cor_1 and "Concede" in stato_cor_2) else "⚪ Difese Medie")

                    lt_tt, tgt_tt, m_tt, col_l_tt = calcola_linea_statistica(proj_tot_tt, 1.6, stato_tot_tt)
                    lt_tp, tgt_tp, m_tp, col_l_tp = calcola_linea_statistica(proj_tot_tp, 0.9, stato_tot_tp)
                    lt_cor, tgt_cor, m_cor, col_l_cor = calcola_linea_statistica(proj_tot_cor, 1.0, stato_tot_cor)

                    st.markdown(f"""
                    <div class="glass-box" style="padding: 16px; border: 1px solid #262e39;">
                        <p style="margin:0 0 10px 0; font-size:0.78em; color:#9ca3af; text-transform:uppercase; letter-spacing:1px;">🌐 Proiezione Linee Totali Match (Casa + Ospite)</p>
                        <div style="display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap;">
                            <div style="flex:1; min-width:180px; background:#0d1014; border:1px solid #1e232a; padding:10px 14px; border-radius:10px; border-left:3px solid {col_l_tt};">
                                <span style="font-size:0.8em; color:#9ca3af;">👟 TIRI TOTALI MATCH</span><br>
                                <b style="font-size:1.15em; color:{col_l_tt}; font-family:'JetBrains Mono', monospace;">{lt_tt}</b>
                                <span style="font-size:0.78em; color:#d1d5db; display:block; margin-top:2px;">Proiezione: <b>{proj_tot_tt:.2f}</b> (Servono {tgt_tt})</span>
                            </div>
                            <div style="flex:1; min-width:180px; background:#0d1014; border:1px solid #1e232a; padding:10px 14px; border-radius:10px; border-left:3px solid {col_l_tp};">
                                <span style="font-size:0.8em; color:#9ca3af;">🥅 TIRI IN PORTA MATCH</span><br>
                                <b style="font-size:1.15em; color:{col_l_tp}; font-family:'JetBrains Mono', monospace;">{lt_tp}</b>
                                <span style="font-size:0.78em; color:#d1d5db; display:block; margin-top:2px;">Proiezione: <b>{proj_tot_tp:.2f}</b> (Servono {tgt_tp})</span>
                            </div>
                            <div style="flex:1; min-width:180px; background:#0d1014; border:1px solid #1e232a; padding:10px 14px; border-radius:10px; border-left:3px solid {col_l_cor};">
                                <span style="font-size:0.8em; color:#9ca3af;">🚩 CORNER TOTALI MATCH</span><br>
                                <b style="font-size:1.15em; color:{col_l_cor}; font-family:'JetBrains Mono', monospace;">{lt_cor}</b>
                                <span style="font-size:0.78em; color:#d1d5db; display:block; margin-top:2px;">Proiezione: <b>{proj_tot_cor:.2f}</b> (Servono {tgt_cor})</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                        
                    # 🧤 FOCUS PORTIERI POTENZIATO CON PARATE REALI + xGOT
                    st.markdown("<h4 style='margin-top: 30px;'>🧤 Focus Portieri & Linea Parate (Parate Reali + xGOT Avversario)</h4>", unsafe_allow_html=True)
                    st.markdown("<p style='color:#9ca3af; font-size:0.85em;'>In Serie A incrocia la media parate reale del portiere con i tiri in porta e l'xGOT dell'avversario per ricavare una linea Over Parate affidabile.</p>", unsafe_allow_html=True)
                    
                    parate_attese_1, tiri_subiti_1, fonte_gk_1 = calcola_parate_portiere(par_real_1, proj_tp_2, xga_def_1, media_xga_1, dna_2)
                    parate_attese_2, tiri_subiti_2, fonte_gk_2 = calcola_parate_portiere(par_real_2, proj_tp_1, xga_def_2, media_xga_2, dna_1)
                    
                    def genera_card_portiere(squadra, stemma_html, parate, par_reali, tiri_subiti, ruolo, fonte_txt):
                        linea_gk, tgt_gk, marg_gk, _ = calcola_linea_statistica(parate, 0.45, "")
                        if parate >= 3.6:
                            col_badge = "#00e676"
                            alert = f"🔥 ALTO ASSEDIO: Consigliato {linea_gk} Parate"
                        elif parate <= 2.2:
                            col_badge = "#ff4b4b"
                            alert = "🧊 BASSO ASSEDIO: Rischio Under Parate"
                        else:
                            col_badge = "#ffb703"
                            alert = f"⚖️ ASSEDIO MEDIO: Linea stimata {linea_gk}"
                        info_reali = f"Media Reale: <b>{par_reali:.2f}</b> • " if par_reali > 0 else ""
                        return f"""
                        <div class="glass-box" style="border-left: 4px solid {col_badge}; padding: 15px; margin-bottom: 0;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <p style="margin: 0; font-size: 0.8em; color: #9ca3af; text-transform: uppercase;">{stemma_html}Portiere {squadra} ({ruolo})</p>
                                <span style="font-size:0.68em; background:#161a20; border:1px solid #2b313a; color:#d1d5db; padding:2px 7px; border-radius:4px;">{fonte_txt}</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:baseline; margin: 6px 0;">
                                <h3 style="margin: 0; color: #fff !important; font-family: 'JetBrains Mono', monospace;">{parate:.2f} Parate Attese</h3>
                                <span style="border: 1px solid {col_badge}; color: {col_badge}; background:#0d1014; padding: 2px 8px; border-radius: 6px; font-family:'JetBrains Mono', monospace; font-size:0.85em; font-weight:800;">{linea_gk}</span>
                            </div>
                            <p style="margin: 0; font-size: 0.82em; color: #d1d5db;">{info_reali}Tiri in porta subiti stimati: <b>{tiri_subiti:.1f}</b></p>
                            <div style="margin-top: 10px; background: #0d1014; border: 1px solid #1e232a; padding: 6px 10px; border-radius: 6px;">
                                <span style="font-size: 0.8em; color: {col_badge}; font-weight: 700;">{alert}</span>
                            </div>
                        </div>
                        """

                    col_gk1, col_gk2 = st.columns(2)
                    with col_gk1:
                        st.markdown(genera_card_portiere(squadra_1, stemma_sq1, parate_attese_1, par_real_1, tiri_subiti_1, "Casa", fonte_gk_1), unsafe_allow_html=True)
                    with col_gk2:
                        st.markdown(genera_card_portiere(squadra_2, stemma_sq2, parate_attese_2, par_real_2, tiri_subiti_2, "Trasferta", fonte_gk_2), unsafe_allow_html=True)

                    st.markdown("<h4 style='margin-top: 30px;'>🥊 Verdetto IA: Testa a Testa (1X2) Tiri, Corner & Falli</h4>", unsafe_allow_html=True)
                    st.markdown("<p style='color:#9ca3af; font-size:0.85em;'>Simulazione dei 4 duelli statistici diretti calibrata con Game State, Qualità Tiro, Cinismo e Affaticamento Coppe.</p>", unsafe_allow_html=True)

                    diff_tt = proj_tt_1 - proj_tt_2
                    if diff_tt >= 3.5:
                        verd_tt = f"1 TIRI TOTALI ({squadra_1})"
                        col_tt = "#00e676"
                        cons_tt = f"Dominio volume (<b>+{diff_tt:.2f} tiri</b>). Ottimo <b>1 Tiri</b> o <b>Handicap -2.5</b>."
                    elif diff_tt <= -3.5:
                        verd_tt = f"2 TIRI TOTALI ({squadra_2})"
                        col_tt = "#ff4b4b"
                        cons_tt = f"Dominio volume (<b>{diff_tt:.2f} tiri</b>). Ottimo <b>2 Tiri</b> o <b>Handicap -2.5 Ospite</b>."
                    elif diff_tt >= 1.5:
                        verd_tt = f"1 Tiri Totali ({squadra_1})"
                        col_tt = "#00e676"
                        cons_tt = f"Buon margine (<b>+{diff_tt:.2f} tiri</b>). Consigliato <b>1 Tiri</b> secco senza handicap."
                    elif diff_tt <= -1.5:
                        verd_tt = f"2 Tiri Totali ({squadra_2})"
                        col_tt = "#ff4b4b"
                        cons_tt = f"Buon margine (<b>{diff_tt:.2f} tiri</b>). Consigliato <b>2 Tiri</b> secco senza handicap."
                    else:
                        verd_tt = "NO BET / EQUILIBRIO TIRI"
                        col_tt = "#ffb703"
                        cons_tt = f"Scarto ridotto (<b>{diff_tt:+.2f} tiri</b>). Meglio puntare sulla linea Over Tiri."

                    diff_tp = proj_tp_1 - proj_tp_2
                    if diff_tp >= 1.5:
                        verd_tp = f"1 TIRI IN PORTA ({squadra_1})"
                        col_tp = "#00e676"
                        cons_tp = f"Netta superiorità (<b>+{diff_tp:.2f} nello specchio</b>). Ottimo <b>1 Tiri Porta</b> o <b>H -1.5</b>."
                    elif diff_tp <= -1.5:
                        verd_tp = f"2 TIRI IN PORTA ({squadra_2})"
                        col_tp = "#ff4b4b"
                        cons_tp = f"Netta superiorità (<b>{diff_tp:.2f} nello specchio</b>). Ottimo <b>2 Tiri Porta</b> o <b>H -1.5</b>."
                    elif diff_tp >= 0.65:
                        verd_tp = f"1 Tiri in Porta ({squadra_1})"
                        col_tp = "#00e676"
                        cons_tp = f"Vantaggio precisione (<b>+{diff_tp:.2f}</b>). Valido <b>1 Tiri in Porta</b> in singola."
                    elif diff_tp <= -0.65:
                        verd_tp = f"2 Tiri in Porta ({squadra_2})"
                        col_tp = "#ff4b4b"
                        cons_tp = f"Vantaggio precisione (<b>{diff_tp:.2f}</b>). Valido <b>2 Tiri in Porta</b> in singola."
                    else:
                        verd_tp = "EQUILIBRIO TIRI IN PORTA"
                        col_tp = "#ffb703"
                        cons_tp = f"Scarto minimo nello specchio (<b>{diff_tp:+.2f}</b>). Duello da tripla."

                    diff_cor = proj_cor_1 - proj_cor_2
                    if diff_cor >= 1.6:
                        verd_cor = f"1 CORNER ({squadra_1})"
                        col_cor = "#00e676"
                        cons_cor = f"Margine netto (<b>+{diff_cor:.2f}</b>). Ottimo <b>1 Corner</b> o <b>Handicap -1.5</b>."
                    elif diff_cor <= -1.6:
                        verd_cor = f"2 CORNER ({squadra_2})"
                        col_cor = "#ff4b4b"
                        cons_cor = f"Margine netto (<b>{diff_cor:.2f}</b>). Ottimo <b>2 Corner</b> o <b>Handicap -1.5 Ospite</b>."
                    elif diff_cor >= 0.65:
                        verd_cor = f"1 Corner Leggero ({squadra_1})"
                        col_cor = "#00e676"
                        cons_cor = f"Vantaggio moderato (<b>+{diff_cor:.2f}</b>). Evita handicap alti, meglio linea Over."
                    elif diff_cor <= -0.65:
                        verd_cor = f"2 Corner Leggero ({squadra_2})"
                        col_cor = "#ff4b4b"
                        cons_cor = f"Vantaggio moderato (<b>{diff_cor:.2f}</b>). Valido in singola secca senza handicap."
                    else:
                        verd_cor = "NO BET / EQUILIBRIO CORNER"
                        col_cor = "#ffb703"
                        cons_cor = f"Scarto minimo (<b>{diff_cor:+.2f}</b>). Il Game State può ribaltare il testa a testa."

                    indice_pressione_1 = (l1 / (l1 + l2)) * 0.5 + (tt_1 / (tt_1 + tt_2 if (tt_1+tt_2)>0 else 1)) * 0.5
                    indice_pressione_2 = 1.0 - indice_pressione_1

                    molt_tattico_fal_1 = (1.0 + ((indice_pressione_2 - 0.50) * 0.35) if indice_pressione_2 > 0.52 else 1.0) * (1.05 if coppe_casa else 1.0)
                    molt_tattico_fal_2 = (1.0 + ((indice_pressione_1 - 0.50) * 0.35) if indice_pressione_1 > 0.52 else 1.0) * (1.05 if coppe_ospite else 1.0)

                    proj_fal_1 = fal_1 * molt_tattico_fal_1
                    proj_fal_2 = fal_2 * molt_tattico_fal_2
                    diff_fal = proj_fal_1 - proj_fal_2

                    if diff_fal >= 1.5:
                        verd_fal = f"PIÙ FALLI: {squadra_1} (Segno 1)"
                        col_fal = "#00e676"
                        cons_fal = f"Scarto stimato: <b>+{diff_fal:.2f} falli</b>. {squadra_1} più fallosa e costretta a spezzare il gioco."
                    elif diff_fal <= -1.5:
                        verd_fal = f"PIÙ FALLI: {squadra_2} (Segno 2)"
                        col_fal = "#ff4b4b"
                        cons_fal = f"Scarto stimato: <b>{abs(diff_fal):.2f} falli</b> in più per {squadra_2} (pressione difensiva alta)."
                    elif diff_fal >= 0.65:
                        verd_fal = f"Leggera Tendenza Falli: {squadra_1}"
                        col_fal = "#00e676"
                        cons_fal = f"Vantaggio contenuto (<b>+{diff_fal:.2f} falli</b>). Giocabile solo a quota >= 1.85."
                    elif diff_fal <= -0.65:
                        verd_fal = f"Leggera Tendenza Falli: {squadra_2}"
                        col_fal = "#ff4b4b"
                        cons_fal = f"Vantaggio contenuto (<b>+{abs(diff_fal):.2f} falli</b>). Giocabile solo a quota >= 1.85."
                    else:
                        verd_fal = "EQUILIBRIO FALLI (Rischio X)"
                        col_fal = "#ffb703"
                        cons_fal = f"Scarto irrisorio (<b>{diff_fal:+.2f}</b>). Meglio puntare sull'Over Falli Totale Match."

                    col_h2h_tt, col_h2h_tp = st.columns(2)
                    with col_h2h_tt:
                        st.markdown(f"""
                        <div class="glass-box" style="border-left: 4px solid {col_tt}; padding: 16px;">
                            <p style="margin: 0; font-size: 0.78em; color: #9ca3af; text-transform: uppercase;">👟 Testa a Testa Tiri Totali (1X2)</p>
                            <h3 style="margin: 6px 0; color: {col_tt} !important; font-family: 'JetBrains Mono', monospace;">{verd_tt}</h3>
                            <p style="margin: 0; font-size: 0.85em; color: #d1d5db;">Proiezione: {stemma_sq1}<b>{squadra_1} ({proj_tt_1:.2f})</b> vs {stemma_sq2}<b>{squadra_2} ({proj_tt_2:.2f})</b></p>
                            <div style="margin-top: 10px; background: #0d1014; border: 1px solid #1e232a; padding: 8px 10px; border-radius: 6px; font-size: 0.8em; color: #d1d5db;">
                                💡 {cons_tt}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col_h2h_tp:
                        st.markdown(f"""
                        <div class="glass-box" style="border-left: 4px solid {col_tp}; padding: 16px;">
                            <p style="margin: 0; font-size: 0.78em; color: #9ca3af; text-transform: uppercase;">🥅 Testa a Testa Tiri in Porta (1X2)</p>
                            <h3 style="margin: 6px 0; color: {col_tp} !important; font-family: 'JetBrains Mono', monospace;">{verd_tp}</h3>
                            <p style="margin: 0; font-size: 0.85em; color: #d1d5db;">Proiezione: {stemma_sq1}<b>{squadra_1} ({proj_tp_1:.2f})</b> vs {stemma_sq2}<b>{squadra_2} ({proj_tp_2:.2f})</b></p>
                            <div style="margin-top: 10px; background: #0d1014; border: 1px solid #1e232a; padding: 8px 10px; border-radius: 6px; font-size: 0.8em; color: #d1d5db;">
                                💡 {cons_tp}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    col_h2h_1, col_h2h_2 = st.columns(2)
                    with col_h2h_1:
                        st.markdown(f"""
                        <div class="glass-box" style="border-left: 4px solid {col_cor}; padding: 16px;">
                            <p style="margin: 0; font-size: 0.78em; color: #9ca3af; text-transform: uppercase;">🚩 Testa a Testa Corner (1X2)</p>
                            <h3 style="margin: 6px 0; color: {col_cor} !important; font-family: 'JetBrains Mono', monospace;">{verd_cor}</h3>
                            <p style="margin: 0; font-size: 0.85em; color: #d1d5db;">Proiezione: {stemma_sq1}<b>{squadra_1} ({proj_cor_1:.2f})</b> vs {stemma_sq2}<b>{squadra_2} ({proj_cor_2:.2f})</b></p>
                            <div style="margin-top: 10px; background: #0d1014; border: 1px solid #1e232a; padding: 8px 10px; border-radius: 6px; font-size: 0.8em; color: #d1d5db;">
                                💡 {cons_cor}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col_h2h_2:
                        st.markdown(f"""
                        <div class="glass-box" style="border-left: 4px solid {col_fal}; padding: 16px;">
                            <p style="margin: 0; font-size: 0.78em; color: #9ca3af; text-transform: uppercase;">🛑 Testa a Testa Falli Commessi (1X2)</p>
                            <h3 style="margin: 6px 0; color: {col_fal} !important; font-family: 'JetBrains Mono', monospace;">{verd_fal}</h3>
                            <p style="margin: 0; font-size: 0.85em; color: #d1d5db;">Proiezione Tattica: {stemma_sq1}<b>{squadra_1} ({proj_fal_1:.2f})</b> vs {stemma_sq2}<b>{squadra_2} ({proj_fal_2:.2f})</b></p>
                            <div style="margin-top: 10px; background: #0d1014; border: 1px solid #1e232a; padding: 8px 10px; border-radius: 6px; font-size: 0.8em; color: #d1d5db;">
                                💡 {cons_fal}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                with tab_scanner:
                    st.markdown("### 📊 Scanner Mercati & Value Bet (Target Singole 1.70 - 2.10)")
                    st.markdown("<p style='color:#9ca3af;'>Analisi delle linee principali con soglie ricalibrate per le singole pure.</p>", unsafe_allow_html=True)
                    
                    tipo_filtro = st.radio("Filtro Storico Partite:", ["🌍 Globale (Tutte le partite della squadra)", "🏠/✈️ Specifico (Solo partite giocate in Casa / Trasferta)"], horizontal=True)
                    modalita_scanner = "specifico" if "Specifico" in tipo_filtro else "globale"
                    
                    st.divider()
                    
                    tot_1, over_1, goal_1 = calcola_mercati_betting(squadra_1, df_partite, modalita=modalita_scanner, ruolo="casa")
                    tot_2, over_2, goal_2 = calcola_mercati_betting(squadra_2, df_partite, modalita=modalita_scanner, ruolo="trasferta")
                    
                    col_sc1, col_sc2 = st.columns(2)
                    with col_sc1:
                        titolo_sq1 = f"{squadra_1} (In Casa)" if modalita_scanner == "specifico" else squadra_1
                        st.markdown(f"<h3 style='text-align: center; color: #00e676 !important;'>{stemma_sq1}{titolo_sq1}</h3>", unsafe_allow_html=True)
                        if tot_1 > 0:
                            st.markdown(genera_html_scanner(over_1, goal_1, tot_1, "#00e676"), unsafe_allow_html=True)
                        else:
                            st.info(f"Nessun dato storico per {titolo_sq1}.")
                            
                    with col_sc2:
                        titolo_sq2 = f"{squadra_2} (In Trasferta)" if modalita_scanner == "specifico" else squadra_2
                        st.markdown(f"<h3 style='text-align: center; color: #ff4b4b !important;'>{stemma_sq2}{titolo_sq2}</h3>", unsafe_allow_html=True)
                        if tot_2 > 0:
                            st.markdown(genera_html_scanner(over_2, goal_2, tot_2, "#ff4b4b"), unsafe_allow_html=True)
                        else:
                            st.info(f"Nessun dato storico per {titolo_sq2}.")

            else:
                if squadra_scelta == "Tutte le squadre":
                    tab_graf, tab_auto = st.tabs(["📊 Grafici Analitici", "🌍 Scanner Universale Scommesse"])

                    with tab_graf:
                        colonne_numeriche = df_selezionato.select_dtypes(include=['number']).columns.tolist()
                        statistica_scelta = st.selectbox("Seleziona la metrica da visualizzare:", colonne_numeriche)
                        scala_emerald_obsidian = [
                            [0.0, "#164e3f"],
                            [0.5, "#00a859"],
                            [1.0, "#00e676"]
                        ]
                        fig_dinamico = px.bar(
                            df_selezionato.sort_values(by=statistica_scelta, ascending=False),
                            x="Squadra",
                            y=statistica_scelta,
                            title=f"Classifica per: {statistica_scelta}",
                            color=statistica_scelta,
                            color_continuous_scale=scala_emerald_obsidian,
                            text_auto='.2f',
                            template="plotly_dark"
                        )
                        fig_dinamico.update_traces(
                            textfont=dict(size=12, color="#e5e7eb", family="JetBrains Mono"),
                            textangle=0,
                            textposition="outside",
                            cliponaxis=False,
                            marker_line_width=0
                        )
                        fig_dinamico.update_layout(
                            coloraxis_showscale=False,
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(family='Outfit', color='#e5e7eb'),
                            yaxis=dict(gridcolor='#1d2229', zerolinecolor='#2b313a'),
                            xaxis=dict(showgrid=False, linecolor='#2b313a')
                        )
                        st.plotly_chart(fig_dinamico, use_container_width=True)
                        
                    with tab_auto:
                        f_it = ottieni_bandiera_html('Serie A', 22)
                        f_en = ottieni_bandiera_html('Premier League', 22)
                        f_es = ottieni_bandiera_html('La Liga', 22)
                        st.markdown(f"### 🌍 Scanner Universale Value Bet ({f_it}Serie A &nbsp;•&nbsp; {f_en}Premier League &nbsp;•&nbsp; {f_es}La Liga)", unsafe_allow_html=True)
                        st.markdown("<p style='color:#9ca3af;'>Motore <b>Salva-Cassa Pro</b> attivo: integra <b>xGOT, Parate Reali (Serie A), Game State, Cinismo, Qualità Tiro, Forma 5G e Coppe</b>.</p>", unsafe_allow_html=True)
                        
                        col_sl1, col_sl2 = st.columns([1, 1])
                        with col_sl1:
                            filtro_eff = st.slider("🎯 Filtro Efficienza Minima (%)", min_value=0, max_value=40, value=5, step=1)
                        with col_sl2:
                            filtro_lega_scanner = st.selectbox("🏆 Filtra Risultati per Campionato:", ["🌍 Tutti i Campionati", "🇮🇹 Serie A", "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League", "🇪🇸 La Liga"])
                        
                        df_palinsesto = dati_campionati.get('Palinsesto', pd.DataFrame())
                        
                        squadre_palinsesto = []
                        if df_palinsesto is not None and not df_palinsesto.empty:
                            sc_c = df_palinsesto['Squadra Casa'].dropna().astype(str).str.strip().tolist() if 'Squadra Casa' in df_palinsesto.columns else []
                            sc_t = df_palinsesto['Squadra Trasferta'].dropna().astype(str).str.strip().tolist() if 'Squadra Trasferta' in df_palinsesto.columns else []
                            squadre_palinsesto = sorted(list(set([s for s in sc_c + sc_t if s and s != '0'])))
                        
                        squadre_coppe_scanner = st.multiselect(
                            "🇪🇺 Squadre reduci da Coppe Europee in settimana (applica freno automatico -10% su xG/Tiri/Corner):",
                            options=squadre_palinsesto,
                            default=[]
                        )

                        col_chk1, col_chk2 = st.columns(2)
                        with col_chk1:
                            solo_prima_scelta = st.checkbox("👑 Mostra SOLO la Giocata più sicura per ogni Partita (Evita indecisioni)", value=True)
                        with col_chk2:
                            nascondi_muri = st.checkbox("🛡️ Nascondi giocate contro 'Difese Muro / Chiuse' (Salva-Cassa)", value=False)

                        st.divider()
                        
                        if df_palinsesto is None or df_palinsesto.empty:
                            st.warning("⚠️ **Foglio 'Palinsesto' non trovato o vuoto.**")
                            testo_istruzioni = (
                                "Assicurati che il foglio si chiami **`Palinsesto`** e usi queste colonne:\n"
                                "`Squadra Casa` | `Squadra Trasferta` | `Quota 1` | `Quota 2` | `Quota GG` | `Linea Over Tiri` | `Quota Over Tiri` | "
                                "`Linea Over Tiri Porta` | `Quota Over Tiri Porta` | `Linea Over Corner` | `Quota Over Corner` | "
                                "`Linea Over Falli` | `Quota Over Falli`\n\n"
                                "COLONNE SQUADRA SINGOLA (Tiri, Corner e opzionale Parate):\n"
                                "`Linea Tiri Casa` | `Quota Tiri Casa` | `Linea Tiri Trasferta` | `Quota Tiri Trasferta` | "
                                "`Linea Corner Casa` | `Quota Corner Casa` | `Linea Corner Trasferta` | `Quota Corner Trasferta` | "
                                "`Linea Parate Casa` | `Quota Parate Casa` | `Linea Parate Trasferta` | `Quota Parate Trasferta`"
                            )
                            st.info(testo_istruzioni)
                        else:
                            risultati_value = []
                            mappa_icone_leghe = {
                                'Serie A': '🇮🇹 Serie A',
                                'Premier League': '🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League',
                                'La Liga': '🇪🇸 La Liga'
                            }

                            for _, row in df_palinsesto.iterrows():
                                casa = str(row.get('Squadra Casa', '')).strip()
                                trasf = str(row.get('Squadra Trasferta', '')).strip()
                                if not casa or not trasf or casa == '0' or trasf == '0':
                                    continue

                                df_lega_match = None
                                nome_lega_match = None
                                lega_pura = None
                                for lega_nome in ['Serie A', 'La Liga', 'Premier League']:
                                    df_temp = dati_campionati.get(lega_nome, pd.DataFrame())
                                    if not df_temp.empty and 'Squadra' in df_temp.columns:
                                        if casa in df_temp['Squadra'].values and trasf in df_temp['Squadra'].values:
                                            df_lega_match = df_temp
                                            nome_lega_match = mappa_icone_leghe.get(lega_nome, lega_nome)
                                            lega_pura = lega_nome
                                            break

                                if df_lega_match is None:
                                    continue

                                dati_c = df_lega_match[df_lega_match['Squadra'] == casa].iloc[0]
                                dati_t = df_lega_match[df_lega_match['Squadra'] == trasf].iloc[0]
                                match_name = f"{casa} - {trasf}"
                                
                                is_coppe_c = casa in squadre_coppe_scanner
                                is_coppe_t = trasf in squadre_coppe_scanner
                                tag_ec_c = " <span style='font-size:0.7em; color:#ffb703;'>[🇪🇺]</span>" if is_coppe_c else ""
                                tag_ec_t = " <span style='font-size:0.7em; color:#ffb703;'>[🇪🇺]</span>" if is_coppe_t else ""

                                stemma_c_card = ottieni_stemma_html(casa, lega_pura, size=22)
                                stemma_t_card = ottieni_stemma_html(trasf, lega_pura, size=22)
                                match_html_card = f"{stemma_c_card}{casa}{tag_ec_c} <span style='color:#6b7280; font-weight:400;'>vs</span> {stemma_t_card}{trasf}{tag_ec_t}"
                                flag_card_html = f"{ottieni_bandiera_html(lega_pura, 16)}{lega_pura}"

                                xg_c_att = dati_c.get('xG Casa', 1.0)
                                xg_t_att = dati_t.get('xG Trasferta', 1.0)
                                xga_c_def = dati_c.get('xGA Casa', 1.0)
                                xga_t_def = dati_t.get('xGA Trasferta', 1.0)
                                xgot_c_att = float(dati_c.get('xGOT Casa', 0.0)) if 'xGOT Casa' in df_lega_match.columns else 0.0
                                xgot_t_att = float(dati_t.get('xGOT Trasferta', 0.0)) if 'xGOT Trasferta' in df_lega_match.columns else 0.0
                                par_c_real = float(dati_c.get('Parate Casa', 0.0)) if 'Parate Casa' in df_lega_match.columns else 0.0
                                par_t_real = float(dati_t.get('Parate Trasferta', 0.0)) if 'Parate Trasferta' in df_lega_match.columns else 0.0
                                xg_c_stag = (dati_c.get('xG Casa', 0) + dati_c.get('xG Trasferta', 0)) / 2.0
                                xg_t_stag = (dati_t.get('xG Casa', 0) + dati_t.get('xG Trasferta', 0)) / 2.0
                                tiri_tot_c = dati_c.get('Tiri totali Casa', 0)
                                tiri_tot_t = dati_t.get('Tiri totali Trasferta', 0)
                                porta_c = dati_c.get('Tiri in porta Casa', 0)
                                porta_t = dati_t.get('Tiri in porta Trasferta', 0)
                                corner_c = dati_c.get('Corner Casa', 0)
                                corner_t = dati_t.get('Corner Trasferta', 0)
                                falli_c = dati_c.get('Falli Commessi Casa', 0)
                                falli_t = dati_t.get('Falli Commessi Trasferta', 0)

                                dna_c = analizza_dna_squadra(casa, df_partite, xg_c_att, tiri_tot_c, xg_c_stag, xgot_c_att)
                                dna_t = analizza_dna_squadra(trasf, df_partite, xg_t_att, tiri_tot_t, xg_t_stag, xgot_t_att)

                                media_tp_1 = df_lega_match['Tiri in porta Casa'].mean() if 'Tiri in porta Casa' in df_lega_match.columns else 4.2
                                media_tp_2 = df_lega_match['Tiri in porta Trasferta'].mean() if 'Tiri in porta Trasferta' in df_lega_match.columns else 3.6
                                media_xga_c = df_lega_match['xGA Casa'].mean() if 'xGA Casa' in df_lega_match.columns else 1.25
                                media_xga_t = df_lega_match['xGA Trasferta'].mean() if 'xGA Trasferta' in df_lega_match.columns else 1.25

                                lmbda_1, lmbda_2, p_1_pura, p_x_pura, p_2_pura, _ = calcola_poisson_match(
                                    xg_c_att, xg_t_att, xga_c_def, xga_t_def, porta_c, porta_t, media_tp_1, media_tp_2,
                                    dna_c, dna_t, is_coppe_c, is_coppe_t, xgot_c_att, xgot_t_att
                                )

                                m_gs_c, lbl_gs_c = calcola_game_state(p_1_pura, p_2_pura)
                                m_gs_t, lbl_gs_t = calcola_game_state(p_2_pura, p_1_pura)
                                m_ec_c = 0.90 if is_coppe_c else 1.00
                                m_ec_t = 0.90 if is_coppe_t else 1.00

                                q_1 = pd.to_numeric(row.get('Quota 1', 0), errors='coerce')
                                q_2 = pd.to_numeric(row.get('Quota 2', 0), errors='coerce')
                                
                                if not pd.isna(q_1) and 1.55 <= q_1 <= 2.25:
                                    prob_book_1 = (100 / q_1) * 0.95
                                    prob_blend_1 = (p_1_pura * 0.65) + (prob_book_1 * 0.35)
                                    q_fair_1 = 100 / prob_blend_1 if prob_blend_1 > 0 else 99.0
                                    edge_1 = prob_blend_1 - (100 / q_1)
                                    
                                    if prob_blend_1 >= 52.0 and edge_1 >= 3.0:
                                        spia_1x2 = f"🎯 {dna_c['momentum_label']} • {dna_c['stato_cinismo'].split(' ')[0]} {dna_c['stato_cinismo'].split(' ')[1]}"
                                        chk_m = edge_1 >= 5.5
                                        chk_d = ((lmbda_1 - lmbda_2) >= 0.45) and (not is_coppe_c)
                                        chk_q = 1.65 <= q_1 <= 2.15
                                        n_sem = int(chk_m) + int(chk_d) + int(chk_q)
                                        str_sem = f"{'🟢' if chk_m else '🟡'}Margine &nbsp;{'🟢' if chk_d else '🟡'}xG/Coppe &nbsp;{'🟢' if chk_q else '🟡'}Quota ({n_sem}/3)"
                                        risultati_value.append({
                                            'Tipo_Mercato': '1X2',
                                            'Campionato': nome_lega_match,
                                            'Campionato_HTML': flag_card_html,
                                            'Partita': match_name,
                                            'Partita_HTML': match_html_card,
                                            'Mercato Consigliato': f"🏆 1 FISSO ({casa})",
                                            'Proiezione WebApp': f"Prob. Calibrata: {prob_blend_1:.1f}%",
                                            'Analisi_Avversario': f"Quota Fair Reale: <b>{q_fair_1:.2f}</b>",
                                            'Stato_Difesa': "🟢 Favorita Solida (Casa)",
                                            'Proiezione_Finale': f"{prob_blend_1:.1f}%",
                                            'Spia_Tattica': spia_1x2,
                                            'Linea Eplay24': '-',
                                            'Quota Eplay24': f"{q_1:.2f}",
                                            'Efficienza': edge_1,
                                            'Semafori': n_sem,
                                            'Semafori_HTML': str_sem,
                                            'Contro_Muro': False,
                                            'Score_Scelta': (n_sem * 15) + (edge_1 * 1.8) - (10 if is_coppe_c else 0)
                                        })
                                        
                                if not pd.isna(q_2) and 1.55 <= q_2 <= 2.25:
                                    prob_book_2 = (100 / q_2) * 0.95
                                    prob_blend_2 = (p_2_pura * 0.65) + (prob_book_2 * 0.35)
                                    q_fair_2 = 100 / prob_blend_2 if prob_blend_2 > 0 else 99.0
                                    edge_2 = prob_blend_2 - (100 / q_2)
                                    
                                    if prob_blend_2 >= 54.0 and edge_2 >= 3.0:
                                        spia_2x = f"🎯 {dna_t['momentum_label']} • {dna_t['stato_cinismo'].split(' ')[0]} {dna_t['stato_cinismo'].split(' ')[1]}"
                                        chk_m = edge_2 >= 5.5
                                        chk_d = ((lmbda_2 - lmbda_1) >= 0.45) and (not is_coppe_t)
                                        chk_q = 1.65 <= q_2 <= 2.15
                                        n_sem = int(chk_m) + int(chk_d) + int(chk_q)
                                        str_sem = f"{'🟢' if chk_m else '🟡'}Margine &nbsp;{'🟢' if chk_d else '🟡'}xG/Coppe &nbsp;{'🟢' if chk_q else '🟡'}Quota ({n_sem}/3)"
                                        risultati_value.append({
                                            'Tipo_Mercato': '1X2',
                                            'Campionato': nome_lega_match,
                                            'Campionato_HTML': flag_card_html,
                                            'Partita': match_name,
                                            'Partita_HTML': match_html_card,
                                            'Mercato Consigliato': f"🏆 2 FISSO ({trasf})",
                                            'Proiezione WebApp': f"Prob. Calibrata: {prob_blend_2:.1f}%",
                                            'Analisi_Avversario': f"Quota Fair Reale: <b>{q_fair_2:.2f}</b>",
                                            'Stato_Difesa': "🟢 Favorita Solida (Ospite)",
                                            'Proiezione_Finale': f"{prob_blend_2:.1f}%",
                                            'Spia_Tattica': spia_2x,
                                            'Linea Eplay24': '-',
                                            'Quota Eplay24': f"{q_2:.2f}",
                                            'Efficienza': edge_2,
                                            'Semafori': n_sem,
                                            'Semafori_HTML': str_sem,
                                            'Contro_Muro': False,
                                            'Score_Scelta': (n_sem * 15) + (edge_2 * 1.8) - (10 if is_coppe_t else 0)
                                        })

                                q_gg = pd.to_numeric(row.get('Quota GG', 0), errors='coerce')
                                if not pd.isna(q_gg) and q_gg >= 1.60:
                                    _, _, goal_c = calcola_mercati_betting(casa, df_partite, "globale")
                                    _, _, goal_t = calcola_mercati_betting(trasf, df_partite, "globale")
                                    perc_gg = (goal_c + goal_t) / 2
                                    q_fair_gg = 100 / perc_gg if perc_gg > 0 else 0
                                    edge_gg = perc_gg - (100 / q_gg)
                                    
                                    if perc_gg >= 55.0 and edge_gg >= 3.5:
                                        chk_m = edge_gg >= 6.0
                                        chk_d = (goal_c >= 55 and goal_t >= 55)
                                        chk_q = 1.65 <= q_gg <= 2.15
                                        n_sem = int(chk_m) + int(chk_d) + int(chk_q)
                                        str_sem = f"{'🟢' if chk_m else '🟡'}Margine &nbsp;{'🟢' if chk_d else '🟡'}Trend GG &nbsp;{'🟢' if chk_q else '🟡'}Quota ({n_sem}/3)"
                                        risultati_value.append({
                                            'Tipo_Mercato': '1X2',
                                            'Campionato': nome_lega_match,
                                            'Campionato_HTML': flag_card_html,
                                            'Partita': match_name,
                                            'Partita_HTML': match_html_card,
                                            'Mercato Consigliato': '⚽ GOAL (Entrambe Segnano)',
                                            'Proiezione WebApp': f"{goal_c:.0f}% Casa / {goal_t:.0f}% Ospite",
                                            'Analisi_Avversario': f"Quota Fair Storica: <b>{q_fair_gg:.2f}</b>",
                                            'Stato_Difesa': "🟢 Storico Favorevole",
                                            'Proiezione_Finale': f"{perc_gg:.1f}%",
                                            'Spia_Tattica': "🔥 Gara Aperta / Scambio Gol",
                                            'Linea Eplay24': '-',
                                            'Quota Eplay24': f"{q_gg:.2f}",
                                            'Efficienza': edge_gg,
                                            'Semafori': n_sem,
                                            'Semafori_HTML': str_sem,
                                            'Contro_Muro': False,
                                            'Score_Scelta': (n_sem * 15) + (edge_gg * 1.6)
                                        })

                                def aggiungi_mercato_statistico(nome_mercato, col_linea, col_quota, val_casa, val_trasf, col_c, col_t, icona, soglia_cuscinetto, mult_c, mult_t):
                                    linea = pd.to_numeric(row.get(col_linea, 0), errors='coerce')
                                    quota = pd.to_numeric(row.get(col_quota, 0), errors='coerce')
                                    
                                    if not pd.isna(linea) and linea > 0 and not pd.isna(quota) and quota > 1.0:
                                        target_cassa = int(math.floor(linea)) + 1
                                        
                                        proiezione_attacchi = val_casa + val_trasf
                                        sub_c, _ = stima_stat_subita(df_lega_match, dati_c, 'Casa', col_t, col_c)
                                        sub_t, _ = stima_stat_subita(df_lega_match, dati_t, 'Trasferta', col_c, col_t)
                                        proiezione_difese = sub_c + sub_t
                                        
                                        proj_casa_cal = ((val_casa + sub_t) / 2.0 if sub_t > 0 else val_casa) * mult_c
                                        proj_trasf_cal = ((val_trasf + sub_c) / 2.0 if sub_c > 0 else val_trasf) * mult_t
                                        proiezione_incrociata = proj_casa_cal + proj_trasf_cal
                                        
                                        media_tot_lega = proiezione_attacchi if proiezione_difese == 0 else (df_lega_match[col_c].mean() + df_lega_match[col_t].mean())
                                        contro_muro = False
                                        if proiezione_difese >= media_tot_lega * 1.05:
                                            stato_dif = "🟢 Difese Permessive"
                                            spia = "🔥 Assedio + Difese Permessive"
                                        elif proiezione_difese <= media_tot_lega * 0.95:
                                            stato_dif = "🔴 Difese Chiuse"
                                            spia = "🧱 Difese Chiuse (Frena Volume)"
                                            contro_muro = True
                                        else:
                                            stato_dif = "⚪ Difese Medie"
                                            spia = "⚖️ Ritmo Calibrato IA"

                                        if is_coppe_c or is_coppe_t:
                                            spia += " • 🇪🇺 Coppe"

                                        scarto_reale = proiezione_incrociata - target_cassa
                                        moltiplicatore_quota = max(0.80, min(1.25, quota / 1.80))
                                        eff = ((scarto_reale / target_cassa) * 100) * moltiplicatore_quota
                                        
                                        if contro_muro:
                                            eff = eff * 0.65
                                            
                                        chk_m = scarto_reale >= soglia_cuscinetto
                                        chk_d = not contro_muro
                                        chk_q = 1.65 <= quota <= 2.15
                                        n_sem = int(chk_m) + int(chk_d) + int(chk_q)
                                        str_sem = f"{'🟢' if chk_m else '🟡'}Cuscinetto(+{scarto_reale:.1f}) &nbsp;{'🟢' if chk_d else '🔴'}Difese &nbsp;{'🟢' if chk_q else '🟡'}Quota ({n_sem}/3)"
                                        
                                        if scarto_reale > 0 and eff > 0:
                                            risultati_value.append({
                                                'Tipo_Mercato': 'STAT',
                                                'Campionato': nome_lega_match,
                                                'Campionato_HTML': flag_card_html,
                                                'Partita': match_name,
                                                'Partita_HTML': match_html_card,
                                                'Mercato Consigliato': f"{icona} OVER {linea} {nome_mercato}",
                                                'Proiezione WebApp': f"{proiezione_attacchi:.2f} (Somma Attacchi)",
                                                'Analisi_Avversario': f"Concessi Difese: <b>{proiezione_difese:.2f}</b>",
                                                'Stato_Difesa': stato_dif,
                                                'Proiezione_Finale': f"{proiezione_incrociata:.2f}",
                                                'Spia_Tattica': spia,
                                                'Linea Eplay24': f"{linea} (Servono: {target_cassa})",
                                                'Quota Eplay24': f"{quota:.2f}",
                                                'Efficienza': eff,
                                                'Semafori': n_sem,
                                                'Semafori_HTML': str_sem,
                                                'Contro_Muro': contro_muro,
                                                'Score_Scelta': (n_sem * 15) + eff - (25 if contro_muro else 0)
                                            })
                                            
                                def aggiungi_mercato_squadra(nome_mercato, col_linea, col_quota, proiezione_sq, icona, nome_squadra, nome_avv, dati_avv, ruolo_avv, col_att, col_dif, soglia_cuscinetto, mult_sq, lbl_gs, dna_sq, is_coppe_sq):
                                    linea = pd.to_numeric(row.get(col_linea, 0), errors='coerce')
                                    quota = pd.to_numeric(row.get(col_quota, 0), errors='coerce')
                                    
                                    if not pd.isna(linea) and linea > 0 and not pd.isna(quota) and quota > 1.0:
                                        target_cassa = int(math.floor(linea)) + 1
                                        
                                        subiti_avv, stato_dif = stima_stat_subita(df_lega_match, dati_avv, ruolo_avv, col_att, col_dif)
                                        proiezione_base = (proiezione_sq + subiti_avv) / 2.0 if subiti_avv > 0 else proiezione_sq
                                        proiezione_incrociata = proiezione_base * mult_sq
                                        
                                        contro_muro = False
                                        if "Concede" in stato_dif:
                                            spia_dif = "🔥 Difesa Fragile"
                                        elif "Solida" in stato_dif:
                                            spia_dif = "🧱 Difesa Solida"
                                            contro_muro = True
                                        else:
                                            spia_dif = "⚖️ Difesa Media"

                                        extra_dna = []
                                        if "Gestione" in lbl_gs:
                                            extra_dna.append("🧊 Gestione")
                                        elif "Spinta" in lbl_gs:
                                            extra_dna.append("🔥 Spinta")
                                        if "Sprecona" in dna_sq['stato_cinismo']:
                                            extra_dna.append("Sprecona")
                                        elif "Iper-Cinica" in dna_sq['stato_cinismo']:
                                            extra_dna.append("Cinica")
                                        if "Corner" in nome_mercato and "Fuori" in dna_sq['stato_tiro']:
                                            extra_dna.append("🚀 Da Fuori")
                                        if is_coppe_sq:
                                            extra_dna.append("🇪🇺 Coppe")
                                        spia = spia_dif + (" • " + " ".join(extra_dna) if extra_dna else "")

                                        scarto_reale = proiezione_incrociata - target_cassa
                                        moltiplicatore_quota = max(0.80, min(1.25, quota / 1.80))
                                        eff = ((scarto_reale / target_cassa) * 100) * moltiplicatore_quota
                                        
                                        if contro_muro:
                                            eff = eff * 0.65
                                            
                                        chk_m = scarto_reale >= soglia_cuscinetto
                                        chk_d = (not contro_muro) and ("Gestione" not in lbl_gs)
                                        chk_q = 1.65 <= quota <= 2.15
                                        n_sem = int(chk_m) + int(chk_d) + int(chk_q)
                                        str_sem = f"{'🟢' if chk_m else '🟡'}Cuscinetto(+{scarto_reale:.1f}) &nbsp;{'🟢' if chk_d else '🔴'}Dif/GS &nbsp;{'🟢' if chk_q else '🟡'}Quota ({n_sem}/3)"
                                        
                                        if scarto_reale > 0 and eff > 0:
                                            risultati_value.append({
                                                'Tipo_Mercato': 'STAT',
                                                'Campionato': nome_lega_match,
                                                'Campionato_HTML': flag_card_html,
                                                'Partita': match_name,
                                                'Partita_HTML': match_html_card,
                                                'Mercato Consigliato': f"{icona} OVER {linea} {nome_mercato} ({nome_squadra})",
                                                'Proiezione WebApp': f"{proiezione_sq:.2f} (Media {nome_squadra})",
                                                'Analisi_Avversario': f"Subiti {nome_avv} ({ruolo_avv}): <b>{subiti_avv:.2f}</b>",
                                                'Stato_Difesa': stato_dif,
                                                'Proiezione_Finale': f"{proiezione_incrociata:.2f}",
                                                'Spia_Tattica': spia,
                                                'Linea Eplay24': f"{linea} (Servono: {target_cassa})",
                                                'Quota Eplay24': f"{quota:.2f}",
                                                'Efficienza': eff,
                                                'Semafori': n_sem,
                                                'Semafori_HTML': str_sem,
                                                'Contro_Muro': contro_muro,
                                                'Score_Scelta': (n_sem * 15) + eff - (25 if contro_muro else 0)
                                            })

                                def aggiungi_mercato_parate(col_linea, col_quota, par_reali, proj_tp_avv, xga_dif, media_xga, dna_avv, nome_gk, nome_avv):
                                    linea = pd.to_numeric(row.get(col_linea, 0), errors='coerce')
                                    quota = pd.to_numeric(row.get(col_quota, 0), errors='coerce')
                                    if not pd.isna(linea) and linea > 0 and not pd.isna(quota) and quota > 1.0:
                                        target_cassa = int(math.floor(linea)) + 1
                                        par_att, t_sub, fonte_gk = calcola_parate_portiere(par_reali, proj_tp_avv, xga_dif, media_xga, dna_avv)
                                        scarto_reale = par_att - target_cassa
                                        molt_q = max(0.80, min(1.25, quota / 1.80))
                                        eff = ((scarto_reale / target_cassa) * 100) * molt_q
                                        chk_m = scarto_reale >= 0.45
                                        chk_d = ("Tiri Parabili" in dna_avv['stato_xgot']) or ("Fuori" in dna_avv['stato_tiro']) or (t_sub >= 4.2)
                                        chk_q = 1.65 <= quota <= 2.15
                                        n_sem = int(chk_m) + int(chk_d) + int(chk_q)
                                        str_sem = f"{'🟢' if chk_m else '🟡'}Cuscinetto(+{scarto_reale:.1f}) &nbsp;{'🟢' if chk_d else '🟡'}Assedio &nbsp;{'🟢' if chk_q else '🟡'}Quota ({n_sem}/3)"
                                        if scarto_reale > 0 and eff > 0:
                                            risultati_value.append({
                                                'Tipo_Mercato': 'STAT',
                                                'Campionato': nome_lega_match,
                                                'Campionato_HTML': flag_card_html,
                                                'Partita': match_name,
                                                'Partita_HTML': match_html_card,
                                                'Mercato Consigliato': f"🧤 OVER {linea} Parate Portiere ({nome_gk})",
                                                'Proiezione WebApp': f"{par_reali:.2f} (Media Reale)" if par_reali > 0 else "Stima da Tiri Subiti",
                                                'Analisi_Avversario': f"Tiri Porta {nome_avv}: <b>{t_sub:.1f}</b> ({fonte_gk})",
                                                'Stato_Difesa': fonte_gk,
                                                'Proiezione_Finale': f"{par_att:.2f}",
                                                'Spia_Tattica': f"🧤 {dna_avv['stato_xgot'] if dna_avv['has_xgot'] else dna_avv['stato_tiro']}",
                                                'Linea Eplay24': f"{linea} (Servono: {target_cassa})",
                                                'Quota Eplay24': f"{quota:.2f}",
                                                'Efficienza': eff,
                                                'Semafori': n_sem,
                                                'Semafori_HTML': str_sem,
                                                'Contro_Muro': False,
                                                'Score_Scelta': (n_sem * 15) + eff
                                            })

                                m_tt_c = max(0.80, min(1.15, m_gs_c * dna_c['mult_cin_stat'] * m_ec_c))
                                m_tt_t = max(0.80, min(1.15, m_gs_t * dna_t['mult_cin_stat'] * m_ec_t))
                                m_tp_c = max(0.82, min(1.12, m_gs_c * m_ec_c))
                                m_tp_t = max(0.82, min(1.12, m_gs_t * m_ec_t))
                                m_cor_c = max(0.80, min(1.16, m_gs_c * dna_c['mult_cin_stat'] * dna_c['mult_cor_tiro'] * m_ec_c))
                                m_cor_t = max(0.80, min(1.16, m_gs_t * dna_t['mult_cin_stat'] * dna_t['mult_cor_tiro'] * m_ec_t))
                                m_fal_c = 1.05 if is_coppe_c else 1.00
                                m_fal_t = 1.05 if is_coppe_t else 1.00

                                aggiungi_mercato_statistico('Tiri Totali', 'Linea Over Tiri', 'Quota Over Tiri', tiri_tot_c, tiri_tot_t, 'Tiri totali Casa', 'Tiri totali Trasferta', '👟', 1.4, m_tt_c, m_tt_t)
                                aggiungi_mercato_squadra('Tiri Totali', 'Linea Tiri Casa', 'Quota Tiri Casa', tiri_tot_c, '👟', casa, trasf, dati_t, 'Trasferta', 'Tiri totali Casa', 'Tiri totali Trasferta', 1.0, m_tt_c, lbl_gs_c, dna_c, is_coppe_c)
                                aggiungi_mercato_squadra('Tiri Totali', 'Linea Tiri Trasferta', 'Quota Tiri Trasferta', tiri_tot_t, '👟', trasf, casa, dati_c, 'Casa', 'Tiri totali Trasferta', 'Tiri totali Casa', 1.0, m_tt_t, lbl_gs_t, dna_t, is_coppe_t)

                                aggiungi_mercato_statistico('Tiri in Porta', 'Linea Over Tiri Porta', 'Quota Over Tiri Porta', porta_c, porta_t, 'Tiri in porta Casa', 'Tiri in porta Trasferta', '🥅', 0.8, m_tp_c, m_tp_t)

                                aggiungi_mercato_statistico('Corner', 'Linea Over Corner', 'Quota Over Corner', corner_c, corner_t, 'Corner Casa', 'Corner Trasferta', '🚩', 0.8, m_cor_c, m_cor_t)
                                aggiungi_mercato_squadra('Corner', 'Linea Corner Casa', 'Quota Corner Casa', corner_c, '🚩', casa, trasf, dati_t, 'Trasferta', 'Corner Casa', 'Corner Trasferta', 0.6, m_cor_c, lbl_gs_c, dna_c, is_coppe_c)
                                aggiungi_mercato_squadra('Corner', 'Linea Corner Trasferta', 'Quota Corner Trasferta', corner_t, '🚩', trasf, casa, dati_c, 'Casa', 'Corner Trasferta', 'Corner Casa', 0.6, m_cor_t, lbl_gs_t, dna_t, is_coppe_t)

                                aggiungi_mercato_statistico('Falli', 'Linea Over Falli', 'Quota Over Falli', falli_c, falli_t, 'Falli Commessi Casa', 'Falli Commessi Trasferta', '🛑', 1.2, m_fal_c, m_fal_t)

                                sub_tp_t_sc, _ = stima_stat_subita(df_lega_match, dati_t, 'Trasferta', 'Tiri in porta Casa', 'Tiri in porta Trasferta')
                                sub_tp_c_sc, _ = stima_stat_subita(df_lega_match, dati_c, 'Casa', 'Tiri in porta Trasferta', 'Tiri in porta Casa')
                                proj_tp_c_sc = ((porta_c + sub_tp_t_sc) / 2.0 if sub_tp_t_sc > 0 else porta_c) * m_tp_c
                                proj_tp_t_sc = ((porta_t + sub_tp_c_sc) / 2.0 if sub_tp_c_sc > 0 else porta_t) * m_tp_t
                                aggiungi_mercato_parate('Linea Parate Casa', 'Quota Parate Casa', par_c_real, proj_tp_t_sc, xga_c_def, media_xga_c, dna_t, casa, trasf)
                                aggiungi_mercato_parate('Linea Parate Trasferta', 'Quota Parate Trasferta', par_t_real, proj_tp_c_sc, xga_t_def, media_xga_t, dna_c, trasf, casa)
                            
                            if len(risultati_value) > 0:
                                df_value = pd.DataFrame(risultati_value)
                                
                                if filtro_lega_scanner != "🌍 Tutti i Campionati":
                                    df_value = df_value[df_value['Campionato'] == filtro_lega_scanner]
                                
                                if nascondi_muri:
                                    df_value = df_value[df_value['Contro_Muro'] == False]
                                    
                                df_value = df_value[df_value['Efficienza'] >= filtro_eff]
                                
                                if not df_value.empty:
                                    df_value = df_value.sort_values(by=['Score_Scelta', 'Efficienza'], ascending=[False, False])
                                    idx_prime_scelte = df_value.groupby('Partita', sort=False).head(1).index
                                    df_value['Prima_Scelta'] = df_value.index.isin(idx_prime_scelte)
                                    
                                    if solo_prima_scelta:
                                        df_value = df_value[df_value['Prima_Scelta'] == True]
                                        
                                    df_value = df_value.sort_values(by=['Semafori', 'Efficienza'], ascending=[False, False])
                                
                                if df_value.empty:
                                    st.warning(f"😔 Nessuna giocata supera i filtri di sicurezza selezionati.")
                                else:
                                    st.success(f"✅ Trovate **{len(df_value)}** Giocate filtrate col Sistema Salva-Cassa Pro!")
                                    
                                    counts = df_value['Partita'].value_counts()
                                    partite_ripetute = counts[counts > 1].index.tolist()
                                    
                                    mappa_colori = {}
                                    palette_colori = [
                                        'rgba(0, 230, 118, 0.08)', 
                                        'rgba(56, 189, 248, 0.08)', 
                                        'rgba(255, 183, 3, 0.08)', 
                                        'rgba(168, 85, 247, 0.08)', 
                                        'rgba(255, 75, 75, 0.08)'
                                    ]
                                    
                                    for i, match in enumerate(partite_ripetute):
                                        mappa_colori[match] = palette_colori[i % len(palette_colori)]
                                        
                                    html_cards = ""
                                    for _, bet in df_value.iterrows():
                                        eff = bet['Efficienza']
                                        tipo_m = bet.get('Tipo_Mercato', 'STAT')
                                        nome_match = bet['Partita']
                                        nome_match_html = bet.get('Partita_HTML', nome_match)
                                        lega_badge_html = bet.get('Campionato_HTML', bet['Campionato'])
                                        colore_sfondo = mappa_colori.get(nome_match, '#13171d')
                                        contro_muro = bet.get('Contro_Muro', False)
                                        n_sem = bet.get('Semafori', 2)
                                        sem_html = bet.get('Semafori_HTML', '')
                                        is_top_match = bet.get('Prima_Scelta', False)
                                        
                                        tag_scelta = "<span style='background:rgba(0,230,118,0.14); color:#00e676; border:1px solid rgba(0,230,118,0.38); padding:2px 6px; border-radius:4px; font-size:0.7em; margin-left:6px; font-weight:700;'>👑 1ª SCELTA MATCH</span>" if is_top_match else "<span style='background:#1a1f27; color:#9ca3af; padding:2px 6px; border-radius:4px; font-size:0.7em; margin-left:6px;'>Alternativa</span>"

                                        if contro_muro:
                                            col_bordo = "#ffb703"
                                            badge = "⚠️ CONTRO DIFESA SOLIDA"
                                            puntata = "Max 1 Unità (Prudenza)"
                                        elif tipo_m == '1X2':
                                            if eff >= 10.0 and n_sem == 3:
                                                col_bordo = "#ff4b4b"
                                                badge = "🛡️ BLINDATA 3/3 (1X2)"
                                                puntata = "3 Unità (Alta Fiducia)"
                                            elif eff >= 6.0 and n_sem >= 2:
                                                col_bordo = "#00e676"
                                                badge = "🟢 OTTIMA (1X2)"
                                                puntata = "2 Unità (Rischio Medio)"
                                            else:
                                                col_bordo = "#ffb703"
                                                badge = "🟡 BUONA (1X2)"
                                                puntata = "1 Unità (Rischio Basso)"
                                        else:
                                            if eff >= 18.0 and n_sem == 3:
                                                col_bordo = "#ff4b4b"
                                                badge = "🛡️ SUPER BLINDATA (3/3)"
                                                puntata = "3 Unità (Alta Fiducia)"
                                            elif eff >= 11.0 and n_sem >= 2:
                                                col_bordo = "#00e676"
                                                badge = "🟢 OTTIMA SCELTA"
                                                puntata = "2 Unità (Rischio Medio)"
                                            else:
                                                col_bordo = "#ffb703"
                                                badge = "🟡 GIOCABILE"
                                                puntata = "1 Unità (Rischio Basso)"
                                            
                                        html_cards += f"""
                                        <div style="background: {colore_sfondo}; border-radius: 10px; border: 1px solid #222831; border-left: 5px solid {col_bordo}; padding: 12px 16px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 16px rgba(0,0,0,0.22); transition: transform 0.2s ease;">
                                            <div style="flex: 1.8; padding-right: 10px;">
                                                <span style="font-size: 0.72em; color: #e5e7eb; background: #1c222b; border: 1px solid #2b313a; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600;">{lega_badge_html}</span>{tag_scelta}
                                                <h4 style="margin: 6px 0 2px 0; color: #fff !important; font-size: 1.05em; font-weight: 700;">{nome_match_html}</h4>
                                                <p style="margin: 2px 0 2px 0; color: #00e676; font-weight: 700; font-size: 0.95em;">{bet['Mercato Consigliato']}</p>
                                                <p style="margin: 0; font-size: 0.75em; color: #9ca3af;">Proiezione: <b>{bet['Proiezione WebApp']}</b> | Linea: <b style="color:#fff;">{bet['Linea Eplay24']}</b></p>
                                            </div>
                                            <div style="flex: 1.7; text-align: center; border-left: 1px solid #222831; padding: 0 10px;">
                                                <p style="margin: 0; font-size: 0.68em; color: #8b949e; text-transform: uppercase; letter-spacing: 0.5px;">Checklist Salva-Cassa Pro</p>
                                                <p style="margin: 4px 0; font-size: 0.74em; color: #e5e7eb; background: #0d1014; border: 1px solid #1e232a; padding: 4px 6px; border-radius: 5px;">{sem_html}</p>
                                                <p style="margin: 2px 0; font-size: 0.72em; color: #00e676;">{bet['Spia_Tattica']} | Reale: <b style="font-family: JetBrains Mono, monospace;">{bet['Proiezione_Finale']}</b></p>
                                            </div>
                                            <div style="flex: 0.85; text-align: center; border-left: 1px solid #222831; border-right: 1px solid #222831; padding: 0 10px;">
                                                <p style="margin: 0; font-size: 0.7em; color: #00e676; text-transform: uppercase; font-weight: 700; letter-spacing: 1px;">Eplay24</p>
                                                <h2 style="margin: 2px 0 0 0; color: #fff !important; font-family: 'JetBrains Mono', monospace; font-size: 1.4em;">{bet['Quota Eplay24']}</h2>
                                            </div>
                                            <div style="flex: 1.35; text-align: right; padding-left: 10px;">
                                                <p style="margin: 0; font-size: 0.75em; color: {col_bordo}; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;">{badge}</p>
                                                <h1 style="margin: 0; color: {col_bordo} !important; font-weight: 800; font-size: 1.6em; font-family: 'JetBrains Mono', monospace;">+{eff:.1f}%</h1>
                                                <p style="margin: 0; font-size: 0.75em; color: #9ca3af;"><b style="color: #fff;">{puntata}</b></p>
                                            </div>
                                        </div>
                                        """
                                    st.markdown(html_cards, unsafe_allow_html=True)
                            else:
                                st.warning("😔 Nessuna giocata consigliata trovata. Verifica che i nomi delle squadre nel foglio 'Palinsesto' coincidano con quelli dei fogli dei campionati.")

                else:
                    stemma_singolo = ottieni_stemma_html(squadra_scelta, campionato_scelto, size=55)
                    forma_str = calcola_forma(squadra_scelta, df_partite)
                    st.markdown(f"""
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
                        {stemma_singolo if stemma_singolo else '<span style="font-size:2.5em;">⚽</span>'}
                        <div>
                            <h2 style="margin:0; color:#fff !important;">Profilo Statistico: {squadra_scelta}</h2>
                            <p style="margin:4px 0 0 0; color:#d1d5db;"><b>Trend Recente (Ultime 5):</b> {forma_str}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.divider()
                    
                    dati_squadra = df_selezionato[df_selezionato['Squadra'] == squadra_scelta].iloc[0]
                    has_xgot_sq = ('xGOT Casa' in df_selezionato.columns) and ('xGOT Trasferta' in df_selezionato.columns)
                    has_par_sq = ('Parate Casa' in df_selezionato.columns) and ('Parate Trasferta' in df_selezionato.columns)
                    
                    tot_p, perc_over, perc_goal = calcola_mercati_betting(squadra_scelta, df_partite, modalita="globale")
                    if tot_p > 0:
                        st.markdown("### 🎯 Scanner Mercati Storici (Globale)")
                        st.markdown(genera_html_scanner(perc_over, perc_goal, tot_p, "#00e676"), unsafe_allow_html=True)
                        st.divider()
                    
                    st.markdown("### ⚔️ Fase Offensiva")
                    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("🎯 xG Casa", formatta_numero(dati_squadra.get('xG Casa', 0)))
                    c2.metric("🎯 xG Trasferta", formatta_numero(dati_squadra.get('xG Trasferta', 0)))
                    c3.metric("🥅 Tiri porta (Casa)", formatta_numero(dati_squadra.get('Tiri in porta Casa', 0)))
                    c4.metric("🥅 Tiri porta (Trasferta)", formatta_numero(dati_squadra.get('Tiri in porta Trasferta', 0)))
                    if has_xgot_sq:
                        cx1, cx2, _, _ = st.columns(4)
                        cx1.metric("🔥 xGOT Casa", formatta_numero(dati_squadra.get('xGOT Casa', 0)))
                        cx2.metric("🔥 xGOT Trasferta", formatta_numero(dati_squadra.get('xGOT Trasferta', 0)))
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown("### 🛡️ Fase Difensiva")
                    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
                    c5, c6, c7, c8 = st.columns(4)
                    c5.metric("🛡️ xGA Subiti (Casa)", formatta_numero(dati_squadra.get('xGA Casa', 0)))
                    c6.metric("🛡️ xGA Subiti (Trasferta)", formatta_numero(dati_squadra.get('xGA Trasferta', 0)))
                    c7.metric("🚩 Corner (Casa)", formatta_numero(dati_squadra.get('Corner Casa', 0)))
                    c8.metric("🚩 Corner (Trasferta)", formatta_numero(dati_squadra.get('Corner Trasferta', 0)))
                    if has_par_sq:
                        cp1, cp2, _, _ = st.columns(4)
                        cp1.metric("🧤 Parate Portiere (Casa)", formatta_numero(dati_squadra.get('Parate Casa', 0)))
                        cp2.metric("🧤 Parate Portiere (Trasferta)", formatta_numero(dati_squadra.get('Parate Trasferta', 0)))
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown("### 🥊 Aggressività & Disciplina")
                    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
                    c9, c10, c11, c12 = st.columns(4)
                    c9.metric("🛑 Falli (Casa)", formatta_numero(dati_squadra.get('Falli Commessi Casa', 0)))
                    c10.metric("🛑 Falli (Trasferta)", formatta_numero(dati_squadra.get('Falli Commessi Trasferta', 0)))
                    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.pagina_impostazioni:
    st.sidebar.divider()
    if st.sidebar.button("🔙 Torna alla Dashboard", use_container_width=True):
        st.session_state.pagina_impostazioni = False
        st.rerun()

    st.title("☁️ Pannello di Controllo Cloud & Google Fogli")
    st.markdown("Gestisci la sincronizzazione in tempo reale con Google Fogli e i collegamenti rapidi.")
    st.divider()
    
    col_conf_1, col_conf_2 = st.columns([1, 1])
    
    with col_conf_1:
        st.subheader("🔗 Connessione Google Fogli")
        st.markdown("Puoi testare al volo un nuovo link Google Fogli incollandolo qui sotto:")
        
        nuovo_link = st.text_input("Link Google Fogli (Chiunque abbia il link):", value=st.session_state.custom_gsheet_url)
        if st.button("💾 Applica Link & Sincronizza Ora", use_container_width=True):
            st.session_state.custom_gsheet_url = nuovo_link
            st.cache_data.clear()
            st.success("✅ Connessione aggiornata! Torna alla dashboard per vedere i dati.")
            
        st.markdown("---")
        st.subheader("🔗 Area Operativa Betting")
        col_lnk1, col_lnk2 = st.columns(2)
        with col_lnk1:
            st.link_button("🌐 Piazza Scommessa (Eplay24)", "https://eplay24.it/", use_container_width=True)
        with col_lnk2:
            st.link_button("📊 Risultati Live (Diretta.it)", "https://www.diretta.it", use_container_width=True)
                
    with col_conf_2:
        st.subheader("📊 Stato Sincronizzazione Cloud")
        id_26 = estrai_id_google_sheet(st.session_state.custom_gsheet_url or LINK_GOOGLE_FOGLI_26_27)
        if id_26:
            st.success("Google Fogli 2026-2027: CONNESSO 🟢")
        else:
            st.warning("Google Fogli 2026-2027: NON CONFIGURATO ⚠️")
            
        st.markdown("---")
        if st.button("🔒 Blocca Sessione (Logout)", use_container_width=True):
            st.session_state.autenticato = False
            st.rerun()

st.sidebar.markdown(
    """
    <div style="margin-top: 60px; padding-top: 15px; border-top: 1px solid #1d2229; color: #6b7280; font-size: 0.85em; text-align: left;">
        <span style="font-weight: 600; color: #8b949e; font-family: 'Outfit', sans-serif;">by Alessandro Gusmeroli</span>
    </div>
    """,
    unsafe_allow_html=True
)
