from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class EmployeeCreate(BaseModel):
    employeeId: str = Field(..., min_length=1)
    fullName: str = Field(..., min_length=1)
    email: EmailStr
    department: str = Field(..., min_length=1)

class EmployeeRead(EmployeeCreate):
    id: str

class EmployeeUpdate(BaseModel):
    fullName: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
