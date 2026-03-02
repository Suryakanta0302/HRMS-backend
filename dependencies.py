from .services.employee_service import EmployeeService
from .services.attendance_service import AttendanceService
from .services.summary_service import SummaryService

# functions import db lazily to avoid circular imports

def get_db():
    from .main import db
    return db


def get_employee_service():
    return EmployeeService(get_db())


def get_attendance_service():
    return AttendanceService(get_db())


def get_summary_service():
    return SummaryService(get_db())
