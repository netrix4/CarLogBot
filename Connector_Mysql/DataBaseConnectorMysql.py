from cryptography.fernet import Fernet
import mysql.connector
import uuid  # Para generar IDs aleatorios únicos

#cargar clave de incriptacion
def load_key():
    with open("secret.key","rb") as key_file:
        return key_file.read()

# Cargar clave de encriptación
key = load_key()
cipher = Fernet(key)  # Crear el objeto de encriptación

# Configuración de conexión a la base de datos
DB_CONFIG = {
    "host": "localhost",      # Cambia esto si la BD está en otro servidor
    "user": "root",     # Tu usuario de MySQL
    "password": "",  # Tu contraseña de MySQL
    "database": "qr"  # Nombre de tu base de datos
}

def conectar_db():
    """Establece la conexión con la base de datos MySQL."""
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        return conexion
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

def generar_id():
    """Genera un ID aleatorio único."""
    return str(uuid.uuid4()) #genera un uuid como string

def encriptar_id(user_id:str)->str:
    """Encripta un ID de usuario"""
    return cipher.encrypt(user_id.encode()).decode()

def agregar_usuario_Mysql(full_name: str, ocupation: str):
    """Inserta un usuario en la tabla USERS."""
    conexion = conectar_db()
    if conexion is None:
        return
    try:
        """Generar un ID aleatorio, lo encriptamos y lo insertamos en MYSQL"""
        #1 Generar un ID unico
        user_id=generar_id()

        #2 encriptar el ID
        encrypted_id= encriptar_id(user_id)

        #3 insertar en la base de datos
        cursor = conexion.cursor()
        queryUsers = "INSERT INTO users (encrypted_id, full_name, ocupation ) VALUES (%s, %s, %s)"
        values=(encrypted_id,full_name,ocupation)

        cursor.execute(queryUsers,values)
        conexion.commit()

    except mysql.connector.Error as err:
        print(f"Error al insertar usuario: {err}")
    finally:
        cursor.close()
        conexion.close()


# Datos de prueba para insertar en la tabla 'users'
usuario_prueba = {
    "FullName": "Juan Pérez",
    "Ocupattion": "Estudiante"
}

# Llamar a la función para insertar en la base de datos
agregar_usuario_Mysql(usuario_prueba["FullName"],usuario_prueba["Ocupattion"])