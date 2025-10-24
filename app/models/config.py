from pydantic import BaseModel

class Credentials(BaseModel):
    username: str
    password: str
    two_factor: str | None = None
    session: dict | None = None


class AIInstructions(BaseModel):
    basic_instruction: str
    stop_responding_instruction: str