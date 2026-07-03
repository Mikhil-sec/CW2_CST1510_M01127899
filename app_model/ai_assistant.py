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
Answer the user's question using ONLY this data. If the answer requires counting, filtering, or calculating, do that accurately based on the rows shown. Be concise and specific.
Do not answer questions that are not related to the dataset. If the question is unrelated, respond with "I can only answer questions about the dataset provided."
User question: {question}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


