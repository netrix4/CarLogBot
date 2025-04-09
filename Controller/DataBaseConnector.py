import json
from Utils.db_config import obtener_conexion

BELONGINGS_JSON = "/home/mario/Documents/ITE2025-1/Backend-1/CarLogBot/Data/belongings.json"
CARS_JSON = "/home/mario/Documents/ITE2025-1/Backend-1/CarLogBot/Data/cars.json"
MESSAGES_JSON = "/home/mario/Documents/ITE2025-1/Backend-1/CarLogBot/Data/messages.json"
USERS_JSON = "/home/mario/Documents/ITE2025-1/Backend-1/CarLogBot/Data/users.json"

def insert_user_local(nuevo_objeto):
    try:
        with open(USERS_JSON, "r", encoding="utf-8") as archivo:
            try:
                datos = json.load(archivo)
                if not isinstance(datos, list):
                    datos = [datos]
            except json.JSONDecodeError:
                datos = []

    except FileNotFoundError:
        datos = []

    datos.append(nuevo_objeto)

    with open(USERS_JSON, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

    print("Objeto agregado correctamente.")

def insert_belonging_local(nuevo_objeto):
    try:
        with open(BELONGINGS_JSON, "r", encoding="utf-8") as archivo:
            try:
                datos = json.load(archivo)
                if not isinstance(datos, list):
                    datos = [datos]
            except json.JSONDecodeError:
                datos = []

    except FileNotFoundError:
        datos = []

    datos.append(nuevo_objeto)

    with open(BELONGINGS_JSON, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

    print("Pertenencia agregada correctamente.")

def insert_car_local(nuevo_objeto):
    try:
        with open(CARS_JSON, "r", encoding="utf-8") as archivo:
            try:
                datos = json.load(archivo)
                if not isinstance(datos, list):
                    datos = [datos]
            except json.JSONDecodeError:
                datos = []

    except FileNotFoundError:
        datos = []

    datos.append(nuevo_objeto)

    with open(CARS_JSON, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

    print("Carro agregado correctamente.")

def insert_message_local(nuevo_objeto):
    try:
        with open(MESSAGES_JSON, "r", encoding="utf-8") as archivo:
            try:
                datos = json.load(archivo)
                if not isinstance(datos, list):
                    datos = [datos]
            except json.JSONDecodeError:
                datos = []

    except FileNotFoundError:
        datos = []

    datos.append(nuevo_objeto)

    with open(MESSAGES_JSON, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

    print("Mensaje agregado correctamente.")

def get_messages_by_user_id_local(id_to_search):
    try:
        with open(MESSAGES_JSON, "r", encoding="utf-8") as archivo:
            try:
                datos = json.load(archivo)
                if not isinstance(datos, list):
                    datos = [datos]
            except json.JSONDecodeError:
                datos = []
    except FileNotFoundError:
        datos = []
    results = []
    for message in datos:
        if message["ReceiverId"] == id_to_search:
            results.append(message)

    return results
def get_cars_by_user_id_local(id_to_search):
    try:
        with open(CARS_JSON, "r", encoding="utf-8") as archivo:
            try:
                datos = json.load(archivo)
                if not isinstance(datos, list):
                    datos = [datos]
            except json.JSONDecodeError:
                datos = []
    except FileNotFoundError:
        datos = []
    results = []
    for car in datos:
        if car["OwnerId"] == id_to_search:
            results.append(car)

    return results
def get_belongings_by_user_id_local(id_to_search):
    try:
        with open(BELONGINGS_JSON, "r", encoding="utf-8") as archivo:
            try:
                datos = json.load(archivo)
                if not isinstance(datos, list):
                    datos = [datos]
            except json.JSONDecodeError:
                datos = []
    except FileNotFoundError:
        datos = []
    results = []
    for belonging in datos:
        if belonging["OwnerId"] == id_to_search:
            results.append(belonging)

    return results

def get_car_by_user_postgres(owner_id):
    conn= obtener_conexion()
    if conn is None:
        print("No se pudo establecer conexión con la base de datos.")
        return
    cursor = conn.cursor()
    query = "SELECT data FROM cars WHERE owner_id = %s;"
    cursor.execute(query, (owner_id,))
    results = [(row[0]) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    print("¡  YA SE HIZO  !")
    return results

def get_belonging_by_user_postgres(owner_id):
    conn= obtener_conexion()
    if conn is None:
        print("No se pudo establecer conexión con la base de datos.")
        return
    cursor = conn.cursor()
    query = "SELECT data FROM belongings WHERE owner_id = %s;"
    cursor.execute(query, (owner_id,))
    results = [(row[0]) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    print("¡  YA SE HIZO  !")
    return results

def insert_user_postgres(user_id,data):
    conn=obtener_conexion()
    if conn is None:
        print("No se pudo establecer conexión con la base de datos.")
        return
    cursor = conn.cursor()
    print(f"Insertando: ID={user_id}, Data={json.dumps(data)}")
    query="INSERT INTO users(id, data) values(%s,%s)"
    cursor.execute(query,(user_id,json.dumps(data)))
    conn.commit()
    cursor.close()
    print("¡  YA SE HIZO  !")

def insert_car_postgres(car_id,owner_id,data):
    conn=obtener_conexion()
    if conn is None:
        print("No se pudo establecer conexión con la base de datos.")
        return
    cursor=conn.cursor()
    
    print(f"Insertando: ID={car_id}, OwnerID={owner_id}, Data={json.dumps(data)}")

    query="INSERT INTO cars(id,owner_id,data) VALUES(%s,%s,%s);"
    cursor.execute(query,(car_id,owner_id,json.dumps(data)))
    conn.commit()
    cursor.close()
    conn.close()
    print(" YA SE HIZO  !")

def insert_belonging_postgres(belonging_id,owner_id,data):
    conn= obtener_conexion()
    if conn is None:
        print("No se pudo establecer conexión con la base de datos.")
        return
    cursor=conn.cursor()

    print(f"Insertando: ID={belonging_id}, OwnerID={owner_id}, Data={json.dumps(data)}")

    query="INSERT INTO belongings(id, owner_id, data) VALUES (%s, %s, %s);"
    cursor.execute(query,(belonging_id,owner_id,json.dumps(data)))
    conn.commit()
    cursor.close()
    conn.close()
    print("¡  YA SE HIZO  !")


# Ejemplo de uso
# nuevo_dato = {
#     "nombre": "Juan",
#     "edad": 30,
#     "ocupacion": "Ingeniero"
# }
