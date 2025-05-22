from pydantic import BaseModel


class ChatMessage(BaseModel):
    user_id: str
    message: str
    timestamp: str
