from motor.motor_asyncio import AsyncIOMotorDatabase
from schemas.attendance import AttendanceCreate
from datetime import datetime

class AttendanceService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def mark(self, att: AttendanceCreate):
        if att.status not in ["Present", "Absent"]:
            return None
        employee = await self.db.employees.find_one({"employeeId": att.employeeId})
        if not employee:
            return None
        try:
            date_obj = datetime.fromisoformat(att.date)
        except Exception:
            return None
        doc = {"employeeId": att.employeeId, "date": date_obj, "status": att.status}
        result = await self.db.attendance.insert_one(doc)
        doc["id"] = str(result.inserted_id)
        doc["date"] = date_obj.isoformat()
        return doc

    async def list_by_employee(self, employeeId: str):
        cursor = self.db.attendance.find({"employeeId": employeeId}).sort("date", -1)
        records = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            if "date" in doc:
                doc["date"] = doc["date"].isoformat()
            records.append(doc)
        return records
