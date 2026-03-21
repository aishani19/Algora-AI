import sys
import os
import bcrypt

# Import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from backend.database import SessionLocal
from backend.models import User, Roadmap
from backend.llm import call_llm

# ------------------ SECURITY ------------------
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    salt = bcrypt.gensalt(rounds=4)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Algora AI", page_icon="🚀", layout="wide")

# ------------------ UI STYLING ------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #0b0e14;
    }

    .main {
        background: linear-gradient(135deg, #0b0e14 0%, #1a1e26 100%);
    }

    /* Professional Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 20, 28, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
    }

    /* Premium Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5rem;
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -10px rgba(99, 102, 241, 0.5);
        filter: brightness(1.1);
    }

    /* Input Fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: white !important;
    }

    /* Tab Headers */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }

    /* Status indicators */
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    h1, h2, h3 {
        color: #f8fafc;
        font-weight: 700;
    }

    .stMarkdown p {
        color: #cbd5e1;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ DB CORE ------------------
def get_user(username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    
    if user and verify_password(password, user.hashed_password):
        return user
    return None

def create_user(username, password):
    db = SessionLocal()
    existing = db.query(User).filter(User.username == username).first()
    
    if existing:
        db.close()
        return False
    
    hashed = get_password_hash(password)
    new_user = User(username=username, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.close()
    return True

# ------------------ APP HEADER ------------------
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://img.icons8.com/clouds/200/rocket.png", width=100)
with col2:
    st.title("Algora AI")
    st.subheader("Your Personal AI Career Mentor & Navigator")

st.divider()

# ------------------ NAVIGATION ------------------
if "user" not in st.session_state:
    st.session_state["user"] = None

with st.sidebar:
    if not st.session_state["user"]:
        menu = st.radio("Navigation", ["Login", "Sign Up"])
    else:
        st.markdown(f"""
            <div style="background: rgba(99, 102, 241, 0.1); padding: 15px; border-radius: 10px; border: 1px solid rgba(99, 102, 241, 0.2); margin-bottom: 20px;">
                <p style="margin:0; font-size: 0.9rem; color: #a5b4fc;">Logged in as</p>
                <h4 style="margin:0; color: white;">{st.session_state['user']}</h4>
            </div>
        """, unsafe_allow_html=True)
        
        menu = st.selectbox("Navigate to", ["🚀 Generator", "📜 History"])
        
        st.divider()
        if st.button("Logout"):
            st.session_state["user"] = None
            st.rerun()

# ------------------ LOGIN / SIGNUP ------------------
if not st.session_state["user"]:
    if menu == "Login":
        st.markdown("### 🔑 Welcome Back")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Access My Workspace"):
            user = get_user(username, password)
            if user:
                st.session_state["user"] = username
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")

    elif menu == "Sign Up":
        st.markdown("### 📝 Create Your Career Account")
        new_username = st.text_input("Choose Username")
        new_password = st.text_input("Choose Password", type="password")
        if st.button("Initialize Account"):
            if create_user(new_username, new_password):
                st.success("Account created! You can now log in.")
            else:
                st.error("Username already taken. Please pick another.")

# ------------------ MAIN WORKSPACE ------------------
else:
    if menu == "🚀 Generator":
        st.markdown("""
            <div class='glass-card'>
                <h2 style='margin-top:0'>🎯 Smart Roadmap Generator</h2>
                <p>Input your target goal and current skills, and our AI will architect your career path.</p>
            </div>
        """, unsafe_allow_html=True)
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            target_goal = st.text_input("What is your dream role?", 
                                     placeholder="e.g. Senior Backend Engineer")
        with col_g2:
            current_skills = st.text_input("Your current skills", 
                                       placeholder="e.g. Python, 기본 SQL, Git")
        
        detailed_context = st.text_area("Additional Context (Optional)", 
                                     placeholder="Any specific interests, time constraints, or background info...")
        
        if st.button("Generate My Roadmap", type="primary"):
            if target_goal:
                with st.spinner("🚀 Architecting your path..."):
                    try:
                        system_prompt = "You are an expert career mentor. You generate structured career roadmaps."
                        user_prompt = f"Goal: {target_goal}\nCurrent Skills: {current_skills}\nContext: {detailed_context}\n\nGenerate a detailed roadmap with phases, topics, and specific resources."
                        
                        response = call_llm(user_prompt=user_prompt, system_prompt=system_prompt)
                        
                        # Save to Database
                        db = SessionLocal()
                        user = db.query(User).filter(User.username == st.session_state["user"]).first()
                        new_roadmap = Roadmap(goal=target_goal, roadmap=response, user_id=user.id)
                        db.add(new_roadmap)
                        db.commit()
                        db.close()
                        
                        st.markdown("---")
                        st.markdown("### 🗺️ Your Personalized Career Path")
                        st.markdown(response)
                        st.balloons()
                    except Exception as e:
                        st.error("Failed to connect to AI engine. Check your API key.")
                        st.exception(e)
            else:
                st.warning("Please specify a target role.")

    elif menu == "📜 History":
        st.markdown("## 📜 Your Career Journey")
        st.write("Review and manage your previously generated roadmaps and analyses.")
        
        db = SessionLocal()
        user = db.query(User).filter(User.username == st.session_state["user"]).first()
        
        # Load Roadmaps
        roadmaps = db.query(Roadmap).filter(Roadmap.user_id == user.id).order_by(Roadmap.id.desc()).all()
        
        if not roadmaps:
            st.info("You haven't generated any roadmaps yet. Go to the Generator to start!")
        else:
            for rm in roadmaps:
                with st.expander(f"📍 Goal: {rm.goal}"):
                    st.markdown(rm.roadmap)
                    if st.button(f"🗑️ Delete Roadmap {rm.id}", key=f"del_rm_{rm.id}"):
                        db.delete(rm)
                        db.commit()
                        st.success("Deleted!")
                        st.rerun()
        
        db.close()
