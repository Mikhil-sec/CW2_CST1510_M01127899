# Cortex — CW2 (CST1510)

A modular Streamlit web app with secure authentication, SQLite-backed data storage, and an AI assistant powered by the Gemini API.

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd CW2_CST1510_M01127899
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # Mac/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Setting up your Gemini API key

The AI assistant feature requires a Gemini API key. For security, real API keys are never committed to this repository — you'll need to add your own.

1. Get a **free** Gemini API key from [Google AI Studio](https://aistudio.google.com) (no credit card required):
   - Sign in with a Google account
   - Click **"Get API key"** → **"Create API key"**
   - Copy the key

2. In the project root, create a new file named exactly `.env` (copy `.env.example` as a starting point)

3. Paste your key in like this:
   ```
   GEMINI_API_KEY=your_actual_key_here
   ```

4. Save the file. The app will automatically load it on startup.

> **Note:** Without a valid key, the app will still run — only the AI assistant feature will fail to respond.

## Running the app

```bash
streamlit run main.py
```

The app will open in your browser automatically at `http://localhost:8501`.

## Project structure

```
CW2_CST1510_M01127899/
├── main.py              # Streamlit entry point
├── .env                 # Your local API key (not committed)
├── .env.example          # Template — copy this to create your .env
├── DATA/
│   ├── project_data.db   # SQLite database (auto-generated, not committed)
│   ├── cyber_incidents.csv
│   ├── datasets_metadata.csv
│   └── it_tickets.csv
└── app_model/
    ├── db.py             # Database connection
    ├── schema.py         # Table definitions
    ├── users.py          # Authentication logic
    ├── cyber_incidents.py
    ├── it_tickets.py
    ├── metadatas.py
    └── ai_assistant.py   # Gemini AI integration
```
