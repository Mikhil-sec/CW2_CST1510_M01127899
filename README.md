# 🛡️ Cortex — Multi-Domain Intelligence Platform
> CST1510 Coursework 2 | BSc Cyber Security and Digital Forensics

A secure, AI-powered web application built with Python and Streamlit for monitoring cybersecurity incidents, IT operations, and dataset analytics.

---

## Features

- 🔐 Secure authentication with bcrypt password hashing
- 📊 Interactive dashboards for three operational domains
- 🧠 Gemini AI assistant embedded per dataset
- 🔍 Cross-domain intelligence analysis across all datasets simultaneously
- 👤 Role-based access control with admin panel
- 📈 Plotly visualisations with SOC-themed design
- ⬇️ CSV export with live filtering

---

## Setup

### 1. Clone the repository
```bash
git clone <https://github.com/Mikhil-sec/CW2_CST1510_M01127899>
cd CW2_CST1510_M01127899
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in your values:
```
GEMINI_API_KEY=your_gemini_api_key_here
ADMIN_CODE=your_chosen_admin_passphrase
```

**Getting a free Gemini API key:**
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with a Google account
3. Click **Get API key** → **Create API key**
4. Paste it into your `.env` file

> Without a valid key the app runs normally — only the AI features will be unavailable.

### 5. Run the app
```bash
streamlit run main.py
```

The app opens automatically at `http://localhost:8501`

---

## Admin Access

To register an admin account, open the **"Have an admin code?"** expander on the registration page and enter the `ADMIN_CODE` value from your `.env` file. Admin accounts have access to the Admin Panel for user management and login activity monitoring.

---

## Project Structure

```
CW2_CST1510_M01127899/
├── main.py                  # Streamlit entry point
├── .env                     # Local secrets (not committed)
├── .env.example             # Environment template
├── requirements.txt
├── DATA/
│   ├── cyber_incidents.csv
│   ├── datasets_metadata.csv
│   └── it_tickets.csv
└── app_model/
    ├── db.py                # Database connection
    ├── schema.py            # Table definitions & CRUD
    ├── users.py             # Authentication & password logic
    ├── cyber_incidents.py   # Incident queries & migration + dashboard
    ├── it_tickets.py        # Ticket queries & migration + dashboard
    ├── metadatas.py         # Metadata queries & migration + dashboard
    └── ai_assistant.py      # Gemini AI integration
```

*Student ID: M01127899*
