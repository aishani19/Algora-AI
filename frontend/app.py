import streamlit as st
import requests
import json

st.set_page_config(page_title="Algora AI", page_icon="🚀", layout="wide")

API = "http://127.0.0.1:8000"

if "token" not in st.session_state:
    st.session_state["token"] = None

def make_authorized_request(method, endpoint, **kwargs):
    if st.session_state["token"]:
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {st.session_state['token']}"
        kwargs["headers"] = headers
    res = requests.request(method, f"{API}{endpoint}", **kwargs)
    if res.status_code == 401:
        st.session_state["token"] = None
        st.error("Session expired. Please log in again.")
        st.rerun()
    return res

with st.sidebar:
    st.header("🔐 Authentication")
    if st.session_state["token"] is None:
        login_tab, signup_tab = st.tabs(["Login", "Sign Up"])
        
        with login_tab:
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login", use_container_width=True):
                with st.spinner("Authenticating..."):
                    res = requests.post(f"{API}/auth/login", data={"username": username, "password": password})
                    if res.status_code == 200:
                        st.session_state["token"] = res.json().get("access_token")
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password!")
                    
        with signup_tab:
            new_user = st.text_input("Username", key="signup_user")
            new_pass = st.text_input("Password", type="password", key="signup_pass")
            if st.button("Sign Up", use_container_width=True):
                with st.spinner("Creating account..."):
                    res = requests.post(f"{API}/auth/signup", json={"username": new_user, "password": new_pass})
                    if res.status_code == 200:
                        st.session_state["token"] = res.json().get("access_token")
                        st.success("Account created and logged in!")
                        st.rerun()
                    else:
                        st.error(res.json().get("detail", "Error creating account"))
    else:
        st.success("You are logged in securely.")
        if st.button("Logout", use_container_width=True):
            st.session_state["token"] = None
            st.rerun()

# Restrict app
if st.session_state["token"] is None:
    st.title("🚀 Algora AI")
    st.markdown("##### Your personal AI career mentor and DSA analyzer.")
    st.info("Please Login or Sign Up using the sidebar to access your private workspace.")
    st.stop()

st.title("🚀 Algora AI")
st.markdown("##### Your personal AI career mentor and DSA analyzer.")
st.divider()

page = st.radio("Navigation", ["🗺️ Roadmap Planner", "🔍 Code Analyzer", "📊 Intelligence Dashboard"], horizontal=True, label_visibility="collapsed")

# ROADMAP
if page == "🗺️ Roadmap Planner":
    goal = st.text_input("Enter your goal")
    if st.button("Generate"):
        with st.spinner("Generating your roadmap..."):
            res = make_authorized_request("POST", "/roadmap/", json={"goal": goal})
            if res.status_code == 200:
                roadmap_str = res.json().get("roadmap", "")
                
                with st.chat_message("assistant"):
                    st.markdown(f"### Here is your path to becoming a **{goal}** ! 🚀")
                    st.divider()
                    
                    try:
                        clean_str = roadmap_str.strip()
                        if clean_str.startswith("```json"):
                            clean_str = clean_str[7:]
                        if clean_str.startswith("```"):
                            clean_str = clean_str[3:]
                        if clean_str.endswith("```"):
                            clean_str = clean_str[:-3]
                            
                        data = json.loads(clean_str.strip())
                        phases = data.get("phases", [])
                        
                        for phase in phases:
                            st.subheader(f"📍 {phase.get('title', 'Phase')} ({phase.get('duration', '')})")
                            st.markdown("**Topics to learn:**")
                            for topic in phase.get("topics", []):
                                st.markdown(f"- {topic}")
                                
                            st.markdown("**Recommended Resources:**")
                            for res_item in phase.get("resources", []):
                                st.markdown(f"- 📚 {res_item}")
                            st.divider()
                            
                    except json.JSONDecodeError:
                        st.markdown(roadmap_str)
            else:
                try:
                    st.error(f"Error: {res.json().get('detail', 'Failed to fetch roadmap data.')}")
                except:
                    st.error("Failed to fetch roadmap data.")

# ANALYZER
elif page == "🔍 Code Analyzer":
    st.header("🔍 DSA Approach Analyzer")
    st.markdown("Describe a DSA problem and your approach, and the AI will critically evaluate it.")
    
    col1, col2 = st.columns(2)
    with col1:
        problem = st.text_input("Problem Name (e.g., Two Sum, Koko Eating Bananas)", placeholder="Enter Problem")
    with col2:
        approach = st.text_area("Your Approach", placeholder="Describe your algorithm...")

    if st.button("Analyze Approach", use_container_width=True, type="primary"):
        with st.spinner("Analyzing your approach..."):
            res = make_authorized_request("POST", "/analyze/", json={
                "problem": problem,
                "approach": approach
            })
            if res.status_code == 200:
                with st.chat_message("assistant"):
                    st.markdown("### 📝 AI Feedback")
                    st.markdown(res.json()["analysis"])
            else:
                try:
                    st.error(f"Error: {res.json().get('detail', 'Failed to analyze approach.')}")
                except:
                    st.error("Failed to analyze approach.")

# DASHBOARD
elif page == "📊 Intelligence Dashboard":
    st.header("📊 Intelligence Dashboard")
    
    dash_tab1, dash_tab2 = st.tabs(["🛣️ Saved Roadmaps", "📝 Saved Analyses"])
    
    with dash_tab1:
        with st.spinner("Loading metrics..."):
            try:
                dash_res = make_authorized_request("GET", "/dashboard/")
                stats_res = make_authorized_request("GET", "/dashboard/stats")
                
                if dash_res.status_code == 200 and stats_res.status_code == 200:
                    data = dash_res.json()
                    stats_data = stats_res.json()
                    
                    total = data.get("total_roadmaps", 0)
                    roadmaps = data.get("data", [])
                    dist = stats_data.get("goal_distribution", {})
                    
                    col1, col2 = st.columns(2)
                    col1.metric(label="Total Goals Generated", value=total, delta="Generated")
                    col2.metric(label="Unique Career Paths", value=len(dist), delta="Explored")
                    
                    st.divider()
                    
                    if dist:
                        st.subheader("📈 Goal Popularity Distribution")
                        st.bar_chart(dist)
                        
                    st.divider()
                    st.subheader("💾 Saved Roadmaps Library")
                    
                    if roadmaps:
                        for r in roadmaps:
                            col_id, col_goal, col_btn = st.columns([1, 4, 1])
                            with col_id:
                                st.write(f"**ID: #{r['id']}**")
                            with col_goal:
                                st.write(f"🎯 **{r['goal'].title()}**")
                            with col_btn:
                                if st.button("🗑️ Remove", key=f"del_{r['id']}"):
                                    make_authorized_request("DELETE", f"/dashboard/{r['id']}")
                                    st.rerun()
                            
                            with st.expander("View Full Career Roadmap", expanded=False):
                                st.markdown(r['roadmap'])
                                
                            st.write("") 
                    else:
                        st.info("No roadmaps tracked yet. Generate one in the 'Roadmap' tab first!")
                else:
                    st.error("Failed to fetch dashboard intelligence.")
            except Exception as e:
                st.error(f"Failed connecting to server infrastructure. Is the backend running? ({e})")
            
    with dash_tab2:
        with st.spinner("Loading analyses..."):
            try:
                ana_res = make_authorized_request("GET", "/dashboard/analyses/")
                if ana_res.status_code == 200:
                    ana_data = ana_res.json()
                    total_ana = ana_data.get("total_analyses", 0)
                    analyses = ana_data.get("data", [])
                    
                    st.metric("Total Analyses Complete", total_ana)
                    st.divider()
                    
                    if analyses:
                        for a in analyses:
                            col_a1, col_a2, col_a3 = st.columns([1, 4, 1])
                            with col_a1:
                                st.write(f"**#{a['id']}**")
                            with col_a2:
                                st.write(f"🔍 **{a['problem'].title()}**")
                            with col_a3:
                                if st.button("🗑️ Remove", key=f"del_ana_{a['id']}"):
                                    make_authorized_request("DELETE", f"/dashboard/analyses/{a['id']}")
                                    st.rerun()
                            
                            with st.expander("View Analysis Details", expanded=False):
                                st.markdown(f"**Your Approach:**")
                                st.info(a['approach'])
                                st.markdown(f"**AI Feedback:**")
                                st.markdown(a['analysis'])
                                
                            st.write("")
                    else:
                        st.info("No analyses saved yet. Go to the Analyzer tab to begin!")
                else:
                    st.error("Failed to fetch analyses.")
            except Exception as e:
                st.error(f"Error fetching analyses: ({e})")

# FOOTER
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Created with ❤️ by <a href='https://github.com/aishani19' target='_blank' style='text-decoration: none; color: #4b8bbe;'>Aishani Billore</a>"
    "</div>",
    unsafe_allow_html=True
)