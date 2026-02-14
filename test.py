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
    page_title="Arsène Solutions - IA & Excellence", 
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
    return hashlib.sha256(str.encode(password)).hexdigest()

def load_db():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"users": {}, "demandes": [], "liens": {}}
    return {"users": {}, "demandes": [], "liens": {}}

def save_db(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

if "db" not in st.session_state:
    st.session_state["db"] = load_db()

if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

if "view" not in st.session_state:
    st.session_state["view"] = "home"

if "pending_req" not in st.session_state:
    st.session_state["pending_req"] = None

# ==========================================
# DESIGN ET ANIMATIONS (UI/UX LAYER)
# ==========================================

def inject_luxe_css():
    st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
        <style>
        /* Fond avec animation de gradient */
        .stApp {
            background: linear-gradient(-45deg, #0a0a12, #1a1a2e, #16213e, #0f3460);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            color: #e0e0e0;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Titre avec effet de lueur */
        .main-title {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(90deg, #00d2ff, #92fe9d);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900;
            font-size: 3.5rem !important;
            text-align: center;
            filter: drop-shadow(0 0 10px rgba(0, 210, 255, 0.3));
            margin-bottom: 0.5rem;
        }

        /* Cartes Glassmorphism */
        .card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            border: 1px solid rgba(0, 210, 255, 0.4);
        }

        /* Input visibilité accrue */
        .stTextInput label, .stSelectbox label, .stTextArea label {
            color: #92fe9d !important;
            font-weight: 700 !important;
            letter-spacing: 1.2px;
        }

        /* Bouton Ultra-Pro */
        .stButton>button {
            border-radius: 30px;
            padding: 0.8rem 2.5rem;
            background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
            border: none;
            color: white !important;
            font-size: 1.1rem;
            font-weight: 800;
            text-transform: uppercase;
            box-shadow: 0 10px 20px rgba(0, 210, 255, 0.3);
            width: 100%;
        }

        .stButton>button:hover {
            box-shadow: 0 15px 30px rgba(0, 210, 255, 0.5);
            transform: scale(1.02);
        }

        /* Barre latérale */
        [data-testid="stSidebar"] {
            background-color: rgba(10, 10, 18, 0.95);
            border-right: 1px solid rgba(0, 210, 255, 0.1);
        }

        /* Badge Status */
        .status-badge {
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            background: rgba(0, 210, 255, 0.2);
            color: #00d2ff;
        }
        </style>
    """, unsafe_allow_html=True)

def show_lottie_anim(url):
    """Affiche une animation Lottie via iframe."""
    components.html(f"""
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <div style="display: flex; justify-content: center;">
            <lottie-player src="{url}" background="transparent" speed="1" style="width: 200px; height: 200px;" loop autoplay></lottie-player>
        </div>
    """, height=220)

# ==========================================
# PAGES
# ==========================================

def show_auth_page():
    inject_luxe_css()
    show_lottie_anim("https://assets10.lottiefiles.com/packages/lf20_myejioos.json") # Animation Lock
    
    st.markdown("<h1 class='main-title animate__animated animate__fadeInDown'>CONNEXION CLIENT</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='card animate__animated animate__fadeInLeft'>", unsafe_allow_html=True)
        st.subheader("Accès Sécurisé")
        with st.form("login"):
            uid = st.text_input("Identifiant")
            pwd = st.text_input("Mot de passe", type="password")
            if st.form_submit_button("SE CONNECTER"):
                db = st.session_state["db"]
                if uid in db["users"] and db["users"][uid]["password"] == hash_password(pwd):
                    st.session_state["current_user"] = uid
                    st.session_state["view"] = "home"
                    st.markdown(f"<script>localStorage.setItem('arsene_user', '{uid}');</script>", unsafe_allow_html=True)
                    st.rerun()
                else: st.error("Identifiants incorrects.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card animate__animated animate__fadeInRight'>", unsafe_allow_html=True)
        st.subheader("Nouveau Compte")
        with st.form("signup"):
            new_uid = st.text_input("Identifiant")
            new_email = st.text_input("Email")
            new_pwd = st.text_input("Mot de passe", type="password")
            if st.form_submit_button("S'INSCRIRE"):
                if new_uid and new_email and new_pwd:
                    db = st.session_state["db"]
                    if new_uid not in db["users"]:
                        db["users"][new_uid] = {"password": hash_password(new_pwd), "email": new_email, "joined": str(datetime.now())}
                        st.session_state["current_user"] = new_uid
                        st.session_state["view"] = "home"
                        save_db(db)
                        st.markdown(f"<script>localStorage.setItem('arsene_user', '{new_uid}');</script>", unsafe_allow_html=True)
                        st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("⬅️ Retourner à l'accueil"):
        st.session_state["view"] = "home"
        st.rerun()

def main_dashboard():
    inject_luxe_css()
    user = st.session_state["current_user"]
    
    with st.sidebar:
        st.markdown(f"<h2 style='text-align:center;'>👑</h2>", unsafe_allow_html=True)
        if user:
            st.success(f"Connecté : {user}")
            if st.button("🚪 QUITTER"):
                st.markdown("<script>localStorage.removeItem('arsene_user');</script>", unsafe_allow_html=True)
                st.session_state["current_user"] = None
                st.rerun()
        else:
            st.warning("Mode Visiteur")
            if st.button("🔐 SE CONNECTER"):
                st.session_state["view"] = "auth"
                st.rerun()
        st.divider()
        st.caption("Arsène Solutions v3.5 - Excellence IA")

    st.markdown("<h1 class='main-title animate__animated animate__zoomIn'>ARSÈNE SOLUTIONS</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["⚡ GÉNÉRATION IA", "💎 MES DOCUMENTS"])

    with tab1:
        st.markdown("<div class='card animate__animated animate__fadeInUp'>", unsafe_allow_html=True)
        col_f, col_wa = st.columns([1, 1])
        with col_f:
            service = st.selectbox("Intelligence à activer", ["Tableur Excel Intelligent", "Rédaction Ghostwriter", "Scripting Automation", "Affiche Premium"])
        with col_wa:
            wa = st.text_input("WhatsApp (Notification)", placeholder="225...")
        
        prompt = st.text_area("Cahier des charges", height=150, placeholder="Décrivez votre projet...")
        
        if st.button("🚀 LANCER LA PRODUCTION"):
            if prompt and wa:
                new_req = {
                    "id": hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8],
                    "user": user if user else "guest",
                    "service": service, "desc": prompt, "whatsapp": wa,
                    "status": "Analyse en cours", "timestamp": str(datetime.now())
                }
                if user:
                    st.session_state["db"]["demandes"].append(new_req)
                    save_db(st.session_state["db"])
                    st.balloons()
                    st.toast("Demande enregistrée avec succès !")
                else:
                    st.session_state["pending_req"] = new_req
                    st.session_state["view"] = "auth"
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        if not user:
            st.info("Veuillez vous connecter pour voir vos livrables.")
        else:
            db = st.session_state["db"]
            user_links = db["liens"].get(user, [])
            user_reqs = [r for r in db["demandes"] if r["user"] == user]

            if not user_links and not user_reqs:
                st.info("Aucun projet ici. Commencez par une nouvelle demande !")
            
            # Grille pour les documents
            for link in user_links:
                st.markdown(f"""
                <div class="card" style="border-left: 5px solid #92fe9d;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <h3 style="margin:0; color:#92fe9d !important;">{link['name']}</h3>
                            <small>Prêt depuis le {link.get('date', '...')}</small>
                        </div>
                        <a href="{link['url']}" target="_blank" style="text-decoration:none;">
                            <button style="padding:10px 20px; background:#92fe9d; color:#0a0a12; border:none; border-radius:10px; font-weight:bold;">TÉLÉCHARGER</button>
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            for r in user_reqs:
                st.markdown(f"""
                <div class="card" style="border-left: 5px solid #00d2ff; opacity: 0.8;">
                    <span class="status-badge">⏳ {r['status']}</span>
                    <h4>{r['service']}</h4>
                    <p style="font-size:0.8rem;">Enregistré le {r['timestamp'][:16]}</p>
                </div>
                """, unsafe_allow_html=True)

    # --- ADMIN ---
    with st.expander("🛠 Gestionnaire Arsène"):
        if st.text_input("Clé Admin", type="password") == ADMIN_CODE:
            show_lottie_anim("https://assets5.lottiefiles.com/packages/lf20_96bov8jm.json") # Animation Admin
            for i, req in enumerate(st.session_state["db"]["demandes"]):
                st.write(f"--- Client: {req['user']} ---")
                st.write(req['desc'])
                url = st.text_input("Lien de livraison", key=f"u_{i}")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("LIVRER", key=f"l_{i}"):
                        if url:
                            if req['user'] not in db["liens"]: db["liens"][req['user']] = []
                            db["liens"][req['user']].append({"name": req['service'], "url": url, "date": datetime.now().strftime("%d/%m/%Y")})
                            db["demandes"].pop(i)
                            save_db(db)
                            st.rerun()
                with c2:
                    if req.get("whatsapp") and url:
                        msg = f"Salut {req['user']} ! Ton fichier est prêt ici : {url}"
                        st.markdown(f'<a href="https://wa.me/{req["whatsapp"]}?text={msg.replace(" ","%20")}" target="_blank"><button style="width:100%; background:#25D366; color:white; border:none; padding:10px; border-radius:10px;">NOTIFIER WHATSAPP</button></a>', unsafe_allow_html=True)

# ==========================================
# RUN
# ==========================================

if st.session_state["view"] == "auth":
    show_auth_page()
else:
    main_dashboard()
