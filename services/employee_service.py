from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from schemas.employee import EmployeeCreate

class EmployeeService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create(self, emp: EmployeeCreate):
        existing = await self.db.employees.find_one({"employeeId": emp.employeeId})
        if existing:
            return None
        doc = emp.dict()
        result = await self.db.employees.insert_one(doc)
        doc["id"] = str(result.inserted_id)
        return doc

    async def list_all(self):
        cursor = self.db.employees.find().sort("fullName", 1)
        employees = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            employees.append(doc)
        return employees

    async def delete(self, id: str):
        try:
            oid = ObjectId(id)
        except Exception:
            return False
        result = await self.db.employees.delete_one({"_id": oid})
        return result.deleted_count > 0

    async def get_by_employeeId(self, employeeId: str):
        return await self.db.employees.find_one({"employeeId": employeeId})

    async def get(self, id: str):
        try:
            oid = ObjectId(id)
        except Exception:
            return None
        return await self.db.employees.find_one({"_id": oid})
