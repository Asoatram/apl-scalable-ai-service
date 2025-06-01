import json
import re

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

    @staticmethod
    async def ask_for_recipe(user_ingredients):
        message = [
            {"role": "system", "content": """
            You are a highly trained culinary expert with professional kitchen experience. Your role is to help a home cook solve specific cooking problems with clear, precise, and technically accurate advice. Keep it short and simple. Speak with authority, avoid casual language or personal stories, and focus only on practical, reliable solutions suitable for a home kitchen. Do not use emojis or unnecessary flourishes.
            Return raw JSON, Do not wrap it in a code block or any markdown. Make sure that the result is possible with `json.loads`, the json have the following formats:
            {
                "recipe_name": "Spaghetti Bolognese",
                "description": "A classic Italian pasta dish with a rich meat sauce.",
                "ingredients": [
                    {
                        "ingredient_name": "Spaghetti"
                    },
                    {
                        "ingredient_name": "Ground Beef"
                    },
                    {
                        "ingredient_name": "Tomato Sauce"
                    },
                    {
                        "ingredient_name": "Onion"
                    },
                    {
                        "ingredient_name": "Garlic"
                    }
                ],
                "steps": [
                    {
                        "step_order": 1,
                        "step_description": "Boil spaghetti until al dente."
                    },
                    {
                        "step_order": 2,
                        "step_description": "Sauté onion and garlic."
                    },
                    {
                        "step_order": 3,
                        "step_description": "Add ground beef and cook thoroughly."
                    },
                    {
                        "step_order": 4,
                        "step_description": "Stir in tomato sauce and simmer."
                    },
                    {
                        "step_order": 5,
                        "step_description": "Combine with spaghetti and serve."
                    }
                ]
            }
            """
            },
            {"role": "user", "content": f"I have a {user_ingredients}"}
        ]
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=message,
        )
        result = response.choices[0].message.content
        cleaned = re.sub(r'^```(?:json)?\n|\n```$', '', result.strip())
        print(cleaned)
        result = json.loads(cleaned)
        return result
