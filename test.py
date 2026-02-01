import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Mon Espace Fichiers")

st.title("📄 Espace Partagé")
st.write("Décris ce dont tu as besoin (Excel ou Word) et je t'envoie le lien ici.")

# --- STOCKAGE EN MÉMOIRE ---
if "demandes" not in st.session_state:
    st.session_state["demandes"] = {}
if "liens" not in st.session_state:
    st.session_state["liens"] = {}

# --- PARTIE CLIENT : Faire une demande ---
with st.expander("➕ Faire une nouvelle demande", expanded=True):
    nom = st.text_input("Ton prénom")
    message = st.text_area("Explique-moi ce que tu veux dans ton fichier...")

    if st.button("Envoyer la demande"):
        if nom and message:
            st.session_state["demandes"][nom] = message
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
else:
    if password:
        st.error("Mot de passe incorrect ❌")
