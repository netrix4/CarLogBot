import json

BELONGINGS_JSON = "./Data/belongings.json"
CARS_JSON = "./Data/cars.json"
MESSAGES_JSON = "./Data/messages.json"
USERS_JSON = "./Data/users.json"

def agregar_usuario_local(nuevo_objeto):
    # USERS_JSON = "./../Data/users.json"
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

# Ejemplo de uso
# nuevo_dato = {
#     "nombre": "Juan",
#     "edad": 30,
#     "ocupacion": "Ingeniero"
# }
