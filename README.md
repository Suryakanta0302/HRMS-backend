# HRMS Lite Backend

This directory contains the Python FastAPI backend for the HRMS Lite project.  It exposes RESTful endpoints for managing employees and attendance data, and persists to MongoDB.

## Project Overview

- **Framework**: FastAPI, an asynchronous Python web framework.
- **Database**: MongoDB via the Motor async driver.
- **Architecture**: modular structure with `schemas` (Pydantic models), `services` (business logic), and `routers` (HTTP endpoints). Dependency injection is used to provide services to routes.
- On startup the application ensures required collections exist and creates a unique index on `employeeId` to prevent duplicates.

## Tech Stack

- Python 3.11+ (or 3.10+)
- FastAPI
- Uvicorn server
- Motor (async MongoDB client)
- Pydantic for schema validation
- python-dotenv for environment variables

## Running Locally

1. **Environment setup**
   - Navigate to `backend` folder.
   - Create a virtual environment (e.g. `python -m venv .venv`) and activate it.
   - Copy `.env.example` to `.env` and set `MONGO_URI` to your MongoDB connection string. Defaults to `mongodb://localhost:27017/hrms`.
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

2. **Starting the server**
   - From the *workspace root* (`e:\HRM_Interview`), run one of:
     ```bash
     python -m uvicorn backend.main:app --reload --port 5000
     ```
     or (if uvicorn is on PATH):
     ```bash
     uvicorn backend.main:app --reload --port 5000
     ```
   - Both forms set the Python path correctly; starting from inside `backend` may result in import errors, though `main.py` now includes a path fix to mitigate that.
   

3. **Verify**
   - Visit `http://localhost:5000/` to see a simple health message.
   - API docs available at `http://localhost:5000/docs` (Swagger) and `http://localhost:5000/redoc`.

4. **Endpoints**
   - `POST /api/employees/` – add employee (409 on duplicate ID)
   - `GET /api/employees/` – list all employees
   - `DELETE /api/employees/{id}` – remove employee
   - `POST /api/attendance/` – mark attendance
   - `GET /api/attendance/{employeeId}` – get records
   - `GET /api/summary/` – overall statistics

## Assumptions & Limitations

- Single admin user; no authentication or authorization.
- No pagination, search, or filtering on backend lists; frontend handles any minimal filtering.
- Attendance entries can be duplicated for the same employee/date (no uniqueness enforced).
- Validation performed by Pydantic schemas; email field uses built-in `EmailStr`.
- Designed for development and demonstration; production deployment may require additional configuration (logging, error handling, security).

Feel free to adapt or extend as needed.