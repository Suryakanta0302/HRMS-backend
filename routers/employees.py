from fastapi import APIRouter, HTTPException, status, Depends
from backend.schemas.employee import EmployeeCreate, EmployeeRead
from backend.services.employee_service import EmployeeService
from backend.dependencies import get_employee_service

router = APIRouter()

@router.post("/", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
async def create_employee(emp: EmployeeCreate, service: EmployeeService = Depends(get_employee_service)):
    result = await service.create(emp)
    if not result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Employee with that ID already exists")
    return result

@router.get("/", response_model=list[EmployeeRead])
async def list_employees(service: EmployeeService = Depends(get_employee_service)):
    return await service.list_all()

@router.delete("/{id}")
async def delete_employee(id: str, service: EmployeeService = Depends(get_employee_service)):
    success = await service.delete(id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found or invalid id")
    return {"message": "Deleted"}
