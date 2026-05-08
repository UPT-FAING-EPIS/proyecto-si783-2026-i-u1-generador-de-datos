from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.database import create_tables
from api.auth_router import router as auth_router
from api.admin_router import router as admin_router
from api.connection_router import router as connection_router
from api.generation_router import router as generation_router
from api.export_router import router as export_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    from models.connection import DBConnection
    from core.database import engine, Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas correctamente")
    yield

app = FastAPI(
    title="SmartGen API",
    description="Sistema Inteligente Generador de Datos para SQL y NoSQL",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(connection_router)
app.include_router(generation_router)
app.include_router(export_router)

@app.get("/", tags=["Sistema"])
async def root():
    return {"message": "SmartGen API activa", "version": "1.0.0"}

@app.get("/health", tags=["Sistema"])
async def health():
    return {"status": "healthy"}
