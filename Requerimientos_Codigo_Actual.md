# Especificación de Requerimientos del Código Actual
*Basado en el análisis estático del código base (Frontend en Next.js y Backend en FastAPI)*

A diferencia de la documentación original (FD01-FD05) que proponía un stack en `.NET 8` y `Angular 17+` limitando la inserción directa de datos, **el código actual implementado** utiliza Python (FastAPI) y React (Next.js) e incluye características avanzadas que no estaban planificadas originalmente. A continuación se detallan los requerimientos funcionales y no funcionales reales del sistema.

---

## 1. Requerimientos Funcionales (RF)

| ID | Requerimiento | Descripción de la Funcionalidad Implementada |
|:---|:---|:---|
| **RF-01** | **Gestión de Autenticación** | El sistema permite el registro e inicio de sesión de usuarios mediante JWT en el backend (`auth_router`) y `next-auth` en el frontend. |
| **RF-02** | **Conexión Multi-Motor** | El sistema se conecta dinámicamente a **MySQL, PostgreSQL, MongoDB, Cassandra, Neo4j y SQL Server** mediante la capa de `connectors`. |
| **RF-03** | **Análisis de Esquema Externo** | A través del endpoint `/connect/schema`, el sistema se conecta a la BD del cliente y extrae de manera automática la estructura de las tablas, columnas, tipos de datos y llaves primarias. |
| **RF-04** | **Gestión de Conexiones** | El usuario puede guardar conexiones exitosas, listarlas (`/connect/saved`) y eliminarlas. Las contraseñas de estas conexiones se guardan encriptadas en la base de datos interna. |
| **RF-05** | **Generación de Vista Previa (Preview)** | Permite generar una muestra reducida de datos sintéticos (usando la librería `Faker`) según la configuración seleccionada en la UI, devolviendo un JSON con los resultados en vivo (`/generate/preview`). |
| **RF-06** | **Exportación de Datos** | El sistema exporta la data masiva generada a archivos en formato **SQL, JSON o CSV** (`/generate/export`). Si son múltiples tablas en CSV, comprime la salida en un archivo ZIP. |
| **RF-07** | **Descarga de Archivos** | Proporciona un endpoint público (`/generate/download/{filename}`) para descargar los archivos temporales de exportación autogenerados. |
| **RF-08** | **Inserción Directa en BD (NUEVO)** | A diferencia del diseño original, el código SÍ permite insertar los datos sintéticos generados **directamente a la base de datos externa conectada** (`/connect/insert`), calculando automáticamente los offsets (MAX) de las llaves primarias. |
| **RF-09** | **Módulo de Comentarios / Administración** | El backend expone rutas para gestión administrativa (`admin_router`) y retroalimentación o comentarios (`comments_router`). |

---

## 2. Requerimientos No Funcionales (RNF)

| ID | Categoría | Descripción Técnica Implementada |
|:---|:---|:---|
| **RNF-01** | **Stack Tecnológico** | El backend está desarrollado en **Python 3** usando **FastAPI** y `uvicorn`. El frontend está construido con **Next.js 16**, **React 19** y componentes de `Radix UI` con **TailwindCSS**. |
| **RNF-02** | **Seguridad en Credenciales** | Las contraseñas de las bases de datos externas de los usuarios son encriptadas y desencriptadas en tiempo de ejecución utilizando la librería `cryptography`, garantizando que no se guarden en texto plano. |
| **RNF-03** | **Seguridad de API** | El backend está protegido mediante el middleware `CORSMiddleware` (configurando los orígenes permitidos) y las rutas de negocio exigen un token de autenticación válido (`Depends(get_current_user)`). |
| **RNF-04** | **Rendimiento y Concurrencia** | FastAPI provee soporte nativo para ejecución asíncrona, y la aplicación exporta archivos temporalmente de manera no bloqueante utilizando `aiofiles`. |
| **RNF-05** | **Modularidad y Patrones** | El código Backend aplica claramente el patrón de **Fábrica (Factory Method)** en `get_connector()` para instanciar dinámicamente la clase correspondiente al motor de base de datos solicitado. |
| **RNF-06** | **Persistencia Interna** | Utiliza **SQLAlchemy** (ORM) y `pymysql` para conectarse a su propia base de datos interna donde persisten los usuarios, las conexiones guardadas y configuraciones. |
| **RNF-07** | **Manejo de Errores** | Excepciones capturadas y envueltas en respuestas `HTTPException` coherentes (400, 404, 500) devolviendo mensajes claros sobre las fallas de inserción, exportación o análisis. |

---

## 3. Desviaciones con respecto a la Documentación Original (FD)

1. **Cambio de Lenguaje y Framework:** La documentación indicaba el uso de **C# .NET 8** y **Angular 17+**. El código real utiliza **Python (FastAPI)** y **Next.js (React)**.
2. **Feature Adelantado (Inserción Directa):** Los documentos FD02 y FD03 señalaban explícitamente que la inserción de datos a bases de datos reales quedaba fuera del alcance (era para una Versión 2.0). Sin embargo, el código implementa robustamente el endpoint `/connect/insert`.
3. **Módulo de Autenticación Integrado:** Mientras que en la documentación se mencionaba como futura funcionalidad, el sistema actual cuenta con un ecosistema completo de creación de usuarios, cifrado de contraseñas de conexiones y protección de rutas mediante JWT.
