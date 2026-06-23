import streamlit as st
import requests

API_URL = "http://localhost:8000/api/v1"

st.set_page_config(page_title="ProFlow Premium", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")

# --- Custom Premium CSS ---
def inject_custom_css():
    st.markdown("""
    <style>
    /* Main Background & Text Colors */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Input Fields */
    .stTextInput input, .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 8px !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        color: white !important;
        border: none !important;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        border: 1px solid rgba(139, 92, 246, 0.5);
    }
    .glass-card h4 {
        margin-top: 0;
        color: #a78bfa;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

st.title("🚀 ProFlow Enterprise")
st.markdown("Welcome to the premium task & team management system.")

# --- Session State Initialization ---
if "token" not in st.session_state:
    st.session_state["token"] = None
if "user_role" not in st.session_state:
    st.session_state["user_role"] = None

# --- Auth Functions ---
def auth_sidebar():
    st.sidebar.markdown("## 🔐 Access Portal")
    tab1, tab2 = st.sidebar.tabs(["Login", "Register"])
    
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", use_container_width=True):
            res = requests.post(f"{API_URL}/auth/login", data={"username": email, "password": password})
            if res.status_code == 200:
                st.session_state["token"] = res.json().get("access_token")
                st.sidebar.success("Welcome back!")
                st.rerun()
            else:
                st.sidebar.error("Invalid credentials")

    with tab2:
        reg_name = st.text_input("Full Name", key="reg_name")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_pass")
        # Giving admin role by default to test all features
        reg_role = st.selectbox("Role", ["admin", "member"], index=0) 
        
        if st.button("Create Account", use_container_width=True):
            data = {
                "email": reg_email,
                "password": reg_password,
                "full_name": reg_name,
                "role": reg_role
            }
            res = requests.post(f"{API_URL}/users/", json=data)
            if res.status_code == 200:
                st.sidebar.success("Account created! Please log in.")
            else:
                st.sidebar.error(res.json().get("detail", "Error creating account"))

if not st.session_state["token"]:
    auth_sidebar()
    st.info("👈 Please Login or Register from the sidebar to access your dashboard.")
else:
    # --- Authenticated Dashboard ---
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"token": None}), use_container_width=True)
    
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    
    # Fetch user details
    me_res = requests.get(f"{API_URL}/users/me", headers=headers)
    if me_res.status_code != 200:
        st.error("Session expired.")
        st.session_state["token"] = None
        st.rerun()
        
    user = me_res.json()
    st.session_state["user_role"] = user.get("role")
    st.sidebar.markdown(f"**👤 {user.get('full_name') or user.get('email')}**")
    st.sidebar.markdown(f"🏷️ Role: `{user.get('role').upper()}`")

    # Fetch Data
    proj_res = requests.get(f"{API_URL}/projects/", headers=headers)
    task_res = requests.get(f"{API_URL}/tasks/", headers=headers)
    
    projects = proj_res.json() if proj_res.status_code == 200 else []
    tasks = task_res.json() if task_res.status_code == 200 else []

    # --- Top Metrics ---
    st.markdown("### 📊 Overview")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Projects", len(projects))
    m2.metric("Total Tasks", len(tasks))
    m3.metric("Pending Tasks", len([t for t in tasks if t.get("status") == "pending"]))
    st.divider()

    # --- Main Content Area ---
    col_proj, col_task = st.columns(2)
    
    with col_proj:
        st.markdown("### 📁 Projects")
        if st.session_state["user_role"] == "admin":
            with st.expander("➕ Create New Project"):
                p_title = st.text_input("Project Title")
                p_desc = st.text_area("Description")
                if st.button("Save Project"):
                    res = requests.post(f"{API_URL}/projects/", json={"title": p_title, "description": p_desc}, headers=headers)
                    if res.status_code == 200:
                        st.success("Project created!")
                        st.rerun()
                    else:
                        st.error("Error creating project")
        
        for p in projects:
            st.markdown(f"""
            <div class="glass-card">
                <h4>{p['title']}</h4>
                <p style="font-size: 14px; color: #cbd5e1;">{p['description'] or 'No description'}</p>
                <small style="color: #64748b;">ID: {p['id']} | Owner ID: {p['owner_id']}</small>
            </div>
            """, unsafe_allow_html=True)
            
    with col_task:
        st.markdown("### 📋 Tasks")
        if st.session_state["user_role"] == "admin":
            with st.expander("➕ Create New Task"):
                t_title = st.text_input("Task Title")
                t_desc = st.text_area("Task Description")
                t_proj = st.selectbox("Assign to Project", [p['id'] for p in projects] if projects else [])
                if st.button("Save Task") and projects:
                    res = requests.post(f"{API_URL}/tasks/", json={"title": t_title, "description": t_desc, "project_id": t_proj}, headers=headers)
                    if res.status_code == 200:
                        st.success("Task created! (Background email triggered)")
                        st.rerun()
                    else:
                        st.error("Error creating task")
        
        for t in tasks:
            status_color = "#3b82f6" if t['status'] == "pending" else "#10b981"
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid {status_color};">
                <h4>{t['title']}</h4>
                <p style="font-size: 14px; color: #cbd5e1;">{t['description'] or 'No description'}</p>
                <span style="background: {status_color}; padding: 2px 8px; border-radius: 12px; font-size: 12px; color: white;">{t['status']}</span>
                <small style="color: #64748b; margin-left: 10px;">Project ID: {t['project_id']}</small>
            </div>
            """, unsafe_allow_html=True)
