from xai_sdk import Client
from xai_sdk.chat import system, user, assistant
from typing import List

from app.models.ai import AIRespond
from app.models.instagram import Conversation
from app.core.config import config

cl = Client(api_key=config.xai_key)

full_instruction = f"""
1.{config.ai_instructions.basic_instruction}\n
2.{config.ai_instructions.stop_responding_instruction}\n
"""

def ai_respond(thread: List[Conversation]) -> AIRespond:
    chat = cl.chat.create(model="grok-4-fast-reasoning")
    chat.append(system(full_instruction))
    for message in thread:
        if message.sender == "user":
            chat.append(user(message.message))
        elif message.sender == "ai":
            chat.append(assistant(message.message))

    full_response, model = chat.parse(AIRespond)
    assert isinstance(model, AIRespond)
    return model



