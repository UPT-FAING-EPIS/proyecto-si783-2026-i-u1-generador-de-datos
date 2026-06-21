import pymysql
import bcrypt
from datetime import datetime

# 1. Configuración de la conexión a tu base de datos MariaDB
DB_CONFIG = {
    'host': '149.34.48.176',
    'port': 3307,
    'user': 'root',
    'password': 'marymar123',  # Presiona Enter si no usas contraseña de root, o colócala aquí si tiene una
    'database': 'datagenerator_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 2. Generar el Hash Bcrypt para la contraseña común: User12345
print("🔐 Generando hash de seguridad para las contraseñas...")
password_plana = "User12345".encode('utf-8')
password_hash = bcrypt.hashpw(password_plana, bcrypt.gensalt(12)).decode('utf-8')

# 3. Lista de nombres y apellidos ficticios para variar los datos
nombres = ["Juan", "Maria", "Pedro", "Ana", "Luis", "Elena", "Diego", "Lucia", "jorge", "Sofia"]
apellidos = ["Gomez", "Rodriguez", "Lopez", "Martinez", "Perez", "Garcia", "Sánchez", "Fernandez", "Torres", "Ramirez"]

try:
    # Conectarse a la base de datos
    conexion = pymysql.connect(**DB_CONFIG)
    with conexion.cursor() as cursor:
        print("📥 Insertando 30 usuarios en la tabla 'usuarios'...")
        
        sql = """
        INSERT INTO usuarios (nombre, apellido, email, password_hash, rol, activo, created_at, updated_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        ahora = datetime.now()
        
        for i in range(1, 31):
            nombre = nombres[i % len(nombres)]
            apellido = apellidos[i % len(apellidos)]
            email = f"user{i}@sistema.com"
            rol = "usuario"
            activo = 1
            
            cursor.execute(sql, (nombre, apellido, email, password_hash, rol, activo, ahora, ahora))
        
        # Guardar los cambios de forma permanente
        conexion.commit()
        print(f"✅ ¡Éxito! Se han creado 30 usuarios correctamente.")
        print("💡 Nota: Todos los usuarios pueden ingresar con la contraseña: User12345")

except Exception as e:
    print(f"❌ Ocurrió un error al insertar los usuarios: {e}")
    print("👉 Si tu usuario 'root' de MariaDB requiere contraseña, edítala en la línea 9 del script.")

finally:
    if 'conexion' in locals() and conexion.open:
        conexion.close()
