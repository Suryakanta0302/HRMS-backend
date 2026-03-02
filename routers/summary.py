from fastapi import APIRouter, Depends
from services.summary_service import SummaryService
from dependencies import get_summary_service

router = APIRouter()

@router.get("/", tags=["summary"])
async def get_summary(service: SummaryService = Depends(get_summary_service)):
    return await service.get_overview()