import streamlit as st
import pandas as pd
import plotly.express as px
from google import genai
from google.genai import types
import time
from datetime import datetime

# --- 1. SYSTEM CONFIGURATION & UI ---
st.set_page_config(page_title="Nexus M&A Autonomous OS", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    .agent-card { padding: 20px; border-radius: 10px; margin-bottom: 15px; border: 1px solid #30363d; }
    .pm-card { border-left: 5px solid #238636; background-color: #0b2533; }
    .auditor-card { border-left: 5px solid #f85149; background-color: #2d1313; }
    .worker-card { border-left: 5px solid #58a6ff; background-color: #161b22; }
    .conflict-card { border-left: 5px solid #ff9b00; background-color: #33220b; }
    .gate-card { padding: 20px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #30363d; }
    .gate-locked { border-left: 5px solid #f85149; background-color: #2d1313; }
    .gate-open { border-left: 5px solid #238636; background-color: #0b2533; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. QUOTA-PROTECTED AGENT ENGINE ---
MODEL_ID = "gemini-2.0-flash" 

def get_client():
    if "GEMINI_API_KEY" in st.secrets:
        return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    return None

def agent_call(role, prompt_text):
    client = get_client()
    if not client: return "Error: API Key missing in Secrets."
    personas = {
        "PM": "Chief M&A Orchestrator. Manage $10.1B deal. Strategic and direct.",
        "Functional": "Implementation Lead. Expert in IT (Entra/Saviynt), HR (Workday), Legal, and Procurement.",
        "Auditor": "Risk Auditor. Scan for SOX, GDPR, SEBI gaps, and cross-stream dependencies."
    }
    sys_instr = f"ROLE: {personas[role]}. Context: BP-Castrol divestiture to Stonepeak (Target Dec 2026)."
    try:
        response = client.models.generate_content(
            model=MODEL_ID, contents=prompt_text,
            config=types.GenerateContentConfig(system_instruction=sys_instr)
        )
        return response.text
    except Exception as e:
        if "429" in str(e): return "⚠️ Quota Limit. Please wait 10 seconds."
        return f"Error: {str(e)}"

# --- 3. PERSISTENT DATA STATE ---
if 'pmi_tracker' not in st.session_state:
    st.session_state.pmi_tracker = pd.DataFrame([
        {"Stream": "IT/Digital", "Task": "AAD Tenant Migration", "Status": "In Progress", "Readiness": 45},
        {"Stream": "HR/People", "Task": "Workday Payroll Split", "Status": "Pending", "Readiness": 20},
        {"Stream": "Legal", "Task": "India MTO Compliance", "Status": "Active", "Readiness": 35},
        {"Stream": "Procurement", "Task": "Vendor Novation", "Status": "Not Started", "Readiness": 10}
    ])

if 'geo_data' not in st.session_state:
    st.session_state.geo_data = pd.DataFrame([
        {"Region": "India", "Exposure": 4500, "Readiness": 35},
        {"Region": "United Kingdom", "Exposure": 3200, "Readiness": 85},
        {"Region": "Germany", "Exposure": 1800, "Readiness": 60},
        {"Region": "United States", "Exposure": 600, "Readiness": 90}
    ])

if 'approvals' not in st.session_state:
    st.session_state.approvals = {
        "IT": {"status": "Pending", "lead": "CTO Office", "ts": None},
        "Legal": {"status": "Pending", "lead": "GC Office", "ts": None},
        "HR": {"status": "Pending", "lead": "CHRO", "ts": None},
        "Finance": {"status": "Pending", "lead": "CFO Office", "ts": None}
    }

if 'action_items' not in st.session_state:
    st.session_state.action_items = pd.DataFrame([
        {"ID": "ACT-001", "Owner": "Legal", "Action": "Finalize India MTO Escrow", "Status": "Open"}
    ])

# --- 4. NAVIGATION ---
with st.sidebar:
    st.title("🛡️ NEXUS OS v15.0")
    nav = st.radio("Management Hub", ["Dashboard & Heatmap", "Agentic War Room", "Readiness Gates", "Action Tracker", "Day 1 Playbook"])
    st.divider()
    all_ready = all(v["status"] == "Approved" for v in st.session_state.approvals.values())
    if all_ready: st.success("🟢 SYSTEM UNLOCKED")
    else: st.error("🔴 GATES LOCKED")
    st.metric("Deal Valuation", "$10.1B")

# --- 5. FUNCTIONAL VIEWS ---

if nav == "Dashboard & Heatmap":
    st.header("PMI Executive Command Center")
    
    fig = px.choropleth(st.session_state.geo_data, locations="Region", locationmode="country names", 
                        color="Readiness", hover_data=["Exposure"], color_continuous_scale="RdYlGn", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Workstream Monitor")
    st.data_editor(st.session_state.pmi_tracker, use_container_width=True)
    
    if st.button("Generate SteerCo Report"):
        with st.spinner("PM Agent synthesizing data..."):
            report = agent_call("PM", f"Draft SteerCo report for: {st.session_state.pmi_tracker.to_string()}")
            st.session_state.current_report = report
            st.markdown(f'<div class="agent-card pm-card">{report}</div>', unsafe_allow_html=True)
            st.download_button("Download Report", report, file_name="SteerCo_Report.md")

elif nav == "Agentic War Room":
    st.header("Autonomous Execution Lab")
    goal = st.text_input("Enter Goal", "Migrate 4,500 users from BP to Castrol Saviynt.")
    if st.button("Execute Agentic Loop"):
        with st.status("Orchestrating (Quota Protected)...") as s:
            plan = agent_call("PM", f"Outline 3 steps for: {goal}")
            time.sleep(4)
            tech = agent_call("Functional", f"Technical config for: {plan}")
            time.sleep(4)
            audit = agent_call("Auditor", f"Audit for security: {tech}")
            s.update(label="Workflow Complete", state="complete")
        st.markdown(f'<div class="agent-card worker-card"><h3>Technical Plan</h3>{tech}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="agent-card auditor-card"><h3>Auditor Verdict</h3>{audit}</div>', unsafe_allow_html=True)

elif nav == "Readiness Gates":
    st.header("🏁 Go/No-Go Readiness Gates")
    
    cols = st.columns(2)
    for i, (stream, data) in enumerate(st.session_state.approvals.items()):
        with cols[i % 2]:
            status_style = "gate-open" if data["status"] == "Approved" else "gate-locked"
            st.markdown(f'<div class="gate-card {status_style}"><h3>{stream}</h3>Status: {data["status"]}</div>', unsafe_allow_html=True)
            if data["status"] == "Pending" and st.button(f"Sign {stream}"):
                st.session_state.approvals[stream]["status"] = "Approved"
                st.session_state.approvals[stream]["ts"] = datetime.now().strftime("%H:%M")
                st.rerun()

elif nav == "Action Tracker":
    st.header("🎯 AI Action Tracker")
    
    st.session_state.action_items = st.data_editor(st.session_state.action_items, use_container_width=True, num_rows="dynamic")
    if st.button("Extract Actions from Report"):
        if 'current_report' in st.session_state:
            new_actions = agent_call("PM", f"Extract 3 tasks from: {st.session_state.current_report}")
            st.info(new_actions)
        else: st.warning("Generate report first.")

elif nav == "Day 1 Playbook":
    st.header("📖 Hour-by-Hour Playbook")
    
    if not all_ready: st.warning("Locked until all Readiness Gates are signed.")
    else:
        event = st.text_input("Cutover Event", "SAP Global Split")
        if st.button("Generate HbH Sequence"):
            seq = agent_call("PM", f"Generate T-minus 24h to T-plus 24h for: {event}")
            st.markdown(f'<div class="agent-card worker-card">{seq}</div>', unsafe_allow_html=True)