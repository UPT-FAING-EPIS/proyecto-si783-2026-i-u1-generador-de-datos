[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/O8I-PXKI)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=23223071)

# 🗃️ CDCart Data Generator - Sidecar API

API de backend local ligera y sin autenticación para la conexión, análisis y generación de datos sintéticos en múltiples motores de bases de datos relacionales y NoSQL. Funciona como un servicio independiente (*sidecar*) bajo el proyecto unificado **CDCart**.

---

## 🛠️ Requisitos Previos

Asegúrate de tener instalado:
* **Python 3.10+** (Probado y compatible hasta Python 3.14.5).
* **Pip** (Administrador de paquetes de Python).
* **Git** (Opcional, para control de versiones).

---

## 🚀 Instalación y Configuración

Sigue estos pasos para configurar el entorno de ejecución en tu máquina local:

### 1. Clonar el repositorio y acceder a la carpeta
```bash
git clone https://github.com/UPT-FAING-EPIS/proyecto-si783-2026-i-u1-generador-de-datos.git
cd proyecto-si783-2026-i-u1-generador-de-datos
```

### 2. Crear y activar un entorno virtual
* **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
* **Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar las dependencias del proyecto
```bash
pip install -r DATA-GENERATOR/backend/requirements.txt
```

---

## 💻 Ejecución en Desarrollo

Para iniciar el servidor FastAPI localmente:

1. Ve a la carpeta raíz del código de la API:
   ```bash
   cd DATA-GENERATOR
   ```
2. Ejecuta el archivo principal:
   ```bash
   python main.py
   ```
3. El servidor iniciará en **`http://127.0.0.1:8000`**.
4. Puedes interactuar con los endpoints y probar la API desde la interfaz de documentación interactiva de Swagger:
   * 🔗 **Swagger UI:** `http://127.0.0.1:8000/docs`
   * 🔗 **ReDoc:** `http://127.0.0.1:8000/redoc`

---

## 📦 Compilación para Producción (PyInstaller)

Si necesitas compilar la API como un ejecutable portable independiente (`.exe` en Windows), ejecuta el script de empaquetado automático:

```bash
cd DATA-GENERATOR
python build_sidecar.py
```

El script instalará automáticamente PyInstaller y empaquetará el backend. El archivo resultante estará disponible en la ruta:
📁 `DATA-GENERATOR/dist/cdcart-backend.exe`

---

## 🔗 Guía de Integración

Este módulo está diseñado para conectarse con los otros dos componentes principales de **CDCart**:

### 1. Integración con el Frontend (Jeff)
El frontend debe realizar llamadas REST a la dirección local del sidecar (`http://localhost:8000/api/v1/`). Los endpoints clave disponibles son:
* **Prueba de Conexión:** `POST /api/v1/connect/test`
* **Extraer Esquema:** `POST /api/v1/connect/schema`
* **Generar Vista Previa:** `POST /api/v1/generate/preview`
* **Exportar Datos Sintéticos (SQL/CSV/JSON):** `POST /api/v1/generate/export`
* **Inserción Directa en BD Externa:** `POST /api/v1/connect/insert`
* **Parsea Script SQL:** `POST /api/v1/parser/analyze`

### 2. Integración con el Analizador de Consultas (André)
Cuando André finalice el enrutador de su módulo (`analyzer_router`), deberá integrarse en el archivo `DATA-GENERATOR/main.py` de la siguiente forma:

```python
# DATA-GENERATOR/main.py — Integración
from backend.api import connector_router, parser_router, generator_router
from query_analyzer.api import analyzer_router  # <-- Importar módulo de André

# Registrar en el API Router
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(connector_router.router)
api_router.include_router(parser_router.router)
api_router.include_router(generator_router.router)
api_router.include_router(analyzer_router.router)  # <-- Añadir router de André
```