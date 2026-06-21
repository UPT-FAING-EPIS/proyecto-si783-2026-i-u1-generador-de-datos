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
| 2.0 | MRL / MCC | ELV | ARV | 05/05/2026 | Expansión profunda de análisis financiero y actualización a Python/Next.js |

---

# Informe de Factibilidad (FD01)

## ÍNDICE GENERAL
1. [Descripción del Proyecto](#1-descripción-del-proyecto)
2. [Riesgos](#2-riesgos)
3. [Análisis de la Situación Actual](#3-análisis-de-la-situación-actual)
4. [Viabilidad Técnica](#4-viabilidad-técnica)
5. [Estudio de Factibilidad](#5-estudio-de-factibilidad)
   - 5.1 Factibilidad Técnica
   - 5.2 Factibilidad Operativa
   - 5.3 Factibilidad Legal
   - 5.4 Factibilidad Social
   - 5.5 Factibilidad Ambiental
   - 5.6 Factibilidad Económica (Tablas de Costos)
6. [Análisis Financiero](#6-análisis-financiero)
   - Flujo de Caja Proyectado
   - VAN, TIR y Relación Beneficio/Costo
7. [Conclusiones](#7-conclusiones)

---

## 1. Descripción del Proyecto
### 1.1 Nombre del Proyecto
**Sistema Inteligente Generador de Datos Sintéticos Multi-Motor (DataGenerator)**.

### 1.2 Duración del Proyecto
El proyecto tiene una duración estimada de **90 días calendarios (3 meses)**, distribuidos en las siguientes fases:
| Fase | Actividad | Duración (Días) |
|---|---|---|
| Fase 1 | Análisis de Requerimientos y Diseño Arquitectónico (UML/C4) | 15 |
| Fase 2 | Desarrollo Frontend (Next.js) y UX/UI | 25 |
| Fase 3 | Desarrollo Backend (FastAPI), Generadores y Conectores de BD | 30 |
| Fase 4 | Integración, Pruebas Unitarias/E2E y Seguridad | 15 |
| Fase 5 | Despliegue en producción y Capacitación | 5 |
| **Total** | **Desarrollo completo hasta MVP productivo** | **90** |

### 1.3 Objetivos
**Objetivo General:**  
Desarrollar una plataforma web capaz de extraer esquemas automáticamente de bases de datos externas e insertar volúmenes masivos de datos sintéticos (hasta 50k registros) directamente a los motores SQL y NoSQL, reduciendo drásticamente los tiempos de QA.

**Objetivos Específicos:**
- Implementar una arquitectura desacoplada Cliente-Servidor (Next.js y FastAPI).
- Asegurar las credenciales de bases de datos utilizando criptografía simétrica (`cryptography`).
- Soportar inserción asíncrona a 6 motores distintos: PostgreSQL, MySQL, MongoDB, SQL Server, Neo4j, Cassandra.

---

## 2. Riesgos
| Tipo de Riesgo | Descripción | Probabilidad | Impacto | Estrategia de Mitigación |
|---|---|---|---|---|
| **Tecnológico** | Incompatibilidad con versiones antiguas de bases de datos (Ej. MySQL 5.7). | Media | Alto | Uso estricto de librerías oficiales actualizadas (`pymysql`, `psycopg2`). |
| **Seguridad** | Exposición de credenciales de bases de datos de clientes si la BD interna es comprometida. | Baja | Crítico | Encriptación en reposo usando Fernet y variables de entorno no versionadas. |
| **Rendimiento** | Bloqueo del servidor por concurrencia extrema durante inserciones masivas. | Media | Alto | Configuración de Workers asíncronos en Uvicorn/FastAPI. |

---

## 3. Análisis de la Situación Actual
### 3.1 Planteamiento del Problema
Actualmente, los equipos de desarrollo y aseguramiento de calidad (QA) pierden un estimado de **4 a 6 horas por sprint** redactando scripts SQL manuales (`INSERT INTO...`) para crear escenarios de prueba. Además, el uso inadvertido de copias de producción reales compromete la privacidad de los usuarios finales y viola normativas de protección de datos.

### 3.2 Consideraciones de Software
El nuevo paradigma propuesto adopta tecnologías Open Source de alto rendimiento:
- **Backend:** Python 3.12, FastAPI, SQLAlchemy.
- **Frontend:** React 19, Next.js 16, TailwindCSS, Radix UI.
- **Persistencia Interna:** MySQL 8.0.

---

## 4. Viabilidad Técnica
### 4.1 Medidas de Seguridad Implementadas
1. **Autenticación Fuerte:** JSON Web Tokens (JWT) para sesiones de usuario con expiración controlada.
2. **Cifrado de Credenciales:** Las contraseñas para conectarse a las BDs externas se cifran simétricamente antes de guardarse en la tabla `conexiones`.
3. **CORS y Rate Limiting:** Protección contra ataques de peticiones cruzadas y fuerza bruta en la API.

### 4.2 Matriz de Evaluación Técnica
| Factor Evaluado | Puntaje (1-5) | Justificación |
|---|---|---|
| Disponibilidad de Herramientas Open Source | 5 | Librerías Faker, FastAPI y Next.js son 100% gratuitas. |
| Capacidad del Personal | 4 | Equipo con conocimiento en Python y JS. Curva de aprendizaje corta. |
| Escalabilidad de la Arquitectura | 5 | Arquitectura sin estado (stateless) lista para Docker/Kubernetes. |

---

## 5. Estudio de Factibilidad

### 5.1 Factibilidad Técnica
Se cuenta con las computadoras, IDEs (VS Code) y cuentas Cloud (Vercel, AWS Free Tier) para levantar los entornos de prueba. La integración entre React y Python a través de API REST garantiza que no haya cuellos de botella tecnológicos.

### 5.2 Factibilidad Operativa
La curva de aprendizaje del cliente final es mínima debido al enfoque "Auto-servicio" de la interfaz gráfica construida con Next.js. El QA no necesita saber código, solo configurar visualmente las tablas y cliquear "Insertar".

### 5.3 Factibilidad Legal
Totalmente factible. Al generar "datos falsos" (nombres ficticios, tarjetas de crédito irreales mediante la librería `Faker`), el sistema anula por completo el riesgo legal de violar la Ley de Protección de Datos Personales (Ley 29733 de Perú) o la GDPR europea.

### 5.4 Factibilidad Social
Aumenta la retención de talento. Los desarrolladores evitan el trabajo monótono y repetitivo de crear datos, incrementando su satisfacción laboral.

### 5.5 Factibilidad Ambiental (Green IT)
El procesamiento asíncrono de FastAPI reduce significativamente el consumo de CPU frente a arquitecturas síncronas tradicionales. Esto significa menos consumo eléctrico en los centros de datos (Cloud), alineándose a las prácticas sostenibles.

### 5.6 Factibilidad Económica (Tablas de Costos)

**A. Inversión Inicial de Capital (CAPEX)** - *Mes 0 a Mes 3*
| Concepto | Cantidad | Costo Unitario (S/) | Total (S/) |
|---|---|---|---|
| Salario Equipo de Desarrollo (2 Devs x 3 Meses) | 6 | 4,500.00 | 27,000.00 |
| Equipos de Cómputo (Laptops Pro) | 2 | 3,500.00 | 7,000.00 |
| Licencias de UI (Componentes Premium) | 1 | 1,000.00 | 1,000.00 |
| **Total Inversión Inicial (I₀)** | | | **35,000.00** |

**B. Costos Operativos Anuales (OPEX)** - *Mantenimiento y Cloud*
| Concepto | Costo Mensual Estimado (S/) | Costo Anual Estimado (S/) |
|---|---|---|
| Servidores Cloud (AWS/DigitalOcean) + Base de Datos | 450.00 | 5,400.00 |
| Soporte y Mantenimiento Técnico | 300.00 | 3,600.00 |
| Servicios Adicionales (Dominios, SSL) | 83.33 | 1,000.00 |
| **Total OPEX Anual** | **833.33** | **10,000.00** |

**C. Beneficios Económicos (Ahorro / Ingresos)**
El beneficio económico proviene del **ahorro directo de horas-hombre**. Si 5 equipos de QA de una empresa dejan de gastar horas en redactar SQL, el ahorro de nómina se calcula en **S/ 27,500.00** anuales (equivalente o ingreso directo por licenciamiento).

---

## 6. Análisis Financiero

Para verificar que el proyecto es financieramente sensato sin recurrir a cifras infladas o poco realistas, se ha utilizado un horizonte de evaluación de **3 años** y una **Tasa de Descuento (COK)** del **12%**.

### 6.1 Flujo de Caja Proyectado
| Concepto | Año 0 | Año 1 | Año 2 | Año 3 |
|---|---|---|---|---|
| **Ingresos / Ahorros (S/)** | 0.00 | 27,500.00 | 27,500.00 | 27,500.00 |
| **Costos Operativos (OPEX) (S/)** | 0.00 | (10,000.00) | (10,000.00) | (10,000.00) |
| **Flujo de Caja Operativo** | 0.00 | **17,500.00** | **17,500.00** | **17,500.00** |
| **Inversión Inicial (CAPEX) (S/)** | (35,000.00)| - | - | - |
| **Flujo de Caja Neto (FCN)** | **(35,000.00)**| **17,500.00** | **17,500.00** | **17,500.00** |

### 6.2 Indicadores de Rentabilidad

1. **VAN (Valor Actual Neto) a COK 12%**
   - PV(Año 1): 17,500 / 1.12 = S/ 15,625.00
   - PV(Año 2): 17,500 / (1.12)^2 = S/ 13,950.89
   - PV(Año 3): 17,500 / (1.12)^3 = S/ 12,456.15
   - **Suma del Valor Presente:** S/ 42,032.04
   - **VAN:** S/ 42,032.04 - Inversión (S/ 35,000) = **S/ 7,032.04**

2. **Relación Beneficio / Costo (B/C)**
   - Suma del Valor Presente / Inversión Inicial
   - S/ 42,032.04 / S/ 35,000.00 = **1.20**
   *(Por cada S/ 1.00 invertido, el proyecto retorna S/ 1.20, demostrando una rentabilidad realista y moderada).*

3. **TIR (Tasa Interna de Retorno)**
   - La TIR estimada es del **23.38%**, la cual es superior a la tasa de descuento (12%), indicando que la inversión generará mejor retorno que un fondo bancario estándar.

4. **Periodo de Recuperación (Payback)**
   - Año 1: Quedan S/ 17,500 por recuperar.
   - Año 2: Inversión totalmente recuperada.
   - **Payback:** Exactamente **2 Años**.

---

## 7. Conclusiones
El proyecto "DataGenerator" es **Altamente Factible** en todos sus aspectos.
- Desde el punto de vista **Técnico**, el uso del framework FastAPI facilita drásticamente la extracción e inserción a múltiples motores sin necesidad de dependencias monolíticas pesadas.
- Desde la óptica **Financiera**, el proyecto presenta indicadores muy saludables y realistas. Un **Beneficio/Costo de 1.20** y un **VAN positivo de S/ 7,032.04** nos aseguran que el proyecto no está ni sobrevaluado financieramente ni incurrirá en pérdidas. El capital inyectado se recupera de manera segura en el segundo año de operatividad, demostrando una excelente salud fiscal corporativa.
