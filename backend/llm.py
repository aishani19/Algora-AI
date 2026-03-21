import os
from groq import Groq
import streamlit as st
from dotenv import load_dotenv

# ------------------ LOAD ENV ------------------
load_dotenv()

# ------------------ LOAD API KEY ------------------
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ API key not found. Add it to Streamlit secrets or .env")

# ------------------ INIT CLIENT ------------------
client = Groq(api_key=GROQ_API_KEY)

# ------------------ MAIN FUNCTION ------------------
def call_llm(user_prompt: str, system_prompt: str, response_format: dict = None) -> str:
    """
    Generates AI-based guidance using Groq LLM with flexiblity for system prompt and format.
    """

    try:
        completion_params = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1024
        }
        
        if response_format:
            completion_params["response_format"] = response_format

        completion = client.chat.completions.create(**completion_params)

        return completion.choices[0].message.content

    except Exception as e:
        return f"Error generating response: {str(e)}"
