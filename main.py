import sys, os

# ensure workspace root is on sys.path so that imports of the `backend` package
# succeed regardless of current working directory.  This covers both the normal
# case (running from root) and the case where someone executes inside backend.
workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# imports using absolute module paths; ensures they resolve even when
# __package__ isn't set correctly in a subprocess
from backend.services.employee_service import EmployeeService
from backend.services.attendance_service import AttendanceService
from backend.routers import employees as employees_router
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import attendance as attendance_router
from backend.routers import summary as summary_router

load_dotenv()

app = FastAPI(title="HRMS Lite API")

# allow cross-origin requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/hrms")
client = AsyncIOMotorClient(MONGO_URI)
db = client.hrms


# include routers
app.include_router(employees_router.router, prefix="/api/employees", tags=["employees"])
app.include_router(attendance_router.router, prefix="/api/attendance", tags=["attendance"])
app.include_router(summary_router.router, prefix="/api/summary", tags=["summary"])

# migration / startup event to ensure indexes and collections
@app.on_event("startup")
async def startup_event():
    # create unique index on employeeId
    await db.employees.create_index("employeeId", unique=True)
    # create index on attendance date for faster querying
    await db.attendance.create_index("date")
    # touch collections so they exist even if empty
    await db.employees.insert_one({"_init": True})
    await db.employees.delete_one({"_init": True})
    await db.attendance.insert_one({"_init": True})
    await db.attendance.delete_one({"_init": True})

@app.get("/", tags=["root"])
async def root():
    return {"message": "HRMS backend running"}
