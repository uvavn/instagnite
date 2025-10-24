from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Union, Literal
from instagrapi.types import MessageReactions


class NotificationStructure(BaseModel):
    text: str = Field(..., alias="message")
    type: Literal["direct_v2_pending", "direct_v2_text"] = Field(..., alias="pushCategory")
    ids: dict = Field(..., alias="actionParams")

    class Config:
        populate_by_name = True


class MessageStructure(BaseModel):
    text: str
    thread_id: str
    username: str

