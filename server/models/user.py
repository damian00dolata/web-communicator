from typing import Optional
from pydantic import BaseModel, Field

class User(BaseModel):
  id: Optional[int] = Field(None)
  username: str
  email: Optional[str] = Field(None)
  password: str