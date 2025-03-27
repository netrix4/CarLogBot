# Módulo de conexión a la base de datos
import mysql.connector
# Configuración de conexión a la base de datos
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
        print(f"Error al conectar a la base de datos: {err}")
        return None
