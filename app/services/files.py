import json
from json import JSONDecodeError
from pathlib import Path

from instagrapi.exceptions import ValidationError

from app.core.logger import logger
from app.models.config import Credentials, AIInstructions

CREDENTIALS: Path = Path.cwd() / "credentials.json"

AI_INSTRUCTIONS: Path = Path.cwd() / "ai_instructions"
STOP_RESPONDING_INSTRUCTION = AI_INSTRUCTIONS / "stop_responding.txt"
BASIC_INSTRUCTION = AI_INSTRUCTIONS / "basic.txt"

def save_credentials(credentials: Credentials) -> None:
    with CREDENTIALS.open(mode="w") as f:
        f.write(json.dumps(credentials.model_dump(), indent=4))

def load_credentials() -> Credentials:
    try:
        with CREDENTIALS.open(mode="r") as f:
            return Credentials(**json.loads(f.read()))
    except (JSONDecodeError, ValidationError) as e:
        logger.error(f"Credentials data invalid: {e}")
        exit(1)

def load_ai_instructions() -> AIInstructions:
    with STOP_RESPONDING_INSTRUCTION.open(mode="r") as f:
        stop_responding_instructions = f.read()
    with BASIC_INSTRUCTION.open(mode="r") as f:
        basic_instructions = f.read()
    return AIInstructions(basic_instruction=basic_instructions,
                          stop_responding_instruction=stop_responding_instructions)