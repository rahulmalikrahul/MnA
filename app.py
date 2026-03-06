import streamlit as st
import pandas as pd
import plotly.express as px
from google import genai
from google.genai import types
import time

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(page_title="Nexus M&A Autonomous OS", layout="wide")

# Theme & UI Styling
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    .agent-card { padding: 20px; border-radius: 10px; margin-bottom: 15px; border: 1px solid #30363d; }
    .pm-card { border-left: 5px solid #238636; background-color: #0b2533; }
    .auditor-card { border-left: 5px solid #f85149; background-color: #2d1313; }
    .worker-card { border-left: 5px solid #58a6ff; background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. UPDATED AGENTIC ENGINE (2026 SDK) ---
MODEL_ID = "gemini-2.0-flash" 

def get_genai_client():
    if "GEMINI_API_KEY" in st.secrets:
        return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("API Key missing. Add GEMINI_API_KEY to Streamlit Secrets.")
        return None

class NexusMA:  # FIX: Removed '&' to resolve SyntaxError
    @staticmethod
    def execute_workflow(role, prompt_text):
        client = get_genai_client()
        if not client: return "Connection Error"
        
        personas = {
            "PM": "Chief M&A Orchestrator. Focus on roadmaps, timelines ($10.1B deal), and cross-stream dependencies.",
            "Functional": "Technical Lead. Expert in Entra ID tenant separation, Saviynt GRC, and Workday HCM data splits.",
            "Auditor": "Risk Auditor. Scan for SOX, GDPR, and SEBI compliance gaps. Be highly critical."
        }
        
        sys_instr = f"ROLE: {personas[role]}. Context: BP-Castrol divestiture to Stonepeak."
        
        try:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt_text,
                config=types.GenerateContentConfig(system_instruction=sys_instr)
            )
            return response.text
        except Exception as e:
            return f"Agent Logic Failed: {str(e)}"

# --- 3. DASHBOARD DATA ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = pd.DataFrame([
        {"ID": "IT-206", "Stream": "Digital", "Task": "AAD Tenant Migration", "Status": "In Progress"},
        {"ID": "HR-401", "Stream": "People", "Task": "Workday Record Partition", "Status": "Pending"},
        {"ID": "LG-902", "Stream": "Legal", "Task": "India MTO Compliance", "Status": "Active"}
    ])

# --- 4. NAVIGATION ---
with st.sidebar:
    st.title("🛡️ NEXUS OS v9.5")
    nav = st.radio("Management Hub", ["Dashboard", "Agentic War Room", "Human Onboarding"])
    st.divider()
    st.metric("Deal Valuation", "$10.1B")
    st.metric("MTO Price", "₹194.04")

# --- 5. FUNCTIONAL VIEWS ---

if nav == "Dashboard":
    st.header("Executive Program Dashboard")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Separation Readiness", "64%", "+2%")
    c2.metric("Open Risks", "14", "High Priority")
    c3.metric("TSA Exit Date", "Dec 2028")
    
    st.subheader("Workstream Task Registry")
    st.data_editor(st.session_state.tasks, use_container_width=True)

elif nav == "Agentic War Room":
    st.header("Autonomous Execution Lab")
    goal = st.text_input("Define Target Goal", "Automate the transfer of 4,500 identities from BP to Castrol standalone Saviynt.")
    
    if st.button("Execute Agentic Loop"):
        with st.status("Agents Syncing...") as s:
            st.write("🤖 PM Agent: Designing sequence...")
            roadmap = NexusMA.execute_workflow("PM", f"Create 3 milestones for: {goal}")
            
            st.write("🛠️ Technical Agent: Configuring logic...")
            tech = NexusMA.execute_workflow("Functional", f"Detail technical steps for: {roadmap}")
            
            st.write("⚖️ Auditor Agent: Validating risks...")
            audit = NexusMA.execute_workflow("Auditor", f"Audit these steps for security flaws: {tech}")
            s.update(label="Workflow Finalized", state="complete")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="agent-card worker-card"><h3>Implementation Guide</h3>{tech}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="agent-card auditor-card"><h3>Auditor Verdict</h3>{audit}</div>', unsafe_allow_html=True)

elif nav == "Human Onboarding":
    st.header("Team Onboarding & Knowledge Graph")
    
    name = st.text_input("New Member Name")
    dept = st.selectbox("Department", ["IT Infrastructure", "HR Ops", "Legal & MTO", "Procurement"])
    if st.button("Generate Onboarding Plan"):
        plan = NexusMA.execute_workflow("PM", f"Onboarding guide for {name} joining {dept}. Focus on Saviynt access.")
        st.info(plan)