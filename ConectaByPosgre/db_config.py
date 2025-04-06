# archivoConectar.py
import psycopg2

DB_PARAMS = {
    "dbname": "db_telegrambot",
    "user": "postgres", #your user
    "password": "", #your password
    "host": "localhost",
    "port": "5432"
}
def obtener_conexion():
    """ Devuelve una conexión activa a la base de datos. """
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        return conn
    except Exception as e:
        print("Error de conexión:", e)
        return None

