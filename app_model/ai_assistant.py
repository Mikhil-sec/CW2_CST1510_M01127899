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


