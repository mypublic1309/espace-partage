import streamlit as st
import json
import os
import hashlib
from datetime import datetime
import streamlit.components.v1 as components

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Arsène Solutions - Espace Partagé", page_icon="👑", layout="wide")

# --- FONCTIONS DE SÉCURITÉ & DONNÉES ---
DATA_FILE = "data_arsene_v2.json"

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"users": {}, "demandes": [], "liens": {}}
    return {"users": {}, "demandes": [], "liens": {}}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# Initialisation de l'état
if "data" not in st.session_state:
    st.session_state["data"] = load_data()

if "user" not in st.session_state:
    st.session_state["user"] = None

if "show_login" not in st.session_state:
    st.session_state["show_login"] = False

if "pending_request" not in st.session_state:
    st.session_state["pending_request"] = None

# --- SYSTÈME DE SESSION PERSISTANTE (COOKIES / LOCALSTORAGE) ---
# Ce script permet de mémoriser l'utilisateur sur son navigateur
def session_manager():
    # Script JS pour lire/écrire l'utilisateur dans le navigateur
    st.markdown("""
        <script>
        const user = localStorage.getItem('arsene_user');
        if (user && !window.parent.location.href.includes('logout')) {
            window.parent.postMessage({type: 'streamlit:set_user', user: user}, '*');
        }
        </script>
    """, unsafe_allow_html=True)

# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: white;
    }
    h1, h2, h3 {
        color: #00d2ff !important;
        text-shadow: 2px 2px 10px rgba(0, 210, 255, 0.4);
    }
    .stButton>button {
        background: linear-gradient(45deg, #00d2ff, #3a7bd5);
        color: white !important;
        border-radius: 25px;
        font-weight: bold;
        transition: 0.3s;
        width: 100%;
        border: none;
    }
    .stTextInput label, .stSelectbox label, .stTextArea label, .stForm label {
        color: #00d2ff !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }
    div[data-baseweb="input"] > div, textarea {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(0, 210, 255, 0.3) !important;
        border-radius: 8px !important;
    }
    .premium-box {
        background: rgba(255, 215, 0, 0.08);
        border: 2px solid #ffd700;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    .download-btn {
        display: block;
        width: 100%;
        padding: 15px;
        background: linear-gradient(45deg, #2ecc71, #27ae60);
        color: white !important;
        text-align: center;
        border-radius: 12px;
        font-weight: bold;
        text-decoration: none;
    }
    .wa-admin-btn {
        display: inline-block;
        padding: 10px 20px;
        background-color: #25D366;
        color: white !important;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
        width: 100%;
        text-align: center;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE D'AUTHENTIFICATION ---
def auth_page():
    st.markdown("<h1 style='text-align: center;'>🔐 Authentification</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Connexion")
        with st.form("login_form"):
            username = st.text_input("Identifiant")
            password = st.text_input("Mot de passe", type="password")
            submit = st.form_submit_button("Se connecter")
            
            if submit:
                users = st.session_state["data"]["users"]
                if username in users and users[username]["password"] == hash_password(password):
                    st.session_state["user"] = username
                    st.session_state["show_login"] = False
                    
                    # Sauvegarde dans le navigateur (JS)
                    st.markdown(f"<script>localStorage.setItem('arsene_user', '{username}');</script>", unsafe_allow_html=True)
                    
                    if st.session_state["pending_request"]:
                        req = st.session_state["pending_request"]
                        req["user"] = username
                        st.session_state["data"]["demandes"].append(req)
                        save_data(st.session_state["data"])
                        st.session_state["pending_request"] = None
                    st.rerun()
                else:
                    st.error("Erreur d'identifiants")

    with col2:
        st.subheader("S'inscrire")
        with st.form("register_form"):
            new_user = st.text_input("Identifiant souhaité")
            email = st.text_input("Email")
            new_password = st.text_input("Mot de passe", type="password")
            register_submit = st.form_submit_button("Créer mon compte")
            
            if register_submit:
                if new_user and email and new_password:
                    if new_user not in st.session_state["data"]["users"]:
                        st.session_state["data"]["users"][new_user] = {
                            "password": hash_password(new_password),
                            "email": email,
                            "created_at": str(datetime.now())
                        }
                        st.session_state["user"] = new_user
                        st.session_state["show_login"] = False
                        
                        # Sauvegarde dans le navigateur (JS)
                        st.markdown(f"<script>localStorage.setItem('arsene_user', '{new_user}');</script>", unsafe_allow_html=True)
                        
                        if st.session_state["pending_request"]:
                            req = st.session_state["pending_request"]
                            req["user"] = new_user
                            st.session_state["data"]["demandes"].append(req)
                        save_data(st.session_state["data"])
                        st.session_state["pending_request"] = None
                        st.rerun()
                    else:
                        st.warning("Identifiant déjà pris.")
    
    if st.button("⬅️ Retour à l'accueil"):
        st.session_state["show_login"] = False
        st.rerun()

# --- APPLICATION PRINCIPALE ---
def main_app():
    user = st.session_state["user"]
    
    with st.sidebar:
        if user:
            st.markdown(f"<h2 style='text-align: center;'>👑 {user}</h2>", unsafe_allow_html=True)
            if st.button("🚪 Déconnexion"):
                # Effacement du stockage local lors de la déconnexion
                st.markdown("<script>localStorage.removeItem('arsene_user');</script>", unsafe_allow_html=True)
                st.session_state["user"] = None
                st.rerun()
        else:
            st.markdown("<h2 style='text-align: center;'>👑 ARSÈNE</h2>", unsafe_allow_html=True)
            if st.button("🔐 Se connecter"):
                st.session_state["show_login"] = True
                st.rerun()
        st.divider()
        st.caption("Arsène Solutions © 2025")

    st.title("📄 AUTO_EXCEL")

    st.markdown(f"""
        <div class="premium-box">
            <h3 style="margin:0; color:#ffd700 !important;">⭐ EXCELLENCE PREMIUM & IA</h3>
            <p>Notification WhatsApp + Vitesse 10<sup>10</sup></p>
        </div>
    """, unsafe_allow_html=True)

    tab_req, tab_stat = st.tabs(["🆕 Nouvelle Demande", "📂 Mes Livrables"])

    with tab_req:
        st.subheader("🤖 Analyse IA")
        default_desc = st.session_state["pending_request"]["desc"] if st.session_state["pending_request"] else ""
        default_wa = st.session_state["pending_request"]["whatsapp"] if st.session_state["pending_request"] else ""
        
        type_f = st.selectbox("Type", ["Tableau Excel", "Document Word", "Script Python", "Design/Affiche"])
        wa_n = st.text_input("WhatsApp", value=default_wa, placeholder="Ex: 22507...")
        desc = st.text_area("Description", value=default_desc, height=150)
        
        if st.button("🚀 GÉNÉRER"):
            if desc and wa_n:
                demande = {
                    "user": user if user else "guest",
                    "type": type_f,
                    "desc": desc,
                    "whatsapp": wa_n,
                    "status": "Analyse en cours...",
                    "date": str(datetime.now())
                }
                if user:
                    st.session_state["data"]["demandes"].append(demande)
                    save_data(st.session_state["data"])
                    st.success("Enregistré !")
                    st.balloons()
                else:
                    st.session_state["pending_request"] = demande
                    st.session_state["show_login"] = True
                    st.rerun()
            else:
                st.warning("Champs requis.")

    with tab_stat:
        if user:
            st.subheader("Suivi de vos fichiers")
            mes_d = [d for d in st.session_state["data"]["demandes"] if d["user"] == user]
            
            if user in st.session_state["data"]["liens"]:
                for item in st.session_state["data"]["liens"][user]:
                    with st.expander(f"✅ DISPONIBLE : {item['name']}", expanded=True):
                        st.markdown(f'<a href="{item["url"]}" target="_blank" class="download-btn">⬇️ TÉLÉCHARGER</a>', unsafe_allow_html=True)
            
            if not mes_d and user not in st.session_state["data"]["liens"]:
                st.info("Rien à afficher pour le moment.")
            
            for d in mes_d:
                st.write(f"⏳ **{d['type']}** - {d['date'][:16]}")
                st.caption(f"Statut : {d['status']}")
                st.divider()
        else:
            st.warning("Veuillez vous connecter pour voir vos livrables.")

    # --- ADMIN ---
    with st.expander("🔐 Admin"):
        pwd = st.text_input("Code", type="password")
        if pwd == "02110240":
            for i, d in enumerate(st.session_state["data"]["demandes"]):
                st.write(f"**{d['user']}** ({d.get('whatsapp')}) : {d['desc']}")
                l_url = st.text_input("Lien", key=f"l_{i}")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Livrer App", key=f"la_{i}"):
                        if l_url:
                            if d['user'] not in st.session_state["data"]["liens"]: st.session_state["data"]["liens"][d['user']] = []
                            st.session_state["data"]["liens"][d['user']].append({"name": d['type'], "url": l_url})
                            st.session_state["data"]["demandes"].pop(i)
                            save_data(st.session_state["data"])
                            st.rerun()
                with c2:
                    if d.get('whatsapp') and l_url:
                        msg = f"Bonjour {d['user']}, votre fichier est prêt : {l_url}"
                        wa = f"https://wa.me/{d['whatsapp']}?text={msg.replace(' ', '%20')}"
                        st.markdown(f'<a href="{wa}" target="_blank" class="wa-admin-btn">💬 WhatsApp</a>', unsafe_allow_html=True)

# --- ROUTAGE ---
if st.session_state["show_login"]:
    auth_page()
else:
    main_app()
