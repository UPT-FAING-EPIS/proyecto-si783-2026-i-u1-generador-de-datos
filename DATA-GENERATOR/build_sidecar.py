import subprocess
import sys

def build():
    print("Iniciando compilación del Sidecar...")
    try:
        import PyInstaller
    except ImportError:
        print("Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    print("Compilando con PyInstaller...")
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--name=cdcart-backend",
        "main.py"
    ]
    subprocess.check_call(cmd)
    print("Compilación finalizada con éxito. El ejecutable se encuentra en dist/cdcart-backend")

if __name__ == "__main__":
    build()
