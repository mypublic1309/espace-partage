import streamlit as st
import json
import os
import hashlib
import time
from datetime import datetime
import streamlit.components.v1 as components

# ==========================================
# CONFIGURATION ET CONSTANTES
# ==========================================
st.set_page_config(
    page_title="Arsène Solutions - Accès Rapide", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "data_arsene_v3.json"
ADMIN_CODE = "02110240"

# --- CONFIGURATION WHATSAPP ---
WHATSAPP_NUMBER = "2250171542505"
PREMIUM_MSG = "J'aimerais passer à la version premium pour bénéficier de la puissance de l'IA et de la rapidité 10^10"
SUPPORT_MSG = "Bonjour, j'ai besoin d'aide avec mon projet sur l'espace client."

# Encodage manuel des espaces pour les liens
whatsapp_premium_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={PREMIUM_MSG.replace(' ', '%20')}"
whatsapp_support_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={SUPPORT_MSG.replace(' ', '%20')}"


# ==========================================
# LOGIQUE DE DONNÉES (DATA LAYER)
# ==========================================

def load_db():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"users": {}, "demandes": [], "liens": {}}
    return {"users": {}, "demandes": [], "liens": {}}

def save_db(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

if "db" not in st.session_state:
    st.session_state["db"] = load_db()

if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

if "view" not in st.session_state:
    st.session_state["view"] = "home"

if "is_glowing" not in st.session_state:
    st.session_state["is_glowing"] = False

# Reconnaissance automatique via URL (Session persistante)
if st.session_state["current_user"] is None:
    stored_user = st.query_params.get("user_id")
    if stored_user and stored_user in st.session_state["db"]["users"]:
        st.session_state["current_user"] = stored_user

# ==========================================
# DESIGN ET STYLE (CSS AVANCÉ)
# ==========================================

def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
        
        * { font-family: 'Poppins', sans-serif; }

        /* FOND APP */
        .stApp {
            background: #0f0c29;
            background: -webkit-linear-gradient(to right, #24243e, #302b63, #0f0c29);
            background: linear-gradient(to right, #24243e, #302b63, #0f0c29);
            color: #ffffff;
            transition: filter 0.5s ease;
        }
        
        /* EFFET D'ILLUMINATION GLOBALE */
        @keyframes glow-pulse {
            0% { filter: brightness(1) saturate(1); box-shadow: inset 0 0 0px transparent; }
            50% { filter: brightness(1.8) saturate(1.5); box-shadow: inset 0 0 100px rgba(0, 210, 255, 0.5); }
            100% { filter: brightness(1) saturate(1); box-shadow: inset 0 0 0px transparent; }
        }

        /* TITRE PRINCIPAL */
        .main-title {
            background: linear-gradient(90deg, #00d2ff, #3a7bd5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 3.5rem !important;
            text-align: center;
            margin-bottom: 20px;
            text-shadow: 0px 0px 20px rgba(0, 210, 255, 0.3);
        }

        /* --- STYLISATION DES ONGLETS (TABS) --- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 20px;
            background-color: rgba(255, 255, 255, 0.05);
            padding: 10px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .stTabs [data-baseweb="tab"] {
            height: 60px;
            white-space: pre-wrap;
            background-color: rgba(0, 210, 255, 0.1);
            border-radius: 10px;
            color: white !important;
            font-weight: 700 !important;
            font-size: 1.2rem !important;
            transition: all 0.3s ease;
            border: 1px solid transparent;
            padding: 0 25px;
        }

        /* Animation spécifique pour l'onglet "Mes Fichiers" (le 2ème onglet) */
        .stTabs [data-baseweb="tab"]:nth-child(2) {
            border: 1px solid #2ecc71 !important;
            box-shadow: 0 0 15px rgba(46, 204, 113, 0.2);
            background-color: rgba(46, 204, 113, 0.1);
        }

        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(0, 210, 255, 0.3);
            transform: translateY(-2px);
        }

        .stTabs [aria-selected="true"] {
            background-color: rgba(0, 210, 255, 0.6) !important;
            border: 1px solid #00d2ff !important;
            box-shadow: 0 0 20px rgba(0, 210, 255, 0.4);
        }

        /* --- CARTE PREMIUM --- */
        .premium-card {
            background: rgba(20, 20, 30, 0.8);
            border: 2px solid #FFD700;
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 0 30px rgba(255, 215, 0, 0.2);
            position: relative;
            overflow: hidden;
        }
        
        .premium-card::before {
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 5px;
            background: linear-gradient(90deg, #FFD700, #FF8C00, #FFD700);
        }

        .premium-title {
            color: #FFD700 !important;
            font-size: 1.5rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 10px;
            letter-spacing: 1px;
        }

        .premium-desc {
            color: #ffffff !important;
            font-size: 1rem;
            margin-bottom: 20px;
            line-height: 1.5;
        }

        /* BOUTON PREMIUM OR */
        .btn-gold {
            background: linear-gradient(45deg, #FFD700, #FF8C00);
            color: #000 !important;
            padding: 12px 30px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 800;
            font-size: 1.1rem;
            display: inline-block;
            box-shadow: 0 5px 15px rgba(255, 215, 0, 0.4);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .btn-gold:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 25px rgba(255, 215, 0, 0.6);
        }

        /* --- ELEMENTS DE FORMULAIRE --- */
        .stTextInput label, .stSelectbox label, .stTextArea label {
            color: #00d2ff !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            margin-bottom: 5px;
        }
        
        div[data-baseweb="input"], textarea, div[data-baseweb="select"] > div {
            border: 1px solid rgba(0, 210, 255, 0.3) !important;
            background-color: rgba(0, 0, 0, 0.5) !important;
            color: white !important;
            border-radius: 10px !important;
        }

        /* BOUTONS STREAMLIT */
        .stButton>button {
            border-radius: 12px;
            padding: 0.8rem 2rem;
            background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
            border: none;
            color: white !important;
            font-weight: 700;
            font-size: 1.1rem;
            width: 100%;
            margin-top: 10px;
            box-shadow: 0 4px 10px rgba(0, 210, 255, 0.3);
            transition: 0.3s;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 210, 255, 0.5);
        }

        /* --- INFO BOX (Sidebar) --- */
        .info-card {
            background: rgba(0, 0, 0, 0.4) !important;
            border-left: 4px solid #00d2ff;
            padding: 15px;
            border-radius: 0 10px 10px 0;
            margin-bottom: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        }
        .info-title {
            color: #00d2ff !important;
            font-weight: bold;
            font-size: 1.1rem;
            display: block;
            margin-bottom: 8px;
            text-transform: uppercase;
        }

        /* --- CARTE DE LIVRABLE --- */
        .file-card {
            background: rgba(255, 255, 255, 0.08);
            border: 2px solid rgba(46, 204, 113, 0.5);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            animation: slideIn 0.5s ease;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* BOUTON SUPPORT */
        .support-btn {
            display: block;
            text-decoration: none;
            background: transparent;
            border: 2px solid #25D366;
            color: #25D366 !important;
            padding: 10px;
            border-radius: 10px;
            font-weight: bold;
            text-align: center;
            margin-top: 10px;
            transition: 0.3s;
        }
        .support-btn:hover {
            background: #25D366;
            color: white !important;
        }

        /* STYLE POUR LA BARRE DE PROGRESSION CUSTOM */
        .stProgress > div > div > div > div {
            background-image: linear-gradient(to right, #00d2ff , #3a7bd5);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Injection dynamique de la classe d'illumination
    if st.session_state["is_glowing"]:
        st.markdown('<style>.stApp { animation: glow-pulse 1.5s ease-in-out infinite; }</style>', unsafe_allow_html=True)

# ==========================================
# PAGES ET COMPOSANTS
# ==========================================

def show_auth_page():
    """Page de connexion Simplifiée (ID + WhatsApp)."""
    st.markdown("<h1 class='main-title'>CONNEXION CLIENT</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(0,0,0,0.4); padding: 20px; border-radius: 15px; border: 1px solid rgba(0,210,255,0.2);">
            <h3 style="color:white; margin-top:0;">🔐 J'ai déjà un compte</h3>
        </div>
        """, unsafe_allow_html=True)
        with st.form("login"):
            uid = st.text_input("Votre Identifiant")
            wa_auth = st.text_input("Votre Numéro WhatsApp", placeholder="Ex: 22501...")
            if st.form_submit_button("ACCÉDER À MON ESPACE"):
                db = st.session_state["db"]
                if uid in db["users"] and db["users"][uid]["whatsapp"] == wa_auth:
                    st.session_state["current_user"] = uid
                    st.session_state["view"] = "home"
                    st.query_params["user_id"] = uid
                    st.rerun()
                else:
                    st.error("❌ Identifiant ou numéro incorrect.")

    with col2:
        st.markdown("""
        <div style="background: rgba(0,0,0,0.4); padding: 20px; border-radius: 15px; border: 1px solid rgba(255,215,0,0.2);">
            <h3 style="color:white; margin-top:0;">✨ Je suis nouveau</h3>
        </div>
        """, unsafe_allow_html=True)
        with st.form("signup"):
            new_uid = st.text_input("Choisissez un Identifiant")
            new_wa = st.text_input("Votre Numéro WhatsApp (Sera votre mot de passe)")
            if st.form_submit_button("CRÉER MON COMPTE GRATUIT"):
                if new_uid and new_wa:
                    db = st.session_state["db"]
                    if new_uid not in db["users"]:
                        db["users"][new_uid] = {
                            "whatsapp": new_wa,
                            "email": "Non renseigné",
                            "joined": str(datetime.now())
                        }
                        st.session_state["current_user"] = new_uid
                        st.session_state["view"] = "home"
                        save_db(db)
                        st.query_params["user_id"] = new_uid
                        st.rerun()
                    else:
                        st.warning("⚠️ Cet identifiant est déjà pris.")
                else:
                    st.error("Champs obligatoires manquants.")

def main_dashboard():
    """Tableau de bord principal."""
    user = st.session_state["current_user"]
    db = st.session_state["db"]
    
    # --- BARRE LATÉRALE ---
    with st.sidebar:
        st.markdown(f"### 👤 {user if user else 'Invité'}")
        if user:
            st.markdown(f"📱 **{db['users'][user]['whatsapp']}**")
            if st.button("Déconnexion"):
                st.session_state["current_user"] = None
                st.query_params.clear()
                st.rerun()
        else:
            if st.button("Se connecter"):
                st.session_state["view"] = "auth"
                st.rerun()
        
        st.divider()
        
        # BOÎTES D'INFO STYLISÉES
        st.markdown(f"""
            <div class="info-card">
                <span class="info-title">🚀 LIVRAISON & ALERTES</span>
                <span style="color:#eee; font-size:0.9rem;">
                    Vos fichiers apparaissent directement dans l'onglet <b>"📂 MES FICHIERS"</b>.
                    <br><br>
                    Une notification WhatsApp vous informe dès que le travail est prêt.
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        # Bouton d'aide Sidebar
        st.markdown(f'<a href="{whatsapp_support_url}" target="_blank" class="support-btn">💬 Service Client</a>', unsafe_allow_html=True)

    # --- CORPS DE PAGE ---
    st.markdown("<h1 class='main-title'>ARSÈNE SOLUTIONS</h1>", unsafe_allow_html=True)

    # --- BANNIÈRE PREMIUM ---
    st.markdown(f"""
        <div class="premium-card">
            <div class="premium-title">⭐ PASSEZ À LA VITESSE SUPÉRIEURE ⭐</div>
            <div class="premium-desc">
                Débloquez la <b>puissance totale de l'IA</b> et une vitesse de traitement de <b>10<sup>10</sup></b>.
            </div>
            <a href="{whatsapp_premium_url}" target="_blank" class="btn-gold">
                💎 ACTIVER LE PREMIUM
            </a>
        </div>
    """, unsafe_allow_html=True)

    # UTILISATION D'ONGLETS TRÈS VISIBLES
    tab1, tab2 = st.tabs(["🚀 LANCER UNE TÂCHE", "📂 MES FICHIERS (ESPACE CLIENT)"])

    with tab1:
        col_f, col_wa = st.columns(2)
        with col_f:
            st.markdown("#### 🛠️ Sélectionnez un service")
            service = st.selectbox(
                "Type de demande", 
                [
                    "📊 Automatisation Excel Avancée", 
                    "📝 Rédaction & Correction", 
                    "⚙️ Script Python", 
                    "🎨 Création Visuelle",
                    "📚 Exposé Scolaire Complet",
                    "👔 Création de CV Professionnel",
                    "📄 Structuration Document Word"
                ]
            )
        with col_wa:
            st.markdown("#### 📞 Confirmation WhatsApp")
            default_wa = db["users"][user]["whatsapp"] if user else ""
            wa_display = st.text_input("Numéro", value=default_wa, placeholder="Ex: 225...")
        
        st.markdown("#### 📝 Description du besoin")
        prompt = st.text_area("Cahier des charges", height=150, placeholder="Soyez précis pour un meilleur résultat...")
        
        if st.button("LANCER L'INTELLIGENCE ARTIFICIELLE"):
            if prompt and wa_display:
                st.session_state["is_glowing"] = True
                st.rerun()
            else:
                st.error("Veuillez remplir tous les champs.")

        if st.session_state["is_glowing"]:
            progress_placeholder = st.empty()
            status_text = st.empty()
            bar = progress_placeholder.progress(0)
            for percent_complete in range(100):
                time.sleep(0.02)
                bar.progress(percent_complete + 1)
                status_text.markdown(f"<p style='text-align:center; color:#00d2ff; font-size:1.2rem; font-weight:bold;'>PROCESSUS IA EN COURS : {percent_complete + 1}%</p>", unsafe_allow_html=True)
            
            new_req = {
                "id": hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8],
                "user": user if user else "guest",
                "service": service,
                "desc": prompt,
                "whatsapp": wa_display,
                "status": "Traitement IA...",
                "timestamp": str(datetime.now())
            }
            st.session_state["db"]["demandes"].append(new_req)
            save_db(st.session_state["db"])
            st.session_state["is_glowing"] = False
            progress_placeholder.empty()
            status_text.empty()
            if user:
                st.success("✅ Demande envoyée ! Consultez l'onglet 'MES FICHIERS' pour voir l'avancement.")
                st.balloons()
                st.rerun()
            else:
                st.session_state["view"] = "auth"
                st.rerun()

    with tab2:
        if not user:
            st.warning("🔒 Connectez-vous pour accéder à vos livrables personnels.")
        else:
            fresh_db = load_db()
            user_links = fresh_db["liens"].get(user, [])
            user_reqs = [r for r in fresh_db["demandes"] if r["user"] == user]
            
            # --- ZONE DE RÉCEPTION (CRITIQUE) ---
            st.markdown("""
                <div style="background: rgba(46, 204, 113, 0.1); padding: 15px; border-radius: 10px; border: 1px dashed #2ecc71; margin-bottom: 20px; text-align: center;">
                    <h2 style="color: #2ecc71; margin: 0;">📥 VOTRE ESPACE DE TÉLÉCHARGEMENT</h2>
                    <p style="color: white; font-size: 0.9rem;">Tous vos fichiers terminés apparaissent ici instantanément.</p>
                </div>
            """, unsafe_allow_html=True)

            if user_links:
                for link in user_links:
                    st.markdown(f"""
                    <div class="file-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h3 style="color:#00d2ff; margin:0;">📄 {link['name']}</h3>
                                <p style="color:#aaa; font-size:0.85rem; margin: 5px 0;">Livré le {link.get('date', 'Récent')}</p>
                            </div>
                            <a href="{link['url']}" target="_blank" style="text-decoration:none;">
                                <button style="padding:10px 25px; background:#2ecc71; color:white; border:none; border-radius:30px; font-weight:bold; cursor:pointer; box-shadow: 0 4px 10px rgba(46,204,113,0.3);">
                                    📥 RÉCUPÉRER
                                </button>
                            </a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # EN COURS
            if user_reqs:
                st.markdown("#### ⏳ Travaux en cours de préparation")
                for r in user_reqs:
                    st.markdown(f"""
                        <div class="file-card" style="border-left: 5px solid #f1c40f; border-color: rgba(241, 196, 15, 0.3);">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <strong style="color: #f1c40f;">{r['service']}</strong><br>
                                    <span style="color:#eee; font-size: 0.9rem;">Statut : {r['status']}</span>
                                </div>
                                <div class="spinner" style="width: 20px; height: 20px; border: 3px solid rgba(255,255,255,0.1); border-top: 3px solid #f1c40f; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                            </div>
                        </div>
                        <style>@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }</style>
                    """, unsafe_allow_html=True)
            
            if not user_links and not user_reqs:
                st.info("Vous n'avez pas encore de fichiers. Lancez une tâche pour commencer !")
            
            # --- SUPPORT ---
            st.write("---")
            st.markdown("### 🆘 Besoin d'aide pour vos fichiers ?")
            col_rel, col_sup = st.columns(2)
            with col_rel:
                relance_msg = f"Bonjour, je relance ma demande IA (ID: {user})."
                wa_relance = f"https://wa.me/{WHATSAPP_NUMBER}?text={relance_msg.replace(' ', '%20')}"
                st.markdown(f'<a href="{wa_relance}" target="_blank" class="support-btn" style="border-color:#f1c40f; color:#f1c40f !important;">🔔 Relancer la livraison</a>', unsafe_allow_html=True)
            with col_sup:
                st.markdown(f'<a href="{whatsapp_support_url}" target="_blank" class="support-btn">🙋 Parler à un agent</a>', unsafe_allow_html=True)

    # --- ADMIN ---
    with st.expander("🛠 Console de Livraison (Admin)"):
        if st.text_input("Code Secret", type="password") == ADMIN_CODE:
            current_db = st.session_state["db"]
            for i, req in enumerate(current_db["demandes"]):
                st.write(f"📦 **{req['user']}** - {req['service']}")
                url_dl = st.text_input(f"Lien pour {req['id']}", key=f"url_{i}")
                if st.button(f"LIVRER MAINTENANT", key=f"btn_{i}"):
                    if url_dl:
                        if req['user'] not in current_db["liens"]: current_db["liens"][req['user']] = []
                        current_db["liens"][req['user']].append({
                            "name": req['service'], 
                            "url": url_dl,
                            "date": datetime.now().strftime("%d/%m/%Y")
                        })
                        current_db["demandes"].pop(i)
                        save_db(current_db)
                        st.rerun()

# ==========================================
# RUNTIME
# ==========================================

inject_custom_css()

# Synchronisation JS
components.html("""
    <script>
    const user = localStorage.getItem('arsene_user');
    const urlParams = new URLSearchParams(window.parent.location.search);
    const currentUser = urlParams.get('user_id');
    
    if (user && !currentUser && !window.parent.location.href.includes('logout')) {
        window.parent.location.href = window.parent.location.origin + window.parent.location.pathname + '?user_id=' + user;
    }
    if (!currentUser && user && window.parent.location.href.includes('logout')) {
        localStorage.removeItem('arsene_user');
    }
    if (currentUser && user !== currentUser) {
        localStorage.setItem('arsene_user', currentUser);
    }
    </script>
""", height=0)

if st.session_state["view"] == "auth":
    show_auth_page()
else:
    main_dashboard()
