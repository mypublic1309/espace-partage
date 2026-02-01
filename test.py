import streamlit as st
import json
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Arsène Solutions - Espace Partagé", page_icon="👑", layout="wide")

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

    /* Section Premium Spécifique */
    .premium-box {
        background: rgba(255, 215, 0, 0.08);
        border: 2px solid #ffd700;
        border-radius: 15px;
        padding: 25px;
        margin-top: 10px;
        box-shadow: 0px 0px 20px rgba(255, 215, 0, 0.15);
        text-align: center;
    }

    /* Bouton Premium Doré */
    .premium-btn {
        display: inline-block;
        padding: 12px 30px;
        background: linear-gradient(45deg, #ffd700, #ff8c00);
        color: #000 !important;
        text-decoration: none;
        font-weight: bold;
        border-radius: 25px;
        margin-top: 15px;
        transition: 0.3s;
        box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.3);
    }

    .premium-btn:hover {
        transform: scale(1.05);
        box-shadow: 0px 6px 20px rgba(255, 215, 0, 0.5);
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

    /* Bouton WhatsApp */
    .whatsapp-btn {
        display: block;
        width: 100%;
        padding: 12px;
        background-color: #25D366;
        color: white;
        text-align: center;
        border-radius: 25px;
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

# --- VARIABLES DE CONTACT ---
WHATSAPP_NUMBER = "2250171542505"
PREMIUM_MSG = "J'aimerais passer à la version premium"
whatsapp_premium_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={PREMIUM_MSG.replace(' ', '%20')}"

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>👑<br>ARSÈNE</h1>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("### ✨ Solutions Arsène")
    st.info("Ingénierie documentaire et conception digitale. Solutions Word, Excel, PowerShell et Design Graphique en accès libre.")
    
    st.markdown("---")
    st.markdown("### ⚡ Délais de traitement")
    st.warning("Les demandes standard sont traitées sous un délai de quelques heures, selon la charge du serveur.")
    
    # Bouton WhatsApp Service Client
    st.markdown(f'<a href="https://wa.me/{WHATSAPP_NUMBER}" target="_blank" class="whatsapp-btn">💬 Contacter l\'Expertise Premium</a>', unsafe_allow_html=True)
    
    st.write("---")
    st.caption("© 2025 - Arsène Investissement | Excellence Digitale")

# --- CORPS PRINCIPAL ---
st.title("📄 Espace Client Collaboratif")

# Bannière Premium Professionnelle avec Bouton d'Action
st.markdown(f"""
    <div class="premium-box">
        <h3 style="margin:0; color:#ffd700 !important;">⭐ ACCOMPAGNEMENT PREMIUM</h3>
        <p style="margin:10px 0; font-size: 1.1em; line-height: 1.6;">
            Bénéficiez d'une <b>analyse approfondie et d'une ingénierie de pointe</b> pour vos projets les plus complexes. 
            L'option Premium garantit une compréhension méticuleuse de vos besoins : chaque détail est étudié avec rigueur 
            pour concevoir une solution qui dépasse vos attentes et reflète parfaitement votre vision.
            <br><b>Priorité absolue de traitement et livrables haute définition.</b>
        </p>
        <a href="{whatsapp_premium_url}" target="_blank" class="premium-btn">✨ PASSER À LA VERSION PREMIUM</a>
    </div>
""", unsafe_allow_html=True)

st.write("### 🚀 Formalisez votre projet")
st.write("Soumettez vos besoins en **bureautique avancée, automatisation système ou identité visuelle**.")

# Utilisation d'onglets
tab_user, tab_files = st.tabs(["🆕 Nouvelle Demande", "📂 Consulter mes Livrables"])

with tab_user:
    st.subheader("Cahier des charges simplifié")
    with st.container():
        nom = st.text_input("Identifiant / Prénom", placeholder="Ex: Jean Dupont").strip()
        message = st.text_area("Description détaillée du livrable souhaité", placeholder="Précisez la nature du fichier (Fonctionnalités Excel, Structure Word, Script PowerShell, etc.)")
        
        st.caption("🔍 Note : Le service standard est gracieux. Pour une étude de cas prioritaire et personnalisée, veuillez solliciter l'assistance Premium via le bouton doré ci-dessus.")
        
        if st.button("🚀 TRANSMETTRE LE DOSSIER"):
            if nom and message:
                st.session_state["demandes"][nom] = message
                save_data()
                st.balloons()
                st.success(f"Dossier transmis avec succès, {nom}. Votre demande est en file d'attente.")
            else:
                st.warning("Veuillez renseigner votre identifiant et la description du projet.")

with tab_files:
    st.subheader("Accès aux documents finalisés")
    client_nom = st.text_input("Saisissez votre identifiant pour accéder à vos fichiers :", key="search").strip()
    
    if client_nom:
        if client_nom in st.session_state["liens"]:
            st.success(f"Analyse terminée, {client_nom}. Votre livrable est disponible ci-dessous.")
            lien = st.session_state["liens"][client_nom]
            st.markdown(f'<a href="{lien}" target="_blank" class="download-btn">⬇️ TÉLÉCHARGER LE LIVRABLE</a>', unsafe_allow_html=True)
        elif client_nom in st.session_state["demandes"]:
            st.warning("⏳ Statut : Traitement en cours. Votre document fait l'objet d'une attention particulière.")
            st.info("💡 Optimisation : Pour un traitement instantané et une étude plus rigoureuse, cliquez sur 'Passer à la version Premium' en haut de page.")
        else:
            st.error("Aucun dossier correspondant n'a été identifié.")

# --- INTERFACE ADMINISTRATION ---
st.write("")
st.divider()
with st.expander("🔐 Console d'Administration"):
    pwd = st.text_input("Code de Sécurité", type="password")
    if pwd == "02110240":
        st.write("### 🛠️ Gestion du Workflow")
        if not st.session_state["demandes"]:
            st.info("Système opérationnel. Aucune tâche en attente.")
        else:
            for n in list(st.session_state["demandes"].keys()):
                with st.container():
                    col_info, col_action = st.columns([3, 2])
                    with col_info:
                        st.markdown(f"**👤 Client :** {n}")
                        st.markdown(f"**📝 Cahier des charges :** {st.session_state['demandes'][n]}")
                    with col_action:
                        lien_u = st.text_input("URL du livrable finalisé", key=f"link_{n}")
                        if st.button(f"Clôturer le dossier {n}", key=f"v_{n}"):
                            if lien_u:
                                st.session_state["liens"][n] = lien_u
                                del st.session_state["demandes"][n]
                                save_data()
                                st.rerun()
                            else:
                                st.error("Lien de destination manquant.")