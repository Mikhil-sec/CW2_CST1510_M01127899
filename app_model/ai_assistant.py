import os
import pandas as pd
from google import genai
from dotenv import load_dotenv
#Comments?
load_dotenv() #no parameter means it will look for .env file
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY")) #searched and ref documentation

def ask_ai_about_data(question, df: pd.DataFrame, dataset_name): #type hint used so editor knows a dataframe is passed to df
    data_as_text = df.to_csv(index=False)  # Convert DataFrame to CSV string without index
    #Prompt:
    prompt= f"""You are a data analyst assistant helping a user explore a dataset called '{dataset_name}'.
    Here is the full dataset in CSV format:
    {data_as_text}
    Your role:
    1. Answer questions accurately based on the data provided
    2. For cybersecurity incidents (Malware, Phishing, DDoS, Ransomware, etc.), supplement your answer with real-world context — common attack vectors, impact, and recommended mitigation measures
    3. If a user asks about a specific incident or category, always include practical security recommendations even if the dataset has no description
    4. Be concise but actionable — respond like a SOC analyst briefing a colleague

    Answer the user's question using ONLY this data. If the answer requires counting, filtering, or calculating, do that accurately based on the rows shown. Be concise and specific.
    Do not answer questions that are not related to the dataset. If the question is unrelated, respond with "I can only answer questions about the dataset provided."
    User question: {question}
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text
def suggest_strong_passwords(weak_password):
    #Asks Gemini to suggest stronger password alternatives
    prompt = f"""A user has entered this weak password: '{weak_password}'

Suggest 3 stronger versions or variations of this password that are:

1. At least 8 characters long
2. Made of REAL English words or based on the original password's theme/words (passphrase style) — for example: "BlueSky$Dance99!" or "Tiger!Runs@Fast7"
3. Include at least one uppercase letter, one number, and one special character naturally within the words
4. Easy to read, say, and remember — NO leetspeak (no @ instead of a, no 3 instead of e, no ! instead of i)

Format your response exactly like this for each suggestion:
Password: [the password]
Why it works: [one sentence explanation]

Do not include any other text."""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Password suggestion error: {e}")
        return "Unable to generate suggestions right now. Try adding uppercase letters, numbers and special characters to your password."
    
#Cross analysis of datasets
def cross_dataset_analysis(analysis_type, df_incidents, df_tickets, df_metadata):
    """
    Sends all three datasets to Gemini for cross-domain analysis.
    analysis_type determines the specific prompt used.
    """
    incidents_csv = df_incidents.to_csv(index=False)
    tickets_csv = df_tickets.to_csv(index=False)
    metadata_csv = df_metadata.to_csv(index=False)

    base_context = f"""You are a senior cybersecurity analyst with access to three operational datasets:

DATASET 1 — CYBER INCIDENTS:
{incidents_csv}

DATASET 2 — IT TICKETS:
{tickets_csv}

DATASET 3 — DATASET METADATA REGISTRY:
{metadata_csv}

"""

    prompts = {
        "high_risk": base_context + """Identify high-risk time periods by cross-referencing the cyber incident timestamps with IT ticket creation dates.
Find periods where both datasets show elevated activity simultaneously.
Format your response as:
- A brief summary of the highest-risk periods identified
- The specific dates or ranges with both high incident and ticket activity
- What this pattern suggests about the organisation's security posture
- One concrete recommendation based on the timing patterns
Be specific and reference actual dates from the data.""",

        "correlate": base_context + """Analyse correlations between cyber incident categories and IT ticket priorities.
Specifically look for:
- Whether certain incident categories (Malware, Phishing, DDoS etc.) tend to coincide with high-priority tickets
- Whether incident severity levels map to ticket priority levels
- Any patterns suggesting incidents are generating tickets or vice versa
Format as a structured analysis with specific findings and supporting evidence from both datasets.""",

        "anomaly": base_context + """Perform anomaly detection across all three datasets.
Look for:
- Unusual spikes or drops in incident frequency
- Tickets with abnormally high or low resolution times compared to their priority
- Any data points that appear inconsistent with the overall patterns
- Anything that would warrant immediate attention from a security team
Format as a prioritised list of anomalies, most concerning first, with a brief explanation of why each is unusual.""",

        "briefing": base_context + """Generate a concise executive threat briefing suitable for a C-suite audience.
Structure it exactly as follows:

EXECUTIVE THREAT BRIEFING
Date: [use the most recent date visible in the data]

OVERALL SECURITY POSTURE: [one sentence — Good/Concerning/Critical and why]

KEY FINDINGS:
- [Finding 1 — cross-domain insight]
- [Finding 2 — cross-domain insight]  
- [Finding 3 — cross-domain insight]

IMMEDIATE PRIORITIES:
1. [Action 1]
2. [Action 2]
3. [Action 3]

RISK OUTLOOK: [2-3 sentences on projected risk based on current trends]

Keep it under 300 words. Be specific — reference actual numbers from the data."""
    }

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompts[analysis_type]
        )
        return response.text
    except Exception as e:
        print(f"Cross-dataset analysis error: {e}")
        return "Analysis unavailable. Please try again."


