import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# --- CONFIG & AI SETUP ---
st.set_page_config(page_title="Nexus M&A Command Center", layout="wide")

# Fetch API Key from Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing GEMINI_API_KEY in Streamlit Secrets.")

# --- AGENTIC ENGINE ---
def nexus_agent(workstream, query):
    model = genai.GenerativeModel('gemini-1.5-flash')
    context = f"You are the {workstream} Lead for the $10.1B BP-Castrol divestiture. Date: March 2026."
    response = model.generate_content(f"{context}\n\nTask: {query}")
    return response.text

# --- UI LAYOUT ---
st.title("🛡️ Nexus M&A: Strategic Command Center")

# Tabbed Workstreams
tabs = st.tabs(["📊 PMO", "⚖️ Legal", "💻 IT/Digital", "👥 HR", "💰 Finance"])

with tabs[2]: # IT/Digital Focus
    st.header("💻 IT & Digital Separation")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Implementation Guidance")
        if st.button("Generate SAP Migration Roadmap"):
            st.info(nexus_agent("IT Lead", "Draft a 5-step SAP 'Clone and Go' roadmap for the Castrol divestiture."))
    with col2:
        st.subheader("Day 1 Readiness Checklist")
        st.checkbox("SAP Instance Cloning Complete", value=False)
        st.checkbox("Cyber Clean Room Scan Verified", value=False)
        st.checkbox("Network 'Kill Switch' Tested", value=False)

# (Other tabs follow the same 'render_workstream' pattern from previous steps)