import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import time

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(page_title="Nexus M&A Autonomous OS", layout="wide")

# Professional Dark Theme Styling
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

# --- 2. UPDATED AGENTIC ENGINE ---
# Using the most stable model string for 2026
MODEL_ID = "gemini-1.5-flash" 

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key missing. Please add GEMINI_API_KEY to your Streamlit Secrets.")

class NexusM&A:
    @staticmethod
    def execute_agent(role, task):
        try:
            model = genai.GenerativeModel(MODEL_ID)
            personas = {
                "PM_Agent": "Chief M&A Orchestrator. You define roadmaps, assign tasks to IT/HR/Legal, and track dependencies. Direct and strategic.",
                "Functional_Agent": "M&A Implementation Specialist. You execute technical tasks in AAD, Saviynt, Workday, and SAP. Technical and detailed.",
                "Auditor_Agent": "M&A Compliance Auditor. You scan work for GDPR, SOX, and SEBI risks. Critical and uncompromising."
            }
            context = f"Context: $10.1B BP-Castrol Divestiture. Valued at $V = 8.6 \\times EBITDA$."
            prompt = f"ROLE: {personas[role]}\n{context}\nTASK: {task}"
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Agent Error: {str(e)}"

# --- 3. PERSISTENT STATE ---
if 'task_registry' not in st.session_state:
    st.session_state.task_registry = pd.DataFrame([
        {"ID": "DIV-001", "Stream": "IT", "Task": "Entra ID Tenant Decoupling", "Status": "Active", "Risk": "Low"},
        {"ID": "DIV-002", "Stream": "Legal", "Task": "India MTO Regulatory Filing", "Status": "In Progress", "Risk": "High"},
        {"ID": "DIV-003", "Stream": "HR", "Task": "Workday Global HCM Split", "Status": "Pending", "Risk": "Medium"}
    ])

# --- 4. NAVIGATION & UI ---
with st.sidebar:
    st.title("🛡️ NEXUS OS v9.0")
    st.caption("Autonomous Divestiture Platform")
    nav = st.radio("Command Center", ["Dashboard", "The War Room", "Team Onboarding", "RAID & Tracking"])
    
    st.divider()
    st.metric("Deal Valuation", "$10.1B")
    st.metric("MTO Price", "₹194.04")
    
    # Diagnostic Tool
    if st.button("Check API Availability"):
        try:
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            st.write("Available Models:", models)
        except:
            st.error("Cannot list models. Check API Key.")

# --- 5. FUNCTIONAL TABS ---

if nav == "Dashboard":
    st.header("Autonomous Program Dashboard")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Overall Readiness", "68%", "+2%")
    c2.metric("Critical Blockers", "3", "-1")
    c3.metric("Agent Sync", "Healthy")
    c4.metric("Days to Day-1", "292")

    st.subheader("Implementation Roadmap")
    df_chart = pd.DataFrame([
        dict(Task="Entity Formation", Start='2026-01-01', End='2026-06-30', Stream='Legal'),
        dict(Task="System Decoupling", Start='2026-03-01', End='2026-10-31', Stream='IT/Digital'),
        dict(Task="Day 1 Cutover", Start='2026-11-01', End='2026-12-31', Stream='Execution')
    ])
    fig = px.timeline(df_chart, x_start="Start", x_end="End", y="Task", color="Stream", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

elif nav == "The War Room":
    st.header("Autonomous Execution Lab")
    st.write("The PM Agent will break down your goal and the Auditor will validate the output.")
    
    user_goal = st.text_input("Enter High-Level Goal", "Implement the Saviynt-to-Workday bridge for 4,500 employees.")
    
    if st.button("Execute Multi-Agent Loop"):
        with st.status("Agentic Orchestration Active...") as status:
            # Step 1: PM Agent
            st.write("🤖 PM Agent: Drafting Workstream Tasks...")
            pm_tasks = NexusM&A.execute_agent("PM_Agent", f"Break this into 3 tasks for IT and HR: {user_goal}")
            
            # Step 2: Functional Agent
            st.write("🛠️ Functional Agent: Generating Implementation Plan...")
            impl_plan = NexusM&A.execute_agent("Functional_Agent", f"Create a technical implementation for: {pm_tasks}")
            
            # Step 3: Auditor Agent
            st.write("⚖️ Auditor Agent: Performing Risk & Compliance Check...")
            audit_report = NexusM&A.execute_agent("Auditor_Agent", f"Audit this plan for SOX/GDPR/Security gaps: {impl_plan}")
            
            status.update(label="Orchestration Complete", state="complete")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="agent-card worker-card"><h3>Proposed Implementation</h3>{impl_plan}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="agent-card auditor-card"><h3>Auditor Verdict</h3>{audit_report}</div>', unsafe_allow_html=True)

elif nav == "Team Onboarding":
    st.header("Resource Training & Tracking")
    
    name = st.text_input("New Member Name")
    stream = st.selectbox("Workstream", ["IT", "Legal", "HR", "Finance", "Procurement"])
    
    if st.button("Launch Onboarding Agent"):
        training_plan = NexusM&A.execute_agent("PM_Agent", f"Generate a 5-day onboarding plan for {name} in {stream}. Include Saviynt and Workday access steps.")
        st.subheader(f"Onboarding Path for {name}")
        st.markdown(training_plan)

elif nav == "RAID & Tracking":
    st.header("Activity Tracker & Autonomous Risk Assessment")
    st.data_editor(st.session_state.task_registry, use_container_width=True, num_rows="dynamic")
    
    if st.button("Run AI Risk Assessment"):
        risk_summary = NexusM&A.execute_agent("Auditor_Agent", f"Review this task registry and identify the #1 risk to a December close: {st.session_state.task_registry.to_string()}")
        st.error(risk_summary)