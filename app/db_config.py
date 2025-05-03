import psycopg2

def obtener_conexion():
    # Parámetros de conexión
    host = "localhost"  # Dirección de tu servidor PostgreSQL
    dbname = "DENTWARE_BD"  # Nombre de tu base de datos
    user = "postgres"  # Tu usuario de PostgreSQL
    password = "ABCD1234"  # Tu contraseña de PostgreSQL

    # Conectar a la base de datos
    try:
        connection = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password
        )
        return connection
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None
