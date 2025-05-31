from dotenv import load_dotenv
import os
from openai import OpenAI
import asyncio
load_dotenv()
client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_URL")
    )

class AiService:
    @staticmethod
    async def ask_for_tips(user_message):
        message = [
            {"role": "system", "content": """
                    You are a highly trained culinary expert with professional kitchen experience. Your role is to help a home cook solve specific cooking problems with clear, precise, and technically accurate advice. Keep it short and simple. Speak with authority, avoid casual language or personal stories, and focus only on practical, reliable solutions suitable for a home kitchen. Do not use emojis or unnecessary flourishes.
                    """},
            {"role": "user", "content": user_message}
        ]

        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, lambda: client.chat.completions.create(
            model="deepseek-chat",
            messages=message,
        ))
        return response.choices[0].message.content
