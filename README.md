# AIAG01 – Agentic AI-Enabled Multi-Tier Phantom Stock Management

## Problem Statement
Manufacturers have limited visibility beyond Tier-1 suppliers. When Tier-2 and Tier-3 suppliers face disruptions such as machine failures, labor shortages, or logistics delays, inventory systems still show stock as available even when it is not physically present. This creates phantom stock, causing production delays, missed delivery deadlines, and financial losses.

The challenge is to build an Agentic AI system that continuously validates multi-tier supplier inventory, detects inconsistencies, and raises early risk alerts.

---

## Solution Description
This project implements a multi-agent AI system that monitors suppliers across Tier-1, Tier-2, and Tier-3 levels. Autonomous agents collect reported inventory, predict expected stock based on production and historical trends, detect mismatches, and estimate disruption risk.

A real-time dashboard visualizes phantom stock, risk levels, and alerts so manufacturers can take proactive action before failures propagate.

---

## Agent Workflow

1. Supply Monitoring Agent  
   Collects supplier inventory, production, and shipment data.

2. Validation Agent  
   Predicts expected stock and compares it with reported inventory.

3. Risk Analysis Agent  
   Calculates phantom stock probability and disruption risk.

4. Supervisor Agent  
   Reviews agent outputs and triggers alerts.

Workflow:
Supplier Data → Monitoring Agent → Validation Agent → Risk Agent → Supervisor Agent → Dashboard & Alerts

---

## Tech Stack Used

Backend:
- Python
- FastAPI
- Uvicorn
- Multi-Agent Orchestration

Frontend:
- HTML
- CSS
- JavaScript

Agentic Tools:
- Amazon Q
- LangFlow / Flowise

Deployment:
- Backend: Render
- Frontend: GitHub Pages

Version Control:
- GitHub

---

## Setup and Execution Steps

1. Clone the repository
   git clone https://github.com/kevinjoelc/AIAG01-Phantom-Stock-Management.git

cd AIAG01-Phantom-Stock-Management

2. Run the backend
cd agentic_system
pip install -r requirements.txt
python main.py

The backend will run at:http://localhost:8000
in any web browser.

---

## Prototype Link

Frontend:
https://kevinjoelc.github.io/AIAG01-Phantom-Stock-Management

Backend API:
https://aiag01-phantom-stock-management.onrender.com

Demo Video:





