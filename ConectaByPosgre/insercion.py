import json
from ConectaByPosgre.db_config import obtener_conexion



def insert_user(user_id,data):
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

def insert_car(car_id,owner_id,data):
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

def insert_belonging(belonging_id,owner_id,data):
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







