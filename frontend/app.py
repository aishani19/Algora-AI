import streamlit as st
from backend.database import SessionLocal
from backend.models import User
from backend.llm import generate_response  # make sure this function exists

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Algora AI", layout="wide")

# ------------------ DB ------------------
def get_user(username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    
    if user and user.password == password:
        return user
    return None

def create_user(username, password):
    db = SessionLocal()
    existing = db.query(User).filter(User.username == username).first()
    
    if existing:
        db.close()
        return False
    
    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    db.close()
    return True

# ------------------ UI ------------------
st.title("🚀 Algora AI")
st.subheader("Your personal AI career navigator")

menu = st.sidebar.selectbox("Menu", ["Login", "Sign Up", "Dashboard"])

# ------------------ LOGIN ------------------
if menu == "Login":
    st.header("🔐 Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = get_user(username, password)
        
        if user:
            st.success("Login successful")
            st.session_state["user"] = username
        else:
            st.error("Invalid credentials")

# ------------------ SIGNUP ------------------
elif menu == "Sign Up":
    st.header("📝 Create Account")
    
    username = st.text_input("Choose Username")
    password = st.text_input("Choose Password", type="password")
    
    if st.button("Sign Up"):
        success = create_user(username, password)
        
        if success:
            st.success("Account created successfully")
        else:
            st.error("Username already exists")

# ------------------ DASHBOARD ------------------
elif menu == "Dashboard":
    if "user" not in st.session_state:
        st.warning("Please login first")
    else:
        st.header(f"📊 Welcome, {st.session_state['user']}")
        
        st.subheader("🎯 Career Guidance")
        
        user_input = st.text_area("Enter your skills / interests")
        
        if st.button("Generate Roadmap"):
            if user_input:
                try:
                    response = generate_response(user_input)
                    st.success("Generated Roadmap:")
                    st.write(response)
                except Exception as e:
                    st.error("Error generating response")
                    st.write(e)
            else:
                st.warning("Please enter some input")
