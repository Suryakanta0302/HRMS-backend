from pydantic import BaseModel, Field
from typing import Optional

class AttendanceModel(BaseModel):
    id: Optional[str]
    employeeId: str
    date: str
    status: str

    class Config:
        orm_mode = True
