from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Union, Literal
from instagrapi.types import MessageReactions


class Conversation(BaseModel):
    model_config = ConfigDict(extra='ignore')
    sender: Union[Literal["AI", "user"], bool] = Field(..., alias="is_sent_by_viewer")
    message: str = Field(..., alias="text")
    user_reacted: Union[MessageReactions, None, bool] = Field(..., alias="reactions")

    @field_validator("sender")
    @classmethod
    def set_sender(cls, v: bool) -> Literal["AI", "user"]:
        if v:
            return "AI"
        return "user"

    @field_validator("user_reacted")
    @classmethod
    def is_reaction(cls, v: Union[MessageReactions, None, bool]) -> bool:
        if v is isinstance(v, MessageReactions):
            return True
        return False
