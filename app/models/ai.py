from pydantic import BaseModel, Field
from typing import Literal

class AIRespond(BaseModel):
    ai_respond: str
    status: Literal["follow-up", "ignore"] = Field(default="follow-up")

