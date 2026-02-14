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
    page_title="Arsène Solutions - Accès Rapide", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "data_arsene_v3.json"
ADMIN_CODE = "02110240"
WHATSAPP_NUMBER = "2250102030405" # Remplacez par votre numéro de support réel

# ==========================================
# LOGIQUE DE DONNÉES (DATA LAYER)
# ==========================================

def load_db():
    """Charge la base de données simulée."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"users": {}, "demandes": [], "liens": {}}
    return {"users": {}, "demandes": [], "liens": {}}

def save_db(data):
    """Sauvegarde les modifications."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# Initialisation du State Streamlit
if "db" not in st.session_state:
    st.session_state["db"] = load_db()

if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

if "view" not in st.session_state:
    st.session_state["view"] = "home"

# ==========================================
# LOGIQUE DE RECONNEXION AUTOMATIQUE
# ==========================================

if st.session_state["current_user"] is None:
    stored_user = st.query_params.get("user_id")
    if stored_user and stored_user in st.session_state["db"]["users"]:
        st.session_state["current_user"] = stored_user

# ==========================================
# DESIGN ET STYLE (UI/UX LAYER)
# ==========================================

def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        
        * { font-family: 'Inter', sans-serif; }

        .stApp {
            background: linear-gradient(145deg, #0a0a12 0%, #1a1a2e 100%);
            color: #e0e0e0;
        }
        
        .main-title {
            background: linear-gradient(90deg, #00d2ff, #3a7bd5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 3rem !important;
            text-align: center;
            margin-bottom: 0.5rem;
        }

        /* Styling Sidebar Box */
        .info-box {
            background: rgba(0, 210, 255, 0.1);
            border: 1px solid rgba(0, 210, 255, 0.3);
            border-radius: 12px;
            padding: 15px;
            margin: 10px 0;
            text-align: center;
        }
        
        .info-box-title {
            color: #00d2ff;
            font-weight: 800;
            font-size: 0.9rem;
            text-transform: uppercase;
            margin-bottom: 8px;
            display: block;
        }

        .stTextInput label, .stSelectbox label, .stTextArea label {
            color: #00d2ff !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            font-size: 0.85rem !important;
        }
        
        div[data-baseweb="input"], textarea {
            border: 1px solid rgba(0, 210, 255, 0.2) !important;
            background-color: rgba(255, 255, 255, 0.03) !important;
            border-radius: 10px !important;
        }

        .stButton>button {
            border-radius: 12px;
            padding: 0.6rem 2rem;
            background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
            border: none;
            color: white !important;
            font-weight: 700;
            width: 100%;
            transition: 0.3s;
        }

        .stButton>button:hover {
            transform: scale(1.02);
            box-shadow: 0 5px 15px rgba(0, 210, 255, 0.4);
        }

        .card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }

        .excel-badge {
            background: #1D6F42;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 10px;
        }

        .support-btn {
            display: inline-block;
            text-decoration: none;
            background: #25D366;
            color: white !important;
            padding: 10px 20px;
            border-radius: 10px;
            font-weight: bold;
            text-align: center;
            width: 100%;
            margin-top: 10px;
        }
        
        .premium-banner {
            background: linear-gradient(90deg, rgba(255, 215, 0, 0.15), rgba(0, 210, 255, 0.1));
            border: 1px solid #ffd700;
            border-radius: 15px;
            padding: 1rem;
            text-align: center;
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# PAGES ET COMPOSANTS
# ==========================================

def show_auth_page():
    """Page de connexion Simplifiée (ID + WhatsApp)."""
    st.markdown("<h1 class='main-title'>ESPACE CLIENT</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Se connecter")
        with st.form("login"):
            uid = st.text_input("Identifiant")
            wa_auth = st.text_input("Numéro WhatsApp", placeholder="Ex: 22501020304")
            if st.form_submit_button("ACCÉDER À MON COMPTE"):
                db = st.session_state["db"]
                if uid in db["users"] and db["users"][uid]["whatsapp"] == wa_auth:
                    st.session_state["current_user"] = uid
                    st.session_state["view"] = "home"
                    st.query_params["user_id"] = uid
                    st.rerun()
                else:
                    st.error("Identifiant ou numéro WhatsApp incorrect.")

    with col2:
        st.subheader("Créer un compte")
        with st.form("signup"):
            new_uid = st.text_input("Identifiant souhaité")
            new_wa = st.text_input("Votre numéro WhatsApp (clé d'accès)")
            new_email = st.text_input("Email (Optionnel)")
            if st.form_submit_button("CRÉER MON ESPACE"):
                if new_uid and new_wa:
                    db = st.session_state["db"]
                    if new_uid not in db["users"]:
                        db["users"][new_uid] = {
                            "whatsapp": new_wa,
                            "email": new_email if new_email else "Non renseigné",
                            "joined": str(datetime.now())
                        }
                        st.session_state["current_user"] = new_uid
                        st.session_state["view"] = "home"
                        save_db(db)
                        st.query_params["user_id"] = new_uid
                        st.rerun()
                    else:
                        st.warning("Cet identifiant est déjà utilisé.")
                else:
                    st.error("L'identifiant et le numéro WhatsApp sont obligatoires.")

def main_dashboard():
    """Tableau de bord principal."""
    user = st.session_state["current_user"]
    db = st.session_state["db"]
    
    # Barre Latérale - DESIGN AMÉLIORÉ
    with st.sidebar:
        st.markdown(f"### 👤 {user if user else 'Invité'}")
        if user:
            st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; margin-bottom: 10px;">
                    <small style="color: #aaa;">Compte vérifié</small><br>
                    <span style="color: #00d2ff; font-weight: bold;">{db['users'][user]['whatsapp']}</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button("🚪 Déconnexion"):
                st.session_state["current_user"] = None
                st.query_params.clear()
                st.rerun()
        else:
            if st.button("🔐 Se connecter"):
                st.session_state["view"] = "auth"
                st.rerun()
        
        st.divider()
        
        # ZONE LIVRAISON MISE EN VALEUR
        st.markdown(f"""
            <div class="info-box">
                <span class="info-box-title">🚀 LIVRAISON SMART</span>
                <p style="font-size: 0.85rem; line-height: 1.4; color: #e0e0e0; margin: 0;">
                    Vos fichiers sont livrés <b>directement ici</b> et une alerte vous est envoyée sur <b>WhatsApp</b> dès que l'IA a terminé.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="info-box" style="border-color: rgba(29, 111, 66, 0.4); background: rgba(29, 111, 66, 0.1);">
                <span class="info-box-title" style="color: #2ecc71;">📊 EXPERT EXCEL</span>
                <p style="font-size: 0.82rem; color: #eee; margin: 0;">
                    Nettoyage de données, Tableaux de bord automatiques et calculs complexes en un clic.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<h1 class='main-title'>ARSÈNE SOLUTIONS IA</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div class='premium-banner'>
            <span style='color:#ffd700; font-weight:bold;'>✨ PUISSANCE IA ACTIVÉE</span> : 
            Transformez vos fichiers Excel statiques en outils intelligents et automatisés.
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🚀 NOUVELLE DEMANDE", "📂 MES LIVRABLES"])

    with tab1:
        col_f, col_wa = st.columns([1, 1])
        with col_f:
            st.markdown('<div class="excel-badge">⚡ SPÉCIALITÉ EXCEL</div>', unsafe_allow_html=True)
            service = st.selectbox("Type de service", ["📊 Automatisation Excel & Data", "📝 Rédaction Documentaire IA", "⚙️ Script Python sur mesure", "🎨 Design Graphique IA"])
        with col_wa:
            default_wa = db["users"][user]["whatsapp"] if user else ""
            wa_display = st.text_input("WhatsApp pour la notification", value=default_wa, placeholder="Ex: 225...")
        
        prompt = st.text_area("Cahier des charges", height=200, placeholder="Ex: Automatise ce fichier Excel pour qu'il calcule les commissions et génère un graphique de performance mensuel...")
        
        if st.button("LANCER LA GÉNÉRATION PAR L'IA"):
            if prompt and wa_display:
                new_req = {
                    "id": hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8],
                    "user": user if user else "guest",
                    "service": service,
                    "desc": prompt,
                    "whatsapp": wa_display,
                    "status": "Analyse du fichier & Traitement...",
                    "timestamp": str(datetime.now())
                }
                
                st.session_state["db"]["demandes"].append(new_req)
                save_db(st.session_state["db"])
                
                if user:
                    st.success("✅ Intelligence Artificielle en action ! Votre fichier arrive bientôt.")
                    st.balloons()
                    st.rerun()
                else:
                    st.session_state["view"] = "auth"
                    st.rerun()
            else:
                st.error("Veuillez remplir la description et le numéro WhatsApp.")

    with tab2:
        if not user:
            st.info("⚠️ Connectez-vous pour voir vos fichiers générés.")
        else:
            fresh_db = load_db()
            user_links = fresh_db["liens"].get(user, [])
            user_reqs = [r for r in fresh_db["demandes"] if r["user"] == user]
            
            if user_links:
                st.subheader("✅ Livrables Prêts")
                for link in user_links:
                    st.markdown(f"""
                    <div class="card">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <h4 style="margin:0; color:#00d2ff;">{link['name']}</h4>
                                <p style="font-size:0.8rem; color:#aaa; margin-top:5px;">Prêt le {link.get('date', 'Récent')}</p>
                            </div>
                            <span style="background: rgba(46, 204, 113, 0.2); color: #2ecc71; padding: 2px 8px; border-radius: 5px; font-size: 0.7rem;">DISPONIBLE</span>
                        </div>
                        <a href="{link['url']}" target="_blank" style="text-decoration:none;">
                            <button style="width:100%; padding:12px; background:#2ecc71; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer; margin-top:15px; transition: 0.3s;">
                                📥 TÉLÉCHARGER MAINTENANT
                            </button>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
            
            if user_reqs:
                st.subheader("⏳ Commandes en cours")
                for r in user_reqs:
                    st.markdown(f"""
                        <div class="card" style="border-left: 4px solid #f1c40f;">
                            <strong style="color: #f1c40f;">{r['service']}</strong><br>
                            <small>Statut actuel : {r['status']}</small><br>
                            <small style="color: #666;">ID: {r['id']}</small>
                        </div>
                    """, unsafe_allow_html=True)
            
            if not user_links and not user_reqs:
                st.info("Vous n'avez pas encore de commandes. Lancez votre première automatisation dans l'onglet précédent !")
            
            # --- RELANCE & SERVICE CLIENT ---
            st.write("---")
            st.write("### 🆘 Support & Assistance")
            
            relance_msg = f"Bonjour, je relance ma demande IA (Client : {user})."
            support_msg = f"Bonjour Arsène Solutions, j'ai une question sur l'automatisation Excel."
            
            whatsapp_relance_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={relance_msg.replace(' ', '%20')}"
            whatsapp_support_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={support_msg.replace(' ', '%20')}"
            
            col_rel, col_sup = st.columns(2)
            with col_rel:
                st.markdown(f'<a href="{whatsapp_relance_url}" target="_blank" class="support-btn" style="background: rgba(255,255,255,0.05); border: 1px solid #25D366; color: #25D366 !important;">🔔 Relancer le traitement</a>', unsafe_allow_html=True)
            with col_sup:
                st.markdown(f'<a href="{whatsapp_support_url}" target="_blank" class="support-btn" style="background:#3a7bd5;">💬 Aide WhatsApp Directe</a>', unsafe_allow_html=True)

    # --- ADMINISTRATION ---
    with st.expander("🛠 Console Administrateur"):
        if st.text_input("Code Secret", type="password") == ADMIN_CODE:
            current_db = st.session_state["db"]
            for i, req in enumerate(current_db["demandes"]):
                st.write(f"**Client :** {req['user']} ({req['whatsapp']})")
                st.caption(f"Besoin : {req['desc']}")
                url_dl = st.text_input(f"Lien de livraison pour {req['id']}", key=f"url_{i}")
                
                if st.button(f"Valider Livraison {req['id']}", key=f"btn_{i}"):
                    if url_dl:
                        if req['user'] not in current_db["liens"]: current_db["liens"][req['user']] = []
                        current_db["liens"][req['user']].append({
                            "name": req['service'], 
                            "url": url_dl,
                            "date": datetime.now().strftime("%d/%m/%Y")
                        })
                        current_db["demandes"].pop(i)
                        save_db(current_db)
                        st.rerun()

# ==========================================
# RUNTIME
# ==========================================

inject_custom_css()

# Script de synchronisation localStorage
components.html("""
    <script>
    const user = localStorage.getItem('arsene_user');
    const urlParams = new URLSearchParams(window.parent.location.search);
    const currentUser = urlParams.get('user_id');
    
    if (user && !currentUser && !window.parent.location.href.includes('logout')) {
        window.parent.location.href = window.parent.location.origin + window.parent.location.pathname + '?user_id=' + user;
    }
    if (!currentUser && user && window.parent.location.href.includes('logout')) {
        localStorage.removeItem('arsene_user');
    }
    if (currentUser && user !== currentUser) {
        localStorage.setItem('arsene_user', currentUser);
    }
    </script>
""", height=0)

if st.session_state["view"] == "auth":
    show_auth_page()
else:
    main_dashboard()
