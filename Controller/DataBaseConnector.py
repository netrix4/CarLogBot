"""import json

BELONGINGS_JSON = "/IA_BACKEND_1/CarLogBot/Data/belongings.json"
CARS_JSON = "/IA_BACKEND_1/CarLogBot/Data/cars.json"
MESSAGES_JSON = "/IA_BACKEND_1/CarLogBot/Data/messages.json"
USERS_JSON = "/IA_BACKEND_1/CarLogBot/Data/users.json"

def agregar_usuario_local(nuevo_objeto):
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

def agregar_belonging_local(nuevo_objeto):
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

def agregar_car_local(nuevo_objeto):
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

def agregar_mensaje_local(nuevo_objeto):
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

def get_messages_by_user_id(id_to_search):
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
def get_cars_by_user_id(id_to_search):
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
def get_belongings_by_user_id(id_to_search):
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


# Ejemplo de uso
# nuevo_dato = {
#     "nombre": "Juan",
#     "edad": 30,
#     "ocupacion": "Ingeniero"
# }
"""
