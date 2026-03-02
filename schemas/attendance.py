from pydantic import BaseModel, Field

class AttendanceCreate(BaseModel):
    employeeId: str
    date: str
    status: str

class AttendanceRead(AttendanceCreate):
    id: str
