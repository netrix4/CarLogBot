from db_config import obtener_conexion


def get_car_by_user(owner_id):
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

def get_belonging_by_user(owner_id):
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


##consultas manuales: **********************************TEST AREA************************
"""
user_id = 1001

carros = get_car_by_user(user_id)
#print("Carros del usuario:", carros)

pertenencias = get_belonging_by_user(user_id)
print("Pertenencias del usuario:", pertenencias)
"""