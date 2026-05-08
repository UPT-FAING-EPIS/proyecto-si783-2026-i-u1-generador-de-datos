from pydantic import BaseModel, field_validator
from typing import Optional, List, Any, Dict
from datetime import datetime
from uuid import UUID
from enum import Enum

class DBEngine(str, Enum):
    mysql = "mysql"
    postgresql = "postgresql"
    sqlserver = "sqlserver"
    oracle = "oracle"
    mongodb = "mongodb"
    cassandra = "cassandra"
    redis = "redis"
    neo4j = "neo4j"
    elasticsearch = "elasticsearch"

class ConnectionCreate(BaseModel):
    name: str
    engine: DBEngine
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    database_name: Optional[str] = None
    extra_params: Optional[Dict[str, Any]] = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()

class ConnectionOut(BaseModel):
    id: UUID
    name: str
    engine: str
    host: str
    port: int
    username: Optional[str]
    database_name: Optional[str]
    is_active: bool
    last_used_at: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}

class ConnectionTest(BaseModel):
    success: bool
    message: str
    engine_version: Optional[str] = None
    latency_ms: Optional[float] = None

class ColumnInfo(BaseModel):
    name: str
    data_type: str
    is_nullable: bool
    is_primary_key: bool
    is_unique: bool
    is_foreign_key: bool
    references_table: Optional[str] = None
    references_column: Optional[str] = None
    default_value: Optional[str] = None
    max_length: Optional[int] = None

class TableSchema(BaseModel):
    name: str
    row_count: Optional[int] = None
    columns: List[ColumnInfo] = []

class SchemaAnalysis(BaseModel):
    engine: str
    database: str
    tables: List[TableSchema] = []
    relationships: List[Dict[str, str]] = []
    total_tables: int
    analyzed_at: datetime
