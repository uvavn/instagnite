import json
from json import JSONDecodeError

from instagrapi.exceptions import ValidationError

from app.core.logger import logger
from app.models.config import Credentials, AIInstructions
from app.core.paths import credentials_file, stop_responding_instructions_file, basic_instructions_file


def save_credentials(credentials: Credentials) -> None:
    with credentials_file.open(mode="w") as f:
        f.write(json.dumps(credentials.model_dump(), indent=4))

def load_credentials() -> Credentials:
    try:
        with credentials_file.open(mode="r") as f:
            return Credentials(**json.loads(f.read()))
    except (JSONDecodeError, ValidationError) as e:
        logger.error(f"Credentials data invalid: {e}")
        exit(1)

def load_ai_instructions() -> AIInstructions:
    with stop_responding_instructions_file.open(mode="r") as f:
        stop_responding_instructions = f.read()
    with basic_instructions_file.open(mode="r") as f:
        basic_instructions = f.read()
    return AIInstructions(basic_instruction=basic_instructions,
                          stop_responding_instruction=stop_responding_instructions)