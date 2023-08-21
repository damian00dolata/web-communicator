from pydantic import BaseModel, Field
from typing import Optional

class Room(BaseModel):
  id: Optional[int] = Field(None)
  roomId: str
  name: str
  maxUsers: int
  isTemporary: int