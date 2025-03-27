import os
import uuid
import mysql.connector
from cryptography.fernet import Fernet

# 📌 Ruta del archivo de la clave
KEY_FILE = "secret.key"

# 🔑 Generar clave solo si no existe
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    print("🔑 Clave generada y guardada en 'secret.key'")
else:
    print("✅ Clave ya existente, cargando...")

# 📌 Función para cargar la clave de encriptación
def load_key():
    """Carga la clave de encriptación desde el archivo."""
    if not os.path.exists(KEY_FILE):
        raise FileNotFoundError("❌ Archivo de clave no encontrado.")
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

# Cargar la clave
key = load_key()
cipher = Fernet(key)  # Crear el objeto de encriptación

# 📌 Configuración de conexión a la base de datos
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "4220",
    "database": "qr_chatbot"
}

def conectar_db():
    """Establece la conexión con la base de datos MySQL."""
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        return conexion
    except mysql.connector.Error as err:
        print(f"❌ Error al conectar a la base de datos: {err}")
        return None

def generar_id():
    """Genera un ID aleatorio único."""
    return str(uuid.uuid4())

def encriptar_id(user_id: str) -> str:
    """Encripta un ID de usuario."""
    return cipher.encrypt(user_id.encode()).decode()

def agregar_usuario_mysql(full_name: str, ocupation: str):
    """Inserta un usuario en la tabla 'users'."""
    conexion = conectar_db()
    if conexion is None:
        return False
    try:
        # 1️⃣ Generar y encriptar el ID
        user_id = generar_id()
        encrypted_id = encriptar_id(user_id)

        # 2️⃣ Insertar en la base de datos
        cursor = conexion.cursor()
        query = "INSERT INTO users (encrypted_id, full_name, ocupation) VALUES (%s, %s, %s)"
        values = (encrypted_id, full_name, ocupation)

        cursor.execute(query, values)
        conexion.commit()
        print("✅ Usuario agregado con éxito.")

    except mysql.connector.Error as err:
        print(f"❌ Error al insertar usuario: {err}")
    finally:
        cursor.close()
        conexion.close()

# 📌 Datos de prueba
usuario_prueba = {
    "FullName": "Juan Pérez",
    "Ocupation": "Estudiante"
}

# 🔥 Insertar usuario de prueba en la BD
agregar_usuario_mysql(usuario_prueba["FullName"], usuario_prueba["Ocupation"])
