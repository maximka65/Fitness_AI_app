from datetime import datetime

from pydantic import BaseModel


class OperationCreate(BaseModel):
    id: int
    Name: str
    Surname: str
    Birthday: str
    Gender: str
    Weight: int
    Height: int
