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


