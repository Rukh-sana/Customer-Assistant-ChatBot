from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GroqClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        self.client = Groq(api_key=self.api_key)

    def get_groq_response(self, messages, model="llama-3.2-11b-vision-preview", temperature=0.2, max_tokens=1024):
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=0.3,
            stream=False,
            stop=None
        )

        response = ""
        for chunk in completion.choices:
            response += chunk.message.content

        return response
