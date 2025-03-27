#encryption.py - Módulo para la encriptación y desencriptación
from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"

def generate_key():
    """Genera y guarda la clave de encriptación si no existe."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        print("🔑 Clave generada y guardada en 'secret.key'")
    else:
        print("✅ Clave ya existente, cargando...")

def load_key():
    """Carga la clave de encriptación desde el archivo."""
    if not os.path.exists(KEY_FILE):
        raise FileNotFoundError("❌ Archivo de clave no encontrado.")
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

# Inicialización
generate_key()
key = load_key()
cipher = Fernet(key)

def encriptar_id(user_id: str) -> str:
    """Encripta un ID de usuario."""
    return cipher.encrypt(user_id.encode()).decode()

def desencriptar_id(encrypted_id: str) -> str:
    """Desencripta un ID de usuario."""
    return cipher.decrypt(encrypted_id.encode()).decode()
