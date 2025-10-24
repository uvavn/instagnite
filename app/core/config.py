from dotenv import load_dotenv
from pydantic import ValidationError
from pydantic_settings import BaseSettings

from app.models.config import Credentials, AIInstructions
from app.services.files import load_credentials, load_ai_instructions
from app.core.logger import logger
from app.db.schema import create_database


load_dotenv()
create_database()

class Config(BaseSettings):
    xai_key: str
    credentials: Credentials = load_credentials()
    ai_instructions: AIInstructions = load_ai_instructions()

try:
    config = Config() # type: ignore
except ValidationError as e:
    logger.error(f"Invalid config: {e}")
    exit(1)