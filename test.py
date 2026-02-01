import streamlit as st
import json
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Mon Espace Fichiers")

st.title("📄 Espace Partagé")
st.write("Décris ce dont tu as besoin (Excel ou Word) et je t'envoie le lien ici.")

# --- FONCTIONS DE SAUVEGARDE ---
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"demandes": {}, "liens": {}}

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"demandes": st.session_state["demandes"],
                   "liens": st.session_state["liens"]}, f, indent=4)

# --- INITIALISATION ---
if "demandes" not in st.session_state or "liens" not in st.session_state:
    data = load_data()
    st.session_state["demandes"] = data["demandes"]
    st.session_state["liens"] = data["liens"]

# --- PARTIE CLIENT : Faire une demande ---
with st.expander("➕ Faire une nouvelle demande", expanded=True):
    nom = st.text_input("Ton prénom")
    message = st.text_area("Explique-moi ce que tu veux dans ton fichier...")

    if st.button("Envoyer la demande"):
        if nom and message:
            st.session_state["demandes"][nom] = message
            save_data()
            st.success("Ta demande est enregistrée. Arsène la traitera bientôt.")
        else:
            st.warning("Merci de remplir tous les champs.")

# --- PARTIE CLIENT : Voir son lien ---
st.divider()
st.subheader("📂 Tes fichiers prêts")

client_nom = st.text_input("Tape ton prénom pour voir ton lien :")

if client_nom:
    if client_nom in st.session_state["liens"]:
        st.info(f"Salut {client_nom}, voici ton fichier : [Lien]({st.session_state['liens'][client_nom]})")
    elif client_nom in st.session_state["demandes"]:
        st.warning("Ta demande est en cours de traitement. Arsène t'enverra le lien bientôt.")
    else:
        st.warning("Aucune demande trouvée pour ce prénom.")

# --- PARTIE ADMIN (protégée par mot de passe) ---
st.divider()
st.subheader("👨‍💻 Interface Arsène (admin)")

password = st.text_input("Mot de passe admin", type="password")

if password == "02110240":
    st.success("Accès admin accordé ✅")
    for nom, demande in st.session_state["demandes"].items():
        st.write(f"**{nom}** a demandé : {demande}")
        lien = st.text_input(f"Lien pour {nom}", key=f"lien_{nom}")
        if lien:
            st.session_state["liens"][nom] = lien
            save_data()
else:
    if password:
        st.error("Mot de passe incorrect ❌")
