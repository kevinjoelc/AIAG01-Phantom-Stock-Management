# AIAG01 - Phantom Stock Detection System

[![Live Demo](https://img.shields.io/badge/Demo-Live-success)](https://your-dashboard-url.vercel.app)
[![API Status](https://img.shields.io/badge/API-Online-brightgreen)](https://your-backend-url.onrender.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> **AI-powered autonomous agent system for real-time phantom stock detection in multi-tier automotive supply chains**

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Agent Workflow](#-agent-workflow)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [API Endpoints](#-api-endpoints)
- [Deployment](#-deployment)
- [Demo & Links](#-demo--links)
- [Documentation](#-documentation)

---

## 🎯 Problem Statement

### The Challenge

In multi-tier automotive supply chains (Tier-1, Tier-2, Tier-3), **phantom stock**—inventory that appears in records but doesn't physically exist—causes:

- ❌ **Production delays** due to unavailable materials
- ❌ **Incorrect demand forecasting** based on false data
- ❌ **Supply chain disruptions** across all tiers
- ❌ **Financial losses** from inflated inventory values
- ❌ **Lack of real-time detection** in traditional systems

### Real-World Impact

- **30-50%** of reported stock can be phantom inventory
- **$2.5M+** average annual loss per manufacturer
- **72 hours** average detection time with manual audits

---

## 💡 Solution

### Agentic AI System

An **autonomous multi-agent system** that detects phantom stock in real-time using:

✅ **4 Specialized Agents** working autonomously  
✅ **Message-based communication** between agents  
✅ **Real-time risk scoring** with AI-powered analysis  
✅ **Automated alerts** for critical suppliers  
✅ **Multi-tier monitoring** (Tier-1, Tier-2, Tier-3)  

### Key Features

- **Autonomous Operation**: Agents make independent decisions
- **Real-time Detection**: 5-second refresh cycle
- **Risk Classification**: CRITICAL (>70), WARNING (40-70), NORMAL (<40)
- **Visual Dashboard**: Live monitoring with color-coded alerts
- **REST API**: 7 endpoints for integration

---

## 🤖 Agent Workflow

```
┌─────────────────┐
│  Data Source    │
│ (8 Suppliers)   │
└────────┬────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│                    AGENT PIPELINE                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐                                       │
│  │ Monitoring Agent │  Validates data quality               │
│  │                  │  Detects anomalies                    │
│  └────────┬─────────┘                                       │
│           │ MonitoringOutput                                │
│           ▼                                                  │
│  ┌──────────────────┐                                       │
│  │ Validation Agent │  Calculates deviations                │
│  │                  │  Predicts expected stock              │
│  └────────┬─────────┘                                       │
│           │ ValidationOutput                                │
│           ▼                                                  │
│  ┌──────────────────┐                                       │
│  │   Risk Agent     │  Scores risk (0-100)                  │
│  │                  │  Classifies suppliers                 │
│  └────────┬─────────┘                                       │
│           │ RiskOutput                                       │
│           ▼                                                  │
│  ┌──────────────────┐                                       │
│  │ Supervisor Agent │  Generates alerts                     │
│  │                  │  Makes final decision                 │
│  └────────┬─────────┘                                       │
│           │ SupervisorOutput                                │
└───────────┼──────────────────────────────────────────────────┘
            │
            ▼
    ┌───────────────┐
    │   Dashboard   │
    │  (Real-time)  │
    └───────────────┘
```

### Agent Details

#### 1️⃣ Monitoring Agent
- **Input**: Raw inventory data (reported stock, production, consumption)
- **Process**: 
  - Validates data quality (no negatives, valid ranges)
  - Checks for missing fields
  - Flags anomalies
- **Output**: `MonitoringOutput` with validated data + anomaly count

#### 2️⃣ Validation Agent
- **Input**: Validated data from Monitoring Agent
- **Process**:
  - Calculates expected stock: `production - consumption`
  - Computes deviation: `reported - expected`
  - Calculates deviation percentage
- **Output**: `ValidationOutput` with deviations + high-risk flags (>20%)

#### 3️⃣ Risk Agent
- **Input**: Deviations from Validation Agent
- **Process**:
  - Applies risk formula: `(deviation × 50) + (tier × 6.67) + (history × 10)`
  - Classifies: CRITICAL (>70), WARNING (40-70), NORMAL (<40)
  - Identifies critical suppliers
- **Output**: `RiskOutput` with risk scores + classifications

#### 4️⃣ Supervisor Agent
- **Input**: Risk assessments from Risk Agent
- **Process**:
  - Generates alerts for critical/warning suppliers
  - Creates actionable recommendations
  - Makes final decision (ATTENTION_REQUIRED or NORMAL)
- **Output**: `SupervisorOutput` with alerts + recommendations

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.109.0
- **Language**: Python 3.9+
- **Architecture**: Autonomous agents with BaseAgent pattern
- **Communication**: Message-based (AgentMessage classes)
- **API**: REST with 7 endpoints

### Frontend
- **Technology**: Vanilla JavaScript (no frameworks)
- **Styling**: CSS3 with gradients & animations
- **Features**: Auto-refresh, real-time updates, responsive design
- **Dependencies**: None (single HTML file)

### Deployment
- **Backend**: Render / Railway (Python)
- **Frontend**: Vercel / Netlify (Static)
- **Containerization**: Docker support
- **CI/CD**: GitHub Actions ready

### Key Libraries
- `fastapi` - REST API framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Modern web browser (Chrome, Firefox, Edge)

### Option 1: One-Click Start (Windows)

```bash
START_DASHBOARD.bat
```

This automatically:
1. Starts the backend server
2. Opens the dashboard in your browser

### Option 2: Manual Start

#### Step 1: Start Backend
```bash
cd agentic_system
pip install -r requirements.txt
python main.py
```

Backend runs on: `http://localhost:8000`

#### Step 2: Open Dashboard
```bash
# Simply double-click:
dashboard/index.html

# Or open in browser:
http://localhost:8000/docs  # API documentation
```

### Option 3: Docker

```bash
docker build -t aiag01-backend .
docker run -p 8000:8000 aiag01-backend
```

### Verify Installation

```bash
# Test backend
curl http://localhost:8000/api/health

# Run automated tests
python test_phantom_detection.py
```

---

## 📡 API Endpoints

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/api/health` | GET | System health check | Status + agent list |
| `/api/suppliers` | GET | Get all suppliers (8 total) | Supplier data by tier |
| `/api/analysis/run` | POST | **Run agent pipeline** | Pipeline execution results |
| `/api/risk-scores` | GET | Get risk assessments | Risk scores + classifications |
| `/api/predicted-stock` | GET | Get stock predictions | Predicted vs reported stock |
| `/api/alerts` | GET | Get alerts & recommendations | Critical alerts + actions |
| `/api/dashboard` | GET | Get dashboard summary | Complete dashboard data |
| `/api/pipeline/trace` | GET | Get execution trace | Agent communication flow |

### Example API Call

```bash
# Run analysis
curl -X POST http://localhost:8000/api/analysis/run

# Get risk scores
curl http://localhost:8000/api/risk-scores
```

**Full API documentation**: http://localhost:8000/docs

---

## 🌐 Deployment

### Deploy Backend (Choose One)

#### Option A: Render
1. Push code to GitHub
2. Go to https://render.com
3. New Web Service → Connect repo
4. Auto-detects `render.yaml`
5. Deploy (takes 3-5 minutes)
6. Copy URL: `https://aiag01-backend.onrender.com`

#### Option B: Railway
1. Push code to GitHub
2. Go to https://railway.app
3. New Project → Deploy from GitHub
4. Auto-detects `railway.json`
5. Generate Domain
6. Copy URL: `https://aiag01-backend.up.railway.app`

### Deploy Frontend (Choose One)

#### Option A: Vercel
1. Update API URL in `dashboard/index.html` (line 317)
2. Push to GitHub
3. Go to https://vercel.com
4. Import repo → Root: `dashboard`
5. Deploy (takes 1-2 minutes)
6. Your URL: `https://aiag01-phantom-stock.vercel.app`

#### Option B: Netlify
1. Update API URL in `dashboard/index.html`
2. Push to GitHub
3. Go to https://netlify.com
4. Import repo → Base: `dashboard`
5. Deploy
6. Your URL: `https://aiag01-phantom-stock.netlify.app`

### Quick Update Script

```bash
# Update API URL for production
UPDATE_API_URL.bat
```

**Full deployment guide**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## 🎥 Demo & Links

### 🌐 Live Deployment

> **📌 ADD YOUR DEPLOYED URLS HERE:**

- **Live Dashboard**: `https://your-dashboard-url.vercel.app` ← Replace with your Vercel URL
- **Backend API**: `https://your-backend-url.onrender.com` ← Replace with your Render URL
- **API Documentation**: `https://your-backend-url.onrender.com/docs`

### 🎬 Demo Video

> **📌 ADD YOUR DEMO VIDEO HERE:**

- **YouTube**: `https://youtu.be/YOUR_VIDEO_ID` ← Upload 3-5 min demo
- **Loom**: `https://loom.com/share/YOUR_VIDEO_ID` ← Alternative platform

**What to show in demo:**
1. Dashboard loading with real-time data
2. Agent pipeline status updates
3. Phantom stock detection (red suppliers)
4. Risk scores and alerts
5. Auto-refresh functionality
6. API endpoints in action

### 📊 Presentation

> **📌 ADD YOUR PRESENTATION HERE:**

- **Google Slides**: `https://docs.google.com/presentation/d/YOUR_PRESENTATION_ID`
- **PDF**: `https://drive.google.com/file/d/YOUR_FILE_ID`

**Recommended slides:**
1. Problem statement
2. Solution overview
3. Agent architecture diagram
4. Live demo screenshots
5. Tech stack
6. Results & impact

### 📸 Screenshots

> **📌 ADD SCREENSHOTS TO `/screenshots` FOLDER:**

```bash
mkdir screenshots
# Add these images:
- dashboard-overview.png
- agent-pipeline.png
- risk-detection.png
- api-docs.png
```

---

## 📚 Documentation

### Setup & Configuration
- [📖 Setup Guide](SETUP.md) - Local installation
- [🚀 Deployment Guide](DEPLOYMENT_GUIDE.md) - Cloud deployment
- [📁 Folder Structure](FINAL_STRUCTURE.md) - Project organization

### API & Testing
- [🧪 API Testing Guide](API_TESTING_GUIDE.md) - Test all endpoints
- [📋 API Examples](agentic_system/API_EXAMPLES.md) - Sample responses
- [🔍 Verification Steps](API_TESTING_GUIDE.md#verify-phantom-stock-detection) - How to verify detection

### Architecture & Integration
- [🏗️ Agent Communication](agentic_system/AGENT_COMMUNICATION.md) - Message flow
- [🔗 Langflow Integration](agentic_system/LANGFLOW_INTEGRATION.md) - Visual workflow
- [🔗 Flowise Integration](agentic_system/FLOWISE_INTEGRATION.md) - Alternative platform

### Dashboard
- [📊 Dashboard Guide](dashboard/README.md) - Frontend setup
- [🎨 UI Components](dashboard/README.md#dashboard-features) - Feature overview

---

## 🧪 Testing

### Run All Tests

```bash
# Automated test suite
RUN_API_TESTS.bat

# Or individual test
python test_phantom_detection.py
```

### Expected Output

```
✅ PHANTOM STOCK DETECTED!

Affected Suppliers:
  - Tier1 Electronics: 3,300 units (63.5% deviation)
  - Tier2 Materials: 1,800 units (45.2% deviation)

Critical Suppliers: 2
Warning Suppliers: 3
Normal Suppliers: 3
```

---

## 📊 Project Stats

- **Lines of Code**: ~4,300
- **Python Files**: 12
- **API Endpoints**: 7
- **Autonomous Agents**: 4
- **Supported Tiers**: 3 (Tier-1, Tier-2, Tier-3)
- **Suppliers Monitored**: 8
- **Refresh Rate**: 5 seconds
- **Detection Accuracy**: Real-time

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

---

## 👥 Team

> **📌 ADD YOUR TEAM INFORMATION:**

- **Team Name**: [Your Team Name]
- **Hackathon**: AIAG01
- **Members**:
  - [Member 1 Name] - [Role] - [GitHub/LinkedIn]
  - [Member 2 Name] - [Role] - [GitHub/LinkedIn]
  - [Member 3 Name] - [Role] - [GitHub/LinkedIn]

---

## 📧 Contact

- **Email**: [your-email@example.com]
- **GitHub**: [https://github.com/your-username]
- **LinkedIn**: [https://linkedin.com/in/your-profile]

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- AIAG01 Hackathon organizers
- FastAPI framework
- Open source community

---

<div align="center">

**Built with ❤️ for AIAG01 Hackathon**

[⬆ Back to Top](#aiag01---phantom-stock-detection-system)

</div>
