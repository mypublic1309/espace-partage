import streamlit as st
import json
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Arsène Solutions - Espace Partagé", page_icon="👑", layout="wide")

# --- STYLE CSS PERSONNALISÉ (DESIGN RESPONSIVE & ENHANCED) ---
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

    /* Style des conteneurs */
    div[data-testid="stExpander"], .stContainer {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(0, 210, 255, 0.2);
        padding: 15px;
        margin-bottom: 15px;
    }

    /* Boutons tactiles */
    .stButton>button {
        background: linear-gradient(45deg, #00d2ff, #3a7bd5);
        color: white !important;
        border-radius: 25px;
        border: none;
        padding: 12px 25px;
        font-weight: bold;
        transition: 0.3s ease;
        width: 100%;
        min-height: 48px;
        box-shadow: 0px 4px 15px rgba(0, 210, 255, 0.2);
    }

    /* Mise en évidence de l'onglet Livrables via CSS */
    .stTabs [data-baseweb="tab-list"] button:nth-child(2) {
        border: 1px solid #2ecc71 !important;
        background-color: rgba(46, 204, 113, 0.1);
        border-radius: 10px 10px 0 0;
    }

    /* Section Premium Adaptative */
    .premium-box {
        background: rgba(255, 215, 0, 0.08);
        border: 2px solid #ffd700;
        border-radius: 15px;
        padding: 20px;
        margin-top: 10px;
        box-shadow: 0px 0px 25px rgba(255, 215, 0, 0.2);
        text-align: center;
    }

    /* Badge IA & Rapidité */
    .ia-badge {
        background: linear-gradient(45deg, #00d2ff, #00ff88);
        color: #000;
        padding: 2px 10px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 0.85em;
        margin-right: 5px;
    }
    
    .speed-badge {
        background: #ffd700;
        color: #000;
        padding: 2px 8px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 0.9em;
    }

    .premium-btn {
        display: block;
        padding: 15px 20px;
        background: linear-gradient(45deg, #ffd700, #ff8c00);
        color: #000 !important;
        text-decoration: none;
        font-weight: bold;
        border-radius: 25px;
        margin: 15px auto 0 auto;
        max-width: 300px;
        box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.4);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0b0b15;
        border-right: 1px solid #00d2ff;
    }

    .download-btn {
        display: block;
        width: 100%;
        padding: 18px;
        background: linear-gradient(45deg, #2ecc71, #27ae60);
        color: white !important;
        text-align: center;
        border-radius: 12px;
        text-decoration: none;
        font-weight: bold;
        font-size: 1.1em;
        margin-top: 15px;
        box-shadow: 0px 5px 15px rgba(46, 204, 113, 0.3);
    }

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

    .support-btn {
        display: block;
        width: 100%;
        padding: 12px;
        background: transparent;
        color: #00d2ff !important;
        text-align: center;
        border: 1px solid #00d2ff;
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

if "demandes" not in st.session_state:
    data = load_data()
    st.session_state["demandes"] = data["demandes"]
    st.session_state["liens"] = data["liens"]

# --- VARIABLES DE CONTACT ---
WHATSAPP_NUMBER = "2250171542505"
PREMIUM_MSG = "J'aimerais passer à la version premium pour bénéficier de la puissance de l'IA et de la rapidité 10^10"
whatsapp_premium_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={PREMIUM_MSG.replace(' ', '%20')}"
SUPPORT_MSG = "Bonjour, j'ai besoin d'aide avec mon projet sur l'espace client."
whatsapp_support_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={SUPPORT_MSG.replace(' ', '%20')}"

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>👑<br>ARSÈNE</h1>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("### ✨ Solutions Arsène")
    st.info("Ingénierie documentaire et conception digitale propulsée par l'Intelligence Artificielle.")
    
    # Options de contact
    st.markdown(f'<a href="{whatsapp_support_url}" target="_blank" class="whatsapp-btn">💬 Service Client WhatsApp</a>', unsafe_allow_html=True)
    
    st.write("---")
    st.caption("© 2025 - Arsène Investissement")

# --- CORPS PRINCIPAL ---
st.title("📄 AUTOMATISATION_EXCEL/Sheet")

# --- OPTION : COMMENT ÇA MARCHE ? ---
with st.expander("❓ COMMENT ÇA MARCHE ?"):
    st.markdown("""
    ### 🚀 Le processus est simple :
    1. **Identifiez-vous** : Entrez votre prénom ou un identifiant unique dans l'onglet 'Nouvelle Demande'.
    2. **Exprimez-vous** : Décrivez votre besoin (fichier Excel, Word, Script, etc.).
    3. **Analyse IA** : Nos algorithmes commencent la structuration de votre projet.
    4. **Récupération** : Une fois prêt, rendez-vous dans l'onglet **'MES LIVRABLES'** avec votre identifiant pour télécharger votre fichier.
    
    ⚠️ **Note sur les délais :**
    - **Version Gratuite** : Le traitement peut prendre **1 à 2 heures** selon la charge du serveur.
    - **Version Premium** : Livraison **immédiate** (Vitesse $10^{10}$).
    """)

# Bannière Premium (Mise en avant IA + Rapidité 10^10)
st.markdown(f"""
    <div class="premium-box">
        <h3 style="margin:0; color:#ffd700 !important;">⭐ EXCELLENCE PREMIUM & IA</h3>
        <p style="margin:10px 0; font-size: 1.1em; line-height: 1.5;">
            <span class="ia-badge">🤖 GÉNÉRATION PAR IA</span> & <span class="speed-badge">RAPIDITÉ +10<sup>10</sup></span><br>
            Évitez les attentes de 2h. Obtenez une précision chirurgicale et une livraison instantanée.
        </p>
        <a href="{whatsapp_premium_url}" target="_blank" class="premium-btn">✨ ACTIVER LA PUISSANCE IA (PREMIUM)</a>
    </div>
""", unsafe_allow_html=True)

st.write("") 

# --- SECTION ONGLETS ---
tab_user, tab_files = st.tabs(["🆕 Nouvelle Demande", "📂 RÉCUPÉRER MES LIVRABLES (ICI)"])

with tab_user:
    st.subheader("🤖 Donnez vie à votre imagination avec Arsène IA")
    with st.container():
        nom = st.text_input("Identifiant / Prénom", placeholder="Ex: Jean Dupont").strip()
        message = st.text_area("Décrivez votre besoin (L'IA s'occupe du reste)", placeholder="Ex: Un tableau de suivi de stock automatisé avec alertes par mail...", height=120)
        
        st.markdown("""
            <div style="font-size:0.85em; opacity:0.8; margin-bottom:10px;">
                🕒 <b>Version Gratuite :</b> Temps de traitement estimé entre 1h et 2h.<br>
                🔹 <b>Capacités :</b> Excel, Word, Scripts PowerShell, Design.
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 LANCER LA GÉNÉRATION"):
            if nom and message:
                st.session_state["demandes"][nom] = message
                save_data()
                st.balloons()
                st.success(f"Dossier transmis, {nom}. Analyse lancée (Prévoyez 1 à 2h pour la version gratuite).")
            else:
                st.warning("Identifiant et description requis pour l'analyse IA.")

with tab_files:
    st.subheader("📁 Zone de Téléchargement")
    st.info("💡 **C'est ici que vous récupérez vos fichiers générés.** Saisissez l'identifiant utilisé lors de votre demande.")
    
    client_nom = st.text_input("Tapez votre Identifiant / Prénom :", key="search", placeholder="Rechercher mon fichier...").strip()
    
    if client_nom:
        if client_nom in st.session_state["liens"]:
            st.success(f"✅ Analyse terminée ! Votre fichier IA est prêt, {client_nom}.")
            lien = st.session_state["liens"][client_nom]
            st.markdown(f'<a href="{lien}" target="_blank" class="download-btn">⬇️ TÉLÉCHARGER MON LIVRABLE</a>', unsafe_allow_html=True)
            st.caption("Le lien s'ouvrira dans un nouvel onglet sécurisé.")
        elif client_nom in st.session_state["demandes"]:
            st.warning(f"⏳ Statut : Analyse IA en cours pour '{client_nom}'...")
            st.info("Traitement gratuit en cours (Délai estimé : 1h à 2h).")
            
            # --- RELANCE & SERVICE CLIENT ---
            st.write("---")
            st.write("Le délai est trop long ?")
            
            relance_msg = f"Bonjour, je relance ma demande IA (Identifiant : {client_nom}). Le traitement semble prendre du temps."
            whatsapp_relance_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={relance_msg.replace(' ', '%20')}"
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<a href="{whatsapp_relance_url}" target="_blank" class="support-btn">🔔 Relancer la demande</a>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<a href="{whatsapp_support_url}" target="_blank" class="support-btn">🙋 Aide Service Client</a>', unsafe_allow_html=True)
        else:
            st.error("❌ Aucun dossier identifié. Vérifiez l'orthographe ou lancez une nouvelle génération.")

# --- ADMINISTRATION ---
st.write("")
st.divider()
with st.expander("🔐 Console Arsène"):
    pwd = st.text_input("Accès sécurisé", type="password")
    if pwd == "02110240":
        if not st.session_state["demandes"]:
            st.info("Aucune tâche en attente.")
        else:
            for n in list(st.session_state["demandes"].keys()):
                with st.container():
                    st.write(f"**Client :** {n}")
                    st.write(f"**Besoin IA :** {st.session_state['demandes'][n]}")
                    lien_u = st.text_input("Lien du livrable généré", key=f"link_{n}")
                    if st.button(f"Livrer à {n}", key=f"v_{n}"):
                        if lien_u:
                            st.session_state["liens"][n] = lien_u
                            del st.session_state["demandes"][n]
                            save_data()

                            st.rerun()





