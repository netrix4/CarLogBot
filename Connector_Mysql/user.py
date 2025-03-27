#user.py - Módulo para la gestión de usuarios
import uuid
import mysql.connector  # Agregar esta línea para manejar la base de datos
from db import conectar_db
from encryption import encriptar_id

def generar_id():
    """Genera un ID aleatorio único."""
    return str(uuid.uuid4())

def agregar_usuario(full_name: str, ocupation: str):
    """Inserta un usuario en la tabla USERS."""
    conexion = conectar_db()
    if conexion is None:
        return False
    try:
        user_id = generar_id()  # Generar un ID único
        encrypted_id = encriptar_id(user_id)  # Encriptar el ID

        # Insertar en la base de datos
        cursor = conexion.cursor()
        query = "INSERT INTO users (encrypted_id, full_name, ocupation) VALUES (%s, %s, %s)"
        cursor.execute(query, (encrypted_id, full_name, ocupation))
        conexion.commit()
        print("✅ Usuario agregado correctamente.")

    except mysql.connector.Error as err:
        print(f"Error al insertar usuario: {err}")
    finally:
        cursor.close()
        conexion.close()
