import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import time
from datetime import datetime

# --- 1. THEME & UI INJECTION ---
st.set_page_config(page_title="Nexus M&A Autonomous OS", layout="wide")

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

# --- 2. MULTI-AGENT ENGINE ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key missing. Add GEMINI_API_KEY to Streamlit Secrets.")

class NexusOS:
    @staticmethod
    def query_agent(role, prompt, model_name='gemini-1.5-flash'):
        model = genai.GenerativeModel(model_name)
        personas = {
            "PM_Agent": "Lead M&A Director. Responsible for master roadmap, task delegation, and workstream synchronization. High-level, strategic, and concise.",
            "IT_Digital_Agent": "Expert in Entra ID, Saviynt, Workday, and SAP. Focuses on identity migration, data scrubbing, and technical cutover.",
            "HR_Legal_Agent": "Expert in TUPE, payroll separation, and SEBI/India MTO regulations. Focuses on people and entity compliance.",
            "Auditor_Agent": "Senior Quality & Risk Auditor. Your job is to find flaws, gaps, and compliance risks in other agents' work. Be critical."
        }
        full_prompt = f"SYSTEM ROLE: {personas[role]}\nCONTEXT: $10.1B Divestiture (Dec 2026 Target)\nTASK: {prompt}"
        return model.generate_content(full_prompt).text

# --- 3. PERSISTENT DATA STATE ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = pd.DataFrame([
        {"ID": "T1", "Stream": "IT", "Activity": "AAD Tenant-to-Tenant Sync", "Status": "80%", "Owner": "IT Agent"},
        {"ID": "T2", "Stream": "Legal", "Activity": "India MTO Pricing Verification", "Status": "20%", "Owner": "Legal Agent"},
        {"ID": "T3", "Stream": "HR", "Activity": "Workday Payroll Cutover", "Status": "0%", "Owner": "HR Agent"}
    ])
if 'team' not in st.session_state:
    st.session_state.team = pd.DataFrame([{"Name": "Nexus AI", "Role": "Lead Architect", "Progress": "100%"}])

# --- 4. NAVIGATION ---
with st.sidebar:
    st.title("🛡️ NEXUS OS v8.0")
    st.subheader("Autonomous Divestiture Engine")
    nav = st.radio("Navigation", ["Command Center", "Agentic War Room", "Team Onboarding", "System Roadmap"])
    st.divider()
    st.metric("Global Readiness", "64%", "+5% vs Last Week")

# --- 5. WORKSTREAM LOGIC ---

if nav == "Command Center":
    st.header("Executive Command Center")
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Open Risks", "12", "4 High Priority")
    with c2: st.metric("Active Agents", "4", "All Systems Green")
    with c3: st.metric("TSA Exit Target", "Dec 2028", "On Track")

    st.subheader("Autonomous Workstream Status")
    fig = px.bar(st.session_state.tasks, x='Activity', y='Status', color='Stream', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    if st.button("Run Global Autonomous Risk Audit"):
        with st.spinner("PM Agent & Auditor Agent collaborating..."):
            report = NexusOS.query_agent("PM_Agent", f"Analyze this task list and identify critical blockers: {st.session_state.tasks.to_string()}")
            st.warning(report)

elif nav == "Agentic War Room":
    st.header("Autonomous Execution Lab")
    goal = st.text_input("Define Program Goal", "Migrate 4,500 identities from BP Entra ID to Castrol standalone tenant via Saviynt.")
    
    if st.button("Execute Agentic Chain"):
        # PM Agent defines the steps
        with st.status("PM Agent defining execution path...") as s:
            steps = NexusOS.query_agent("PM_Agent", f"Break this goal into 3 technical tasks: {goal}")
            st.markdown(f'<div class="agent-card pm-card"><b>PM Agent Output:</b><br>{steps}</div>', unsafe_allow_html=True)
            
            # IT Agent implements
            st.write("IT Agent drafting technical requirements...")
            tech_plan = NexusOS.query_agent("IT_Digital_Agent", f"Create a technical plan for these steps: {steps}")
            st.markdown(f'<div class="agent-card worker-card"><b>IT Agent Plan:</b><br>{tech_plan}</div>', unsafe_allow_html=True)
            
            # Auditor checks
            st.write("Auditor Agent performing security & compliance audit...")
            audit = NexusOS.query_agent("Auditor_Agent", f"Critically review this plan for security flaws in AAD/Saviynt: {tech_plan}")
            st.markdown(f'<div class="agent-card auditor-card"><b>Auditor Agent Verdict:</b><br>{audit}</div>', unsafe_allow_html=True)
            s.update(label="Workflow Complete", state="complete")

elif nav == "Team Onboarding":
    st.header("Human Onboarding & Tracking")
    name = st.text_input("Full Name")
    role = st.selectbox("Assigned Workstream", ["IT", "HR", "Legal", "Finance"])
    
    if st.button("Onboard New Member"):
        training = NexusOS.query_agent("PM_Agent", f"Create a 5-day onboarding plan for {name} joining the {role} team for the BP-Castrol divestiture.")
        st.success(f"{name} added to the orchestration loop.")
        st.markdown(training)
        new_row = {"Name": name, "Role": role, "Progress": "0%"}
        st.session_state.team = pd.concat([st.session_state.team, pd.DataFrame([new_row])], ignore_index=True)
    
    st.subheader("Team Progress Tracking")
    st.table(st.session_state.team)

elif nav == "System Roadmap":
    st.header("Full Landscape Readiness")
    
    st.info("The agents are currently monitoring cross-system dependencies between Workday (Identity Source) and Saviynt (Governance).")
    st.data_editor(st.session_state.tasks, use_container_width=True)