import streamlit as st
import json
import os
import hashlib
from datetime import datetime
import streamlit.components.v1 as components

# ==========================================
# CONFIGURATION ET CONSTANTES
# ==========================================
st.set_page_config(
    page_title="Arsène Solutions - Plateforme Professionnelle", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "data_arsene_v3.json"
ADMIN_CODE = "02110240"

# ==========================================
# LOGIQUE DE DONNÉES (DATA LAYER)
# ==========================================

def hash_password(password):
    """Hachage sécurisé des mots de passe."""
    return hashlib.sha256(str.encode(password)).hexdigest()

def load_db():
    """Charge la base de données simulée."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"users": {}, "demandes": [], "liens": {}}
    return {"users": {}, "demandes": [], "liens": {}}

def save_db(data):
    """Sauvegarde les modifications."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# Initialisation du State Streamlit
if "db" not in st.session_state:
    st.session_state["db"] = load_db()

if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

if "view" not in st.session_state:
    st.session_state["view"] = "home"

if "pending_req" not in st.session_state:
    st.session_state["pending_req"] = None

# ==========================================
# DESIGN ET STYLE (UI/UX LAYER)
# ==========================================

def inject_custom_css():
    st.markdown("""
        <style>
        /* Thème sombre et moderne */
        .stApp {
            background: linear-gradient(145deg, #0a0a12 0%, #1a1a2e 100%);
            color: #e0e0e0;
        }
        
        /* Typographie et Titres */
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            letter-spacing: -0.5px;
        }
        
        .main-title {
            background: linear-gradient(90deg, #00d2ff, #3a7bd5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 3rem !important;
            text-align: center;
            margin-bottom: 1rem;
        }

        /* Composants de formulaire */
        .stTextInput label, .stSelectbox label, .stTextArea label {
            color: #00d2ff !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            font-size: 0.85rem !important;
            letter-spacing: 1px;
        }
        
        div[data-baseweb="input"], textarea {
            border: 1px solid rgba(0, 210, 255, 0.2) !important;
            background-color: rgba(255, 255, 255, 0.03) !important;
            border-radius: 10px !important;
        }

        /* Boutons Professionnels */
        .stButton>button {
            border-radius: 12px;
            padding: 0.6rem 2rem;
            background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
            border: none;
            color: white !important;
            font-weight: 700;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 210, 255, 0.2);
            width: 100%;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 210, 255, 0.4);
        }

        /* Cartes de contenu */
        .card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .premium-banner {
            background: linear-gradient(90deg, rgba(255, 215, 0, 0.1), rgba(255, 165, 0, 0.1));
            border: 1px solid #ffd700;
            border-radius: 15px;
            padding: 1rem;
            text-align: center;
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# PAGES ET COMPOSANTS
# ==========================================

def show_auth_page():
    """Page de connexion / Inscription."""
    st.markdown("<h1 class='main-title'>ESPACE CLIENT</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Se connecter")
        with st.form("login"):
            uid = st.text_input("Identifiant")
            pwd = st.text_input("Mot de passe", type="password")
            if st.form_submit_button("CONNEXION"):
                db = st.session_state["db"]
                if uid in db["users"] and db["users"][uid]["password"] == hash_password(pwd):
                    st.session_state["current_user"] = uid
                    st.session_state["view"] = "home"
                    # Persistance locale
                    st.markdown(f"<script>localStorage.setItem('arsene_user', '{uid}');</script>", unsafe_allow_html=True)
                    st.rerun()
                else:
                    st.error("Identifiants incorrects.")

    with col2:
        st.subheader("Créer un compte")
        with st.form("signup"):
            new_uid = st.text_input("Identifiant souhaité")
            new_email = st.text_input("Email de contact")
            new_pwd = st.text_input("Mot de passe", type="password")
            if st.form_submit_button("S'INSCRIRE"):
                if new_uid and new_email and new_pwd:
                    db = st.session_state["db"]
                    if new_uid not in db["users"]:
                        db["users"][new_uid] = {
                            "password": hash_password(new_pwd),
                            "email": new_email,
                            "joined": str(datetime.now())
                        }
                        st.session_state["current_user"] = new_uid
                        st.session_state["view"] = "home"
                        save_db(db)
                        st.markdown(f"<script>localStorage.setItem('arsene_user', '{new_uid}');</script>", unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.warning("Cet identifiant est déjà utilisé.")
                else:
                    st.error("Veuillez remplir tous les champs.")

def main_dashboard():
    """Tableau de bord principal."""
    user = st.session_state["current_user"]
    
    # Barre Latérale Pro
    with st.sidebar:
        st.markdown(f"### 👤 {user if user else 'Invité'}")
        if user:
            if st.button("🚪 Déconnexion"):
                st.markdown("<script>localStorage.removeItem('arsene_user');</script>", unsafe_allow_html=True)
                st.session_state["current_user"] = None
                st.rerun()
        else:
            if st.button("🔐 Se connecter"):
                st.session_state["view"] = "auth"
                st.rerun()
        
        st.divider()
        st.info("💡 Vos fichiers sont conservés 30 jours après leur génération.")

    # En-tête
    st.markdown("<h1 class='main-title'>ARSÈNE SOLUTIONS IA</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div class='premium-banner'>
            <span style='color:#ffd700; font-weight:bold;'>⭐ SERVICE PREMIUM ACTIVÉ</span> : 
            Livraison ultra-rapide par IA et support WhatsApp 24/7.
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🚀 NOUVELLE DEMANDE", "📂 MES LIVRABLES"])

    with tab1:
        col_f, col_wa = st.columns([1, 1])
        with col_f:
            service = st.selectbox("Service demandé", ["Analyse Excel Profonde", "Rédaction Documentaire", "Automatisation Python", "Design Graphique IA"])
        with col_wa:
            wa = st.text_input("Numéro WhatsApp (Format: 225...)", placeholder="Indispensable pour la notification")
        
        prompt = st.text_area("Cahier des charges (Détaillez votre besoin)", height=200, placeholder="Ex: Je veux un tableau croisé dynamique qui analyse mes ventes par région...")
        
        if st.button("LANCER L'INTELLIGENCE ARTIFICIELLE"):
            if prompt and wa:
                new_req = {
                    "id": hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8],
                    "user": user if user else "guest",
                    "service": service,
                    "desc": prompt,
                    "whatsapp": wa,
                    "status": "En cours d'exécution",
                    "timestamp": str(datetime.now())
                }
                
                if user:
                    st.session_state["db"]["demandes"].append(new_req)
                    save_db(st.session_state["db"])
                    st.success("✅ Votre demande a été transmise à nos algorithmes.")
                    st.balloons()
                else:
                    st.session_state["pending_req"] = new_req
                    st.session_state["view"] = "auth"
                    st.rerun()
            else:
                st.error("Veuillez fournir une description et un numéro de contact.")

    with tab2:
        if not user:
            st.info("Connectez-vous pour accéder à votre historique de fichiers.")
        else:
            db = st.session_state["db"]
            # Fichiers livrés
            user_links = db["liens"].get(user, [])
            if user_links:
                st.subheader("✅ Fichiers Prêts")
                for link in user_links:
                    with st.container():
                        st.markdown(f"""
                        <div class="card">
                            <h4 style="margin:0;">{link['name']}</h4>
                            <p style="font-size:0.8rem; color:#aaa;">Livré le {link.get('date', 'Récemment')}</p>
                            <a href="{link['url']}" target="_blank" style="text-decoration:none;">
                                <button style="width:100%; padding:10px; background:#2ecc71; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">
                                    TÉLÉCHARGER LE LIVRABLE
                                </button>
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Demandes en cours
            user_reqs = [r for r in db["demandes"] if r["user"] == user]
            if user_reqs:
                st.subheader("⏳ Demandes en Traitement")
                for r in user_reqs:
                    st.markdown(f"""
                        <div class="card" style="border-left: 4px solid #00d2ff;">
                            <strong>{r['service']}</strong><br>
                            <small>Statut: {r['status']}</small>
                        </div>
                    """, unsafe_allow_html=True)
            
            if not user_links and not user_reqs:
                st.info("Vous n'avez aucun projet actif pour le moment.")

    # --- ADMINISTRATION (PROTECTION PRO) ---
    st.write("")
    with st.expander("🛠 Console de Gestion (Arsène Only)"):
        admin_input = st.text_input("Clé d'accès administrateur", type="password")
        if admin_input == ADMIN_CODE:
            db = st.session_state["db"]
            if not db["demandes"]:
                st.write("Aucune demande en attente.")
            
            for i, req in enumerate(db["demandes"]):
                st.markdown(f"**Client:** {req['user']} | **Service:** {req['service']}")
                st.caption(f"Détail: {req['desc']}")
                url_delivery = st.text_input(f"URL de livraison pour {req['id']}", key=f"url_{i}")
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.button(f"Livrer {req['id']}", key=f"dlv_{i}"):
                        if url_delivery:
                            if req['user'] not in db["liens"]: db["liens"][req['user']] = []
                            db["liens"][req['user']].append({
                                "name": req['service'], 
                                "url": url_delivery,
                                "date": datetime.now().strftime("%d/%m/%Y %H:%M")
                            })
                            db["demandes"].pop(i)
                            save_db(db)
                            st.rerun()
                with c2:
                    if req.get("whatsapp") and url_delivery:
                        msg = f"Arsène Solutions : Votre fichier ({req['service']}) est disponible ! Téléchargez-le ici : {url_delivery}"
                        wa_link = f"https://wa.me/{req['whatsapp']}?text={msg.replace(' ', '%20')}"
                        st.markdown(f"""<a href="{wa_link}" target="_blank"><button style="width:100%; background:#25D366; color:white; border:none; border-radius:5px; padding:5px;">Notifier WhatsApp</button></a>""", unsafe_allow_html=True)

# ==========================================
# GESTION DU CYCLE DE VIE (RUNTIME)
# ==========================================

inject_custom_css()

# Script de reconnexion auto via localStorage
components.html("""
    <script>
    const user = localStorage.getItem('arsene_user');
    if (user && !window.parent.location.href.includes('logout')) {
        // Envoi d'un message à Streamlit ou gestion via cookie en prod réelle
    }
    </script>
""", height=0)

if st.session_state["view"] == "auth":
    show_auth_page()
else:
    main_dashboard()
