import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def call_llm(user_prompt: str, system_prompt: str = "", response_format: dict = None) -> str:
    try:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})

        kwargs = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "temperature": 0.7,
        }
        if response_format:
            kwargs["response_format"] = response_format

        response = client.chat.completions.create(**kwargs)

        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating response: {str(e)}"