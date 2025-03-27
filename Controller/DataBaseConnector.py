import json

BELONGINGS_JSON = "/home/mario/Documents/ITE2025-1/Backend-1/CarLogBot/Data/belongings.json"
CARS_JSON = "/home/mario/Documents/ITE2025-1/Backend-1/CarLogBot/Data/cars.json"
MESSAGES_JSON = "/home/mario/Documents/ITE2025-1/Backend-1/CarLogBot/Data/messages.json"
USERS_JSON = "/home/mario/Documents/ITE2025-1/Backend-1/CarLogBot/Data/users.json"

def agregar_usuario_local(nuevo_objeto):
    #USERS_JSON = "./../Data/users.json"
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
<<<<<<< HEAD
# nuevo_dato = {
#     "nombre": "Juan",
#     "edad": 30,
#     "ocupacion": "Ingeniero"
# }
=======
#nuevo_dato = {
#    "nombre": "Ruben caballero",
#    "edad": 30,
#    "ocupacion": "IngenieroSmook"
#}

#agregar_usuario_local(nuevo_dato)
>>>>>>> dd3b1df (Agrego Conector_Mysql con onsercion a tabla users con id incriptado)
