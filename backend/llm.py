import os
from groq import Groq
import streamlit as st

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
def generate_response(user_input: str) -> str:
    """
    Generates AI-based career guidance using Groq LLM
    """

    try:
        prompt = f"""
        You are an expert career advisor.

        Based on the following user input, provide:
        1. Career suggestions
        2. Required skills
        3. Learning roadmap (step-by-step)

        User input:
        {user_input}

        Give a clear and structured answer.
        """

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful AI career advisor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"Error generating response: {str(e)}"
