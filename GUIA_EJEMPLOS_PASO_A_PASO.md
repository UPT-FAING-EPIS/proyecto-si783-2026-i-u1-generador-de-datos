# Ejemplos Paso a Paso: Configurar Conexiones en Cada Entorno

## 📱 Interfaz de Formulario del Sistema

El formulario de tu sistema tiene estos campos:

```
┌─────────────────────────────────────────┐
│  NUEVA CONEXIÓN A BASE DE DATOS         │
├─────────────────────────────────────────┤
│                                         │
│  Nombre:        [Ingresa un nombre]     │
│  Motor:         [PostgreSQL ▼]          │
│  Host:          [host o localhost]      │
│  Puerto:        [número]                │
│  Usuario:       [nombre de usuario]     │
│  Contraseña:    [contraseña]            │
│  Base de Datos: [nombre de BD]          │
│  Parámetros extra: [JSON opcional]      │
│                                         │
│  [Probar Conexión]  [Guardar]           │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🎓 Ejemplo 1: Conexión Local - PostgreSQL en tu PC

### Escenario
- Estás desarrollando en tu PC
- Instalaste PostgreSQL de forma nativa (o via brew/apt)
- Quieres que el backend también en tu PC se conecte

### Paso 1: Obtener los datos

```bash
# En tu terminal, conecta a PostgreSQL para ver configuración
psql -U postgres

# Una vez dentro, verifica:
postgres=# SELECT version();
 PostgreSQL 14.5 (Ubuntu 14.5-1.pgdg20.04+1)

# Presiona Ctrl+D para salir
```

### Paso 2: Llenar el formulario

```
Nombre:           Mi PostgreSQL Local
Motor:            PostgreSQL
Host:             localhost
Puerto:           5432
Usuario:          postgres
Contraseña:       tu_contraseña_de_postgres
Base de Datos:    postgres (o tu BD actual)
Parámetros extra: (dejar vacío)
```

### Paso 3: Probar conexión

```
[Probar Conexión]
↓
Resultado esperado:
✓ Conexión exitosa
  Versión: PostgreSQL 14.5
  Latencia: 5.23 ms
```

### ¿Por qué funciona?
- `localhost` se resuelve a `127.0.0.1` (el PC mismo)
- PostgreSQL escucha en puerto 5432 en ese PC
- Credenciales son válidas

---

## 🎓 Ejemplo 2: MySQL Local desde XAMPP

### Escenario
- XAMPP instalado en tu PC
- Backend también en tu PC (Python Flask/FastAPI)
- Quieres conectar a MySQL de XAMPP

### Paso 1: Verificar que XAMPP esté corriendo

```
1. Abre XAMPP Control Panel
2. Presiona "Start" para MySQL
3. Verifica que dice "Running" y el puerto es 3306
```

### Paso 2: Encontrar credenciales

```bash
# XAMPP usa por defecto:
# Usuario: root
# Contraseña: (vacío)
# Servidor: localhost
# Puerto: 3306

# Verifica conectando manualmente:
mysql -h localhost -u root
mysql> SHOW DATABASES;
mysql> CREATE DATABASE testdb;
mysql> EXIT;
```

### Paso 3: Llenar el formulario

```
Nombre:           MySQL XAMPP
Motor:            MySQL
Host:             localhost
Puerto:           3306
Usuario:          root
Contraseña:       (dejar vacío si no tiene)
Base de Datos:    testdb
Parámetros extra: (dejar vacío)
```

### Paso 4: Probar

```
[Probar Conexión]
↓
✓ Conexión exitosa
  Versión: MySQL 8.0.32
  Latencia: 3.45 ms
```

---

## 🐳 Ejemplo 3: PostgreSQL en Docker Local

### Escenario
- Corriste `docker-compose up -d` en tu proyecto
- Quieres conectar desde tu PC (fuera del Docker) y desde backend (dentro de Docker)

### Parte A: Desde tu PC (acceso externo)

**Paso 1: Verifica que docker esté corriendo**

```bash
docker-compose ps

# Resultado:
# NAME                 IMAGE          STATUS
# smartgen_postgres    postgres:16    Up 2 minutes
```

**Paso 2: Llenar el formulario**

```
Nombre:           PostgreSQL Docker Local
Motor:            PostgreSQL
Host:             localhost           ← Desde tu PC
Puerto:           5433                ← Puerto PUBLICADO (del -p 5433:5432)
Usuario:          admin
Contraseña:       admin123
Base de Datos:    smartgen_db
Parámetros extra: (dejar vacío)
```

**Paso 3: Probar**

```
[Probar Conexión]
↓
✓ Conexión exitosa
  Versión: PostgreSQL 16.1
  Latencia: 8.92 ms
```

**¿Por qué funciona?**
- `localhost:5433` desde tu PC → se mapea a `127.0.0.1:5433`
- Docker mapea puerto 5433 (tu PC) → 5432 (contenedor)
- Credenciales coinciden con docker-compose.yml

---

### Parte B: Desde Backend en Docker (acceso interno)

**Paso 1: Conecta al contenedor del backend**

```bash
docker exec -it smartgen_backend bash
# Ahora estás DENTRO del contenedor
```

**Paso 2: Prueba conectar desde dentro**

```bash
# Desde dentro del contenedor, postgres NO está en localhost
# Está en el otro contenedor llamado "postgres_main"

psql -h postgres_main -U admin -d smartgen_db
# Pide contraseña: admin123

# Si funciona:
smartgen_db=# \dt  (lista tablas)
smartgen_db=# EXIT;
```

**Paso 3: Llenar el formulario (con backend DENTRO del contenedor)**

```
Nombre:           PostgreSQL Docker Interno
Motor:            PostgreSQL
Host:             postgres_main       ← Nombre del servicio, no localhost
Puerto:           5432                ← Puerto INTERNO, no publicado
Usuario:          admin
Contraseña:       admin123
Base de Datos:    smartgen_db
Parámetros extra: (dejar vacío)
```

**Paso 4: Probar**

```
[Probar Conexión]
↓
✓ Conexión exitosa
  Versión: PostgreSQL 16.1
  Latencia: 2.34 ms (más rápido, misma red)
```

**¿Por qué es diferente?**

```
Desde PC:
localhost:5433 → (tu router) → Docker → Contenedor postgres:5432

Desde contenedor del backend:
postgres_main:5432 → (red Docker) → Contenedor postgres:5432
```

---

## ☁️ Ejemplo 4: Supabase (PostgreSQL en la nube)

### Escenario
- Creaste un proyecto en Supabase
- Backend está desplegado en un servidor
- Quieres conectar a Supabase

### Paso 1: Obtener credenciales de Supabase

```
1. Abre https://supabase.com
2. Inicia sesión en tu proyecto
3. Ve a: Settings → Database
4. Sección "Connection String" - modo "URI"
5. Copia el string, debería verse así:

postgresql://postgres:TuPasswordMuySeguro@db.xyzabc123.supabase.co:5432/postgres
         ↑            ↑                     ↑                              ↑
      usuario    contraseña              host                         base_datos
```

### Paso 2: Desglosar los componentes

```
postgresql://
  postgres                    ← Usuario
  :TuPasswordMuySeguro       ← Contraseña  
  @db.xyzabc123.supabase.co  ← Host
  :5432                      ← Puerto
  /postgres                  ← Base de datos
```

### Paso 3: Llenar el formulario

```
Nombre:           Supabase Production
Motor:            PostgreSQL
Host:             db.xyzabc123.supabase.co
Puerto:           5432
Usuario:          postgres
Contraseña:       TuPasswordMuySeguro
Base de Datos:    postgres
Parámetros extra: {"sslmode": "require"}
```

⚠️ **Importante**: Supabase REQUIERE SSL, por eso agregamos `"sslmode": "require"`

### Paso 4: Probar

```
[Probar Conexión]
↓
✓ Conexión exitosa
  Versión: PostgreSQL 15.1
  Latencia: 245.67 ms (más lento, conexión a internet)
```

### ¿Por qué funciona?
- `db.xyzabc123.supabase.co` es un dominio DNS público
- Supabase expone el puerto 5432
- SSL encripta la conexión
- Cualquiera (con credenciales) puede conectar

---

## ☁️ Ejemplo 5: AWS RDS PostgreSQL

### Escenario
- Creaste una instancia RDS en AWS
- Backend está desplegado en EC2
- Quieres conectar el backend a RDS

### Paso 1: Obtener el endpoint de RDS

```
AWS Console → RDS → Databases → Tu DB
↓
Conectividad & Seguridad
↓
Endpoint & puerto:
mydb-instance.c9akciq32.us-east-1.rds.amazonaws.com:5432
```

### Paso 2: Obtener credenciales

```
Durante la creación guardaste:
- Usuario: admin
- Contraseña: MyPassword123!
- Base de datos: myappdb
```

### Paso 3: Llenar el formulario

```
Nombre:           AWS RDS Production
Motor:            PostgreSQL
Host:             mydb-instance.c9akciq32.us-east-1.rds.amazonaws.com
Puerto:           5432
Usuario:          admin
Contraseña:       MyPassword123!
Base de Datos:    myappdb
Parámetros extra: {"sslmode": "require"}
```

### Paso 4: Probar

```
[Probar Conexión]
↓
✗ Connection refused / Timeout?

↓ Verifica Security Group:
AWS Console → EC2 → Security Groups → Tu grupo
→ Inbound Rules
→ ¿Permite puerto 5432 desde tu IP/SG?

Si no, agrega:
Tipo: PostgreSQL
Protocolo: TCP
Puerto: 5432
Origen: 0.0.0.0/0 (o la IP de tu backend)

↓ Intenta de nuevo:

✓ Conexión exitosa
  Versión: PostgreSQL 15.3
  Latencia: 187.34 ms
```

---

## 📊 Ejemplo 6: MongoDB Atlas (NoSQL en la nube)

### Escenario
- Creaste un cluster en MongoDB Atlas
- Backend también está en un servidor
- Quieres conectar a MongoDB

### Paso 1: Obtener cadena de conexión de MongoDB Atlas

```
1. Abre MongoDB Atlas → Tu cluster
2. Click: "Connect"
3. Selecciona: "Connection String"
4. Copia la URI (debe comenzar con mongodb+srv://)

mongodb+srv://admin_user:MyPasswordMongo123!@cluster0.mongodb.net/myappdb?retryWrites=true&w=majority
```

### Paso 2: Opción A - Usar URI directamente (recomendado)

```
Nombre:           MongoDB Atlas
Motor:            MongoDB
Host:             (puede quedar vacío si usas URI)
Puerto:           (puede quedar vacío si usas URI)
Usuario:          (puede quedar vacío si usas URI)
Contraseña:       (puede quedar vacío si usas URI)
Base de Datos:    myappdb
Parámetros extra: {
  "uri": "mongodb+srv://admin_user:MyPasswordMongo123!@cluster0.mongodb.net/myappdb?retryWrites=true&w=majority"
}
```

### Paso 3: Opción B - Desglosar componentes

```
mongodb+srv://
  admin_user                           ← Usuario
  :MyPasswordMongo123!                 ← Contraseña
  @cluster0.mongodb.net                ← Host (con srv)
  /myappdb                             ← Base de datos
  ?retryWrites=true&w=majority         ← Parámetros
```

Si tu sistema permite separar usuario/pass/host:

```
Nombre:           MongoDB Atlas Desglosado
Motor:            MongoDB
Host:             cluster0.mongodb.net
Puerto:           27017
Usuario:          admin_user
Contraseña:       MyPasswordMongo123!
Base de Datos:    myappdb
Parámetros extra: {"ssl": true}
```

### Paso 4: Probar

```
[Probar Conexión]
↓
✓ Conexión exitosa
  Versión: MongoDB 6.0
  Latencia: 267.45 ms
```

---

## 🚫 Ejemplo 7: Lo que NO funciona (pero podrías intentar)

### Intento fallido: Conectar a BD local desde servidor remoto

**Configuración que ALGUIEN PODRÍA intentar:**

```
Nombre:           PostgreSQL en mi PC (INTENTO FALLIDO)
Motor:            PostgreSQL
Host:             192.168.1.100        ← Tu PC (IP privada)
Puerto:           5432
Usuario:          postgres
Contraseña:       password
Base de Datos:    testdb
```

**Resultado:**

```
[Probar Conexión]
↓
✗ Connection refused / Timeout
  No route to host
  
Razón: 192.168.1.100 es una IP privada
       Solo accesible dentro de tu red local
       Servidor remoto está en internet diferente
       ↓
       ¡IMPOSIBLE CONECTAR!
```

**¿Cómo solucionarlo?** (Si realmente lo necesitas)

```
Opción 1: Usar VPN
  - Backend conecta a VPN
  - Ahora puede ver tu red local
  - Luego conecta a 192.168.1.100
  
Opción 2: Port forwarding en router (NO RECOMENDADO)
  - Router: Mapea puerto externo (ej: 15432) → 192.168.1.100:5432
  - Backend: Conecta a IP_PUBLICA:15432
  - PROBLEMA: Expondrías BD a internet ⚠️
  
Opción 3: Mover BD a la nube
  - Supabase, AWS RDS, etc.
  - RECOMENDADO para producción
```

---

## 🔄 Flujo Completo: Desarrollo → Producción

### Local (Dev)

```
┌─────────────────────────────────────┐
│ Tu PC                               │
│                                     │
│ Frontend (localhost:3000)           │
│        ↓                            │
│ Backend (localhost:8000)            │
│        ↓                            │
│ PostgreSQL local (localhost:5432)   │
│                                     │
└─────────────────────────────────────┘

Configuración:
Host: localhost
Puerto: 5432
Usuario: postgres
Contraseña: dev_password
```

### Docker Local (Testing)

```
┌────────────────────────────────────────────┐
│ Docker Network                             │
│                                            │
│ ┌─────────┐  ┌────────┐  ┌────────────┐  │
│ │Frontend │→ │Backend │→ │PostgreSQL  │  │
│ └─────────┘  └────────┘  └────────────┘  │
│  :3000       :8000        :5432(interno)  │
│                                            │
│ (Publicado: localhost:5433)               │
│                                            │
└────────────────────────────────────────────┘

Configuración (desde backend):
Host: postgres_main
Puerto: 5432
Usuario: admin
Contraseña: admin123
```

### Producción (Server)

```
┌─────────────────────────────────────────────┐
│ Servidor Remoto                             │
│                                             │
│ Docker Network                              │
│ ┌──────────┐  ┌────────┐  ┌────────────┐   │
│ │   CDN    │  │Backend │→ │PostgreSQL  │   │
│ │/Frontend │  │Docker  │  │Docker      │   │
│ └──────────┘  └────────┘  └────────────┘   │
│   Nginx        Port 8000    Port 5432      │
│   Port 443                  (no publicado) │
│   Port 80                                  │
│                                             │
│ Ó alternativamente:                        │
│                                             │
│ ┌────────┐              ┌──────────────┐   │
│ │Backend │─────────────→│Supabase / AWS│   │
│ │Docker  │   SSL/TLS    │Cloud Provider   │
│ └────────┘              └──────────────┘   │
│ Port 8000                                  │
│                                             │
└─────────────────────────────────────────────┘

Configuración (desde backend):
Opción 1 (BD local en server):
  Host: postgres_main
  Puerto: 5432
  Usuario: admin
  Contraseña: production_password
  
Opción 2 (BD en la nube):
  Host: db.abc123.supabase.co
  Puerto: 5432
  Usuario: postgres
  Contraseña: cloud_password
  Parámetros: {"sslmode": "require"}
```

---

## 📸 Captura de Pantalla: Cómo se vería el formulario

### Escenario: Supabase en Producción

```
╔════════════════════════════════════════════════╗
║         NUEVA CONEXIÓN A BASE DE DATOS        ║
╠════════════════════════════════════════════════╣
║                                                ║
║  Nombre:                                       ║
║  ┌──────────────────────────────────────────┐ ║
║  │ Supabase Production                      │ ║
║  └──────────────────────────────────────────┘ ║
║                                                ║
║  Motor:                                        ║
║  ┌──────────────────────────────────────────┐ ║
║  │ PostgreSQL                            ▼ │ ║
║  └──────────────────────────────────────────┘ ║
║                                                ║
║  Host:                                         ║
║  ┌──────────────────────────────────────────┐ ║
║  │ db.xyzabc123.supabase.co                 │ ║
║  └──────────────────────────────────────────┘ ║
║                                                ║
║  Puerto:                                       ║
║  ┌──────────────────────────────────────────┐ ║
║  │ 5432                                     │ ║
║  └──────────────────────────────────────────┘ ║
║                                                ║
║  Usuario:                                      ║
║  ┌──────────────────────────────────────────┐ ║
║  │ postgres                                 │ ║
║  └──────────────────────────────────────────┘ ║
║                                                ║
║  Contraseña:                                   ║
║  ┌──────────────────────────────────────────┐ ║
║  │ ••••••••••••••••••••••••••••••••••••     │ ║
║  └──────────────────────────────────────────┘ ║
║                                                ║
║  Base de Datos:                                ║
║  ┌──────────────────────────────────────────┐ ║
║  │ postgres                                 │ ║
║  └──────────────────────────────────────────┘ ║
║                                                ║
║  Parámetros extra (JSON):                      ║
║  ┌──────────────────────────────────────────┐ ║
║  │ {"sslmode": "require"}                   │ ║
║  └──────────────────────────────────────────┘ ║
║                                                ║
║  ┌──────────────────────┐  ┌───────────────┐ ║
║  │ Probar Conexión      │  │    Guardar    │ ║
║  └──────────────────────┘  └───────────────┘ ║
║                                                ║
║  Resultado de prueba:                          ║
║  ┌──────────────────────────────────────────┐ ║
║  │ ✓ Conexión exitosa                       │ ║
║  │   Versión: PostgreSQL 15.1               │ ║
║  │   Latencia: 245.67 ms                    │ ║
║  └──────────────────────────────────────────┘ ║
║                                                ║
╚════════════════════════════════════════════════╝
```

---

## 🧪 Pruebas de Conexión en Terminal

Después de configurar en el formulario, puedes validar manualmente:

### PostgreSQL

```bash
# Local
psql -h localhost -p 5432 -U postgres -d testdb

# Supabase
psql -h db.xyz.supabase.co -p 5432 -U postgres -d postgres

# AWS RDS
psql -h mydb.rds.amazonaws.com -p 5432 -U admin -d mydb
```

### MySQL

```bash
# Local
mysql -h localhost -u root -p testdb

# Cloud
mysql -h db.cloud.mysql.com -u admin -p -D mydb
```

### MongoDB

```bash
# Local
mongosh "mongodb://localhost:27017"

# Atlas
mongosh "mongodb+srv://admin:password@cluster0.mongodb.net/mydb"
```

---

**Última actualización:** Mayo 2026
