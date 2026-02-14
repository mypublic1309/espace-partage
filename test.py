import streamlit as st
import json
import os
import hashlib
from datetime import datetime

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
    }
    .login-container {
        max-width: 400px;
        margin: auto;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(0, 210, 255, 0.3);
    }
    .premium-box {
        background: rgba(255, 215, 0, 0.08);
        border: 2px solid #ffd700;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
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
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE D'AUTHENTIFICATION ---
def auth_page():
    st.markdown("<h1 style='text-align: center;'>🔐 Accès Client</h1>", unsafe_allow_html=True)
    
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
                    st.rerun()
                else:
                    st.error("Identifiant ou mot de passe incorrect")

    with col2:
        st.subheader("Créer un compte")
        with st.form("register_form"):
            new_user = st.text_input("Choisir un identifiant")
            email = st.text_input("Votre Email (pour les notifications)")
            new_password = st.text_input("Mot de passe", type="password")
            register_submit = st.form_submit_button("S'enregistrer")
            
            if register_submit:
                if new_user and email and new_password:
                    if new_user not in st.session_state["data"]["users"]:
                        st.session_state["data"]["users"][new_user] = {
                            "password": hash_password(new_password),
                            "email": email,
                            "created_at": str(datetime.now())
                        }
                        save_data(st.session_state["data"])
                        st.success("Compte créé avec succès ! Connectez-vous à gauche.")
                    else:
                        st.warning("Cet identifiant existe déjà.")
                else:
                    st.error("Veuillez remplir tous les champs.")

# --- PAGE PRINCIPALE (APRÈS LOGIN) ---
def main_app():
    user = st.session_state["user"]
    
    # Barre Latérale
    with st.sidebar:
        st.markdown(f"<h2 style='text-align: center;'>👑 Bonjour,<br>{user}</h2>", unsafe_allow_html=True)
        if st.button("Déconnexion"):
            st.session_state["user"] = None
            st.rerun()
        
        st.write("---")
        st.info("Système de notification activé par mail dès que votre fichier est prêt.")

    st.title("📄 AUTO_EXCEL - Tableau de Bord")

    # Bannière Premium
    st.markdown(f"""
        <div class="premium-box">
            <h3 style="margin:0; color:#ffd700 !important;">⭐ EXCELLENCE PREMIUM & IA</h3>
            <p>Notification Instantanée WhatsApp + Livraison Prioritaire (Vitesse 10<sup>10</sup>)</p>
        </div>
    """, unsafe_allow_html=True)
    st.write("")

    tab_request, tab_status = st.tabs(["🆕 Nouvelle Demande", "📂 Mes Livrables & Statut"])

    with tab_request:
        st.subheader("🤖 Nouvelle Analyse IA")
        with st.container():
            type_fichier = st.selectbox("Type de projet", ["Tableau Excel", "Document Word", "Script Python", "Design/Affiche"])
            description = st.text_area("Décrivez précisément votre besoin", height=150)
            
            if st.button("🚀 LANCER LA GÉNÉRATION"):
                if description:
                    nouvelle_demande = {
                        "user": user,
                        "type": type_fichier,
                        "desc": description,
                        "status": "En cours d'analyse",
                        "date": str(datetime.now())
                    }
                    st.session_state["data"]["demandes"].append(nouvelle_demande)
                    save_data(st.session_state["data"])
                    st.balloons()
                    st.success("Demande enregistrée ! Vous recevrez un mail dès que le lien sera disponible.")
                else:
                    st.warning("Veuillez décrire votre besoin.")

    with tab_status:
        st.subheader("Mes Projets")
        mes_demandes = [d for d in st.session_state["data"]["demandes"] if d["user"] == user]
        mes_liens = st.session_state["data"]["liens"].get(user, [])

        if not mes_demandes and not mes_liens:
            st.info("Vous n'avez aucune demande en cours.")
        
        # Affichage des fichiers prêts
        if user in st.session_state["data"]["liens"]:
            for i, item in enumerate(st.session_state["data"]["liens"][user]):
                with st.expander(f"✅ PRÊT : {item['name']}", expanded=True):
                    st.markdown(f'<a href="{item["url"]}" target="_blank" class="download-btn">⬇️ TÉLÉCHARGER LE FICHIER</a>', unsafe_allow_html=True)

        # Affichage des demandes en cours
        for d in mes_demandes:
            with st.container():
                st.write(f"⏳ **{d['type']}** - *Demande faite le {d['date'][:16]}*")
                st.caption(f"Statut : {d['status']} (Délai estimé : 1-2h)")
                st.divider()

    # --- SECTION ADMIN ---
    st.write("")
    with st.expander("🔐 Console Arsène (Admin)"):
        pwd = st.text_input("Accès sécurisé", type="password", key="admin_pwd")
        if pwd == "02110240":
            st.subheader("Gestion des demandes")
            for i, d in enumerate(st.session_state["data"]["demandes"]):
                st.write(f"**Client:** {d['user']} | **Email:** {st.session_state['data']['users'][d['user']]['email']}")
                st.write(f"**Besoin:** {d['desc']}")
                link_url = st.text_input(f"Lien pour {d['user']}", key=f"admin_link_{i}")
                if st.button(f"Livrer & Notifier {d['user']}", key=f"btn_{i}"):
                    if link_url:
                        # Ajouter aux liens livrés
                        if d['user'] not in st.session_state["data"]["liens"]:
                            st.session_state["data"]["liens"][d['user']] = []
                        
                        st.session_state["data"]["liens"][d['user']].append({
                            "name": d['type'],
                            "url": link_url,
                            "date": str(datetime.now())
                        })
                        
                        # Retirer de la liste des demandes
                        st.session_state["data"]["demandes"].pop(i)
                        save_data(st.session_state["data"])
                        st.success(f"Notification envoyée à {d['user']} !")
                        st.rerun()

# --- ROUTAGE ---
if st.session_state["user"] is None:
    auth_page()
else:
    main_app()
