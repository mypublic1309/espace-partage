import streamlit as st
import json
import os
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Arsène Solutions - Espace Partagé", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- STYLE CSS PERSONNALISÉ (DESIGN ULTRA-MODERNE) ---
st.markdown("""
    <style>
    /* Import de polices modernes */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fond dégradé dynamique */
    .stApp {
        background: radial-gradient(circle at top right, #1e1e2f, #0b0b15);
        color: #ffffff;
    }
    
    /* En-têtes stylisés */
    h1, h2, h3 {
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }

    /* Boîtes de contenu premium */
    div[data-testid="stExpander"], .stContainer {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(10px);
        padding: 20px;
    }

    /* Inputs personnalisés */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(0, 210, 255, 0.3) !important;
        border-radius: 12px !important;
    }

    /* Boutons principaux */
    .stButton>button {
        background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 210, 255, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 210, 255, 0.5);
        border: none !important;
    }

    /* Section Premium Or */
    .premium-card {
        background: linear-gradient(145deg, rgba(255, 215, 0, 0.1), rgba(255, 140, 0, 0.05));
        border: 1px solid rgba(255, 215, 0, 0.4);
        border-radius: 24px;
        padding: 25px;
        text-align: center;
        margin: 20px 0;
        position: relative;
        overflow: hidden;
    }

    .premium-badge {
        position: absolute;
        top: 10px;
        right: 10px;
        background: #ffd700;
        color: black;
        font-size: 10px;
        font-weight: bold;
        padding: 2px 8px;
        border-radius: 20px;
    }

    /* Boutons de téléchargement et liens */
    .custom-link-btn {
        display: block;
        text-align: center;
        padding: 15px;
        border-radius: 14px;
        text-decoration: none !important;
        font-weight: bold;
        margin: 10px 0;
        transition: 0.3s;
    }
    
    .btn-download { background: linear-gradient(90deg, #2ecc71, #27ae60); color: white !important; }
    .btn-premium { background: linear-gradient(90deg, #ffd700, #f39c12); color: #000 !important; }
    .btn-whatsapp { background: #25D366; color: white !important; }
    .btn-claim { background: #e74c3c; color: white !important; }
    .btn-outline { border: 1px solid #00d2ff; color: #00d2ff !important; }

    .custom-link-btn:hover { opacity: 0.9; transform: scale(1.02); }

    /* Suppression du padding Streamlit inutile */
    .block-container { padding-top: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE DE DONNÉES ---
DATA_FILE = "arsene_db.json"

def init_db():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"demandes": {}, "liens": {}}, f)

def load_data():
    init_db()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"demandes": {}, "liens": {}}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# Initialisation session_state
if "db" not in st.session_state:
    st.session_state.db = load_data()

# --- CONSTANTES ---
WHATSAPP_NUMBER = "2250171542505"

def get_whatsapp_link(msg):
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={msg.replace(' ', '%20')}"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #ffd700 !important;'>👑 ARSÈNE</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.write("**Expertise Digitale & IA**")
    st.info("Conception de documents intelligents et solutions d'automatisation sur mesure.")
    
    st.markdown(f'<a href="{get_whatsapp_link("Bonjour, je souhaite des informations sur vos services.")}" class="custom-link-btn btn-whatsapp">💬 Support WhatsApp</a>', unsafe_allow_html=True)
    st.write("---")
    st.caption("v2.2 | © 2025 Arsène Investissement")

# --- HEADER PRINCIPAL ---
col_logo, col_title = st.columns([1, 5])
with col_title:
    st.title("Génération Documentaire par IA")
    st.write("Transformez vos idées en fichiers professionnels (Excel, Word, PDF, Scripts).")

# --- SECTION PREMIUM ---
st.markdown(f"""
    <div class="premium-card">
        <div class="premium-badge">NEW</div>
        <h2 style="margin:0; color:#ffd700 !important;">⭐ ACCÈS PREMIUM IA</h2>
        <p style="color: rgba(255,255,255,0.8); font-size: 1.1em; margin: 15px 0;">
            <b>Vitesse Instantanée ($10^{{10}}$)</b> • Précision Algorithmique • Support Prioritaire<br>
            <i>Libérez-vous des délais de la version gratuite (2h d'attente).</i>
        </p>
        <a href="{get_whatsapp_link("Je souhaite activer mon accès Premium pour une livraison instantanée.")}" class="custom-link-btn btn-premium">✨ ACTIVER LA PUISSANCE IA</a>
    </div>
""", unsafe_allow_html=True)

# --- ONGLETS PRINCIPAUX ---
tab_create, tab_retrieve, tab_help = st.tabs(["🚀 Nouvelle Demande", "📂 Récupérer mon Fichier", "❓ Aide & Délais"])

with tab_create:
    st.subheader("Décrivez votre projet")
    with st.container():
        user_id = st.text_input("Votre Identifiant / Prénom", placeholder="Ex: Marc_225").strip()
        user_prompt = st.text_area("Que doit générer l'IA pour vous ?", placeholder="Ex: Un fichier Excel de gestion de stock avec calcul de marge automatique et graphique de tendance...", height=150)
        
        col_btn, col_info = st.columns([1, 2])
        with col_btn:
            if st.button("LANCER L'IA"):
                if user_id and user_prompt:
                    st.session_state.db["demandes"][user_id] = {
                        "prompt": user_prompt,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    save_data(st.session_state.db)
                    st.balloons()
                    st.success("✅ Demande enregistrée ! L'IA travaille sur votre dossier.")
                else:
                    st.error("⚠️ Veuillez remplir tous les champs.")
        with col_info:
            st.caption("🕒 Version gratuite : Traitement sous 1 à 2 heures.")
            st.caption("📂 Formats : .xlsx, .docx, .ps1, .py, .pdf")

with tab_retrieve:
    st.subheader("Espace de téléchargement")
    search_id = st.text_input("Saisissez votre Identifiant pour vérifier l'état :", key="search_bar").strip()
    
    if search_id:
        if search_id in st.session_state.db["liens"]:
            st.success(f"✨ Félicitations {search_id} ! Votre livrable est prêt.")
            file_url = st.session_state.db["liens"][search_id]
            st.markdown(f'<a href="{file_url}" target="_blank" class="custom-link-btn btn-download">⬇️ TÉLÉCHARGER MON FICHIER</a>', unsafe_allow_html=True)
            st.info("Le lien s'ouvrira dans un nouvel onglet.")
        elif search_id in st.session_state.db["demandes"]:
            st.warning(f"⏳ Patience... Votre demande pour '{search_id}' est en cours d'analyse.")
            st.markdown(f"""
                <div style="padding: 15px; background: rgba(0,210,255,0.1); border-radius: 10px;">
                    <b>Statut :</b> En file d'attente (Gratuit)<br>
                    <b>Heure de dépôt :</b> {st.session_state.db['demandes'][search_id]['timestamp']}
                </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            st.write("**L'attente est trop longue ?**")
            claim_msg = f"Bonjour, je souhaite réclamer mon fichier car l'attente est longue. Mon identifiant est : {search_id}"
            st.markdown(f'<a href="{get_whatsapp_link(claim_msg)}" target="_blank" class="custom-link-btn btn-claim">🚩 RÉCLAMER MON FICHIER (WhatsApp)</a>', unsafe_allow_html=True)
            
            col_rel, col_sup = st.columns(2)
            with col_rel:
                rel_link = get_whatsapp_link(f"Relance de ma demande IA pour l'identifiant : {search_id}")
                st.markdown(f'<a href="{rel_link}" class="custom-link-btn btn-outline">🔔 Relancer l\'IA</a>', unsafe_allow_html=True)
            with col_sup:
                sup_link = get_whatsapp_link(f"Aide technique requise pour l'identifiant : {search_id}")
                st.markdown(f'<a href="{sup_link}" class="custom-link-btn btn-outline">🙋 Aide en direct</a>', unsafe_allow_html=True)
        else:
            st.error("🔍 Aucun dossier trouvé à ce nom. Vérifiez l'orthographe ou créez une demande.")

with tab_help:
    st.markdown("""
    ### 🏁 Guide d'utilisation rapide
    1. **Dépôt** : Vous décrivez votre besoin.
    2. **Traitement** : Notre IA structure les données et génère le fichier.
    3. **Livraison** : Vous récupérez le lien de téléchargement ici-même.
    
    ### ⏱️ Délais constatés
    - **Standard (Gratuit)** : 60 à 120 minutes.
    - **Premium (VIP)** : Moins de 60 secondes.
    
    ### 🔒 Sécurité
    Tous les fichiers sont scannés contre les virus et hébergés sur des serveurs sécurisés.
    """)

# --- CONSOLE ADMIN ---
st.write("")
st.markdown("---")
with st.expander("🛠️ Administration Système"):
    admin_code = st.text_input("Code d'accès", type="password")
    if admin_code == "02110240":
        st.subheader("Gestion des livraisons")
        
        pending = st.session_state.db["demandes"]
        if not pending:
            st.write("Aucune demande en attente.")
        else:
            for client, details in list(pending.items()):
                with st.container():
                    st.write(f"👤 **{client}** | 📅 {details['timestamp']}")
                    st.info(f"📝 {details['prompt']}")
                    
                    link_input = st.text_input(f"Lien Cloud pour {client}", key=f"inp_{client}")
                    if st.button(f"LIVRER À {client.upper()}", key=f"btn_{client}"):
                        if link_input:
                            st.session_state.db["liens"][client] = link_input
                            del st.session_state.db["demandes"][client]
                            save_data(st.session_state.db)
                            st.rerun()
                        else:
                            st.warning("Veuillez entrer un lien.")
                    st.write("---")
        
        if st.button("Nettoyer la base de données (Liens uniquement)"):
            st.session_state.db["liens"] = {}
            save_data(st.session_state.db)
            st.rerun()