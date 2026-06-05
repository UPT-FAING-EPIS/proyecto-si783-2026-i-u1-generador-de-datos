# 🗃️ Plan de Mariela — Generador de Datos (CDCart Sidecar)

**Proyecto:** `proyecto-si783-2026-i-u1-generador-de-datos/DATA-GENERATOR`
**Objetivo:** Refactorizar la API para que funcione como un servicio local sin autenticación, con SQLite como BD interna, y preparar un `APIRouter` limpio que se integrará en el backend unificado de CDCart.

---

## 📋 Resumen de Cambios

Tu proyecto actualmente está diseñado como un SaaS web multi-usuario. Necesitas convertirlo en un servicio local de un solo usuario. Esto implica:

1. Eliminar todo lo relacionado con autenticación y usuarios
2. Cambiar la base de datos interna de MySQL a SQLite
3. Limpiar los endpoints para que no dependan de `get_current_user`
4. Preparar tu código para que André pueda acoplar su API

---

## ✅ Tareas Detalladas

### FASE 1: Limpieza de Autenticación (Eliminar código muerto)

#### 1.1 Eliminar archivos completos
- [ ] Eliminar `backend/auth/dependencies.py` (middleware JWT `get_current_user`)
- [ ] Eliminar `backend/auth/jwt_handler.py` (creación/validación de tokens)
- [ ] Eliminar `backend/auth/password.py` (hash de contraseñas)
- [ ] Eliminar `backend/api/auth_router.py` (registro, login, OAuth)
- [ ] Eliminar `backend/api/admin_router.py` (panel de administración)
- [ ] Eliminar `backend/api/comments_router.py` (comentarios de usuarios)
- [ ] Crear archivo `backend/auth/__init__.py` vacío o eliminar la carpeta `auth/` completa

#### 1.2 Limpiar `main.py`
El `main.py` ya tiene los imports removidos del paso anterior. Verificar que quede así:
```python
from backend.api import (
    connector_router,
    parser_router,
    generator_router
)
# y en el router:
api_router.include_router(connector_router.router)
api_router.include_router(parser_router.router)
api_router.include_router(generator_router.router)
```

#### 1.3 Limpiar `backend/api/__init__.py`
- [ ] Abrir `backend/api/__init__.py` y quitar los imports de `auth_router`, `admin_router` y `comments_router`.

---

### FASE 2: Eliminar `get_current_user` de los Endpoints

Cada endpoint actualmente requiere un usuario autenticado. Debes eliminar esa dependencia.

#### 2.1 Modificar `connector_router.py`
En **cada función** de este archivo, eliminar el parámetro `current_user`:

**ANTES** (ejemplo `test_connection` en línea 33):
```python
def test_connection(
    req: ConexionRequest,
    current_user: UsuarioResponse = Depends(get_current_user)
):
```

**DESPUÉS:**
```python
def test_connection(req: ConexionRequest):
```

Hacer esto en TODAS las funciones:
- [ ] `test_connection` (línea 33)
- [ ] `get_external_schema` (línea 52) — También quitar `current_user.id` de la lógica de guardar conexión (ver Fase 3)
- [ ] `list_saved_connections` (línea 106)
- [ ] `delete_saved_connection` (línea 146)
- [ ] `insert_generated_data` (línea 169)

Eliminar el import de la línea 10:
```python
# ELIMINAR esta línea:
from backend.auth.dependencies import get_current_user
```

#### 2.2 Modificar `generator_router.py`
- [ ] Eliminar `current_user: UsuarioResponse = Depends(get_current_user)` de `generate_preview` (línea 24)
- [ ] Eliminar `current_user: UsuarioResponse = Depends(get_current_user)` de `export_data` (línea 55)
- [ ] Eliminar el import `from backend.auth.dependencies import get_current_user` (línea 10)
- [ ] Eliminar el import de `UsuarioResponse` del bloque de imports de schemas (línea 16)

#### 2.3 Modificar `parser_router.py`
- [ ] Eliminar `current_user: UsuarioResponse = Depends(get_current_user)` de `analyze_sql_script` (línea 19)
- [ ] Eliminar `from backend.auth.dependencies import get_current_user` (línea 8)
- [ ] Eliminar `UsuarioResponse` del import de schemas (línea 12)

---

### FASE 3: Migrar la Base de Datos Interna a SQLite

#### 3.1 Modificar `backend/core/config.py`
Reemplazar toda la configuración de MySQL y JWT por algo simple:

```python
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # ── Base de datos interna (SQLite) ───────────────────────
    DATABASE_PATH: str = "./cdcart_data.db"

    # ── Frontend / CORS ────────────────────────────────────────
    ALLOWED_ORIGINS: str = "http://localhost:1420,http://localhost:3000,tauri://localhost"

    # ── Faker ──────────────────────────────────────────────────
    FAKER_LOCALE: str = "es_ES"

    # ── Archivos temporales ────────────────────────────────────
    TEMP_DIR: str = "./tmp_exports"

    @property
    def DATABASE_URL(self) -> str:
        return f"sqlite:///{self.DATABASE_PATH}"

    @property
    def CORS_ORIGINS(self) -> List[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
os.makedirs(settings.TEMP_DIR, exist_ok=True)
```

- [ ] Implementar los cambios anteriores en `config.py`
- [ ] Eliminar las secciones JWT, OAuth, Superadmin del config

#### 3.2 Modificar `backend/core/database.py`
Cambiar el engine de MySQL a SQLite:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # Necesario para SQLite
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- [ ] Implementar los cambios anteriores en `database.py`

#### 3.3 Simplificar `backend/models/models.py`
Eliminar los modelos `Usuario`, `Sesion`, `Log`, `Comentario`. Solo conservar `Conexion` pero **sin referencia a `usuario_id`**:

```python
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from backend.core.database import Base

class Conexion(Base):
    __tablename__ = "conexiones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_alias = Column(String(100), nullable=True)
    motor_bd = Column(String(50), nullable=False)
    host = Column(String(255), nullable=False)
    puerto = Column(Integer, nullable=False)
    nombre_bd = Column(String(255), nullable=False)
    usuario_db = Column(String(255), nullable=True)
    password_db = Column(Text, nullable=True)  # Cifrado con Fernet
    registros_generados = Column(Integer, nullable=False, default=0)
    registros_insertados = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now())
```

- [ ] Implementar el modelo simplificado
- [ ] Eliminar imports de `enum`, `ForeignKey`, `relationship`, `Boolean`

#### 3.4 Limpiar `backend/models/schemas.py`
Eliminar todos los schemas innecesarios. Conservar SOLO:
- [ ] `MotorBDEnum` (línea 26)
- [ ] `ConexionRequest` (línea 139)
- [ ] `ConexionResponse` (línea 148)
- [ ] `ConexionGuardadaResponse` (línea 162)
- [ ] `ColumnSchema`, `TableSchema`, `DatabaseSchema` (líneas 181-202)
- [ ] `TableGenerationConfig`, `GenerateRequest`, `GeneratePreviewRequest` (líneas 208-224)
- [ ] `GeneratedDataResponse` (línea 227)
- [ ] `ExportRequest`, `ExportResponse` (líneas 234-246)
- [ ] `InsertRequest`, `InsertResponse` (líneas 252-264)
- [ ] `ParseSQLRequest`, `ParseSQLResponse` (líneas 270-278)

**Eliminar completamente:**
- [ ] `RolEnum`, `MetodoLoginEnum` (líneas 14-24)
- [ ] `RegisterRequest`, `LoginRequest`, `OAuthCallbackRequest`, `TokenResponse` (líneas 38-73)
- [ ] `UsuarioResponse`, `UsuarioAdminResponse`, `BlockUserRequest` (líneas 78-101)
- [ ] `SesionResponse` (líneas 106-117)
- [ ] `LogResponse` (líneas 122-134)
- [ ] `ComentarioCreate`, `ComentarioUpdate`, `ComentarioResponse`, `PaginatedComentarios` (líneas 284-315)
- [ ] `LoginStatPoint`, `EngineStatPoint`, `AdminStatsResponse` (líneas 320-336)
- [ ] `PaginatedResponse` (línea 338)
- [ ] `TokenResponse.model_rebuild()` (línea 347)
- [ ] Quitar import de `EmailStr` (línea 5)

---

### FASE 4: Actualizar la Lógica de Negocio (connector_router.py)

#### 4.1 Quitar `usuario_id` de las consultas de conexiones
En `connector_router.py`, la función `get_external_schema` (línea 66) filtra por `Conexion.usuario_id == current_user.id`. Como ya no hay usuarios:

**ANTES:**
```python
existing = db.query(Conexion).filter(
    Conexion.usuario_id == current_user.id,
    Conexion.host == req.host,
    ...
).first()
```

**DESPUÉS:**
```python
existing = db.query(Conexion).filter(
    Conexion.host == req.host,
    Conexion.puerto == req.puerto,
    Conexion.nombre_bd == req.nombre_bd,
    Conexion.usuario_db == req.usuario,
).first()
```

- [ ] Actualizar `get_external_schema` — quitar `usuario_id` del filtro y del `Conexion()` nuevo (líneas 66-93)
- [ ] Actualizar `list_saved_connections` — quitar filtro por `usuario_id` (línea 112)
- [ ] Actualizar `delete_saved_connection` — quitar filtro por `usuario_id` (líneas 152-155)
- [ ] Actualizar `insert_generated_data` — quitar `usuario_id` del filtro de estadísticas (líneas 229-234)

---

### FASE 5: Limpiar Dependencias

#### 5.1 Actualizar `requirements.txt`
- [ ] Eliminar `python-jose[cryptography]` (JWT)
- [ ] Eliminar `passlib[bcrypt]` (hash contraseñas)
- [ ] Eliminar `python-multipart` (form uploads de auth)
- [ ] Eliminar `httpx` (OAuth callbacks)
- [ ] Eliminar `pymysql` (ya no se usa MySQL como BD interna)
- [ ] Agregar `aiosqlite` o verificar que SQLAlchemy funciona bien con SQLite sin dependencia extra
- [ ] Mantener: `fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2-binary`, `pymongo`, `cassandra-driver`, `neo4j`, `faker`, `sqlparse`, `pydantic`, `pydantic-settings`, `cryptography` (para Fernet de contraseñas cifradas), `pyodbc`

#### 5.2 Eliminar archivos de infraestructura web
- [ ] Eliminar `backend/core/init_db.py` (creaba el superadmin)
- [ ] Evaluar si `backend/core/logger.py` y `backend/core/encryption.py` siguen siendo necesarios (encryption sí, para contraseñas de conexiones guardadas)

---

### FASE 6: Preparación del Sidecar

#### 6.1 Actualizar `main.py` para usar un puerto fijo
- [ ] Agregar al final del `main.py`:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

#### 6.2 Preparar script de compilación con PyInstaller
- [ ] Crear archivo `build_sidecar.py` o agregar un comando al Makefile:
```bash
pyinstaller --onefile --name cdcart-backend main.py
```
- [ ] Probar que `dist/cdcart-backend.exe` arranca y responde en `http://localhost:8000/docs`

---

## 🔗 Cómo se Conecta tu Trabajo con el Frontend (Jeff)

Una vez que hayas terminado las fases 1-5, Jeff podrá hacer lo siguiente desde el frontend:

```typescript
// Ejemplo: Probar conexión a BD del usuario
const response = await fetch("http://localhost:8000/api/v1/connect/test", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
        host: "localhost",
        puerto: 5432,
        usuario: "postgres",
        password: "mi_password",
        nombre_bd: "mi_base_de_datos",
        motor: "postgresql"
    })
});
const result = await response.json();
// result = { success: true, motor: "PostgreSQLConnector", database: "mi_base_de_datos", tables_count: 12 }
```

```typescript
// Ejemplo: Generar datos y exportar a SQL
const exportResponse = await fetch("http://localhost:8000/api/v1/generate/export", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
        schema: { motor: "postgresql", database_name: "test", tables: [...] },
        table_configs: [{ table_name: "usuarios", record_count: 100, selected: true }],
        format: "sql",
        locale: "es_ES"
    })
});
// Luego descargar el archivo:
// GET http://localhost:8000/api/v1/generate/download/{file_id}.sql
```

## 🔗 Cómo se Conecta tu Trabajo con André

Cuando André termine su `APIRouter`, tú lo integrarás en el `main.py`:

```python
# main.py — Versión final unificada
from backend.api import connector_router, parser_router, generator_router
from query_analyzer.api import analyzer_router  # <-- André entrega esto

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(connector_router.router)
api_router.include_router(parser_router.router)
api_router.include_router(generator_router.router)
api_router.include_router(analyzer_router.router)  # <-- Se agrega aquí
```

---

## 📁 Estructura Final Esperada

```
DATA-GENERATOR/
├── main.py                        # Punto de entrada unificado
├── backend/
│   ├── api/
│   │   ├── connector_router.py    # (limpio, sin auth)
│   │   ├── generator_router.py    # (limpio, sin auth)
│   │   └── parser_router.py       # (limpio, sin auth)
│   ├── connectors/
│   │   ├── base.py                # (sin cambios)
│   │   ├── connector_factory.py   # (sin cambios)
│   │   ├── postgres_connector.py  # (sin cambios)
│   │   ├── mysql_connector.py     # (sin cambios)
│   │   ├── mongodb_connector.py   # (sin cambios)
│   │   ├── sqlserver_connector.py # (sin cambios)
│   │   ├── cassandra_connector.py # (sin cambios)
│   │   └── neo4j_connector.py     # (sin cambios)
│   ├── core/
│   │   ├── config.py              # (simplificado: SQLite + CORS local)
│   │   ├── database.py            # (SQLite engine)
│   │   └── encryption.py          # (sin cambios, se usa para conexiones)
│   ├── generators/
│   │   ├── data_generator.py      # (sin cambios)
│   │   ├── exporters.py           # (sin cambios)
│   │   └── faker_mappings.py      # (sin cambios)
│   ├── models/
│   │   ├── models.py              # (solo Conexion, sin Usuario/Sesion/Log)
│   │   └── schemas.py             # (limpio, ~150 líneas en vez de 348)
│   ├── parsers/
│   │   └── sql_parser.py          # (sin cambios)
│   └── analyzers/
│       └── schema_analyzer.py     # (sin cambios)
├── requirements.txt               # (limpio, sin JWT/OAuth)
└── build_sidecar.py               # (NUEVO: script PyInstaller)
```

### Archivos/Carpetas ELIMINADOS:
```
❌ backend/auth/                    # Carpeta completa
❌ backend/api/auth_router.py
❌ backend/api/admin_router.py
❌ backend/api/comments_router.py
❌ backend/core/init_db.py
❌ frontend/                        # Ya no se usa (Jeff lo maneja)
❌ ecosystem.config.js
❌ nginx.conf
❌ start.sh
❌ docker-compose.yml               # (del root del proyecto)
```
