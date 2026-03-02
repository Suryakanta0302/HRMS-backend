import sys, os

# ensure project root (where this file lives) is on sys.path so that imports of
# the `backend` package succeed regardless of current working directory.  The
# previous implementation walked one level too far up, putting `/workspaces`
# on the path when running from inside the container.  That meant the
# `backend` package directory was not available and resulted in
# `ModuleNotFoundError`.  Adding the directory containing `main.py` itself is
# sufficient for normal usage; it's also a no-op when already on the path.
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# imports using absolute module paths; ensures they resolve even when
# __package__ isn't set correctly in a subprocess.  Since the project root is
# a package, the paths are simply relative to the top-level package rather than
# a nonexistent `backend` package.
from services.employee_service import EmployeeService
from services.attendance_service import AttendanceService
from routers import employees as employees_router
from fastapi.middleware.cors import CORSMiddleware
from routers import attendance as attendance_router
from routers import summary as summary_router

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
    """Ensure indexes/collections exist on startup.

    The environment may not have a MongoDB instance running (e.g. local
    development without `mongod`), which would cause the whole application to
    crash with ``ServerSelectionTimeoutError`` as seen in the startup trace.
    Catching that exception allows the server to start and return a helpful
    message instead.  The frontend or clients will still fail if they attempt to
    use the database, but at least the process will be alive for debugging or
    documentation.
    """
    from pymongo.errors import ServerSelectionTimeoutError

    try:
        # create unique index on employeeId
        await db.employees.create_index("employeeId", unique=True)
        # create index on attendance date for faster querying
        await db.attendance.create_index("date")
        # touch collections so they exist even if empty
        await db.employees.insert_one({"_init": True})
        await db.employees.delete_one({"_init": True})
        await db.attendance.insert_one({"_init": True})
        await db.attendance.delete_one({"_init": True})
    except ServerSelectionTimeoutError as exc:
        # log error and continue startup; clients will experience errors
        import logging
        logging.error(
            "Could not connect to MongoDB at %s: %s",
            MONGO_URI,
            exc,
        )
        logging.error(
            "Make sure MongoDB is running and MONGO_URI is correctly set."
        )

@app.get("/", tags=["root"])
async def root():
    return {"message": "HRMS backend running"}
