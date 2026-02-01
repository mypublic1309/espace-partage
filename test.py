import streamlit as st
import json
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Arsène Solutions - Espace Partagé", page_icon="👑", layout="wide")

# --- STYLE CSS PERSONNALISÉ (DESIGN RESPONSIVE) ---
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
        padding: 15px;
        margin-bottom: 15px;
    }

    /* Boutons personnalisés et tactiles */
    .stButton>button {
        background: linear-gradient(45deg, #00d2ff, #3a7bd5);
        color: white !important;
        border-radius: 25px;
        border: none;
        padding: 12px 25px;
        font-weight: bold;
        transition: 0.3s ease;
        width: 100%;
        min-height: 45px; /* Meilleur pour le tactile */
        box-shadow: 0px 4px 15px rgba(0, 210, 255, 0.2);
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 6px 20px rgba(0, 210, 255, 0.5);
    }

    /* Section Premium Adaptative */
    .premium-box {
        background: rgba(255, 215, 0, 0.08);
        border: 2px solid #ffd700;
        border-radius: 15px;
        padding: 20px;
        margin-top: 10px;
        box-shadow: 0px 0px 20px rgba(255, 215, 0, 0.15);
        text-align: center;
    }

    /* Bouton Premium Responsive */
    .premium-btn {
        display: block; /* Prend toute la largeur sur mobile par défaut */
        padding: 15px 20px;
        background: linear-gradient(45deg, #ffd700, #ff8c00);
        color: #000 !important;
        text-decoration: none;
        font-weight: bold;
        border-radius: 25px;
        margin: 15px auto 0 auto;
        max-width: 300px;
        transition: 0.3s;
        box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.3);
    }

    /* Bouton Relance Responsive */
    .reminder-btn {
        display: block;
        padding: 12px 20px;
        background: linear-gradient(45deg, #bdc3c7, #2c3e50);
        color: white !important;
        text-decoration: none;
        font-size: 0.95em;
        border-radius: 20px;
        margin: 10px auto;
        max-width: 280px;
        transition: 0.3s;
    }

    /* Optimisations pour mobiles (écrans < 768px) */
    @media (max-width: 768px) {
        .premium-box p {
            font-size: 0.95em !important;
        }
        h1 { font-size: 1.8em !important; }
        h2 { font-size: 1.5em !important; }
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 0.85em;
            padding: 10px 5px;
        }
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
    st.info("Ingénierie documentaire et conception digitale. Solutions Word, Excel, PowerShell et Design Graphique.")
    
    st.markdown("---")
    st.markdown("### ⚡ Délais de traitement")
    st.warning("Traitement standard sous quelques heures.")
    
    # Bouton WhatsApp Service Client
    st.markdown(f'<a href="https://wa.me/{WHATSAPP_NUMBER}" target="_blank" class="whatsapp-btn">💬 Aide & Expertise</a>', unsafe_allow_html=True)
    
    st.write("---")
    st.caption("© 2025 - Arsène Investissement")

# --- CORPS PRINCIPAL ---
st.title("📄 Espace Client Collaboratif")

# --- SECTION GUIDE D'UTILISATION ---
with st.expander("📖 Guide d'utilisation : Comment ça marche ?"):
    st.markdown("""
    **Étapes simples pour obtenir votre fichier :**
    1. **Demande** : Onglet **'Nouvelle Demande'**.
    2. **Identification** : Entrez votre **identifiant**.
    3. **Description** : Expliquez votre besoin précisément.
    4. **Envoi** : Appuyez sur **'Transmettre'**.
    5. **Récupération** : Onglet **'Mes Livrables'** pour télécharger !
    """)

# Bannière Premium (Optimisée Mobile)
st.markdown(f"""
    <div class="premium-box">
        <h3 style="margin:0; color:#ffd700 !important;">⭐ ACCOMPAGNEMENT PREMIUM</h3>
        <p style="margin:10px 0; font-size: 1.05em; line-height: 1.5;">
            <b>Ingénierie de pointe</b> pour vos projets complexes. 
            Priorité absolue et étude méticuleuse de chaque détail.
        </p>
        <a href="{whatsapp_premium_url}" target="_blank" class="premium-btn">✨ PASSER AU PREMIUM</a>
    </div>
""", unsafe_allow_html=True)

st.write("") # Espacement

# Utilisation d'onglets (Adaptés mobile)
tab_user, tab_files = st.tabs(["🆕 Nouvelle Demande", "📂 Mes Livrables"])

with tab_user:
    st.subheader("Cahier des charges")
    with st.container():
        nom = st.text_input("Identifiant / Prénom", placeholder="Ex: Jean Dupont").strip()
        message = st.text_area("Description du livrable souhaité", placeholder="Précisez votre besoin (Excel, Word, Script, Design...)", height=150)
        
        st.caption("💡 Note : Service standard gracieux. Priorité disponible via l'option Premium.")
        
        if st.button("🚀 TRANSMETTRE LE DOSSIER"):
            if nom and message:
                st.session_state["demandes"][nom] = message
                save_data()
                st.balloons()
                st.success(f"Dossier transmis, {nom}. En attente.")
            else:
                st.warning("Identifiant et description requis.")

with tab_files:
    st.subheader("Accès aux documents")
    client_nom = st.text_input("Identifiant :", key="search", placeholder="Votre nom...").strip()
    
    if client_nom:
        if client_nom in st.session_state["liens"]:
            st.success(f"Disponible, {client_nom} !")
            lien = st.session_state["liens"][client_nom]
            st.markdown(f'<a href="{lien}" target="_blank" class="download-btn">⬇️ TÉLÉCHARGER LE FICHIER</a>', unsafe_allow_html=True)
        elif client_nom in st.session_state["demandes"]:
            st.warning("⏳ Statut : Traitement en cours...")
            
            # --- RELANCE ---
            reminder_msg = f"Bonjour Arsène, je me permets de vous relancer (Identifiant : {client_nom})."
            whatsapp_reminder_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={reminder_msg.replace(' ', '%20')}"
            
            st.markdown(f"""
                <div style="text-align: center;">
                    <a href="{whatsapp_reminder_url}" target="_blank" class="reminder-btn">🔔 Relancer via WhatsApp</a>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Aucun dossier identifié.")

# --- ADMINISTRATION ---
st.write("")
st.divider()
with st.expander("🔐 Administration"):
    pwd = st.text_input("Code", type="password")
    if pwd == "02110240":
        if not st.session_state["demandes"]:
            st.info("Aucune tâche.")
        else:
            for n in list(st.session_state["demandes"].keys()):
                with st.container():
                    st.write(f"**Client :** {n}")
                    st.write(f"**Besoin :** {st.session_state['demandes'][n]}")
                    lien_u = st.text_input("Lien du fichier", key=f"link_{n}")
                    if st.button(f"Clôturer {n}", key=f"v_{n}"):
                        if lien_u:
                            st.session_state["liens"][n] = lien_u
                            del st.session_state["demandes"][n]
                            save_data()
                            st.rerun()