from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Message(BaseModel):
  id: Optional[int] = Field(None)
  clientName: str
  message: str
  roomId: str
  date: Optional[datetime] = Field(None)