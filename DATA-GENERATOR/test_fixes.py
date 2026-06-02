import os
import sys
import base64
import hashlib

# Fix encoding para Windows
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("VERIFICACION DE FIXES CRITICOS -- DATA-GENERATOR")
print("=" * 60)

# Cargar variables de entorno del .env
from dotenv import load_dotenv
load_dotenv(".env")

passed = 0
failed = 0

def check(name, condition, detail=""):
    global passed, failed
    if condition:
        print(f"  [OK]  {name}")
        passed += 1
    else:
        print(f"  [FAIL] {name}")
        if detail:
            print(f"         -> {detail}")
        failed += 1


# ─────────────────────────────────────────────
print("\n[Fix C2] JWT_SECRET_KEY seguro")
jwt_key = os.getenv("JWT_SECRET_KEY", "")
check("JWT_SECRET_KEY no es el valor por defecto",
      jwt_key not in ("cambia_esto_por_una_clave_segura_de_al_menos_32_chars", "secret_key_change_me", ""),
      f"Valor actual: '{jwt_key[:10]}...'")
check("JWT_SECRET_KEY tiene al menos 32 caracteres",
      len(jwt_key) >= 32,
      f"Longitud actual: {len(jwt_key)}")

# ─────────────────────────────────────────────
print("\n[Fix C2] ENCRYPTION_KEY separado")
enc_key = os.getenv("ENCRYPTION_KEY", "")
check("ENCRYPTION_KEY existe y no está vacío",
      enc_key not in ("", "encryption_key_change_me"),
      f"Valor: '{enc_key[:10]}...'")
check("ENCRYPTION_KEY es diferente de JWT_SECRET_KEY",
      enc_key != jwt_key,
      "Ambas claves son idénticas — riesgo de pérdida de datos al rotar JWT")

# ─────────────────────────────────────────────
print("\n[Fix C3] Contraseña superadmin")
admin_pw = os.getenv("SUPERADMIN_PASSWORD", "")
check("Contraseña no es 'Admin123!' (valor expuesto)",
      admin_pw != "Admin123!",
      f"Valor actual: '{admin_pw}'")
check("Contraseña tiene al menos 12 caracteres",
      len(admin_pw) >= 12,
      f"Longitud: {len(admin_pw)}")

# ─────────────────────────────────────────────
print("\n[Fix S2] encryption.py usa ENCRYPTION_KEY")
try:
    with open("backend/core/encryption.py", "r", encoding="utf-8") as f:
        enc_content = f.read()
    check("encryption.py usa ENCRYPTION_KEY (no JWT_SECRET_KEY)",
          "ENCRYPTION_KEY" in enc_content and "JWT_SECRET_KEY" not in enc_content,
          "El archivo todavía referencia JWT_SECRET_KEY")
except FileNotFoundError:
    check("encryption.py encontrado", False, "Archivo no encontrado")

# ─────────────────────────────────────────────
print("\n[Fix S1] API no devuelve contraseñas")
try:
    with open("backend/api/connector_router.py", "r", encoding="utf-8") as f:
        conn_content = f.read()
    check("connector_router.py no llama a decrypt_password en /saved",
          "decrypt_password" not in conn_content or "password_db=None" in conn_content,
          "Todavía llama a decrypt_password y devuelve el valor")
    check("connector_router.py retorna password_db=None",
          "password_db=None" in conn_content,
          "El campo password_db no se está forzando a None")
except FileNotFoundError:
    check("connector_router.py encontrado", False, "Archivo no encontrado")

# ─────────────────────────────────────────────
print("\n[Fix S4] Protección contra path traversal")
try:
    with open("backend/api/generator_router.py", "r", encoding="utf-8") as f:
        gen_content = f.read()
    check("generator_router.py valida con os.path.realpath",
          "os.path.realpath" in gen_content,
          "No se encontró validación de path traversal")
    check("generator_router.py tiene whitelist de extensiones",
          "ALLOWED_EXTENSIONS" in gen_content,
          "No hay whitelist de extensiones de archivo")
    check("endpoint /download requiere autenticación",
          "get_current_user" in gen_content.split("/download")[1] if "/download" in gen_content else False,
          "El endpoint de descarga no requiere autenticación")
except FileNotFoundError:
    check("generator_router.py encontrado", False, "Archivo no encontrado")

# ─────────────────────────────────────────────
print("\n[Fix C4] TEMP_DIR no hardcodeado")
try:
    with open("backend/generators/exporters.py", "r", encoding="utf-8") as f:
        exp_content = f.read()
    check("exporters.py no usa /tmp/data_generator hardcodeado",
          "/tmp/data_generator" not in exp_content,
          "Todavía contiene la ruta hardcodeada /tmp/data_generator")
    check("exporters.py importa settings",
          "from backend.core.config import settings" in exp_content,
          "No importa settings")
    check("exporters.py usa settings.TEMP_DIR",
          "settings.TEMP_DIR" in exp_content,
          "No usa settings.TEMP_DIR")
except FileNotFoundError:
    check("exporters.py encontrado", False, "Archivo no encontrado")

# ─────────────────────────────────────────────
print("\n[Fix C5] Nginx sin rewrite incorrecto")
try:
    with open("nginx.conf", "r", encoding="utf-8") as f:
        nginx_content = f.read()
    check("nginx.conf no reescribe /api/ eliminando el prefijo",
          "rewrite ^/api/" not in nginx_content,
          "Todavía tiene la reescritura incorrecta de /api/")
    check("nginx.conf pasa X-Real-IP al backend",
          "X-Real-IP" in nginx_content,
          "No pasa la IP real al backend")
except FileNotFoundError:
    check("nginx.conf encontrado", False, "Archivo no encontrado")

# ─────────────────────────────────────────────
print("\n[Extra] Importaciones funcionales del backend")
try:
    sys.path.insert(0, ".")
    from backend.core.config import settings as cfg
    check("Settings carga correctamente desde .env",
          cfg.JWT_SECRET_KEY != "secret_key_change_me",
          f"JWT_SECRET_KEY sigue siendo el valor por defecto")
    check("ENCRYPTION_KEY está disponible en settings",
          hasattr(cfg, "ENCRYPTION_KEY") and cfg.ENCRYPTION_KEY != "encryption_key_change_me",
          "ENCRYPTION_KEY no está en settings o es el valor por defecto")
except Exception as e:
    check("Settings importa sin errores", False, str(e))

# ─────────────────────────────────────────────
print("\n" + "=" * 60)
total = passed + failed
print(f"RESULTADO: {passed}/{total} verificaciones pasaron")
if failed == 0:
    print("✅ TODOS LOS FIXES CRÍTICOS VERIFICADOS CORRECTAMENTE")
else:
    print(f"⚠️  {failed} verificación(es) fallaron — revisar los items ❌ arriba")
print("=" * 60)
