from pydantic import BaseModel, Field
from typing import Optional

class Todo(BaseModel):
    title: str
    description: Optional[str]
    priorty: int = Field(gt=0,lt=6,description="Must be between 1 - 5")
    complete :bool