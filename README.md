# Partner Integration Onboarding Simulator

A REST API platform that validates publisher API integrations against Google Ad Manager configuration standards - simulating real-world **Product Solutions Engineer** workflows at Google.

---

## Overview

When a publisher partner onboards onto Google Ad Manager, a PSE validates their technical integration setup, identifies misconfigurations, and provides actionable fix recommendations. This project simulates that exact workflow as a full-stack application.

```
Partner submits integration details
        ↓
System validates their API configuration
        ↓
Pandas generates a health report with scores
        ↓
Dashboard surfaces issues and recommended fixes
```

---

## Features

- **Partner Registration** — onboard publisher partners with their API and ad platform details
- **Automated Validation Engine** — runs 4 checks against partner API integrations
  - Endpoint Reachability
  - Response Latency
  - HTTPS Security
  - Authentication Method Validity
- **Pandas Health Reports** — aggregates validation results into a scored health report
- **Real-time Dashboard** — Streamlit UI for visualizing integration health across partners
- **JWT Authentication** — secured endpoints
- **Auto-generated API Docs** — Swagger UI at `/docs`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Database | OracleDB, SQLAlchemy |
| Data Processing | Pandas |
| Frontend | Streamlit |
| Authentication | JWT |
| Validation | Pydantic |
| HTTP Client | httpx (async) |
| Deployment | GCP Cloud Run |

---

## Project Structure

```
partner-onboarding-simulator/
│
├── main.py                  # FastAPI app entry point
├── requirements.txt         # Dependencies
├── .env.example             # Environment variable template
│
├── database/
│   ├── connection.py        # OracleDB connection + session
│   └── models.py            # SQLAlchemy table models
│
├── schemas/
│   └── partner.py           # Pydantic validation schemas
│
├── services/
│   ├── validator.py         # Async validation engine
│   └── report_generator.py  # Pandas health report generator
│
└── dashboard/
    └── app.py               # Streamlit dashboard
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `GET` | `/status` | Server uptime and version |
| `GET` | `/info` | Project information |
| `POST` | `/partners` | Register new partner |
| `GET` | `/partners` | List all partners |
| `GET` | `/partners/{id}` | Get partner by ID |
| `POST` | `/validate/{id}` | Run validation + generate health report |
| `POST` | `/auth/register` | Register new user |
| `POST` | `/auth/login` | Login and get JWT token |

---

## Validation Checks

| Check | Severity | What it Tests |
|---|---|---|
| Endpoint Reachability | Critical | Is the partner API accessible? |
| Response Latency | Warning | Does it respond under 2000ms? |
| HTTPS Security | Critical | Is the connection encrypted? |
| Auth Method Validity | Critical | Is the auth method valid for the ad platform? |

---

## Sample Health Report Response

```json
{
  "health_score": 75.0,
  "status": "Not bad",
  "total_checks": 4,
  "passed_checks": 3,
  "failed_checks": 1,
  "critical_issues": [
    {
      "check_type": "HTTPS Security",
      "message": "Endpoint is not using HTTPS",
      "fix": "Use HTTPS instead of HTTP"
    }
  ],
  "warnings": []
}
```

---

## Local Setup

### Prerequisites
- Python 3.10+
- Oracle XE (local) or any Oracle DB instance
- Oracle Instant Client (for thick mode)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/partner-onboarding-simulator.git
cd partner-onboarding-simulator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory:

```
ORACLE_USER=your_username
ORACLE_PASSWORD=your_password
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE=XE
```

### Run the Application

```bash
# Terminal 1 — Start FastAPI backend
uvicorn main:app --reload

# Terminal 2 — Start Streamlit dashboard
streamlit run dashboard/app.py
```

- API: `http://localhost:8000`
- Swagger Docs: `http://localhost:8000/docs`
- Dashboard: `http://localhost:8501`

---

## Requirements

```
fastapi
uvicorn
sqlalchemy
oracledb
pandas
pydantic
python-jose[cryptography]
passlib[bcrypt]
python-dotenv
streamlit
requests
httpx
```

---

## PSE Relevance

This project directly mirrors Product Solutions Engineer responsibilities at Google:

| PSE Responsibility | How This Project Covers It |
|---|---|
| Delivering solutions to partner problems | Automated validation engine flags partner issues |
| Troubleshooting implementation issues | Health reports with root cause and fix recommendations |
| Providing technical guidance | Actionable fix suggestions per failed check |
| Ensuring client satisfaction | Health scoring system with pass/fail per check |
| Advocating for product features | Ad platform-specific validation rules |

---

## Author

**Sathwik K**
- GitHub: [Sathwik464](https://github.com/Sathwik464)
- LinkedIn: [linkedin.com/in/sathwik46](https://www.linkedin.com/in/sathwik46)
- Blog: https://sathwikk.hashnode.dev/
