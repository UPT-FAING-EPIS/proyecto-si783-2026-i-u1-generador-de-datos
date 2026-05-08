from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Dict, List, Any
from core.database import get_db
from auth.dependencies import get_current_user
from models.user import User
from services.export_service import (
    export_to_json, export_to_csv, export_to_excel,
    export_to_sql, export_to_xml
)

router = APIRouter(prefix="/export", tags=["Exportacion"])

class ExportRequest(BaseModel):
    data: Dict[str, List[Dict[str, Any]]]
    engine: str = "mysql"

@router.post("/json")
async def export_json(request: ExportRequest, current_user: User = Depends(get_current_user)):
    content = export_to_json(request.data)
    return Response(content=content, media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=smartgen_export.json"})

@router.post("/csv")
async def export_csv(request: ExportRequest, current_user: User = Depends(get_current_user)):
    content = export_to_csv(request.data)
    return Response(content=content, media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=smartgen_export.csv"})

@router.post("/excel")
async def export_excel(request: ExportRequest, current_user: User = Depends(get_current_user)):
    content = export_to_excel(request.data)
    return Response(content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=smartgen_export.xlsx"})

@router.post("/sql")
async def export_sql(request: ExportRequest, current_user: User = Depends(get_current_user)):
    content = export_to_sql(request.data, request.engine)
    return Response(content=content, media_type="text/plain",
        headers={"Content-Disposition": "attachment; filename=smartgen_export.sql"})

@router.post("/xml")
async def export_xml(request: ExportRequest, current_user: User = Depends(get_current_user)):
    content = export_to_xml(request.data)
    return Response(content=content, media_type="application/xml",
        headers={"Content-Disposition": "attachment; filename=smartgen_export.xml"})
