import os
# Deployment Version: 2026.03.31.2335
from groq import Groq
import streamlit as st
from dotenv import load_dotenv

# ------------------ LOAD ENV ------------------
load_dotenv()

# ------------------ LOAD API KEY ------------------
# ------------------ LOAD API KEY ------------------
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

# Remove module-level raise to prevent app-wide crash
# ------------------ INIT CLIENT ------------------
client = None
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)

# ------------------ MAIN FUNCTION ------------------
def call_llm(user_prompt: str, system_prompt: str, response_format: dict = None) -> str:
    """
    Generates AI-based guidance using Groq LLM with flexiblity for system prompt and format.
    """

    if not GROQ_API_KEY or not client:
        return "Error: GROQ API key not found. Please add it to Streamlit secrets or your .env file."

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
