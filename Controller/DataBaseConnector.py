import json

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

# Ejemplo de uso
# nuevo_dato = {
#     "nombre": "Juan",
#     "edad": 30,
#     "ocupacion": "Ingeniero"
# }

# agregar_usuario_local(nuevo_dato)
