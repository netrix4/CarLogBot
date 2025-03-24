import json

MESSAGES_JSON = "../Data/messages.json"
USERS_JSON = "../Data/users.json"

def agregar_a_json(archivo_json, nuevo_objeto):
    try:
        # Intenta abrir el archivo y leer los datos existentes
        with open(archivo_json, "r", encoding="utf-8") as archivo:
            try:
                datos = json.load(archivo)  # Cargar el JSON existente
                if not isinstance(datos, list):  # Asegurar que sea una lista
                    datos = [datos]
            except json.JSONDecodeError:
                datos = []  # Si el archivo está vacío o mal formado, iniciamos con una lista vacía

    except FileNotFoundError:
        datos = []  # Si el archivo no existe, creamos una nueva lista

    # Agregar el nuevo objeto a la lista
    datos.append(nuevo_objeto)

    # Guardar la lista actualizada en el archivo JSON
    with open(archivo_json, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

    print("Objeto agregado correctamente.")

# Ejemplo de uso
nuevo_dato = {
    "nombre": "Juan",
    "edad": 30,
    "ocupacion": "Ingeniero"
}

agregar_a_json("datos.json", nuevo_dato)
