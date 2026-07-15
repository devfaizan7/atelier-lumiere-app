import streamlit as st
from datetime import datetime
import random
import base64
from pathlib import Path
import json
import os

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="ATELIER LUMIÈRE | Haute Couture",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# DATABASE & DATA PERSISTENCE
# ==========================================
DB_FILE = "data.json"
USERS_FILE = "users.json"

DEFAULT_DB = {
    "site_contact": {
        "email": "concierge@atelierlumiere.com",
        "phone": "+92 300 123 4567",
        "address": "Liberty Market, Gulberg III, Lahore, Pakistan",
    },
    "collection_showcase": [
        {"name": "Tuxedo", "caption": "Classic evening tailoring — worn for black-tie galas and formal receptions.",
         "image": "https://images.unsplash.com/photo-1593032465175-481ac7f401a0?q=80&w=700"},
        {"name": "Sherwani", "caption": "Hand-embroidered ceremonial coat — worn by grooms for the wedding day and baraat.",
         "image": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?q=80&w=700"},
        {"name": "Shalwar Qameez", "caption": "Relaxed tailored silhouette — worn for nikah ceremonies and daytime festivities.",
         "image": "https://images.unsplash.com/photo-1617137968427-85924c800a22?q=80&w=700"},
        {"name": "Shawl", "caption": "Draped heritage textile — worn over the shoulder for receptions and winter ceremonies.",
         "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?q=80&w=700"},
    ],
    "category_products": {
        "Tuxedo": [
            {"name": "Onyx Peak-Lapel Dinner Tuxedo", "price": 950,
             "image": "https://images.unsplash.com/photo-1593032465175-481ac7f401a0?q=80&w=700"},
            {"name": "Ivory Shawl-Collar Evening Jacket", "price": 890,
             "image": "https://images.unsplash.com/photo-1593032465175-481ac7f401a0?q=80&w=700"},
        ],
        "Sherwani": [
            {"name": "Imperial Crimson Wedding Sherwani", "price": 1450,
             "image": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?q=80&w=700"},
            {"name": "Ivory Zardozi Groom's Sherwani", "price": 1600,
             "image": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?q=80&w=700"},
        ],
        "Shalwar Qameez": [
            {"name": "Classic Premium Cotton Shalwar Kameez", "price": 620,
             "image": "https://images.unsplash.com/photo-1617137968427-85924c800a22?q=80&w=700"},
            {"name": "Charcoal Linen-Blend Shalwar Kameez", "price": 580,
             "image": "https://images.unsplash.com/photo-1617137968427-85924c800a22?q=80&w=700"},
        ],
        "Shawl": [
            {"name": "Pure Pashmina Heritage Shawl", "price": 340,
             "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?q=80&w=700"},
            {"name": "Jamawar Silk Ceremonial Shawl", "price": 410,
             "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?q=80&w=700"},
        ],
    },
    "rtw_items": [
        {"name": "Italian Wool 3-Piece Tuxedo (Ready-to-Wear)", "stock": 15, "price": 850,
         "image": "https://images.unsplash.com/photo-1593032465175-481ac7f401a0?q=80&w=700"},
        {"name": "Imperial Raw Silk Sherwani (Ready-to-Wear)", "stock": 8, "price": 1450,
         "image": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?q=80&w=700"},
        {"name": "Classic Premium Cotton Shalwar Kameez (Ready-to-Wear)", "stock": 22, "price": 620,
         "image": "https://images.unsplash.com/photo-1617137968427-85924c800a22?q=80&w=700"},
    ],
    "attire_options": [
        {"label": "Classic 3-Piece Tailored Tuxedo (Western Formal)",
         "image": "https://images.unsplash.com/photo-1593032465175-481ac7f401a0?q=80&w=700"},
        {"label": "Imperial Royal Sherwani (Eastern Groom)",
         "image": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?q=80&w=700"},
        {"label": "Luxury Kurta Shalwar Kameez (Traditional Elegance)",
         "image": "https://images.unsplash.com/photo-1617137968427-85924c800a22?q=80&w=700"},
        {"label": "Heritage Pashmina Shawl (Couture Layering)",
         "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?q=80&w=700"},
    ],
    "fabric_options": [
        {"name": "Italian Super 120s Loro Piana Wool", "price": 1200,
         "image": "https://images.unsplash.com/photo-1636715986446-d58f0f9b3916?q=80&w=700"},
        {"name": "Premium Handcrafted Banarasi Jamawar", "price": 1500,
         "image": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?q=80&w=700"},
        {"name": "Fine Egyptian Giza Cotton", "price": 650,
         "image": "https://images.unsplash.com/photo-1617137968427-85924c800a22?q=80&w=700"},
        {"name": "Authentic Kashmiri Raw Silk", "price": 800,
         "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?q=80&w=700"},
    ],
    "measurement_videos": {
        "Shoulder": "https://www.youtube.com/watch?v=zElyGr6NxM8",
        "Chest": "https://www.youtube.com/watch?v=SKw52-D3asg",
        "Waist": "https://www.youtube.com/watch?v=nwBniB9amJY",
        "Length": "https://www.youtube.com/watch?v=R5XXMQBKxn8",
        "Collar": "https://www.youtube.com/watch?v=eSaa5_IIqNA",
    },
    "submitted_orders": []
}

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump(DEFAULT_DB, f, indent=4)
        return DEFAULT_DB
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f, indent=4)
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_user(email, user_data):
    users = load_users()
    users[email] = user_data
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Load database on startup
g_db = load_db()

# ------------------------------------------------------------------
# HERO IMAGE
# ------------------------------------------------------------------
def _load_hero_data_uri():
    hero_path = Path(__file__).parent / "hero.jpg"
    if hero_path.exists():
        b64 = base64.b64encode(hero_path.read_bytes()).decode("utf-8")
        return f"data:image/jpeg;base64,{b64}"
    return "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?q=80&w=1600"

HERO_IMAGE_URI = _load_hero_data_uri()

ADMIN_PASSWORD_DEFAULT = "atelier2026"
ADMIN_GATE_PARAM_VALUE = "system-admin-module"

# ==========================================
# GLOBAL CSS (BLACK & GOLD THEME)
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300&family=Montserrat:wght@200;300;400;500&display=swap');

    /* Global Background and Typography */
    .stApp { 
        background-color: #0B0B0C !important; 
        font-family: 'Montserrat', sans-serif !important; 
    }

    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
        color: #F9F9FB !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 300 !important;
        letter-spacing: 0.05em !important;
    }

    .hero-title {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 3.8rem !important;
        font-weight: 300 !important;
        line-height: 1.1 !important;
        color: #FFFFFF !important;
        text-align: center;
        margin-top: 0;
        margin-bottom: 0.5rem;
        letter-spacing: 0.12em !important;
        text-shadow: 0 2px 18px rgba(0,0,0,0.55);
    }
    .hero-subtitle {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 300 !important;
        color: #E8E8EA !important;
        text-align: center;
        letter-spacing: 0.12em !important;
        text-shadow: 0 2px 12px rgba(0,0,0,0.6);
    }

    .page-title {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 3rem !important;
        font-weight: 300 !important;
        color: #F9F9FB !important;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .page-subtitle {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.9rem !important;
        color: #8E8E93 !important;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 0.2em !important;
        margin-bottom: 2rem;
    }

    .section-header {
        font-size: 2.2rem !important;
        border-bottom: 1px solid rgba(212, 175, 55, 0.2);
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
        color: #F9F9FB !important;
    }

    /* Luxury Cards */
    .luxury-card {
        background-color: #121214 !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 0px !important;
        padding: 2.5rem !important;
        margin-bottom: 1.5rem !important;
        transition: all 0.4s ease;
    }
    .luxury-card:hover {
        border-color: rgba(212, 175, 55, 0.4) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
    }
    .luxury-card h2, .luxury-card h3, .luxury-card h4 { color: #D4AF37 !important; }

    /* Fused Cards - Minimizes gap between content and button */
    .fused-card {
        margin-bottom: 0px !important;
        border-bottom: none !important;
    }

    /* Zero out Streamlit's own inter-element spacing immediately after
       a fused card, regardless of which wrapper level it lives on in
       your Streamlit version. */
    div:has(> .fused-card) + div[data-testid="stButton"],
    div:has(> .fused-card) + div[data-testid="stElementContainer"],
    div:has(> .fused-card) + div.element-container {
        margin-top: 0px !important;
        padding-top: 0px !important;
    }
    div:has(> .fused-card) + div[data-testid="stButton"] > button {
        border-top: none !important;
        border-radius: 0px !important;
        margin-top: 0px !important;
    }
/* Uniform selectable-card grid — attire / fabric / RTW / category cards */
    .card-shell {
        height: 460px !important;
        display: flex !important;
        flex-direction: column !important;
        overflow: hidden !important;
    }
    .card-shell .card-img {
        width: 100%;
        height: 260px !important;
        min-height: 260px !important;
        max-height: 260px !important;
        flex-shrink: 0;
        background-size: cover !important;
        background-position: center !important;
        margin: 0;
    }
    .card-shell .card-body {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        padding: 0.6rem 1.25rem 1rem 1.25rem;
        overflow: hidden;
    }
    .card-shell .badge-gold {
        flex-shrink: 0;
        margin-top: 0;
    }
    .card-shell h4.card-title-clamp {
        margin-top: 0.5rem;
        margin-bottom: 0;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        font-size: 0.98rem;
        line-height: 1.3;
        flex-shrink: 0;
    }

    .collection-caption {
        color: #9A9AA1 !important;
        font-size: 0.76rem;
        font-style: italic;
        background: #121214;
        margin: 0 !important;
        padding: 4px 10px !important;
        line-height: 1.3 !important;
    }

    .badge-gold {
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
        padding: 0.25rem 0.75rem !important;
        font-size: 0.72rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.15em !important;
        display: inline-block;
    }

    div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="textarea"] {
        background-color: #161619 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 0px !important;
    }
    div[data-baseweb="input"] input { color: #F9F9FB !important; }

    .tailor-sheet {
        background-color: #050506 !important;
        border: 1px dashed rgba(212, 175, 55, 0.3) !important;
        padding: 2rem !important;
        font-family: monospace !important;
        color: #A4A4AB !important;
        line-height: 1.5;
    }

    /* Standard Buttons */
    .stButton > button {
        background-color: #0B0B0C !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(212, 175, 55, 0.45) !important;
        border-radius: 0px !important;
        letter-spacing: 0.06em;
        transition: all 0.25s ease !important;
    }
    .stButton > button:hover {
        background-color: #D4AF37 !important;
        color: #0B0B0C !important;
        border-color: #D4AF37 !important;
    }

    /* ================================================================
       NAVBAR BUTTONS — scoped via st.container(key="navbar_row"),
       which Streamlit renders as div.st-key-navbar_row. This is a
       stable hook, unlike sibling-selector tricks that depend on
       exact DOM nesting.
       ================================================================ */
    .st-key-navbar_row .stButton > button,
    .st-key-navbar_row .stButton > button:hover,
    .st-key-navbar_row .stButton > button:focus,
    .st-key-navbar_row .stButton > button:active,
    .st-key-navbar_row .stButton > button:focus-visible {
        background: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        -webkit-box-shadow: none !important;
    }

    .st-key-navbar_row .stButton > button {
        color: #F9F9FB !important;
        font-size: 1.3rem !important;
        padding: 0 !important;
        height: 40px !important;
        display: flex;
        justify-content: center;
        align-items: center;
        font-family: 'Cormorant Garamond', serif !important;
        letter-spacing: 0.1em !important;
        transition: color 0.2s ease !important;
    }

    .st-key-navbar_row .stButton > button:hover,
    .st-key-navbar_row .stButton > button:focus {
        color: #D4AF37 !important;
        background: transparent !important;
    }

    /* Hero Banner - Dark Gradient ensures NO white light */
    .hero-banner { position: relative; width: 100%; height: 480px; overflow: hidden; margin-bottom: 2rem; background-size: cover; background-position: center; }
    .hero-banner-overlay {
        position: absolute; inset: 0;
        background: linear-gradient(180deg, rgba(0,0,0,0.10) 0%, rgba(0,0,0,0.65) 100%);
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        text-align: center; padding: 2rem;
    }

    /* Collection strip rows */
    .collection-media {
        position: relative; height: 108px; background-size: cover; background-position: center;
        display: flex; align-items: flex-end;
    }
    .collection-media::after {
        content: ""; position: absolute; inset: 0;
        background: linear-gradient(180deg, rgba(0,0,0,0) 35%, rgba(0,0,0,0.78) 100%);
    }
    .collection-name {
        position: relative; z-index: 2; color: #F9F9FB !important;
        font-family: 'Cormorant Garamond', serif; font-size: 1.6rem;
        padding: 8px 16px; letter-spacing: 0.05em;
        text-shadow: 1px 1px 5px rgba(0,0,0,0.5);
    }
    .collection-caption { color: #9A9AA1 !important; font-size: 0.76rem; padding: 6px 10px; font-style: italic; background: #121214; margin: 0; }

    /* Footer */
    .site-footer { border-top: 1px solid rgba(212,175,55,0.2); margin-top: 3rem; padding-top: 2rem; background-color: transparent; padding-bottom: 2rem; }
    .footer-brand { color: #D4AF37 !important; font-family: 'Cormorant Garamond', serif; letter-spacing: 0.25em; font-size: 1.1rem; }
    .footer-line { color: #8E8E93 !important; font-size: 0.82rem; line-height: 1.9; }
    .footer-rights { color: #55555a !important; font-size: 0.72rem; letter-spacing: 0.1em; text-align: center; margin-top: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================
def _default(key, value):
    if key not in st.session_state:
        st.session_state[key] = value

_default("mode", None)
_default("step", 1)
_default("order_data", {})
_default("cart", [])
_default("checkout_items", [])
_default("checkout_from_cart", False)
_default("checkout_step", 1)
_default("checkout_contact", {})
_default("last_order", None)
_default("rtw_selected", None)
_default("selected_category", None)
_default("category_selected_product", None)
_default("current_user", None)
_default("is_admin", False)
_default("admin_password", ADMIN_PASSWORD_DEFAULT)

MEASUREMENT_CONFIG = [
    {"key": "Shoulder", "label": "Shoulder Width", "min": 15.0, "max": 25.0, "default": 18.0, "step": 0.5},
    {"key": "Chest", "label": "Chest Circumference", "min": 30.0, "max": 60.0, "default": 40.0, "step": 0.5},
    {"key": "Waist", "label": "Waist Line", "min": 25.0, "max": 55.0, "default": 34.0, "step": 0.5},
    {"key": "Length", "label": "Total Jacket/Kameez Length", "min": 25.0, "max": 50.0, "default": 32.0, "step": 0.5},
    {"key": "Collar", "label": "Collar / Neck", "min": 12.0, "max": 22.0, "default": 15.5, "step": 0.5},
]

SIZE_CHART_URL = "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?q=80&w=700"

# Sync external parameters (Dropdown routing & Admin Gate)
_query_params = st.query_params
if "category" in _query_params:
    st.session_state.mode = "CATEGORY"
    st.session_state.selected_category = _query_params["category"]
    st.session_state.category_selected_product = None
    st.query_params.clear()

# ==========================================
# HELPERS
# ==========================================
def go_to_step(n):
    st.session_state.step = n
    st.rerun()

def reset_to_home():
    st.session_state.mode = None
    st.session_state.step = 1
    st.session_state.order_data = {}
    st.session_state.rtw_selected = None
    st.session_state.selected_category = None
    st.session_state.category_selected_product = None
    st.session_state.checkout_step = 1
    st.rerun()

def find_rtw(name):
    for i in g_db["rtw_items"]:
        if i["name"] == name:
            return i
    return None

def find_fabric(name):
    for f in g_db["fabric_options"]:
        if f["name"] == name:
            return f
    return None

def make_rtw_item(name, size):
    rec = find_rtw(name) or {"price": 850}
    return {
        "id": random.randint(1_000_000, 9_999_999),
        "kind": "Ready-to-Wear",
        "title": name,
        "subtitle": f"Size: {size}",
        "price": rec["price"],
        "measurements": None,
    }

def make_category_item(product, size):
    return {
        "id": random.randint(1_000_000, 9_999_999),
        "kind": "Ready-to-Wear",
        "title": product["name"],
        "subtitle": f"Size: {size}",
        "price": product["price"],
        "measurements": None,
    }

def make_bespoke_item(order_data):
    fabric_name = order_data.get("fabric", "Reserve Fabric")
    rec = find_fabric(fabric_name) or {"price": order_data.get("fabric_base_price", 1000)}
    return {
        "id": random.randint(1_000_000, 9_999_999),
        "kind": "Bespoke Commission",
        "title": order_data.get("attire_type", "Custom Commission"),
        "subtitle": f"{fabric_name} — {order_data.get('selected_color', 'Classic Shade')}",
        "price": rec["price"],
        "measurements": order_data.get("measurements"),
    }

def add_to_cart(item):
    st.session_state.cart.append(item)

def to_checkout(items, from_cart=False):
    st.session_state.checkout_items = items
    st.session_state.checkout_from_cart = from_cart
    st.session_state.checkout_step = 1
    st.session_state.mode = "CHECKOUT"

def render_selectable_card(image_url, title, badge_text, selected, button_key, disabled=False, button_label=None):
    st.markdown(f"""
        <div class="luxury-card fused-card card-shell" style="padding: 0 !important;">
            <div class="card-img" style="background-image: url('{image_url}');"></div>
            <div class="card-body">
                <span class="badge-gold">{badge_text}</span>
                <h4 class="card-title-clamp">{title}</h4>
            </div>
        </div>
    """, unsafe_allow_html=True)
    label = button_label or ("Selected ✓" if selected else "Select")
    return st.button(label, key=button_key, disabled=disabled, use_container_width=True)

def render_row_card(image_url, name, caption, button_key):
    st.markdown(f"""
        <div class="luxury-card fused-card collection-row-card" style="padding: 0 !important; overflow: hidden;">
            <div class="collection-media" style="background-image:url('{image_url}');">
                <span class="collection-name">{name}</span>
            </div>
            <p class="collection-caption" style="padding: 10px 15px;">{caption}</p>
        </div>
    """, unsafe_allow_html=True)
    return st.button(f"View {name} Collection", key=button_key, use_container_width=True)
# ==========================================
# DEDICATED CART & AUTH PAGES
# ==========================================
def render_cart_page():
    st.markdown("<h1 class='page-title'>Your Cart</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Review your selected pieces</p>", unsafe_allow_html=True)

    if not st.session_state.cart:
        st.info("Your cart is currently empty. Return home to explore our collections.")
        if st.button("← Return Home"):
            reset_to_home()
        return

    total = 0
    for i, item in enumerate(list(st.session_state.cart)):
        with st.container(border=True):
            c1, c2, c3 = st.columns([4, 1, 1])
            with c1:
                st.markdown(f"**{item['title']}**  \n<span style='color:#8E8E93;font-size:0.85rem;'>{item['subtitle']}</span>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"**${item['price']}**")
            with c3:
                if st.button("Remove", key=f"cart_pg_rem_{item['id']}_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()
        total += item["price"]

    st.markdown(f"<h3 style='color:#D4AF37 !important; text-align:right;'>Subtotal: ${total} USD</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Continue Browsing", use_container_width=True):
            reset_to_home()
    with col2:
        if st.button("Proceed to Checkout →", key="cart_pg_chk", use_container_width=True):
            to_checkout(list(st.session_state.cart), from_cart=True)
            st.rerun()

def render_auth_page():
    st.markdown("<h1 class='page-title'>Account Access</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Securely manage your tailoring measurements</p>", unsafe_allow_html=True)

    users = load_users()
    if st.session_state.current_user:
        record = users.get(st.session_state.current_user, {})
        st.success(f"You are securely signed in as **{record.get('full_name', 'Guest')}** ({st.session_state.current_user}).")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Return Home", use_container_width=True):
                reset_to_home()
        with col2:
            if st.button("Logout", key="auth_pg_logout", use_container_width=True):
                st.session_state.current_user = None
                st.rerun()
        return

    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

    with tab_login:
        email = st.text_input("Email Address", key="login_email")
        pw = st.text_input("Password", type="password", key="login_pass")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Return", use_container_width=True):
                reset_to_home()
        with col2:
            if st.button("Secure Login", key="login_submit", use_container_width=True):
                record = users.get(email)
                if record and record["password"] == pw:
                    st.session_state.current_user = email
                    reset_to_home()
                else:
                    st.error("Invalid email or password.")

    with tab_signup:
        full_name = st.text_input("Full Name", key="signup_name")
        new_email = st.text_input("Email Address", key="signup_email")
        new_pw = st.text_input("Choose a Password", type="password", key="signup_pass")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Cancel", key="signup_cancel", use_container_width=True):
                reset_to_home()
        with col2:
            if st.button("Create Profile", key="signup_submit", use_container_width=True):
                if not full_name or not new_email or not new_pw:
                    st.error("Please fill in your name, email, and password.")
                elif new_email in users:
                    st.error("An account with that email already exists.")
                else:
                    new_user_data = {"password": new_pw, "full_name": full_name, "measurements": {}}
                    save_user(new_email, new_user_data)
                    st.session_state.current_user = new_email
                    reset_to_home()

# ==========================================
# NAVBAR
# ==========================================
def render_navbar():
    with st.container(key="navbar_row"):
        col1, sp1, col_center, sp2, col_cart, col_auth = st.columns([1, 3, 4, 2.5, 0.75, 0.75])

        with col1:
            if st.button("AL", key="nav_logo_btn", use_container_width=True):
                reset_to_home()

        with col_center:
            if st.button("ATELIER LUMIÈRE", key="nav_brand_btn", use_container_width=True):
                reset_to_home()

        with col_cart:
            cart_count = len(st.session_state.cart)
            cart_label = f"🛒 ({cart_count})" if cart_count > 0 else "🛒"
            if st.button(cart_label, key="nav_cart_btn", use_container_width=True):
                st.session_state.mode = "CART"
                st.rerun()

        with col_auth:
            if st.button("👤", key="nav_auth_btn", use_container_width=True):
                st.session_state.mode = "AUTH"
                st.rerun()

    st.markdown("<hr style='border-color: rgba(212, 175, 55, 0.15); margin: 0.5rem 0 2rem 0;'>", unsafe_allow_html=True)
# ==========================================
# FOOTER
# ==========================================
def render_footer():
    st.markdown('<div class="site-footer">', unsafe_allow_html=True)
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        st.markdown('<p class="footer-brand">ATELIER LUMIÈRE</p>', unsafe_allow_html=True)
        st.markdown('<p class="footer-line">Bespoke tailoring, handcrafted in Pakistan,<br>delivered worldwide.</p>', unsafe_allow_html=True)
    with fc2:
        sc = g_db["site_contact"]
        st.markdown(f"""
            <p class="footer-line">
            ✉ {sc['email']}<br>
            ☎ {sc['phone']}<br>
            📍 {sc['address']}
            </p>
        """, unsafe_allow_html=True)
    with fc3:
        st.markdown('<p class="footer-line">Handcrafted by Master Artisans in Pakistan<br>Express Insured DHL Shipping<br>Secure Encrypted Payments Only</p>', unsafe_allow_html=True)
    st.markdown(f"<p class='footer-rights'>© {datetime.now().year} Atelier Lumière. All rights reserved.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# LANDING PAGE
# ==========================================
def render_landing():
    st.markdown(f"""
        <div class="hero-banner" style="background-image:url('{HERO_IMAGE_URI}');">
            <div class="hero-banner-overlay">
                <h1 class="hero-title">ATELIER LUMIÈRE</h1>
                <p class="hero-subtitle">Bespoke Luxury. Crafted Without Borders. Handcrafted in Pakistan • Delivered Globally.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Homepage Layout: Our Collection is featured first
    st.markdown("<h2 class='section-header' style='text-align:center; border-bottom:none;'>Our Collection</h2>", unsafe_allow_html=True)
    
    cats = g_db["collection_showcase"]
    for i, cat in enumerate(cats):
        if render_row_card(cat['image'], cat['name'], cat['caption'], f"landing_cat_{i}"):
            st.session_state.mode = "CATEGORY"
            st.session_state.selected_category = cat["name"]
            st.session_state.category_selected_product = None
            st.rerun()
    st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin:3rem 0;'>", unsafe_allow_html=True)

    # Ready to Wear and Digital Atelier featured below Collection cards
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.markdown("""
            <div class="luxury-card fused-card">
                <span class="badge-gold">Immediate Dispatch</span>
                <h2 style="font-size: 2rem; margin-top: 0.5rem; margin-bottom: 1rem;">Ready-to-Wear</h2>
                <p style="color: #8E8E93; font-size: 0.9rem; line-height: 1.6; margin-bottom: 0;">
                    Curated silhouettes tailored to standard global measurements. Perfect for quick affairs, gala events, and emergency wedding ensembles.
                </p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Collections", use_container_width=True, key="landing_rtw_btn"):
            st.session_state.mode = "RTW"
            st.rerun()

    with col2:
        st.markdown("""
            <div class="luxury-card fused-card">
                <span class="badge-gold">Bespoke Fitting</span>
                <h2 style="font-size: 2rem; margin-top: 0.5rem; margin-bottom: 1rem;">The Digital Atelier</h2>
                <p style="color: #8E8E93; font-size: 0.9rem; line-height: 1.6; margin-bottom: 0;">
                    Uncompromising couture. Custom-tailored to your precise anatomical measurements and crafted from our reserve fabric selection.
                </p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Begin Custom Commission", use_container_width=True, key="landing_bespoke_btn"):
            st.session_state.mode = "BESPOKE"
            go_to_step(1)

# ==========================================
# CATEGORY PRODUCT LISTING
# ==========================================
def render_category_page():
    cat_name = st.session_state.selected_category
    products = g_db["category_products"].get(cat_name, [])

    st.markdown(f"<h1 class='page-title'>{cat_name} Collection</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Curated pieces from this collection</p>", unsafe_allow_html=True)

    if not products:
        st.info("No pieces have been added to this collection yet — check back soon.")
        if st.button("← Back to Collections"):
            reset_to_home()
        return

    cols = st.columns(min(len(products), 3))
    for i, product in enumerate(products):
        with cols[i % len(cols)]:
            selected = st.session_state.category_selected_product == product["name"]
            if render_selectable_card(product["image"], product["name"], f"${product['price']}", selected, f"catprod_{i}"):
                st.session_state.category_selected_product = product["name"]
                st.rerun()

    st.markdown("---")
    if st.session_state.category_selected_product:
        st.markdown(f"### Configuring: {st.session_state.category_selected_product}")
        
        c1, c2 = st.columns([1, 2])
        with c1:
            size = st.selectbox(
                "Select Standard Fit Size (US/UK Scale):",
                ["US/UK 36R (Small)", "US/UK 38R (Medium)", "US/UK 40R (Large)", "US/UK 42R (XL)", "US/UK 44R (XXL)"],
                key="cat_size",
            )
        with c2:
            with st.expander("View Size Reference Chart"):
                st.image(SIZE_CHART_URL, caption="Standard Global Measurement Sizing Reference Guide", use_container_width=True)

        product = next(p for p in products if p["name"] == st.session_state.category_selected_product)
        col_back, col_cart, col_buy = st.columns(3)
        with col_back:
            if st.button("← Back to Collections", use_container_width=True):
                reset_to_home()
        with col_cart:
            if st.button("Add to Cart", use_container_width=True):
                add_to_cart(make_category_item(product, size))
                st.success(f"Added '{product['name']}' to your cart.")
        with col_buy:
            if st.button("Buy Now →", use_container_width=True):
                to_checkout([make_category_item(product, size)], from_cart=False)
                st.rerun()
    else:
        st.info("Select a piece above to choose your size.")
        if st.button("← Back to Collections"):
            reset_to_home()

# ==========================================
# READY-TO-WEAR
# ==========================================
def render_rtw():
    st.markdown("<h1 class='page-title'>The Ready-to-Wear Collection</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Immediate Dispatch. Select Your Standard Cut.</p>", unsafe_allow_html=True)

    items = g_db["rtw_items"]
    cols = st.columns(len(items))
    for i, rec in enumerate(items):
        with cols[i]:
            stock = rec["stock"]
            badge = f"${rec['price']} · {stock} in stock" if stock > 0 else f"${rec['price']} · Out of stock"
            selected = st.session_state.rtw_selected == rec["name"]
            if render_selectable_card(rec["image"], rec["name"], badge, selected, f"rtw_sel_{i}", disabled=(stock <= 0)):
                st.session_state.rtw_selected = rec["name"]
                st.rerun()

    st.markdown("---")

    if st.session_state.rtw_selected:
        st.markdown(f"### Configuring: {st.session_state.rtw_selected}")
        
        c1, c2 = st.columns([1, 2])
        with c1:
            size = st.selectbox(
                "Select Standard Fit Size (US/UK Scale):",
                ["US/UK 36R (Small)", "US/UK 38R (Medium)", "US/UK 40R (Large)", "US/UK 42R (XL)", "US/UK 44R (XXL)"],
                key="rtw_size",
            )
        with c2:
            with st.expander("View Size Reference Chart"):
                st.image(SIZE_CHART_URL, caption="Standard Global Measurement Sizing Reference Guide", use_container_width=True)

        col_back, col_cart, col_buy = st.columns(3)
        with col_back:
            if st.button("← Return", use_container_width=True):
                reset_to_home()
        with col_cart:
            if st.button("Add to Cart", use_container_width=True):
                add_to_cart(make_rtw_item(st.session_state.rtw_selected, size))
                st.success(f"Added '{st.session_state.rtw_selected}' to your cart.")
        with col_buy:
            if st.button("Buy Now →", use_container_width=True):
                to_checkout([make_rtw_item(st.session_state.rtw_selected, size)], from_cart=False)
                st.rerun()
    else:
        st.info("Select a garment above to choose your size.")
        if st.button("← Return to Gateway"):
            reset_to_home()

# ==========================================
# BESPOKE PIPELINE
# ==========================================
def render_bespoke():
    st.markdown(f"<p style='text-align: center; color: #D4AF37; letter-spacing: 0.15em; font-size: 0.8rem; text-transform: uppercase; margin-bottom: 0.5rem;'>Step {st.session_state.step} of 5</p>", unsafe_allow_html=True)

    if st.session_state.step == 1:
        st.markdown("<h1 class='page-title'>Select Your Silhouette</h1>", unsafe_allow_html=True)
        st.markdown("<p class='page-subtitle'>The architectural canvas of your ensemble</p>", unsafe_allow_html=True)

        options = g_db["attire_options"]
        cols = st.columns(2)
        for i, opt in enumerate(options):
            with cols[i % 2]:
                selected = st.session_state.order_data.get("attire_type") == opt["label"]
                if render_selectable_card(opt["image"], opt["label"], "Bespoke Silhouette", selected, f"attire_sel_{i}"):
                    st.session_state.order_data["attire_type"] = opt["label"]
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Cancel & Return", use_container_width=True):
                reset_to_home()
        with col2:
            if st.button("Proceed to Fabrics →", use_container_width=True, disabled=not st.session_state.order_data.get("attire_type")):
                go_to_step(2)

    elif st.session_state.step == 2:
        st.markdown("<h1 class='page-title'>Select Your Fabric</h1>", unsafe_allow_html=True)
        st.markdown("<p class='page-subtitle'>Directly sourced. Sensation and drape built for real-world presence.</p>", unsafe_allow_html=True)

        fabrics = g_db["fabric_options"]
        cols = st.columns(2)
        for i, fab in enumerate(fabrics):
            with cols[i % 2]:
                selected = st.session_state.order_data.get("fabric") == fab["name"]
                if render_selectable_card(fab["image"], fab["name"], f"${fab['price']}", selected, f"fabric_sel_{i}"):
                    st.session_state.order_data["fabric"] = fab["name"]
                    st.session_state.order_data["fabric_base_price"] = fab["price"]
                    st.rerun()

        selected_fabric = st.session_state.order_data.get("fabric")
        if selected_fabric:
            st.markdown(f"""
                <div class="luxury-card" style="margin-top: 1rem;">
                    <span class="badge-gold">Atelier Textile Analysis</span>
                    <h4 style="margin-top: 0.5rem;">{selected_fabric}</h4>
                    <p style="color: #8E8E93; font-size: 0.85rem; line-height: 1.6;">
                        This fabric is renowned for its structure and breathability. Woven utilizing historical techniques in our local reserve loom facilities in Pakistan, the yarn delivers an exquisite drape under event lighting and a heavy, high-trust tactile premium weight.
                    </p>
                </div>
            """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Previous Step", use_container_width=True):
                go_to_step(1)
        with col2:
            if st.button("Proceed to Measurements →", use_container_width=True, disabled=not selected_fabric):
                go_to_step(3)

    elif st.session_state.step == 3:
        st.markdown("<h1 class='page-title'>The Tailoring Grid</h1>", unsafe_allow_html=True)
        st.markdown("<p class='page-subtitle'>Input your exact proportions — watch each clip to measure with confidence.</p>", unsafe_allow_html=True)

        saved_m = {}
        if st.session_state.current_user:
            users = load_users()
            saved_m = users.get(st.session_state.current_user, {}).get("measurements") or {}

        measurements = {}
        for cfg in MEASUREMENT_CONFIG:
            col_a, col_b = st.columns([1.4, 1])
            with col_a:
                st.markdown(f"**{cfg['label']}**")
                val = st.slider(
                    cfg["label"], cfg["min"], cfg["max"],
                    saved_m.get(cfg["key"], cfg["default"]), cfg["step"],
                    key=f"m_{cfg['key']}", label_visibility="collapsed",
                )
                measurements[cfg["key"]] = val
            with col_b:
                st.caption(f"▶ How to measure: {cfg['label']}")
                st.video(g_db["measurement_videos"].get(cfg["key"], ""))
            st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin:0.5rem 0 1.2rem 0;'>", unsafe_allow_html=True)

        st.session_state.order_data["measurements"] = measurements

        if st.session_state.current_user:
            users = load_users()
            record = users[st.session_state.current_user]
            save_toggle = st.toggle("💾 Save these measurements to my profile", value=True, key="save_measurements_toggle")
            if save_toggle:
                record["measurements"] = measurements
                save_user(st.session_state.current_user, record)
                st.caption(f"✓ Saved to your profile.")
            else:
                st.caption("Not saved — flip the toggle on to remember these for next time.")
        else:
            st.info("✉ Sign in (optional, top right) to save your measurements to your profile for next time.")

        st.markdown("""
            <div class="luxury-card">
                <span class="badge-gold">Master Tailor's Assistant</span>
                <h4 style="margin-top: 0.5rem; margin-bottom: 1rem;">Need Guided Verification?</h4>
                <p style="color: #8E8E93; font-size: 0.85rem; line-height: 1.7; margin-bottom: 1.5rem;">
                    Our pattern cutters will review your submissions against anatomical ratios. If a sizing anomaly is detected, our head workshop technician will reach out directly prior to cutting.
                </p>
                <p style="color: #D4AF37; font-size: 0.8rem; font-weight: 500;">
                    ✓ Free Virtual Fitting Consultations via WhatsApp or Zoom can be scheduled post-order.
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Previous Step", use_container_width=True):
                go_to_step(2)
        with col2:
            if st.button("Generate AI Fitting Render →", use_container_width=True):
                go_to_step(4)

    elif st.session_state.step == 4:
        st.markdown("<h1 class='page-title'>The AI Design Render</h1>", unsafe_allow_html=True)
        st.markdown("<p class='page-subtitle'>Interactive Real-Time Virtual Blueprint of Your Design</p>", unsafe_allow_html=True)

        swatch_color = st.select_slider("Review Fabric Color Grading:", options=["Midnight Velvet", "Royal Ivory", "Antique Crimson", "Obsidian Shadow"])
        st.session_state.order_data["selected_color"] = swatch_color

        current_garment = st.session_state.order_data.get("attire_type", "Suit")
        current_fabric = st.session_state.order_data.get("fabric", "Premium Fabric")

        preview_image = None
        for opt in g_db["attire_options"]:
            if opt["label"] == current_garment:
                preview_image = opt["image"]
                break

        col_img, col_txt = st.columns([1, 1.3], gap="large")
        with col_img:
            if preview_image:
                st.image(preview_image, use_container_width=True, caption="Mock AI render placeholder — illustrative only")
        with col_txt:
            st.markdown(f"""
                <div class="luxury-card" style="text-align: center; border: 1px solid #D4AF37; height:100%;">
                    <span class="badge-gold">AI Showroom Generation</span>
                    <h3 style="font-size: 2rem; margin-top: 1rem;">{current_garment}</h3>
                    <p style="color: #D4AF37; font-size: 0.95rem; letter-spacing: 0.1em; margin-bottom: 1.5rem;">
                        Rendered in {current_fabric} — Shade: {swatch_color}
                    </p>
                    <p style="color: #8E8E93; font-size: 0.85rem; max-width: 600px; margin: 0 auto; line-height: 1.6;">
                        "Visualizing structural form matching your anatomical metrics. The shoulder line drop is modeled at {st.session_state.order_data['measurements']['Shoulder']}\" with a targeted drape length of {st.session_state.order_data['measurements']['Length']}\". Tailored specifically for immediate confidence."
                    </p>
                </div>
            """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("← Change Fabric or Measurements", use_container_width=True):
                go_to_step(3)
        with col2:
            if st.button("Add to Cart", use_container_width=True):
                add_to_cart(make_bespoke_item(st.session_state.order_data))
                st.success("Added your custom commission to the cart. Keep browsing or check out anytime from the cart icon above.")
        with col3:
            if st.button("Proceed to Checkout →", use_container_width=True):
                to_checkout([make_bespoke_item(st.session_state.order_data)], from_cart=False)
                st.rerun()

# ==========================================
# CHECKOUT
# ==========================================
def render_checkout():
    st.markdown("<h1 class='page-title'>Atelier Ledger</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Complete checkout & authorize construction sheet</p>", unsafe_allow_html=True)

    items = st.session_state.checkout_items
    if not items:
        st.warning("There is nothing to check out yet.")
        if st.button("← Back to Shop"):
            reset_to_home()
        return

    st.markdown(f"<p style='text-align:center; color:#D4AF37; letter-spacing:0.15em; font-size:0.8rem; text-transform:uppercase;'>Checkout Step {st.session_state.checkout_step} of 2</p>", unsafe_allow_html=True)

    if st.session_state.checkout_step == 1:
        st.markdown("### Delivery & Contact Details")
        contact = st.session_state.checkout_contact
        name = st.text_input("Full Name (Point of Contact)", value=contact.get("name", ""), key="chk_name")
        email = st.text_input("Email Address", value=contact.get("email", ""), key="chk_email")
        phone = st.text_input("Phone Number", value=contact.get("phone", ""), key="chk_phone")
        address = st.text_area("Global Delivery Address (DHL Insured Route)", value=contact.get("address", ""), key="chk_addr")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back to Shop", use_container_width=True):
                reset_to_home()
        with col2:
            if st.button("Continue to Payment →", use_container_width=True):
                if name and email and phone and address:
                    st.session_state.checkout_contact = {"name": name, "email": email, "phone": phone, "address": address}
                    st.session_state.checkout_step = 2
                    st.rerun()
                else:
                    st.error("Please complete all contact and delivery fields.")

    else:
        col_inv, col_pay = st.columns(2, gap="large")

        with col_inv:
            st.markdown("### Itemized Commission Invoice")
            total = 0
            for item in items:
                total += item["price"]
                st.markdown(f"""
                    <div class="luxury-card">
                        <p style="margin: 0; color: #8E8E93;">{item['kind']}</p>
                        <h4 style="margin: 0.2rem 0 0.6rem 0;">{item['title']}</h4>
                        <p style="margin: 0; color: #8E8E93; font-size:0.85rem;">{item['subtitle']}</p>
                        <hr style="border-color: rgba(255,255,255,0.05);">
                        <h4 style="color: #D4AF37 !important; margin:0;">${item['price']} USD</h4>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown(f"<h3 style='color:#D4AF37 !important;'>Grand Total: ${total} USD</h3>", unsafe_allow_html=True)

            contact = st.session_state.checkout_contact
            st.markdown(f"""
                <p style="color:#8E8E93; font-size:0.85rem;">
                Shipping to <b>{contact.get('name','')}</b><br>
                {contact.get('address','')}<br>
                {contact.get('phone','')} · {contact.get('email','')}
                </p>
            """, unsafe_allow_html=True)

        with col_pay:
            st.markdown("### Secure Payment")
            card_num = st.text_input("Card Number", placeholder="•••• •••• •••• ••••", key="chk_card")
            st.markdown("""
                <p style="font-size: 0.75rem; color: #8E8E93; line-height: 1.4;">
                    🔒 Secure SSL Handshake Payment Processing. Since your custom commission will be hand-embellished in our artisan studio in Pakistan and shipped directly to your location, <b>Cash on Delivery (COD) is strictly unavailable.</b>
                </p>
            """, unsafe_allow_html=True)

            if st.button("Place Commission Order & Transmit to Workshop", use_container_width=True):
                if card_num:
                    order = {
                        "order_id": f"ATL-{random.randint(100000, 999999)}",
                        "order_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "customer_name": contact.get("name", ""),
                        "customer_email": contact.get("email", ""),
                        "customer_phone": contact.get("phone", ""),
                        "shipping_address": contact.get("address", ""),
                        "items": items,
                        "total": total,
                    }
                    # Save order to database persistently
                    g_db["submitted_orders"].append(order)
                    save_db(g_db)
                    
                    st.session_state.last_order = order
                    if st.session_state.checkout_from_cart:
                        st.session_state.cart = []
                    st.session_state.checkout_items = []
                    st.session_state.checkout_contact = {}
                    st.session_state.checkout_step = 1
                    st.session_state.mode = "CONFIRMATION"
                    st.rerun()
                else:
                    st.error("Please enter your card details to complete the order.")

        if st.button("← Back to Contact Details"):
            st.session_state.checkout_step = 1
            st.rerun()

# ==========================================
# CONFIRMATION
# ==========================================
def render_confirmation():
    st.markdown("<h1 class='page-title'>Commission Accepted</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Your digital tailor card has been transmitted to our workshop in Pakistan.</p>", unsafe_allow_html=True)

    order = st.session_state.last_order
    if not order:
        st.info("No recent order found.")
        if st.button("Back to Home"):
            reset_to_home()
        return

    lines = [
        "============================================================",
        "ATELIER LUMIÈRE — PRODUCTION WORK ORDER SHEET",
        "============================================================",
        f"ORDER TRACKING ID: {order['order_id']}",
        f"COMMISSION TIMESTAMP: {order['order_date']}",
        f"CLIENT CONTACT: {order['customer_name']}",
        f"EMAIL: {order.get('customer_email','')}",
        f"PHONE: {order.get('customer_phone','')}",
        f"SHIPPING COORDINATE: {order['shipping_address']}",
    ]
    for idx, item in enumerate(order["items"], start=1):
        lines.append("------------------------------------------------------------")
        lines.append(f"LINE {idx}: {item['kind']}")
        lines.append(f"PATTERN OUTLINE: {item['title']}")
        lines.append(f"DETAIL: {item['subtitle']}")
        if item.get("measurements"):
            lines.append("MEASUREMENT PROPORTIONS (INCHES):")
            for k, v in item["measurements"].items():
                lines.append(f"  - {k}: {v}")
    lines.append("============================================================")
    lines.append(f"GRAND TOTAL: ${order['total']} USD")
    lines.append("[TRANSMITTED VIA DHL COURIER INTEGRATION • INITIATING WEAVING PROCESS]")

    st.markdown(f'<div class="tailor-sheet">{"<br>".join(lines)}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("✉ A confirmation copy has been sent to your registered secure email along with active workshop updates.")
    if st.button("Close Order Card & Back to Home Menu", use_container_width=True):
        reset_to_home()

# ==========================================
# ADMIN MODULE
# ==========================================
def render_admin():
    top1, top2 = st.columns([5, 1])
    with top1:
        st.markdown("<h1 class='page-title'>Workshop Admin Portal</h1>", unsafe_allow_html=True)
        st.markdown("<p class='page-subtitle'>Real-Time Operations & Live Global Inventory Controller</p>", unsafe_allow_html=True)
    with top2:
        st.write("")
        if st.button("Exit Admin Module", use_container_width=True):
            st.session_state.is_admin = False
            st.rerun()

    tabs = st.tabs([
        "Orders Received", "Ready-to-Wear Inventory", "Fabric Catalog & Pricing",
        "Bespoke Attire Options", "Landing Collection Cards", "Category Products", "Site Settings",
    ])

    with tabs[0]:
        st.markdown("### Every Submitted Order — Full Customer & Measurement Detail")
        if not g_db["submitted_orders"]:
            st.info("No orders have been submitted in this session. Go back to the client view and place a test order!")
        else:
            for order in reversed(g_db["submitted_orders"]):
                items_html = ""
                for item in order["items"]:
                    items_html += f"<p style='font-size:0.85rem; margin:0.2rem 0;'><b>{item['kind']}:</b> {item['title']} — {item['subtitle']} (${item['price']})</p>"
                    if item.get("measurements"):
                        m_str = ", ".join(f"{k}: {v}\"" for k, v in item["measurements"].items())
                        items_html += f"<p style='font-size:0.78rem; color:#8E8E93; margin:0 0 0.6rem 1rem;'>Measurements — {m_str}</p>"
                st.markdown(f"""
                    <div class="luxury-card">
                        <span class="badge-gold">ACTIVE PRODUCTION</span>
                        <h4 style="margin: 0.5rem 0 0.2rem 0;">{order.get('order_id')} — {order.get('customer_name')}</h4>
                        <p style="font-size: 0.85rem; color: #8E8E93;">
                            ✉ {order.get('customer_email','—')} &nbsp;·&nbsp; ☎ {order.get('customer_phone','—')}<br>
                            📍 {order.get('shipping_address')}
                        </p>
                        <hr style="border-color: rgba(255,255,255,0.05);">
                        {items_html}
                        <p style="color:#D4AF37 !important; margin-top:0.6rem;"><b>Total: ${order.get('total')} USD</b></p>
                    </div>
                """, unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("### Ready-to-Wear — Stock, Price &amp; Image per Item")
        for idx, rec in enumerate(list(g_db["rtw_items"])):
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([2.2, 1, 1, 0.6])
                with c1:
                    rec["name"] = st.text_input("Item Name", value=rec["name"], key=f"rtw_name_{idx}")
                    rec["image"] = st.text_input("Image URL", value=rec["image"], key=f"rtw_img_{idx}")
                with c2:
                    rec["stock"] = st.number_input("Stock Qty", min_value=0, max_value=999, value=rec["stock"], key=f"rtw_stock_{idx}")
                with c3:
                    rec["price"] = st.number_input("Price ($)", min_value=0, max_value=20000, value=rec["price"], key=f"rtw_price_{idx}")
                with c4:
                    st.write("")
                    if st.button("Remove", key=f"rtw_remove_{idx}"):
                        g_db["rtw_items"].pop(idx)
                        save_db(g_db)
                        st.rerun()
        
        if st.button("Save Live RTW Inventory changes", key="save_rtw_changes_btn"):
            save_db(g_db)
            st.success("RTW inventory updated successfully in real time.")
            
        with st.expander("+ Add New Ready-to-Wear Item"):
            new_name = st.text_input("New Item Name", key="new_rtw_name")
            new_img = st.text_input("New Item Image URL", key="new_rtw_img")
            new_stock = st.number_input("Initial Stock", min_value=0, max_value=999, value=10, key="new_rtw_stock")
            new_price = st.number_input("Initial Price ($)", min_value=0, max_value=20000, value=800, key="new_rtw_price")
            if st.button("Add Item", key="add_rtw_btn"):
                if new_name and new_img:
                    g_db["rtw_items"].append({"name": new_name, "stock": new_stock, "price": new_price, "image": new_img})
                    save_db(g_db)
                    st.rerun()
                else:
                    st.error("Please provide both a name and an image URL.")

    with tabs[2]:
        st.markdown("### Reserve Fabrics — Price per Fabric (not per yard) &amp; Close-Up Image")
        for idx, fab in enumerate(list(g_db["fabric_options"])):
            with st.container(border=True):
                c1, c2, c3 = st.columns([2.2, 1, 0.6])
                with c1:
                    fab["name"] = st.text_input("Fabric Name", value=fab["name"], key=f"fab_name_{idx}")
                    fab["image"] = st.text_input("Close-Up Image URL", value=fab["image"], key=f"fab_img_{idx}")
                with c2:
                    fab["price"] = st.number_input("Price per Garment ($)", min_value=0, max_value=20000, value=fab["price"], key=f"fab_price_{idx}")
                with c3:
                    st.write("")
                    if st.button("Remove", key=f"fab_remove_{idx}"):
                        g_db["fabric_options"].pop(idx)
                        save_db(g_db)
                        st.rerun()
                        
        if st.button("Save Live Fabric Changes", key="save_fabrics_changes_btn"):
            save_db(g_db)
            st.success("Fabric selection updated persistently.")
            
        with st.expander("+ Add New Fabric"):
            new_fname = st.text_input("New Fabric Name", key="new_fab_name")
            new_fimg = st.text_input("New Fabric Image URL", key="new_fab_img")
            new_fprice = st.number_input("Price ($)", min_value=0, max_value=20000, value=1000, key="new_fab_price")
            if st.button("Add Fabric", key="add_fab_btn"):
                if new_fname and new_fimg:
                    g_db["fabric_options"].append({"name": new_fname, "price": new_fprice, "image": new_fimg})
                    save_db(g_db)
                    st.rerun()
                else:
                    st.error("Please provide both a name and an image URL.")

    with tabs[3]:
        st.markdown("### Silhouettes Offered in the Bespoke Commission Flow")
        for idx, opt in enumerate(list(g_db["attire_options"])):
            with st.container(border=True):
                c1, c2 = st.columns([3, 0.6])
                with c1:
                    opt["label"] = st.text_input("Silhouette Label", value=opt["label"], key=f"attire_label_{idx}")
                    opt["image"] = st.text_input("Image URL", value=opt["image"], key=f"attire_img_{idx}")
                with c2:
                    st.write("")
                    if st.button("Remove", key=f"attire_remove_{idx}"):
                        g_db["attire_options"].pop(idx)
                        save_db(g_db)
                        st.rerun()
                        
        if st.button("Save Silhouette Changes", key="save_sil_btn"):
            save_db(g_db)
            st.success("Bespoke silhouettes saved successfully.")
            
        with st.expander("+ Add New Silhouette"):
            new_alabel = st.text_input("New Silhouette Label", key="new_attire_label")
            new_aimg = st.text_input("New Image URL", key="new_attire_img")
            if st.button("Add Silhouette", key="add_attire_btn"):
                if new_alabel and new_aimg:
                    g_db["attire_options"].append({"label": new_alabel, "image": new_aimg})
                    save_db(g_db)
                    st.rerun()
                else:
                    st.error("Please provide both a label and an image URL.")

    with tabs[4]:
        st.markdown("### The Collection Cards on the Landing Page")
        for idx, cat in enumerate(list(g_db["collection_showcase"])):
            with st.container(border=True):
                c1, c2 = st.columns([3, 0.6])
                with c1:
                    old_name = cat["name"]
                    cat["name"] = st.text_input("Name", value=cat["name"], key=f"coll_name_{idx}")
                    cat["caption"] = st.text_input("Caption (what it is / when worn)", value=cat["caption"], key=f"coll_cap_{idx}")
                    cat["image"] = st.text_input("Image URL", value=cat["image"], key=f"coll_img_{idx}")
                    if cat["name"] != old_name and old_name in g_db["category_products"]:
                        g_db["category_products"][cat["name"]] = g_db["category_products"].pop(old_name)
                with c2:
                    st.write("")
                    if st.button("Remove", key=f"coll_remove_{idx}"):
                        g_db["collection_showcase"].pop(idx)
                        save_db(g_db)
                        st.rerun()
                        
        if st.button("Save Live Collection Changes", key="save_colls_btn"):
            save_db(g_db)
            st.success("Homepage Collection showcase cards saved successfully.")
            
        with st.expander("+ Add New Collection Card"):
            new_cname = st.text_input("Name", key="new_coll_name")
            new_ccap = st.text_input("Caption", key="new_coll_cap")
            new_cimg = st.text_input("Image URL", key="new_coll_img")
            if st.button("Add Card", key="add_coll_btn"):
                if new_cname and new_cimg:
                    g_db["collection_showcase"].append({"name": new_cname, "caption": new_ccap, "image": new_cimg})
                    g_db["category_products"].setdefault(new_cname, [])
                    save_db(g_db)
                    st.rerun()
                else:
                    st.error("Please provide both a name and an image URL.")

    with tabs[5]:
        st.markdown("### Products Shown Inside Each Collection Page")
        st.caption("These are the live pieces per category. Changes reflect immediately on the user-end client site.")
        for cat_name, products in list(g_db["category_products"].items()):
            st.markdown(f"#### {cat_name}")
            for idx, product in enumerate(list(products)):
                with st.container(border=True):
                    c1, c2, c3 = st.columns([2.2, 1, 0.6])
                    with c1:
                        product["name"] = st.text_input("Product Name", value=product["name"], key=f"catprod_name_{cat_name}_{idx}")
                        product["image"] = st.text_input("Image URL", value=product["image"], key=f"catprod_img_{cat_name}_{idx}")
                    with c2:
                        product["price"] = st.number_input("Price ($)", min_value=0, max_value=20000, value=product["price"], key=f"catprod_price_{cat_name}_{idx}")
                    with c3:
                        st.write("")
                        if st.button("Remove", key=f"catprod_remove_{cat_name}_{idx}"):
                            g_db["category_products"][cat_name].pop(idx)
                            save_db(g_db)
                            st.rerun()
            with st.expander(f"+ Add Product to {cat_name}"):
                np_name = st.text_input("Product Name", key=f"new_catprod_name_{cat_name}")
                np_img = st.text_input("Image URL", key=f"new_catprod_img_{cat_name}")
                np_price = st.number_input("Price ($)", min_value=0, max_value=20000, value=800, key=f"new_catprod_price_{cat_name}")
                if st.button(f"Add to {cat_name}", key=f"add_catprod_{cat_name}"):
                    if np_name and np_img:
                        g_db["category_products"][cat_name].append({"name": np_name, "image": np_img, "price": np_price})
                        save_db(g_db)
                        st.rerun()
                    else:
                        st.error("Please provide both a name and an image URL.")
            st.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
            
        if st.button("Save Live Product Changes", key="save_live_prods_btn"):
            save_db(g_db)
            st.success("All Category inventory updates saved successfully.")

    with tabs[6]:
        st.markdown("### Contact Details Shown in the Footer")
        sc = g_db["site_contact"]
        sc["email"] = st.text_input("Contact Email", value=sc["email"], key="site_email")
        sc["phone"] = st.text_input("Contact Phone", value=sc["phone"], key="site_phone")
        sc["address"] = st.text_input("Studio Address", value=sc["address"], key="site_address")

        st.markdown("---")
        st.markdown("### Measurement Tutorial Videos")
        for cfg in MEASUREMENT_CONFIG:
            g_db["measurement_videos"][cfg["key"]] = st.text_input(
                f"Video URL — {cfg['label']}",
                value=g_db["measurement_videos"].get(cfg["key"], ""),
                key=f"video_{cfg['key']}",
            )

        st.markdown("---")
        st.markdown("### Admin Password")
        new_pw = st.text_input("Set New Admin Password", type="password", key="new_admin_pw")
        if st.button("Update Password/Settings", key="update_admin_pw_btn"):
            save_db(g_db)
            if new_pw:
                st.session_state.admin_password = new_pw
                st.success("Admin settings and credentials updated globally.")
            else:
                st.success("Contact configurations updated successfully.")

# ==========================================
# ADMIN GATE
# ==========================================
def render_admin_gate():
    st.markdown("<h1 class='page-title'>Restricted Access</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Atelier Lumière — Workshop Administration</p>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        with st.container(border=True):
            pw = st.text_input("Admin Password", type="password", key="admin_gate_pw")
            if st.button("Enter Admin Module", use_container_width=True, key="admin_gate_submit"):
                if pw == st.session_state.admin_password:
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    st.error("Incorrect password.")
            if st.button("← Back to Shop", use_container_width=True, key="admin_gate_back"):
                try:
                    del st.query_params["page"]
                except KeyError:
                    pass
                st.rerun()

# ==========================================
# MAIN ROUTER
# ==========================================
_admin_gate_requested = _query_params.get("page") == ADMIN_GATE_PARAM_VALUE

if st.session_state.is_admin:
    render_admin()
elif _admin_gate_requested:
    render_admin_gate()
else:
    render_navbar()

    if st.session_state.mode is None:
        render_landing()
    elif st.session_state.mode == "RTW":
        render_rtw()
    elif st.session_state.mode == "CATEGORY":
        render_category_page()
    elif st.session_state.mode == "BESPOKE":
        render_bespoke()
    elif st.session_state.mode == "CHECKOUT":
        render_checkout()
    elif st.session_state.mode == "CONFIRMATION":
        render_confirmation()
    elif st.session_state.mode == "CART":
        render_cart_page()
    elif st.session_state.mode == "AUTH":
        render_auth_page()

    render_footer()