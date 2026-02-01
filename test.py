import streamlit as st
import json
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Mon Espace Fichiers", layout="wide")
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"demandes": {}, "liens": {}}

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "demandes": st.session_state["demandes"],
            "liens": st.session_state["liens"]
        }, f, indent=4)

# --- INITIALISATION ---
if "demandes" not in st.session_state:
    data = load_data()
    st.session_state["demandes"] = data["demandes"]
    st.session_state["liens"] = data["liens"]

st.title("📄 Espace Partagé")

# --- INTERFACE UTILISATEUR ---
col1, col2 = st.columns(2)

with col1:
    with st.expander("➕ Faire une nouvelle demande", expanded=True):
        nom = st.text_input("Ton prénom").strip()
        message = st.text_area("Explique-moi ton besoin...")
        if st.button("Envoyer la demande"):
            if nom and message:
                st.session_state["demandes"][nom] = message
                save_data()
                st.success("Demande enregistrée !")
            else:
                st.warning("Remplis tous les champs.")

with col2:
    st.subheader("📂 Ton lien")
    client_nom = st.text_input("Tape ton prénom pour vérifier :").strip()
    if client_nom:
        if client_nom in st.session_state["liens"]:
            st.info(f"Fichier prêt : [Clique ici]({st.session_state['liens'][client_nom]})")
        elif client_nom in st.session_state["demandes"]:
            st.warning("En cours de traitement...")
        else:
            st.error("Aucune demande trouvée.")

# --- INTERFACE ADMIN (Suppression automatique) ---
st.divider()
st.subheader("👨‍💻 Gestion Arsène")
pwd = st.text_input("Code secret", type="password")

if pwd == "02110240":
    if not st.session_state["demandes"]:
        st.write("☕ Aucune demande en attente. Repose-toi !")
    else:
        # On fait une liste des noms pour pouvoir modifier le dictionnaire en bouclant
        for nom in list(st.session_state["demandes"].keys()):
            with st.container():
                c1, c2, c3 = st.columns([2, 4, 2])
                c1.write(f"**{nom}**")
                c2.write(st.session_state["demandes"][nom])
                
                # Input pour le lien
                lien_input = c3.text_input("Coller le lien", key=f"in_{nom}")
                
                if c3.button("Valider & Supprimer", key=f"btn_{nom}"):
                    if lien_input:
                        # 1. On ajoute au dictionnaire des liens
                        st.session_state["liens"][nom] = lien_input
                        # 2. On SUPPRIME de la liste des demandes
                        del st.session_state["demandes"][nom]
                        # 3. Sauvegarde et actualisation
                        save_data()
                        st.rerun()
                    else:
                        st.error("Ajoute un lien avant de valider.")