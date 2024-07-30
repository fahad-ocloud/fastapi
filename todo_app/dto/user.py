from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username:str
    email:Optional[str]
    first_name :str
    last_name:str
    password:str