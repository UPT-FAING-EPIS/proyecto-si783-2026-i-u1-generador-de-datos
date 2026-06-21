# UNIVERSIDAD PRIVADA DE TACNA
## FACULTAD DE INGENIERIA
### Escuela Profesional de Ingeniería de Sistemas

---

# Proyecto: Sistema Generador de Datos Sintéticos (DataGenerator)
**Curso:** Análisis y Diseño de Sistemas de Información  
**Docente:** Ing. Arquímedes Rodríguez Vásquez  
**Integrantes:**  
- Ramos Loza, Mariela Estefany (2023077478)  
- Calloticona Chambilla, Marymar Danytza (2023076791)  

**Tacna -- Perú**  
**2026**

---

## CONTROL DE VERSIONES
| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
|---------|-----------|--------------|--------------|-------|--------|
| 2.0 | MRL / MCC | ELV | ARV | 05/05/2026 | Expansión comercial profunda y actualización técnica a Python/Next.js |

---

# Documento de Visión (FD02)

## ÍNDICE GENERAL
1. [Introducción](#1-introducción)
2. [Posicionamiento](#2-posicionamiento)
   - Oportunidad de Negocio
   - Definición del Problema
3. [Descripción de los Interesados (Stakeholders) y Usuarios](#3-descripción-de-los-interesados-stakeholders-y-usuarios)
   - Perfiles de los Interesados y Usuarios
   - Entorno de Usuario
   - Matriz de Necesidades
4. [Vista General del Producto](#4-vista-general-del-producto)
   - Perspectiva del Producto
   - Resumen de Capacidades
   - Suposiciones y Dependencias
   - Costos y Licenciamiento
5. [Características del Producto](#5-características-del-producto)
6. [Restricciones](#6-restricciones)
7. [Rangos de Calidad](#7-rangos-de-calidad)
8. [Otros Requerimientos del Producto](#8-otros-requerimientos-del-producto)

---

## 1. Introducción
### 1.1 Propósito
El propósito de este documento es recopilar, analizar y definir las necesidades de alto nivel y las características clave del **Sistema Generador de Datos Sintéticos**. En lugar de enfocarse puramente en lo técnico, este documento actúa como un acuerdo entre los Stakeholders del negocio y el equipo de desarrollo, estipulando *para qué* se usará la plataforma y qué impacto comercial y operativo tendrá.

### 1.2 Alcance
El sistema entregará una plataforma Web (SPA) que permite a los usuarios autenticarse, configurar esquemas conectándose a sus propias bases de datos (SQL y NoSQL) de manera automática, y generar e insertar hasta 50,000 registros sintéticos por lote en la BD de destino. No incluye generación de archivos multimedia falsos, solo datos estructurados alfanuméricos.

---

## 2. Posicionamiento
### 2.1 Oportunidad de Negocio
Las leyes de privacidad internacionales obligan a las empresas a anonimizar bases de datos de producción antes de dárselas a los programadores. Este proceso es costoso y tedioso. El "DataGenerator" irrumpe en el mercado al permitir generar conjuntos de datos "Fake" matemáticamente coherentes en segundos, acoplándose directamente al servidor final, eliminando el traspaso manual de archivos SQL.

### 2.2 Definición del Problema
Para asegurar el impacto comercial, el problema que se resuelve ha sido formalizado de la siguiente manera:

| Factor | Descripción |
|---|---|
| **El problema de...** | Generar datos de prueba manualmente mediante scripts SQL o clonando bases de datos de producción enteras. |
| **Afecta a...** | Equipos de Desarrollo, Equipos de QA (Testers) y Administradores de Base de Datos (DBA). |
| **El impacto asociado es...** | Pérdida de hasta el 20% del tiempo de un Sprint de desarrollo en tareas manuales; y un alto riesgo de multas si se usan datos reales de clientes en entornos locales no seguros. |
| **Una solución adecuada sería...** | Proveer un sistema web auto-gestionable, independiente del motor de BD, donde el usuario visualice sus tablas, genere 50k registros con Faker, e inyecte la data en vivo de manera asíncrona. |

---

## 3. Descripción de los Interesados (Stakeholders) y Usuarios

### 3.1 Perfiles de los Interesados y Usuarios

**A. Stakeholders (No operan el sistema pero se benefician)**
| Rol | Representante | Responsabilidades y Metas | Criterios de Éxito |
|---|---|---|---|
| Inversionista | TechData Solutions | Monetizar la plataforma o ahorrar costos operativos internamente. | ROI en el 2do año, TCO bajo (Cloud Serverless). |
| Gerente de TI | Director del Área | Asegurar que su personal de desarrollo sea 20% más productivo. | Adopción del sistema por el 100% de los QAs. |

**B. Usuarios Finales (Operan directamente el sistema)**
| Perfil | Nivel Técnico | Frecuencia de Uso | Objetivos / Comportamiento esperado |
|---|---|---|---|
| **Ingeniero QA / Tester** | Medio | Alta (Diaria) | Necesita interfaz muy visual (Next.js), quiere previsualizar (Preview) los datos antes de inyectarlos, prefiere no tocar código. |
| **Desarrollador Backend**| Alto | Alta (Semanal) | Usa el sistema para llenar su BD local vacía y poder testear su propia API. Exige conexión a múltiples motores (Postgres, Mongo). |
| **SuperAdmin** | Alto | Baja (Mensual) | Auditar los registros creados. Desea un dashboard de estadísticas. |

### 3.2 Entorno de Usuario (Flujo de Uso Típico)
El flujo operativo inicia en la computadora local del QA usando un navegador moderno (Chrome/Edge). 
1. Hace Login. 
2. Ingresa las credenciales de la BD de un entorno de pruebas (ej. `Staging DB en AWS RDS`). 
3. El sistema lee el esquema. 
4. El QA marca "Insertar 10,000 usuarios". 
5. Cierra la sesión en el DataGenerator y pasa a testear su propia App con la data recién inyectada.

### 3.3 Matriz de Necesidades vs Características
| Necesidad / Dolor | Prioridad | Característica Propuesta (Feature) | Solución Actual (Competencia o Status Quo) |
|---|---|---|---|
| **No quiero programar los INSERTs a mano.** | Alta | Interfaz de selección de tablas que automatiza los queries. | Hacer scripts en DBeaver o PgAdmin línea a línea. |
| **Uso bases de datos raras o modernas.** | Alta | El backend implementa un *Factory Pattern* conectándose a SQL Server, Neo4j, Mongo, Postgres y MySQL. | Sistemas antiguos que solo soportan SQL Server. |
| **Miedo a que el generador borre mi Data.** | Crítica | El sistema extrae el esquema solo en modo lectura, calculando los *Offsets* del Primary Key (MAX(id)) para insertar sin pisar data existente. | Herramientas manuales que hacen truncate tables. |
| **No quiero volver a tipear las credenciales cada día.** | Media | Guardar la configuración de conexión cifrada (cryptography) vinculada al usuario logueado. | Anotar passwords en archivos de texto (inseguro). |

---

## 4. Vista General del Producto
### 4.1 Perspectiva del Producto
El sistema sigue un modelo Cliente-Servidor Desacoplado:
- **Cliente:** Desarrollado en **Next.js (React 19)** con **Radix UI**, ofreciendo una experiencia Single Page Application ultra-rápida.
- **Servidor API:** Expone interfaces RESTful con **FastAPI** (Python). Sirve como el puente que se conecta mediante los drivers nativos a las bases de datos de los clientes.

### 4.2 Resumen de Capacidades
- Escaneo de estructuras (Schema Analyzer).
- Generación de diccionarios de datos sintéticos (Librería Faker).
- Inyección paralela/asíncrona hacia BD remota.
- Descarga offline de reportes SQL, JSON y CSV comprimidos en ZIP.

### 4.3 Suposiciones y Dependencias
- Se asume que el usuario proporcionará credenciales de base de datos externas que tienen permisos de escritura (`GRANT INSERT`).
- Se asume que las bases de datos del cliente son accesibles vía TCP/IP (puertos expuestos) desde el servidor de DataGenerator.

### 4.4 Costos y Licenciamiento
- **Cloud Computing:** Desplegado en Vercel (Front) y DigitalOcean (Back) con OPEX proyectado en $200/mes para instancias con alta CPU.
- **Licenciamiento:** Toda la tecnología subyacente (FastAPI, React, Faker) está bajo licenciamiento libre de uso comercial (MIT / Apache 2.0).

---

## 5. Características del Producto (Features Principales)
1. **Autenticación Multi-Tenant (JWT):** Garantiza que cada usuario vea únicamente las credenciales y bases de datos que ha guardado en su perfil.
2. **Generador Asíncrono no-bloqueante:** Generar e inyectar 50k registros demora la CPU. El uso de la concurrencia nativa de Python asegura que otros usuarios logueados no experimenten lentitud.
3. **Múltiples Locales (Idiomas):** La data sintética (nombres, direcciones) generada respeta el formato del país deseado (ej. DNI y direcciones Peruanas `es_PE`).

---

## 6. Restricciones
- **Limitación de Volumen:** Como política del MVP, se limita la generación de registros a 50,000 por tabla por intento, para evitar saturar la memoria RAM del servidor (Restricción Operacional).
- **Formatos LOB:** No soporta la inyección ni exportación de archivos Blob (Imágenes, Videos) falsos en las tablas.

---

## 7. Rangos de Calidad
Métricas explícitamente acordadas como garantía del software:
- **Disponibilidad (Uptime):** El sistema API y Web deben estar operativos el 99.0% del mes laborable.
- **Rendimiento:** El proceso de `Schema Analysis` de una BD externa de 50 tablas no debe tardar más de 3.5 segundos en responder a la UI.
- **Extensibilidad:** Añadir un nuevo "Driver" (ej. Oracle) no debe requerir recodificar la UI, únicamente agregar la clase correspondiente en el backend.

---

## 8. Otros Requerimientos del Producto
### 8.1 Estándares Legales
- Cumplimiento de **Políticas de Datos Limpios**: Las contraseñas de las BD externas de los usuarios no existen en texto plano, impidiendo cualquier hackeo de la base de datos interna.

### 8.2 Estándares de Comunicación
- Uso estricto de **JSON sobre HTTP/1.1 (o HTTP/2)** para toda transacción entre Next.js y FastAPI.
- El servidor expone configuraciones **CORS** explícitas para prevenir ataques XSS y CSRF.
