from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class EmployeeModel(BaseModel):
    id: Optional[str]
    employeeId: str = Field(..., min_length=1)
    fullName: str = Field(..., min_length=1)
    email: EmailStr
    department: str = Field(..., min_length=1)

    class Config:
        orm_mode = True
