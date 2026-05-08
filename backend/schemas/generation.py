from pydantic import BaseModel
from typing import Optional, Dict, List, Any
from uuid import UUID

class TableGenerationConfig(BaseModel):
    table_name: str
    count: int = 10

class GenerationRequest(BaseModel):
    connection_id: UUID
    tables: List[TableGenerationConfig]
    preview_only: bool = False

class InsertPreviewRequest(BaseModel):
    connection_id: UUID
    confirmed_data: Dict[str, List[Dict[str, Any]]]

class GenerationPreview(BaseModel):
    table_name: str
    count: int
    sample: List[Dict[str, Any]]
    all_data: List[Dict[str, Any]]

class GenerationResult(BaseModel):
    table_name: str
    requested: int
    inserted: int
    errors: List[Dict] = []

class GenerationResponse(BaseModel):
    connection_id: str
    engine: str
    database: str
    results: List[GenerationResult] = []
    previews: List[GenerationPreview] = []
    total_inserted: int = 0
    total_errors: int = 0
    preview_only: bool = False
