import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import math
import os
import datetime
import re
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

# ==========================================
# 1. IMPOSTAZIONI GENERALI E STILE AVANZATO
# ==========================================
st.set_page_config(
    page_title="Dashboard Betting", 
    layout="wide", 
    initial_sidebar_state="auto"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Outfit:wght@300;400;600;800&display=swap');

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stHeader"] { background-color: transparent; }
    
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif !important; }
    @keyframes slideUpFade {
        0% { opacity: 0; transform: translateY(15px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .main .block-container { 
        padding-top: 1.5rem; 
        animation: slideUpFade 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    h1 {
        background: -webkit-linear-gradient(45deg, #ffffff, #00cc66);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    h2, h3, h4 { font-weight: 700 !important; }
    
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
    }

    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(0, 204, 102, 0.05), transparent 30%),
                    radial-gradient(circle at 90% 80%, rgba(0, 102, 204, 0.04), transparent 30%);
        background-color: #0e1117;
    }

    [data-testid="stSidebar"] {
        background-color: rgba(18, 22, 28, 0.5) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    div[data-baseweb="select"] > div {
        background-color: rgba(0, 0, 0, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 10px !important;
        transition: border 0.3s ease;
    }
    div[data-baseweb="select"] > div:hover {
        border: 1px solid rgba(0, 204, 102, 0.5) !important;
    }
    
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.2); }

    .stTabs [data-baseweb="tab-list"] { gap: 2rem; border-bottom: 2px solid rgba(255, 255, 255, 0.05); }
    .stTabs [data-baseweb="tab"] { height: 50px; font-weight: 600; font-size: 1.05rem; color: #7a7a7a; padding-bottom: 10px; transition: color 0.3s ease; }
    .stTabs [data-baseweb="tab"]:hover { color: #d0d0d0; }
    .stTabs [aria-selected="true"] { color: #00cc66 !important; border-bottom-color: #00cc66 !important; }
    
    .stButton>button { 
        border-radius: 12px; 
        background: rgba(0, 204, 102, 0.15); 
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        color: #00cc66; 
        font-weight: 700; 
        border: 1px solid rgba(0, 204, 102, 0.4); 
        box-shadow: 0 4px 15px rgba(0,204,102, 0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        background: rgba(0, 204, 102, 0.9); 
        color: white;
        box-shadow: 0 6px 20px rgba(0,204,102, 0.4);
        transform: translateY(-2px);
    }
    
    div[data-testid="metric-container"] {
        background: rgba(30, 30, 36, 0.4) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        padding: 15% 10% !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15) !important;
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        border: 1px solid rgba(0, 204, 102, 0.3) !important;
        box-shadow: 0 12px 40px 0 rgba(0, 204, 102, 0.1) !important;
    }
    div[data-testid="metric-container"] label {
        color: #a0a0a0 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }
    
    .glass-box {
        background: rgba(22, 26, 33, 0.5);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15);
        margin-bottom: 24px;
        transition: transform 0.3s ease;
    }
    .glass-box:hover { border-color: rgba(255, 255, 255, 0.12); }
    
    [data-testid="stTable"] table { width: 100% !important; background: transparent !important; color: #e0e0e0; border-collapse: collapse; }
    [data-testid="stTable"] tbody tr { transition: background-color 0.2s ease; }
    [data-testid="stTable"] tbody tr:hover { background-color: rgba(255, 255, 255, 0.06) !important; }
    [data-testid="stTable"] th {
        background-color: rgba(255, 255, 255, 0.02) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        text-transform: uppercase;
        font-size: 0.85em;
        letter-spacing: 1px;
    }
    [data-testid="stTable"] th, [data-testid="stTable"] td { 
        text-align: center !important; 
        border-color: rgba(255, 255, 255, 0.03) !important;
        padding: 12px 8px !important;
    }
</style>
""", unsafe_allow_html=True)

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
        'Falli commessi Casa': 'Falli Commessi Casa', 'Falli commessi Trasferta': 'Falli Commessi Trasferta'
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
    
    # 1. Tentativo di caricamento da Google Fogli (Cloud)
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

    # 2. Fallback automatico su file Excel locale
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

def genera_html_scanner(perc_over, perc_goal, tot_partite, color_accent="#00cc66"):
    if perc_over > 0:
        quota_over = 100 / perc_over
        testo_q_over = f"<span style='color:#a0a0a0; font-size:0.85em;'>Quota Fair:</span> <b style='color:#fff; font-family: JetBrains Mono, monospace;'>{quota_over:.2f}</b>"
    else:
        testo_q_over = "<span style='color:#a0a0a0; font-size:0.85em;'>Quota Fair:</span> <b style='color:#fff; font-family: JetBrains Mono, monospace;'>N/D</b>"

    if perc_goal > 0:
        quota_goal = 100 / perc_goal
        testo_q_goal = f"<span style='color:#a0a0a0; font-size:0.85em;'>Quota Fair:</span> <b style='color:#fff; font-family: JetBrains Mono, monospace;'>{quota_goal:.2f}</b>"
    else:
        testo_q_goal = "<span style='color:#a0a0a0; font-size:0.85em;'>Quota Fair:</span> <b style='color:#fff; font-family: JetBrains Mono, monospace;'>N/D</b>"

    return f"""
    <div class="glass-box">
        <p style="margin:0; font-size:12px; color:#888; text-align: right; text-transform: uppercase; letter-spacing: 1px;">Match Storici Analizzati: {tot_partite}</p>
        <div style="margin-top: 5px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <strong style="color: #fff; font-size: 1.1em;">🔥 OVER 2.5</strong>
                <div style="text-align: right;">
                    <span style="margin-right: 12px; background: rgba(0,0,0,0.3); padding: 3px 8px; border-radius: 6px;">{testo_q_over}</span>
                    <span style="font-weight:800; font-size: 1.1em; color: {color_accent}; font-family: 'JetBrains Mono', monospace;">{perc_over:.1f}%</span>
                </div>
            </div>
            <div style="background: rgba(255,255,255,0.05); border-radius: 12px; width: 100%; height: 16px; overflow: hidden; border: 1px solid rgba(255,255,255,0.05);">
                <div style="background: linear-gradient(90deg, transparent, {color_accent}); border-radius: 12px; width: {perc_over}%; height: 100%; box-shadow: 0 0 12px {color_accent}; transition: width 1s ease-in-out;"></div>
            </div>
        </div>
        <div style="margin-top: 30px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <strong style="color: #fff; font-size: 1.1em;">⚽ GOAL (GG)</strong>
                <div style="text-align: right;">
                    <span style="margin-right: 12px; background: rgba(0,0,0,0.3); padding: 3px 8px; border-radius: 6px;">{testo_q_goal}</span>
                    <span style="font-weight:800; font-size: 1.1em; color: {color_accent}; font-family: 'JetBrains Mono', monospace;">{perc_goal:.1f}%</span>
                </div>
            </div>
            <div style="background: rgba(255,255,255,0.05); border-radius: 12px; width: 100%; height: 16px; overflow: hidden; border: 1px solid rgba(255,255,255,0.05);">
                <div style="background: linear-gradient(90deg, transparent, {color_accent}); border-radius: 12px; width: {perc_goal}%; height: 100%; box-shadow: 0 0 12px {color_accent}; transition: width 1s ease-in-out;"></div>
            </div>
        </div>
    </div>
    """

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
    campionato_scelto = st.sidebar.selectbox("🏆 Seleziona il Campionato:", ['Serie A', 'La Liga', 'Premier League'])

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
            
            if modalita_confronto:
                st.sidebar.markdown("**Seleziona le squadre:**")
                squadra_1 = st.sidebar.selectbox("🏠 Prima Squadra (Casa):", lista_squadre_pure)
                squadra_2 = st.sidebar.selectbox("✈️ Seconda Squadra (Ospite):", lista_squadre_pure, index=1 if len(lista_squadre_pure)>1 else 0)
                simula_reale = st.sidebar.checkbox("🏟️ Usa Dati Reali (Solo Casa vs Trasferta)")
            else:
                lista_squadre = ["Tutte le squadre"] + lista_squadre_pure
                squadra_scelta = st.sidebar.selectbox("🔎 Seleziona la Squadra:", lista_squadre)

            st.sidebar.divider()
            col_txt_ingr, col_btn_ingr = st.sidebar.columns([4, 1])
            with col_txt_ingr:
                st.markdown("<p style='font-size: 0.85em; color: #888; margin-top: 8px;'>Impostazioni Cloud</p>", unsafe_allow_html=True)
            with col_btn_ingr:
                if st.button("⚙️", help="Gestisci il collegamento Cloud"):
                    st.session_state.pagina_impostazioni = not st.session_state.pagina_impostazioni
                    st.rerun()

            if modalita_confronto:
                col_t1, col_vs, col_t2 = st.columns([2, 1, 2])
                with col_t1:
                    st.markdown(f"<h2 style='text-align: right; color: #00cc66; text-shadow: 0 0 20px rgba(0,204,102,0.4);'>{squadra_1}</h2>", unsafe_allow_html=True)
                with col_vs:
                    st.markdown("<h2 style='text-align: center; color: #555;'>vs</h2>", unsafe_allow_html=True)
                with col_t2:
                    st.markdown(f"<h2 style='text-align: left; color: #ff4b4b; text-shadow: 0 0 20px rgba(255,75,75,0.4);'>{squadra_2}</h2>", unsafe_allow_html=True)
            else:
                col_titolo, col_data = st.columns([3, 1])
                with col_titolo:
                    st.markdown(f"<h1><span style='-webkit-text-fill-color: initial;'>⚽</span> Statistiche {campionato_scelto}</h1>", unsafe_allow_html=True)
                with col_data:
                    st.markdown(f"<p style='text-align: right; color: #666; font-size: 0.85em; margin-top: 1.5em;'>⏱️ Fonte Dati:<br><b style='color:#00cc66;'>{data_aggiornamento}</b></p>", unsafe_allow_html=True)
            
            st.markdown(f"<p style='color:#888;'>Stagione sportiva {stagione_scelta}</p>", unsafe_allow_html=True)
            st.divider()

            if modalita_confronto:
                dati_sq1 = df_selezionato[df_selezionato['Squadra'] == squadra_1].iloc[0]
                dati_sq2 = df_selezionato[df_selezionato['Squadra'] == squadra_2].iloc[0]
                
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
                    fig_radar.add_trace(go.Scatterpolar(r=v1_norm, theta=categorie_radar, fill='toself', name=nome_1, line_color='#00cc66', line_width=3))
                    fig_radar.add_trace(go.Scatterpolar(r=v2_norm, theta=categorie_radar, fill='toself', name=nome_2, line_color='#ff4b4b', line_width=3))
                    fig_radar.update_layout(template="plotly_dark", polar=dict(radialaxis=dict(visible=False, range=[0, 100])), showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=420, margin=dict(t=30, b=30), font=dict(family='Outfit', size=13))
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
                    else:
                        lista_stats = [(col, dati_sq1[col], dati_sq2[col]) for col in colonne_numeriche]
                    
                    html_content = '<div class="glass-box" style="padding: 30px;">'
                    for nome_stat, v1, v2 in lista_stats:
                        tot = v1 + v2
                        p1 = 50 if tot == 0 else (v1 / tot) * 100
                        p2 = 50 if tot == 0 else (v2 / tot) * 100
                        
                        v1_str = formatta_numero(v1)
                        v2_str = formatta_numero(v2)
                        
                        html_content += f"""
                        <div style="margin-bottom: 22px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; font-weight: 600; font-size: 0.95em; color: #ddd; font-family: 'Outfit', sans-serif;">
                                <span style="color: #00cc66; width: 30%; text-align: left; font-family: 'JetBrains Mono', monospace; font-size: 1.1em;">{v1_str}</span>
                                <span style="width: 40%; text-align: center; font-size: 0.95em; text-transform: uppercase; letter-spacing: 1px;">{nome_stat}</span>
                                <span style="color: #ff4b4b; width: 30%; text-align: right; font-family: 'JetBrains Mono', monospace; font-size: 1.1em;">{v2_str}</span>
                            </div>
                            <div style="display: flex; width: 100%; height: 10px; border-radius: 5px; overflow: hidden; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);">
                                <div style="width: {p1}%; background-color: #00cc66; box-shadow: 0 0 10px rgba(0,204,102,0.5);"></div>
                                <div style="width: {p2}%; background-color: #ff4b4b; box-shadow: 0 0 10px rgba(255,75,75,0.5);"></div>
                            </div>
                        </div>
                        """
                    html_content += "</div>"
                    st.components.v1.html(html_content, height=450, scrolling=True)

                with tab_pronostici_ia:
                    mod_testo = "Dati Reali (Casa vs Trasferta)" if simula_reale else "Media Stagionale Globale"
                    st.markdown("### 🧠 Centrale Pronostici IA: 1X2, Multigol & Bussola Tattica")
                    st.markdown(f"<p style='color:#a0a0a0; font-size:0.9em;'>Motore predittivo basato su distribuzione di Poisson, fattore campo, incrocio difensivo (xGA) e volume di tiro (Modalità: <b>{mod_testo}</b>).</p>", unsafe_allow_html=True)

                    if simula_reale:
                        xg_base_1 = (dati_sq1.get('xG Casa', 1.0) + dati_sq2.get('xGA Trasferta', 1.0)) / 2.0
                        xg_base_2 = (dati_sq2.get('xG Trasferta', 1.0) + dati_sq1.get('xGA Casa', 1.0)) / 2.0
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
                    else:
                        xg_base_1 = ((dati_sq1.get('xG Casa',0)+dati_sq1.get('xG Trasferta',0))/2.0 + (dati_sq2.get('xGA Casa',0)+dati_sq2.get('xGA Trasferta',0))/2.0) / 2.0
                        xg_base_2 = ((dati_sq2.get('xG Casa',0)+dati_sq2.get('xG Trasferta',0))/2.0 + (dati_sq1.get('xGA Casa',0)+dati_sq1.get('xGA Trasferta',0))/2.0) / 2.0
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

                    fattore_tp_1 = max(0.85, min(1.18, tp_1 / media_tp_1)) if media_tp_1 > 0 else 1.0
                    fattore_tp_2 = max(0.85, min(1.18, tp_2 / media_tp_2)) if media_tp_2 > 0 else 1.0

                    gol_sq1 = ((xg_base_1 * 0.85) + (xg_base_1 * fattore_tp_1 * 0.15)) * 1.06
                    gol_sq2 = ((xg_base_2 * 0.85) + (xg_base_2 * fattore_tp_2 * 0.15)) * 0.94
                    xg_totali_match = gol_sq1 + gol_sq2

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

                    p_1x = p_1 + p_x
                    p_x2 = p_x + p_2

                    qf_1 = 100 / p_1 if p_1 > 0 else 99.0
                    qf_x = 100 / p_x if p_x > 0 else 99.0
                    qf_2 = 100 / p_2 if p_2 > 0 else 99.0
                    qf_1x = 100 / p_1x if p_1x > 0 else 99.0
                    qf_x2 = 100 / p_x2 if p_x2 > 0 else 99.0

                    risultati_esatti.sort(key=lambda x: x[1])
                    top_2_ris = f"{risultati_esatti[-1][0]} ({risultati_esatti[-1][1]:.1f}%)  |  {risultati_esatti[-2][0]} ({risultati_esatti[-2][1]:.1f}%)"

                    if p_1 >= 56:
                        esito_consigliato = f"1 FISSO ({squadra_1})"
                        prob_esito = p_1
                        qf_esito = qf_1
                        col_esito = "#00cc66"
                    elif p_2 >= 56:
                        esito_consigliato = f"2 FISSO ({squadra_2})"
                        prob_esito = p_2
                        qf_esito = qf_2
                        col_esito = "#ff4b4b"
                    elif p_1 >= 44:
                        esito_consigliato = f"DOPPIA CHANCE 1X ({squadra_1} o Pareggio)"
                        prob_esito = p_1x
                        qf_esito = qf_1x
                        col_esito = "#00cc66"
                    elif p_2 >= 44:
                        esito_consigliato = f"DOPPIA CHANCE X2 ({squadra_2} o Pareggio)"
                        prob_esito = p_x2
                        qf_esito = qf_x2
                        col_esito = "#ff4b4b"
                    else:
                        esito_consigliato = "GARA IN EQUILIBRIO (Meglio Mercati Gol / Statistiche)"
                        prob_esito = max(p_1x, p_x2)
                        qf_esito = 100 / prob_esito if prob_esito > 0 else 1.50
                        col_esito = "#ffb703"

                    st.markdown(f"""
                    <div class="glass-box" style="border-top: 4px solid {col_esito}; padding: 20px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                            <div>
                                <p style="margin:0; font-size:0.75em; color:#888; text-transform:uppercase; letter-spacing:1px;">Esito Principale Consigliato dall'IA</p>
                                <h2 style="margin: 4px 0; color: {col_esito}; font-family: 'JetBrains Mono', monospace;">🏆 {esito_consigliato}</h2>
                                <p style="margin:0; font-size:0.85em; color:#ccc;">Probabilità Stimata: <b>{prob_esito:.1f}%</b> | Quota Fair: <b>{qf_esito:.2f}</b> &nbsp;•&nbsp; 🎯 Risultati più probabili: <b>{top_2_ris}</b></p>
                            </div>
                            <div style="display: flex; gap: 15px; margin-top: 10px;">
                                <div style="background: rgba(0,204,102,0.1); border: 1px solid rgba(0,204,102,0.3); padding: 8px 14px; border-radius: 10px; text-align: center;">
                                    <span style="font-size:0.75em; color:#aaa;">SEGNO 1</span><br>
                                    <b style="color:#00cc66; font-family:'JetBrains Mono', monospace; font-size:1.15em;">{p_1:.1f}%</b><br>
                                    <span style="font-size:0.7em; color:#888;">Fair: {qf_1:.2f}</span>
                                </div>
                                <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.15); padding: 8px 14px; border-radius: 10px; text-align: center;">
                                    <span style="font-size:0.75em; color:#aaa;">SEGNO X</span><br>
                                    <b style="color:#fff; font-family:'JetBrains Mono', monospace; font-size:1.15em;">{p_x:.1f}%</b><br>
                                    <span style="font-size:0.7em; color:#888;">Fair: {qf_x:.2f}</span>
                                </div>
                                <div style="background: rgba(255,75,75,0.1); border: 1px solid rgba(255,75,75,0.3); padding: 8px 14px; border-radius: 10px; text-align: center;">
                                    <span style="font-size:0.75em; color:#aaa;">SEGNO 2</span><br>
                                    <b style="color:#ff4b4b; font-family:'JetBrains Mono', monospace; font-size:1.15em;">{p_2:.1f}%</b><br>
                                    <span style="font-size:0.7em; color:#888;">Fair: {qf_2:.2f}</span>
                                </div>
                            </div>
                        </div>
                        <div style="margin-top: 14px; display: flex; width: 100%; height: 10px; border-radius: 6px; overflow: hidden;">
                            <div style="width: {p_1}%; background: #00cc66;" title="1: {p_1:.1f}%"></div>
                            <div style="width: {p_x}%; background: #888888;" title="X: {p_x:.1f}%"></div>
                            <div style="width: {p_2}%; background: #ff4b4b;" title="2: {p_2:.1f}%"></div>
                        </div>
                        <div style="display:flex; justify-content:space-between; font-size:0.78em; color:#999; margin-top:8px; font-family:'JetBrains Mono', monospace;">
                            <span>Doppia Chance 1X: <b style="color:#fff;">{p_1x:.1f}%</b> (Fair {qf_1x:.2f})</span>
                            <span>Gol Totali Attesi nel Match: <b style="color:#00cc66;">{xg_totali_match:.2f} xG</b></span>
                            <span>Doppia Chance X2: <b style="color:#fff;">{p_x2:.1f}%</b> (Fair {qf_x2:.2f})</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    def analizza_squadra_ia(lmbda, tiri_tot, tiri_porta):
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

                        rapporto_xg_tiri = lmbda / tiri_tot if tiri_tot > 0 else 0.10
                        if lmbda >= 1.45 and rapporto_xg_tiri >= 0.125:
                            bussola = "🎯 <b>SQUADRA CINICA:</b> Segna con pochi tiri (rischio sblocco rapido e calo di ritmo). <b>Meglio Multigol / 1X2</b> rispetto a Tiri/Corner."
                        elif tiri_tot >= 13.0 and rapporto_xg_tiri < 0.115:
                            bussola = "🔥 <b>ALTO VOLUME D'ASSEDIO:</b> Tira tantissimo ma fatica a chiuderla. Scenario <b>TOP per Over Tiri e Corner</b>."
                        else:
                            bussola = "⚖️ <b>PRODUZIONE BILANCIATA:</b> Equilibrio tra occasioni create e volume di tiro. Valido sia il <b>Multigol</b> sia le <b>Statistiche</b>."

                        return consiglio, prob_scelta, quota_fair, mg_1_2, mg_1_3, mg_2_3, bussola

                    cons_1, prob_1, qf_1_mg, m12_1, m13_1, m23_1, buss_1 = analizza_squadra_ia(l1, tt_1, tp_1)
                    cons_2, prob_2, qf_2_mg, m12_2, m13_2, m23_2, buss_2 = analizza_squadra_ia(l2, tt_2, tp_2)

                    col_mg1, col_mg2 = st.columns(2)
                    
                    with col_mg1:
                        st.markdown(f"""
                        <div class="glass-box" style="border-left: 5px solid #00cc66;">
                            <h4 style="margin:0; color:#00cc66;">🏠 {squadra_1} (xG Incrociati: {l1:.2f})</h4>
                            <p style="margin: 8px 0 4px 0; font-size: 0.82em; color: #aaa;">Multigol Squadra Consigliato:</p>
                            <h2 style="margin:0; color:#fff; font-family:'JetBrains Mono', monospace;">⚽ {cons_1}</h2>
                            <p style="margin: 4px 0 12px 0; font-size: 0.85em; color: #00cc66;">Probabilità: <b>{prob_1:.1f}%</b> | Quota Fair: <b>{qf_1_mg:.2f}</b></p>
                            <div style="background: rgba(0,0,0,0.25); padding: 10px; border-radius: 8px; font-size: 0.8em; color: #ddd; margin-bottom: 12px;">
                                {buss_1}
                            </div>
                            <div style="display:flex; justify-content:space-between; font-size:0.8em; color:#aaa; font-family:'JetBrains Mono', monospace;">
                                <span>MG 1-2: <b style="color:#fff;">{m12_1:.1f}%</b></span>
                                <span>MG 1-3: <b style="color:#fff;">{m13_1:.1f}%</b></span>
                                <span>MG 2-3: <b style="color:#fff;">{m23_1:.1f}%</b></span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col_mg2:
                        st.markdown(f"""
                        <div class="glass-box" style="border-left: 5px solid #ff4b4b;">
                            <h4 style="margin:0; color:#ff4b4b;">✈️ {squadra_2} (xG Incrociati: {l2:.2f})</h4>
                            <p style="margin: 8px 0 4px 0; font-size: 0.82em; color: #aaa;">Multigol Squadra Consigliato:</p>
                            <h2 style="margin:0; color:#fff; font-family:'JetBrains Mono', monospace;">⚽ {cons_2}</h2>
                            <p style="margin: 4px 0 12px 0; font-size: 0.85em; color: #ff4b4b;">Probabilità: <b>{prob_2:.1f}%</b> | Quota Fair: <b>{qf_2_mg:.2f}</b></p>
                            <div style="background: rgba(0,0,0,0.25); padding: 10px; border-radius: 8px; font-size: 0.8em; color: #ddd; margin-bottom: 12px;">
                                {buss_2}
                            </div>
                            <div style="display:flex; justify-content:space-between; font-size:0.8em; color:#aaa; font-family:'JetBrains Mono', monospace;">
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
                        
                    st.markdown("<h4 style='margin-top: 30px;'>🧤 Focus Portieri & Indice di Assedio (Scommesse Speciali)</h4>", unsafe_allow_html=True)
                    st.markdown("<p style='color:#a0a0a0; font-size:0.85em;'>Calcola le parate attese incrociando i tiri in porta dell'avversario con la vulnerabilità difensiva della squadra.</p>", unsafe_allow_html=True)
                    
                    molt_difesa_1 = (dati_sq1.get('xGA Casa', 1.25) / 1.25) if simula_reale else 1.0
                    tiri_subiti_1 = tp_2 * molt_difesa_1
                    parate_attese_1 = tiri_subiti_1 * 0.725
                    
                    molt_difesa_2 = (dati_sq2.get('xGA Trasferta', 1.25) / 1.25) if simula_reale else 1.0
                    tiri_subiti_2 = tp_1 * molt_difesa_2
                    parate_attese_2 = tiri_subiti_2 * 0.725
                    
                    def genera_card_portiere(squadra, parate, tiri_subiti, ruolo):
                        if parate >= 3.6:
                            col_badge = "#00cc66"
                            alert = "🔥 ALTO ASSEDIO: Ottimo per OVER Parate Portiere"
                        elif parate <= 2.2:
                            col_badge = "#ff4b4b"
                            alert = "🧊 BASSO ASSEDIO: Rischio Under Parate"
                        else:
                            col_badge = "#ffb703"
                            alert = "⚖️ ASSEDIO MEDIO: Linea standard (2-3 parate)"
                            
                        return f"""
                        <div class="glass-box" style="border-left: 4px solid {col_badge}; padding: 15px; margin-bottom: 0;">
                            <p style="margin: 0; font-size: 0.8em; color: #aaa; text-transform: uppercase;">Portiere {squadra} ({ruolo})</p>
                            <h3 style="margin: 5px 0; color: #fff; font-family: 'JetBrains Mono', monospace;">{parate:.1f} Parate Attese</h3>
                            <p style="margin: 0; font-size: 0.85em; color: #ddd;">Tiri in porta subiti stimati: <b>{tiri_subiti:.1f}</b></p>
                            <div style="margin-top: 10px; background: rgba(0,0,0,0.3); padding: 6px 10px; border-radius: 6px;">
                                <span style="font-size: 0.8em; color: {col_badge}; font-weight: 700;">{alert}</span>
                            </div>
                        </div>
                        """

                    col_gk1, col_gk2 = st.columns(2)
                    with col_gk1:
                        st.markdown(genera_card_portiere(squadra_1, parate_attese_1, tiri_subiti_1, "Casa"), unsafe_allow_html=True)
                    with col_gk2:
                        st.markdown(genera_card_portiere(squadra_2, parate_attese_2, tiri_subiti_2, "Trasferta"), unsafe_allow_html=True)

                    st.markdown("<h4 style='margin-top: 30px;'>🥊 Verdetto IA: Testa a Testa (1X2) Corner & Falli</h4>", unsafe_allow_html=True)
                    st.markdown("<p style='color:#a0a0a0; font-size:0.85em;'>Simulazione del duello statistico diretto calibrata con l'indice di possesso/pressione tattica (Game State).</p>", unsafe_allow_html=True)

                    sub_cor_2, _ = stima_stat_subita(df_selezionato, dati_sq2, 'Trasferta', 'Corner Casa', 'Corner Trasferta')
                    sub_cor_1, _ = stima_stat_subita(df_selezionato, dati_sq1, 'Casa', 'Corner Trasferta', 'Corner Casa')
                    proj_cor_1 = (cor_1 + sub_cor_2) / 2.0 if sub_cor_2 > 0 else cor_1
                    proj_cor_2 = (cor_2 + sub_cor_1) / 2.0 if sub_cor_1 > 0 else cor_2
                    diff_cor = proj_cor_1 - proj_cor_2

                    if diff_cor >= 1.6:
                        verd_cor = f"1 CORNER ({squadra_1})"
                        col_cor = "#00cc66"
                        cons_cor = f"Margine netto (<b>+{diff_cor:.2f}</b>). Ottimo <b>1 Corner</b> o <b>Handicap -1.5</b>."
                    elif diff_cor <= -1.6:
                        verd_cor = f"2 CORNER ({squadra_2})"
                        col_cor = "#ff4b4b"
                        cons_cor = f"Margine netto (<b>{diff_cor:.2f}</b>). Ottimo <b>2 Corner</b> o <b>Handicap -1.5 Ospite</b>."
                    elif diff_cor >= 0.65:
                        verd_cor = f"1 Corner Leggero ({squadra_1})"
                        col_cor = "#00cc66"
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

                    molt_tattico_fal_1 = 1.0 + ((indice_pressione_2 - 0.50) * 0.35) if indice_pressione_2 > 0.52 else 1.0
                    molt_tattico_fal_2 = 1.0 + ((indice_pressione_1 - 0.50) * 0.35) if indice_pressione_1 > 0.52 else 1.0

                    proj_fal_1 = fal_1 * molt_tattico_fal_1
                    proj_fal_2 = fal_2 * molt_tattico_fal_2
                    diff_fal = proj_fal_1 - proj_fal_2

                    if diff_fal >= 1.5:
                        verd_fal = f"PIÙ FALLI: {squadra_1} (Segno 1)"
                        col_fal = "#00cc66"
                        cons_fal = f"Scarto stimato: <b>+{diff_fal:.2f} falli</b>. {squadra_1} più fallosa e costretta a spezzare il gioco."
                    elif diff_fal <= -1.5:
                        verd_fal = f"PIÙ FALLI: {squadra_2} (Segno 2)"
                        col_fal = "#ff4b4b"
                        cons_fal = f"Scarto stimato: <b>{abs(diff_fal):.2f} falli</b> in più per {squadra_2} (pressione difensiva alta)."
                    elif diff_fal >= 0.65:
                        verd_fal = f"Leggera Tendenza Falli: {squadra_1}"
                        col_fal = "#00cc66"
                        cons_fal = f"Vantaggio contenuto (<b>+{diff_fal:.2f} falli</b>). Giocabile solo a quota >= 1.85."
                    elif diff_fal <= -0.65:
                        verd_fal = f"Leggera Tendenza Falli: {squadra_2}"
                        col_fal = "#ff4b4b"
                        cons_fal = f"Vantaggio contenuto (<b>+{abs(diff_fal):.2f} falli</b>). Giocabile solo a quota >= 1.85."
                    else:
                        verd_fal = "EQUILIBRIO FALLI (Rischio X)"
                        col_fal = "#ffb703"
                        cons_fal = f"Scarto irrisorio (<b>{diff_fal:+.2f}</b>). Meglio puntare sull'Over Falli Totale Match."

                    col_h2h_1, col_h2h_2 = st.columns(2)
                    with col_h2h_1:
                        st.markdown(f"""
                        <div class="glass-box" style="border-left: 4px solid {col_cor}; padding: 16px;">
                            <p style="margin: 0; font-size: 0.78em; color: #aaa; text-transform: uppercase;">🚩 Testa a Testa Corner (1X2)</p>
                            <h3 style="margin: 6px 0; color: {col_cor}; font-family: 'JetBrains Mono', monospace;">{verd_cor}</h3>
                            <p style="margin: 0; font-size: 0.85em; color: #ddd;">Proiezione: <b>{squadra_1} ({proj_cor_1:.2f})</b> vs <b>{squadra_2} ({proj_cor_2:.2f})</b></p>
                            <div style="margin-top: 10px; background: rgba(0,0,0,0.3); padding: 8px 10px; border-radius: 6px; font-size: 0.8em; color: #ccc;">
                                💡 {cons_cor}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col_h2h_2:
                        st.markdown(f"""
                        <div class="glass-box" style="border-left: 4px solid {col_fal}; padding: 16px;">
                            <p style="margin: 0; font-size: 0.78em; color: #aaa; text-transform: uppercase;">🛑 Testa a Testa Falli Commessi (1X2)</p>
                            <h3 style="margin: 6px 0; color: {col_fal}; font-family: 'JetBrains Mono', monospace;">{verd_fal}</h3>
                            <p style="margin: 0; font-size: 0.85em; color: #ddd;">Proiezione Tattica: <b>{squadra_1} ({proj_fal_1:.2f})</b> vs <b>{squadra_2} ({proj_fal_2:.2f})</b></p>
                            <div style="margin-top: 10px; background: rgba(0,0,0,0.3); padding: 8px 10px; border-radius: 6px; font-size: 0.8em; color: #ccc;">
                                💡 {cons_fal}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                with tab_scanner:
                    st.markdown("### 📊 Scanner Mercati & Value Bet (Target Singole 1.70 - 2.10)")
                    st.markdown("<p style='color:#a0a0a0;'>Analisi delle linee principali con soglie ricalibrate per le singole pure.</p>", unsafe_allow_html=True)
                    
                    tipo_filtro = st.radio("Filtro Storico Partite:", ["🌍 Globale (Tutte le partite della squadra)", "🏠/✈️ Specifico (Solo partite giocate in Casa / Trasferta)"], horizontal=True)
                    modalita_scanner = "specifico" if "Specifico" in tipo_filtro else "globale"
                    
                    st.divider()
                    
                    tot_1, over_1, goal_1 = calcola_mercati_betting(squadra_1, df_partite, modalita=modalita_scanner, ruolo="casa")
                    tot_2, over_2, goal_2 = calcola_mercati_betting(squadra_2, df_partite, modalita=modalita_scanner, ruolo="trasferta")
                    
                    col_sc1, col_sc2 = st.columns(2)
                    with col_sc1:
                        titolo_sq1 = f"{squadra_1} (In Casa)" if modalita_scanner == "specifico" else squadra_1
                        st.markdown(f"<h3 style='text-align: center; color: #00cc66;'>{titolo_sq1}</h3>", unsafe_allow_html=True)
                        if tot_1 > 0:
                            st.markdown(genera_html_scanner(over_1, goal_1, tot_1, "#00cc66"), unsafe_allow_html=True)
                        else:
                            st.info(f"Nessun dato storico per {titolo_sq1}.")
                            
                    with col_sc2:
                        titolo_sq2 = f"{squadra_2} (In Trasferta)" if modalita_scanner == "specifico" else squadra_2
                        st.markdown(f"<h3 style='text-align: center; color: #ff4b4b;'>{titolo_sq2}</h3>", unsafe_allow_html=True)
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
                        fig_dinamico = px.bar(df_selezionato.sort_values(by=statistica_scelta, ascending=False), x="Squadra", y=statistica_scelta, title=f"Classifica per: {statistica_scelta}", color=statistica_scelta, color_continuous_scale="Greens", text_auto='.2f', template="plotly_dark")
                        fig_dinamico.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
                        fig_dinamico.update_layout(coloraxis_showscale=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family='Outfit'))
                        st.plotly_chart(fig_dinamico, use_container_width=True)
                        
                    with tab_auto:
                        st.markdown("### 🌍 Scanner Universale Value Bet (Serie A + Premier League + La Liga)")
                        st.markdown("<p style='color:#a0a0a0;'>Analizza simultaneamente tutte le partite del foglio <b>'Palinsesto'</b> da Google Fogli con <b>Filtro Anti-Azzardo 1X2</b>.</p>", unsafe_allow_html=True)
                        
                        col_sl1, col_sl2 = st.columns([1, 1])
                        with col_sl1:
                            filtro_eff = st.slider("🎯 Filtro Efficienza Minima (%)", min_value=0, max_value=40, value=4, step=1)
                        with col_sl2:
                            filtro_lega_scanner = st.selectbox("🏆 Filtra Risultati per Campionato:", ["🌍 Tutti i Campionati", "🇮🇹 Serie A", "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League", "🇪🇸 La Liga"])
                        
                        st.divider()
                        
                        df_palinsesto = dati_campionati.get('Palinsesto', pd.DataFrame())
                        
                        if df_palinsesto is None or df_palinsesto.empty:
                            st.warning("⚠️ **Foglio 'Palinsesto' non trovato o vuoto.**")
                            testo_istruzioni = (
                                "Assicurati che il foglio si chiami **`Palinsesto`** e usi queste colonne:\n"
                                "`Squadra Casa` | `Squadra Trasferta` | `Quota 1` | `Quota 2` | `Quota GG` | `Linea Over Tiri` | `Quota Over Tiri` | "
                                "`Linea Over Tiri Porta` | `Quota Over Tiri Porta` | `Linea Over Corner` | `Quota Over Corner` | "
                                "`Linea Over Falli` | `Quota Over Falli`\n\n"
                                "COLONNE SQUADRA SINGOLA (Solo Tiri e Corner):\n"
                                "`Linea Tiri Casa` | `Quota Tiri Casa` | `Linea Tiri Trasferta` | `Quota Tiri Trasferta` | "
                                "`Linea Corner Casa` | `Quota Corner Casa` | `Linea Corner Trasferta` | `Quota Corner Trasferta`"
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
                                for lega_nome in ['Serie A', 'La Liga', 'Premier League']:
                                    df_temp = dati_campionati.get(lega_nome, pd.DataFrame())
                                    if not df_temp.empty and 'Squadra' in df_temp.columns:
                                        if casa in df_temp['Squadra'].values and trasf in df_temp['Squadra'].values:
                                            df_lega_match = df_temp
                                            nome_lega_match = mappa_icone_leghe.get(lega_nome, lega_nome)
                                            break

                                if df_lega_match is None:
                                    continue

                                dati_c = df_lega_match[df_lega_match['Squadra'] == casa].iloc[0]
                                dati_t = df_lega_match[df_lega_match['Squadra'] == trasf].iloc[0]
                                match_name = f"{casa} - {trasf}"

                                q_1 = pd.to_numeric(row.get('Quota 1', 0), errors='coerce')
                                q_2 = pd.to_numeric(row.get('Quota 2', 0), errors='coerce')
                                
                                if (not pd.isna(q_1) and q_1 > 1.0) or (not pd.isna(q_2) and q_2 > 1.0):
                                    xg_base_1 = (dati_c.get('xG Casa', 1.0) + dati_t.get('xGA Trasferta', 1.0)) / 2.0
                                    xg_base_2 = (dati_t.get('xG Trasferta', 1.0) + dati_c.get('xGA Casa', 1.0)) / 2.0
                                    tp_1 = dati_c.get('Tiri in porta Casa', 4.0)
                                    tp_2 = dati_t.get('Tiri in porta Trasferta', 4.0)
                                    media_tp_1 = df_lega_match['Tiri in porta Casa'].mean() if 'Tiri in porta Casa' in df_lega_match.columns else 4.2
                                    media_tp_2 = df_lega_match['Tiri in porta Trasferta'].mean() if 'Tiri in porta Trasferta' in df_lega_match.columns else 3.6
                                    
                                    f_tp_1 = max(0.85, min(1.18, tp_1 / media_tp_1)) if media_tp_1 > 0 else 1.0
                                    f_tp_2 = max(0.85, min(1.18, tp_2 / media_tp_2)) if media_tp_2 > 0 else 1.0
                                    
                                    lmbda_1 = max(0.1, ((xg_base_1 * 0.85) + (xg_base_1 * f_tp_1 * 0.15)) * 1.06)
                                    lmbda_2 = max(0.1, ((xg_base_2 * 0.85) + (xg_base_2 * f_tp_2 * 0.15)) * 0.94)
                                    
                                    probs_1 = [(math.exp(-lmbda_1) * (lmbda_1**k)) / math.factorial(k) for k in range(7)]
                                    probs_2 = [(math.exp(-lmbda_2) * (lmbda_2**k)) / math.factorial(k) for k in range(7)]
                                    
                                    p_1, p_x, p_2 = 0.0, 0.0, 0.0
                                    for i in range(7):
                                        for j in range(7):
                                            p_ij = probs_1[i] * probs_2[j]
                                            if i > j: p_1 += p_ij
                                            elif i == j: p_x += p_ij
                                            else: p_2 += p_ij
                                            
                                    tot_p = p_1 + p_x + p_2
                                    p_1_pura = (p_1 / tot_p) * 100 if tot_p > 0 else 0
                                    p_2_pura = (p_2 / tot_p) * 100 if tot_p > 0 else 0
                                    
                                    if not pd.isna(q_1) and 1.55 <= q_1 <= 2.25:
                                        prob_book_1 = (100 / q_1) * 0.95
                                        prob_blend_1 = (p_1_pura * 0.65) + (prob_book_1 * 0.35)
                                        q_fair_1 = 100 / prob_blend_1 if prob_blend_1 > 0 else 99.0
                                        edge_1 = prob_blend_1 - (100 / q_1)
                                        
                                        if prob_blend_1 >= 52.0 and edge_1 >= 3.0:
                                            risultati_value.append({
                                                'Tipo_Mercato': '1X2',
                                                'Campionato': nome_lega_match,
                                                'Partita': match_name,
                                                'Mercato Consigliato': f"🏆 1 FISSO ({casa})",
                                                'Proiezione WebApp': f"Prob. Calibrata: {prob_blend_1:.1f}%",
                                                'Analisi_Avversario': f"Quota Fair Reale: <b>{q_fair_1:.2f}</b>",
                                                'Stato_Difesa': "🟢 Favorita Solida (Casa)",
                                                'Proiezione_Finale': f"{prob_blend_1:.1f}%",
                                                'Spia_Tattica': "🎯 Esito Finale Validato",
                                                'Linea Eplay24': '-',
                                                'Quota Eplay24': f"{q_1:.2f}",
                                                'Efficienza': edge_1
                                            })
                                            
                                    if not pd.isna(q_2) and 1.55 <= q_2 <= 2.25:
                                        prob_book_2 = (100 / q_2) * 0.95
                                        prob_blend_2 = (p_2_pura * 0.65) + (prob_book_2 * 0.35)
                                        q_fair_2 = 100 / prob_blend_2 if prob_blend_2 > 0 else 99.0
                                        edge_2 = prob_blend_2 - (100 / q_2)
                                        
                                        if prob_blend_2 >= 54.0 and edge_2 >= 3.0:
                                            risultati_value.append({
                                                'Tipo_Mercato': '1X2',
                                                'Campionato': nome_lega_match,
                                                'Partita': match_name,
                                                'Mercato Consigliato': f"🏆 2 FISSO ({trasf})",
                                                'Proiezione WebApp': f"Prob. Calibrata: {prob_blend_2:.1f}%",
                                                'Analisi_Avversario': f"Quota Fair Reale: <b>{q_fair_2:.2f}</b>",
                                                'Stato_Difesa': "🟢 Favorita Solida (Ospite)",
                                                'Proiezione_Finale': f"{prob_blend_2:.1f}%",
                                                'Spia_Tattica': "🎯 Esito Finale Validato",
                                                'Linea Eplay24': '-',
                                                'Quota Eplay24': f"{q_2:.2f}",
                                                'Efficienza': edge_2
                                            })

                                q_gg = pd.to_numeric(row.get('Quota GG', 0), errors='coerce')
                                if not pd.isna(q_gg) and q_gg >= 1.60:
                                    _, _, goal_c = calcola_mercati_betting(casa, df_partite, "globale")
                                    _, _, goal_t = calcola_mercati_betting(trasf, df_partite, "globale")
                                    perc_gg = (goal_c + goal_t) / 2
                                    q_fair_gg = 100 / perc_gg if perc_gg > 0 else 0
                                    edge_gg = perc_gg - (100 / q_gg)
                                    
                                    if perc_gg >= 55.0 and edge_gg >= 3.5:
                                        risultati_value.append({
                                            'Tipo_Mercato': '1X2',
                                            'Campionato': nome_lega_match,
                                            'Partita': match_name,
                                            'Mercato Consigliato': '⚽ GOAL (Entrambe Segnano)',
                                            'Proiezione WebApp': f"{goal_c:.0f}% Casa / {goal_t:.0f}% Ospite",
                                            'Analisi_Avversario': f"Quota Fair Storica: <b>{q_fair_gg:.2f}</b>",
                                            'Stato_Difesa': "🟢 Storico Favorevole",
                                            'Proiezione_Finale': f"{perc_gg:.1f}%",
                                            'Spia_Tattica': "🔥 Gara Aperta / Scambio Gol",
                                            'Linea Eplay24': '-',
                                            'Quota Eplay24': f"{q_gg:.2f}",
                                            'Efficienza': edge_gg
                                        })

                                def aggiungi_mercato_statistico(nome_mercato, col_linea, col_quota, val_casa, val_trasf, col_c, col_t, icona):
                                    linea = pd.to_numeric(row.get(col_linea, 0), errors='coerce')
                                    quota = pd.to_numeric(row.get(col_quota, 0), errors='coerce')
                                    
                                    if not pd.isna(linea) and linea > 0 and not pd.isna(quota) and quota > 1.0:
                                        proiezione_attacchi = val_casa + val_trasf
                                        sub_c, _ = stima_stat_subita(df_lega_match, dati_c, 'Casa', col_t, col_c)
                                        sub_t, _ = stima_stat_subita(df_lega_match, dati_t, 'Trasferta', col_c, col_t)
                                        proiezione_difese = sub_c + sub_t
                                        proiezione_incrociata = (proiezione_attacchi + proiezione_difese) / 2.0
                                        
                                        media_tot_lega = proiezione_attacchi if proiezione_difese == 0 else (df_lega_match[col_c].mean() + df_lega_match[col_t].mean())
                                        if proiezione_difese >= media_tot_lega * 1.05:
                                            stato_dif = "🟢 Difese Permessive"
                                            spia = "🔥 Gara da Assedio Totale"
                                        elif proiezione_difese <= media_tot_lega * 0.95:
                                            stato_dif = "🔴 Difese Chiuse"
                                            spia = "⚠️ Rischio Muro Avversario"
                                        else:
                                            stato_dif = "⚪ Difese Medie"
                                            spia = "⚖️ Ritmo Regolare"

                                        scarto = proiezione_incrociata - linea
                                        eff = (scarto / linea) * 100 
                                        if eff > 0:
                                            risultati_value.append({
                                                'Tipo_Mercato': 'STAT',
                                                'Campionato': nome_lega_match,
                                                'Partita': match_name,
                                                'Mercato Consigliato': f"{icona} OVER {linea} {nome_mercato}",
                                                'Proiezione WebApp': f"{proiezione_attacchi:.2f} (Somma Attacchi)",
                                                'Analisi_Avversario': f"Concessi Difese: <b>{proiezione_difese:.2f}</b>",
                                                'Stato_Difesa': stato_dif,
                                                'Proiezione_Finale': f"{proiezione_incrociata:.2f}",
                                                'Spia_Tattica': spia,
                                                'Linea Eplay24': str(linea),
                                                'Quota Eplay24': f"{quota:.2f}",
                                                'Efficienza': eff
                                            })
                                            
                                def aggiungi_mercato_squadra(nome_mercato, col_linea, col_quota, proiezione_sq, icona, nome_squadra, nome_avv, dati_avv, ruolo_avv, col_att, col_dif):
                                    linea = pd.to_numeric(row.get(col_linea, 0), errors='coerce')
                                    quota = pd.to_numeric(row.get(col_quota, 0), errors='coerce')
                                    
                                    if not pd.isna(linea) and linea > 0 and not pd.isna(quota) and quota > 1.0:
                                        subiti_avv, stato_dif = stima_stat_subita(df_lega_match, dati_avv, ruolo_avv, col_att, col_dif)
                                        proiezione_incrociata = (proiezione_sq + subiti_avv) / 2.0 if subiti_avv > 0 else proiezione_sq
                                        
                                        if "Concede" in stato_dif:
                                            spia = "🔥 Spinta e Rincorsa Costante"
                                        elif "Solida" in stato_dif:
                                            spia = "⚠️ Possibile Vantaggio / Calo"
                                        else:
                                            spia = "⚖️ Copione Regolare"

                                        scarto = proiezione_incrociata - linea
                                        eff = (scarto / linea) * 100 
                                        if eff > 0:
                                            risultati_value.append({
                                                'Tipo_Mercato': 'STAT',
                                                'Campionato': nome_lega_match,
                                                'Partita': match_name,
                                                'Mercato Consigliato': f"{icona} OVER {linea} {nome_mercato} ({nome_squadra})",
                                                'Proiezione WebApp': f"{proiezione_sq:.2f} (Media {nome_squadra})",
                                                'Analisi_Avversario': f"Subiti {nome_avv} ({ruolo_avv}): <b>{subiti_avv:.2f}</b>",
                                                'Stato_Difesa': stato_dif,
                                                'Proiezione_Finale': f"{proiezione_incrociata:.2f}",
                                                'Spia_Tattica': spia,
                                                'Linea Eplay24': str(linea),
                                                'Quota Eplay24': f"{quota:.2f}",
                                                'Efficienza': eff
                                            })

                                tiri_tot_c = dati_c.get('Tiri totali Casa', 0)
                                tiri_tot_t = dati_t.get('Tiri totali Trasferta', 0)
                                aggiungi_mercato_statistico('Tiri Totali', 'Linea Over Tiri', 'Quota Over Tiri', tiri_tot_c, tiri_tot_t, 'Tiri totali Casa', 'Tiri totali Trasferta', '👟')
                                aggiungi_mercato_squadra('Tiri Totali', 'Linea Tiri Casa', 'Quota Tiri Casa', tiri_tot_c, '👟', casa, trasf, dati_t, 'Trasferta', 'Tiri totali Casa', 'Tiri totali Trasferta')
                                aggiungi_mercato_squadra('Tiri Totali', 'Linea Tiri Trasferta', 'Quota Tiri Trasferta', tiri_tot_t, '👟', trasf, casa, dati_c, 'Casa', 'Tiri totali Trasferta', 'Tiri totali Casa')

                                porta_c = dati_c.get('Tiri in porta Casa', 0)
                                porta_t = dati_t.get('Tiri in porta Trasferta', 0)
                                aggiungi_mercato_statistico('Tiri in Porta', 'Linea Over Tiri Porta', 'Quota Over Tiri Porta', porta_c, porta_t, 'Tiri in porta Casa', 'Tiri in porta Trasferta', '🥅')

                                corner_c = dati_c.get('Corner Casa', 0)
                                corner_t = dati_t.get('Corner Trasferta', 0)
                                aggiungi_mercato_statistico('Corner', 'Linea Over Corner', 'Quota Over Corner', corner_c, corner_t, 'Corner Casa', 'Corner Trasferta', '🚩')
                                aggiungi_mercato_squadra('Corner', 'Linea Corner Casa', 'Quota Corner Casa', corner_c, '🚩', casa, trasf, dati_t, 'Trasferta', 'Corner Casa', 'Corner Trasferta')
                                aggiungi_mercato_squadra('Corner', 'Linea Corner Trasferta', 'Quota Corner Trasferta', corner_t, '🚩', trasf, casa, dati_c, 'Casa', 'Corner Trasferta', 'Corner Casa')

                                falli_c = dati_c.get('Falli Commessi Casa', 0)
                                falli_t = dati_t.get('Falli Commessi Trasferta', 0)
                                aggiungi_mercato_statistico('Falli', 'Linea Over Falli', 'Quota Over Falli', falli_c, falli_t, 'Falli Commessi Casa', 'Falli Commessi Trasferta', '🛑')
                            
                            if len(risultati_value) > 0:
                                df_value = pd.DataFrame(risultati_value)
                                
                                if filtro_lega_scanner != "🌍 Tutti i Campionati":
                                    df_value = df_value[df_value['Campionato'] == filtro_lega_scanner]
                                
                                df_value = df_value[df_value['Efficienza'] >= filtro_eff]
                                df_value = df_value.sort_values(by='Efficienza', ascending=False)
                                
                                if df_value.empty:
                                    st.warning(f"😔 Nessuna giocata supera il **{filtro_eff}%** di Efficienza per i filtri selezionati.")
                                else:
                                    st.success(f"✅ Trovate **{len(df_value)}** Giocate Premium per le Singole!")
                                    
                                    counts = df_value['Partita'].value_counts()
                                    partite_ripetute = counts[counts > 1].index.tolist()
                                    
                                    mappa_colori = {}
                                    palette_colori = [
                                        'rgba(0, 204, 102, 0.15)', 
                                        'rgba(0, 153, 255, 0.15)', 
                                        'rgba(255, 153, 0, 0.15)', 
                                        'rgba(204, 0, 204, 0.15)', 
                                        'rgba(255, 51, 51, 0.15)'
                                    ]
                                    
                                    for i, match in enumerate(partite_ripetute):
                                        mappa_colori[match] = palette_colori[i % len(palette_colori)]
                                        
                                    html_cards = ""
                                    for _, bet in df_value.iterrows():
                                        eff = bet['Efficienza']
                                        tipo_m = bet.get('Tipo_Mercato', 'STAT')
                                        nome_match = bet['Partita']
                                        lega_badge = bet['Campionato']
                                        colore_sfondo = mappa_colori.get(nome_match, 'rgba(22, 26, 33, 0.7)')
                                        
                                        if tipo_m == '1X2':
                                            if eff >= 10.0:
                                                col_bordo = "#ff4b4b"
                                                badge = "🔥 SUPER VALUE (1X2)"
                                                puntata = "3 Unità (Rischio Alto)"
                                            elif eff >= 6.0:
                                                col_bordo = "#00cc66"
                                                badge = "🟢 OTTIMA (1X2)"
                                                puntata = "2 Unità (Rischio Medio)"
                                            else:
                                                col_bordo = "#ffb703"
                                                badge = "🟡 BUONA (1X2)"
                                                puntata = "1 Unità (Rischio Basso)"
                                        else:
                                            if eff >= 22.0:
                                                col_bordo = "#ff4b4b"
                                                badge = "🔥 SUPER VALUE"
                                                puntata = "3 Unità (Rischio Alto)"
                                            elif eff >= 13.0:
                                                col_bordo = "#00cc66"
                                                badge = "🟢 OTTIMA"
                                                puntata = "2 Unità (Rischio Medio)"
                                            else:
                                                col_bordo = "#ffb703"
                                                badge = "🟡 BUONA"
                                                puntata = "1 Unità (Rischio Basso)"
                                            
                                        html_cards += f"""
                                        <div style="background: {colore_sfondo}; backdrop-filter: blur(10px); border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); border-left: 5px solid {col_bordo}; padding: 10px 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 8px rgba(0,0,0,0.15); transition: transform 0.2s ease;">
                                            <div style="flex: 1.8; padding-right: 10px;">
                                                <span style="font-size: 0.7em; color: #bbb; background: rgba(255,255,255,0.08); padding: 2px 7px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px;">{lega_badge}</span>
                                                <h4 style="margin: 4px 0 0 0; color: #fff; font-size: 1.05em; font-weight: 700;">{nome_match}</h4>
                                                <p style="margin: 2px 0 2px 0; color: #00cc66; font-weight: 700; font-size: 0.95em;">{bet['Mercato Consigliato']}</p>
                                                <p style="margin: 0; font-size: 0.75em; color: #aaa;">Proiezione: <b>{bet['Proiezione WebApp']}</b> | Linea: <b>{bet['Linea Eplay24']}</b></p>
                                            </div>
                                            <div style="flex: 1.6; text-align: center; border-left: 1px solid rgba(255,255,255,0.1); padding: 0 10px;">
                                                <p style="margin: 0; font-size: 0.68em; color: #888; text-transform: uppercase; letter-spacing: 0.5px;">Analisi & Game State</p>
                                                <p style="margin: 2px 0; font-size: 0.8em; color: #ddd;">{bet['Analisi_Avversario']}</p>
                                                <p style="margin: 2px 0; font-size: 0.72em; color: #00cc66;">{bet['Spia_Tattica']} | Reale: <b style="font-family: JetBrains Mono, monospace;">{bet['Proiezione_Finale']}</b></p>
                                            </div>
                                            <div style="flex: 0.9; text-align: center; border-left: 1px solid rgba(255,255,255,0.1); border-right: 1px solid rgba(255,255,255,0.1); padding: 0 10px;">
                                                <p style="margin: 0; font-size: 0.7em; color: #00cc66; text-transform: uppercase; font-weight: 700; letter-spacing: 1px;">Eplay24</p>
                                                <h2 style="margin: 2px 0 0 0; color: #fff; font-family: 'JetBrains Mono', monospace; font-size: 1.4em;">{bet['Quota Eplay24']}</h2>
                                            </div>
                                            <div style="flex: 1.3; text-align: right; padding-left: 10px;">
                                                <p style="margin: 0; font-size: 0.75em; color: {col_bordo}; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;">{badge}</p>
                                                <h1 style="margin: 0; color: {col_bordo}; font-weight: 800; font-size: 1.6em; font-family: 'JetBrains Mono', monospace;">+{eff:.1f}%</h1>
                                                <p style="margin: 0; font-size: 0.75em; color: #aaa;"><b style="color: #fff;">{puntata}</b></p>
                                            </div>
                                        </div>
                                        """
                                    st.markdown(html_cards, unsafe_allow_html=True)
                            else:
                                st.warning("😔 Nessuna giocata consigliata trovata. Verifica che i nomi delle squadre nel foglio 'Palinsesto' coincidano con quelli dei fogli dei campionati.")

                else:
                    col_logo, col_titolo = st.columns([1, 8])
                    with col_logo:
                        percorso_immagine = f"Stemmi/{squadra_scelta}.png"
                        if os.path.exists(percorso_immagine): st.image(percorso_immagine, width=80)
                        else: st.write("⚽")
                    with col_titolo:
                        st.subheader(f"Profilo Statistico: {squadra_scelta}")
                        forma_str = calcola_forma(squadra_scelta, df_partite)
                        st.markdown(f"**Trend Recente (Ultime 5):** {forma_str}")
                    
                    st.divider()
                    
                    dati_squadra = df_selezionato[df_selezionato['Squadra'] == squadra_scelta].iloc[0]
                    
                    tot_p, perc_over, perc_goal = calcola_mercati_betting(squadra_scelta, df_partite, modalita="globale")
                    if tot_p > 0:
                        st.markdown("### 🎯 Scanner Mercati Storici (Globale)")
                        st.markdown(genera_html_scanner(perc_over, perc_goal, tot_p, "#00cc66"), unsafe_allow_html=True)
                        st.divider()
                    
                    st.markdown("### ⚔️ Fase Offensiva")
                    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("🎯 xG Casa", formatta_numero(dati_squadra.get('xG Casa', 0)))
                    c2.metric("🎯 xG Trasferta", formatta_numero(dati_squadra.get('xG Trasferta', 0)))
                    c3.metric("🥅 Tiri porta (Casa)", formatta_numero(dati_squadra.get('Tiri in porta Casa', 0)))
                    c4.metric("🥅 Tiri porta (Trasferta)", formatta_numero(dati_squadra.get('Tiri in porta Trasferta', 0)))
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown("### 🛡️ Fase Difensiva")
                    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
                    c5, c6, c7, c8 = st.columns(4)
                    c5.metric("🛡️ xGA Subiti (Casa)", formatta_numero(dati_squadra.get('xGA Casa', 0)))
                    c6.metric("🛡️ xGA Subiti (Trasferta)", formatta_numero(dati_squadra.get('xGA Trasferta', 0)))
                    c7.metric("🚩 Corner (Casa)", formatta_numero(dati_squadra.get('Corner Casa', 0)))
                    c8.metric("🚩 Corner (Trasferta)", formatta_numero(dati_squadra.get('Corner Trasferta', 0)))
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

st.sidebar.markdown(
    """
    <div style="margin-top: 60px; padding-top: 15px; border-top: 1px solid rgba(255, 255, 255, 0.05); color: #666; font-size: 0.85em; text-align: left;">
        <span style="font-weight: 600; color: #888; font-family: 'Outfit', sans-serif;">by Alessandro Gusmeroli</span>
    </div>
    """,
    unsafe_allow_html=True
)
