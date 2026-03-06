# 🛡️ Nexus M&A Autonomous OS (v14.0)
### **The Digital PMO for the $10.1B BP-Castrol / Stonepeak Divestiture**

Nexus M&A OS is an agentic orchestration platform designed to manage the high-stakes separation of global IT, HR, Legal, and Procurement landscapes. It solves the "Execution Gap" by replacing manual tracking with autonomous oversight and risk-adjusted decision gates.

---

## 🚀 Core Functional Suites

### 1. **Autonomous Execution Lab (Agentic War Room)**
Uses a multi-agent loop (**PM Agent, Functional Agent, Auditor Agent**) to transform high-level goals into technical implementation plans. Includes built-in **Quota Protection** (4s pacing) to ensure stability on Free Tier APIs.

### 2. **Global Risk Heatmap & Dashboard**
Visualizes the $10.1B exposure across key geographies (India, UK, Germany, USA). Dynamic readiness scores update automatically as workstreams complete their tasks.


### 3. **Readiness Gates (The Digital Gatekeeper)**
A formalized "Go/No-Go" framework. Access to the **Day 1 Playbook** is strictly locked until leads from IT, Legal, HR, and Finance certify their readiness via digital signature.

### 4. **Dependency & Conflict Mapper**
The **Auditor Agent** scans the task registry to identify "Toxic Dependencies"—identifying where a delay in one stream (e.g., Legal Entity Setup) will inevitably block another (e.g., AAD Tenant Migration).


### 5. **AI Action Tracker & SteerCo Reporting**
- **SteerCo Gen:** One-click generation of Weekly Steering Committee reports (Markdown format).
- **Action Tracker:** The AI automatically extracts action items from reports and assigns owners.
- **Auto-Nudge:** Generates context-aware follow-ups for overdue tasks.

---

## 🛠️ Installation & Deployment

### **Step 1: Repository Setup**
Clone this repository and ensure the following file structure:
- `app.py` (The core engine)
- `requirements.txt` (The dependency list)
- `.streamlit/secrets.toml` (For local testing)

### **Step 2: Environment Config**
Install dependencies:
```bash
pip install streamlit pandas plotly google-genai