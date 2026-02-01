import streamlit as st
import json
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="L'Espace d'Arsène", page_icon="👑", layout="wide")

# --- STYLE CSS PERSONNALISÉ (DESIGN ARSÈNE) ---
st.markdown("""
    <style>
    /* Fond dégradé premium */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: white;
    }
    
    /* Titres avec effet néon bleu */
    h1, h2, h3 {
        color: #00d2ff !important;
        text-shadow: 2px 2px 10px rgba(0, 210, 255, 0.4);
        font-family: 'Segoe UI', sans-serif;
    }

    /* Style des conteneurs (Cartes) */
    div[data-testid="stExpander"], .stContainer {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(0, 210, 255, 0.2);
        padding: 20px;
        margin-bottom: 20px;
    }

    /* Boutons personnalisés */
    .stButton>button {
        background: linear-gradient(45deg, #00d2ff, #3a7bd5);
        color: white !important;
        border-radius: 25px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
        transition: 0.3s ease;
        width: 100%;
        box-shadow: 0px 4px 15px rgba(0, 210, 255, 0.2);
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 6px 20px rgba(0, 210, 255, 0.5);
    }

    /* Sidebar (Barre latérale) */
    [data-testid="stSidebar"] {
        background-color: #0b0b15;
        border-right: 1px solid #00d2ff;
    }

    /* Liens de téléchargement */
    .download-btn {
        display: block;
        width: 100%;
        padding: 15px;
        background-color: #2ecc71;
        color: white;
        text-align: center;
        border-radius: 10px;
        text-decoration: none;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GESTION DES DONNÉES ---
DATA_FILE = "data_arsene.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"demandes": {}, "liens": {}}
    return {"demandes": {}, "liens": {}}

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "demandes": st.session_state["demandes"],
            "liens": st.session_state["liens"]
        }, f, indent=4)

# --- INITIALISATION DE L'ÉTAT ---
if "demandes" not in st.session_state:
    data = load_data()
    st.session_state["demandes"] = data["demandes"]
    st.session_state["liens"] = data["liens"]

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>👑<br>ARSÈNE</h1>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("### ✨ Univers Arsène")
    st.info("Bienvenue sur votre portail de gestion de fichiers. Qualité et rapidité garanties.")
    st.write("---")
    st.caption("© 2025 - Arsène Investissement")

# --- CORPS PRINCIPAL ---
st.title("📄 L'Espace Partagé d'Arsène")
st.write("Envoyez vos demandes et récupérez vos fichiers personnalisés en toute sécurité.")

# Utilisation d'onglets pour une interface plus propre
tab_user, tab_files = st.tabs(["🆕 Faire une demande", "📂 Mes fichiers"])

with tab_user:
    st.subheader("Décrivez votre besoin")
    with st.container():
        nom = st.text_input("Votre Prénom", placeholder="Entrez votre prénom...").strip()
        message = st.text_area("Détails du fichier (Excel, Word, etc.)", placeholder="Arsène, j'aimerais un fichier qui...")
        
        if st.button("🚀 ENVOYER À ARSÈNE"):
            if nom and message:
                st.session_state["demandes"][nom] = message
                save_data()
                st.balloons()
                st.success(f"Demande enregistrée ! Arsène a bien reçu votre message, {nom}.")
            else:
                st.warning("Veuillez remplir votre nom et votre demande.")

with tab_files:
    st.subheader("Récupération de vos documents")
    client_nom = st.text_input("Tapez votre prénom pour vérifier vos fichiers :", key="search").strip()
    
    if client_nom:
        if client_nom in st.session_state["liens"]:
            st.success(f"Bonne nouvelle {client_nom} ! Votre document est prêt.")
            lien = st.session_state["liens"][client_nom]
            st.markdown(f'<a href="{lien}" target="_blank" class="download-btn">⬇️ TÉLÉCHARGER LE FICHIER</a>', unsafe_allow_html=True)
        elif client_nom in st.session_state["demandes"]:
            st.warning("⏳ En cours de traitement... Arsène peaufine votre demande.")
        else:
            st.error("Aucune demande trouvée à ce nom.")

# --- INTERFACE ADMINISTRATION ---
st.write("")
st.write("")
st.divider()
with st.expander("🔐 Bureau Privé d'Arsène"):
    pwd = st.text_input("Code Secret", type="password")
    if pwd == "02110240":
        st.write("### 🛠️ Gestion des demandes")
        
        if not st.session_state["demandes"]:
            st.info("☕ Aucune demande en attente. Repose-toi Arsène !")
        else:
            # On boucle sur une copie des clés pour permettre la suppression en direct
            for n in list(st.session_state["demandes"].keys()):
                with st.container():
                    col_info, col_action = st.columns([3, 2])
                    with col_info:
                        st.markdown(f"**👤 Client :** {n}")
                        st.markdown(f"**📝 Besoin :** {st.session_state['demandes'][n]}")
                    with col_action:
                        lien_u = st.text_input("Coller le lien du fichier", key=f"link_{n}")
                        if st.button(f"Valider & Effacer {n}", key=f"v_{n}"):
                            if lien_u:
                                # 1. On stocke le lien pour le client
                                st.session_state["liens"][n] = lien_u
                                # 2. On supprime la demande de la liste
                                del st.session_state["demandes"][n]
                                # 3. Sauvegarde
                                save_data()
                                st.rerun()
                            else:
                                st.error("Veuillez entrer un lien avant de valider.")