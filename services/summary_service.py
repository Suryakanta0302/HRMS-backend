from motor.motor_asyncio import AsyncIOMotorDatabase

class SummaryService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def get_overview(self):
        total_employees = await self.db.employees.count_documents({})
        total_attendance = await self.db.attendance.count_documents({})
        total_present = await self.db.attendance.count_documents({"status": "Present"})
        return {
            "totalEmployees": total_employees,
            "totalAttendance": total_attendance,
            "totalPresent": total_present
        }
