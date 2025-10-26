from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from app.models.config import Credentials, AIInstructions
from app.services.files import load_credentials, load_ai_instructions


load_dotenv()


class Config(BaseSettings):
    xai_key: str
    credentials: Credentials = load_credentials()
    ai_instructions: AIInstructions = load_ai_instructions()


config = Config()