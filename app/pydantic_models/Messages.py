from pydantic import BaseModel
from typing import Optional

class CreateMessage(BaseModel):
    chat_id: str
    user_id: str
    message: Optional[str]

class UpdateMessage(BaseModel):
    chat_id: str
    user_id: str
    message: str