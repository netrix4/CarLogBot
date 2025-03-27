from user import agregar_usuario

# Datos de prueba para insertar en la tabla 'users'
usuario_prueba = {
    "FullName": "Ruben caballero",
    "Ocupation": "smooker"
}

# Llamar a la función para insertar en la base de datos
agregar_usuario(usuario_prueba["FullName"], usuario_prueba["Ocupation"])
