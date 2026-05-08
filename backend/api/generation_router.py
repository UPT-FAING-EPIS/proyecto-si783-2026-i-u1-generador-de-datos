from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from auth.dependencies import get_current_user
from models.user import User
from schemas.generation import GenerationRequest, GenerationResponse, InsertPreviewRequest
from services.generation_service import generate_data_service, insert_preview_service

router = APIRouter(prefix="/generate", tags=["Generacion de Datos"])

@router.post("/", response_model=GenerationResponse, summary="Generar datos o vista previa")
async def generate(
    request: GenerationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await generate_data_service(db, current_user.id, request)

@router.post("/insert-preview", response_model=GenerationResponse, summary="Insertar datos confirmados desde preview")
async def insert_preview(
    request: InsertPreviewRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await insert_preview_service(db, current_user.id, request)
