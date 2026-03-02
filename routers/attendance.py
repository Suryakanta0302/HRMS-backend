from fastapi import APIRouter, HTTPException, status, Depends
from schemas.attendance import AttendanceCreate, AttendanceRead
from services.attendance_service import AttendanceService
from dependencies import get_attendance_service

router = APIRouter()

@router.post("/", response_model=AttendanceRead, status_code=status.HTTP_201_CREATED)
async def mark_attendance(att: AttendanceCreate, service: AttendanceService = Depends(get_attendance_service)):
    result = await service.mark(att)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data or employee not found")
    return result

@router.get("/{employeeId}", response_model=list[AttendanceRead])
async def get_attendance(employeeId: str, service: AttendanceService = Depends(get_attendance_service)):
    return await service.list_by_employee(employeeId)
