import random
from faker import Faker
import psycopg2
from datetime import timedelta

fake = Faker('es')  # Generar datos realistas para Perú

# Conectar a PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Estados civiles válidos
estados_civiles = ['soltero', 'casado', 'conviviente', 'divorciado', 'viudo']

# Generar pacientes
dni_usados = set()
for _ in range(10):  # Cambia el número según la cantidad que necesites
    while True:
        dni = str(fake.unique.random_number(digits=8))
        if len(dni) == 8 and dni not in dni_usados:
            dni_usados.add(dni)
            break

    nombres = fake.first_name()
    apellidos = fake.last_name()
    nacimiento = fake.date_of_birth(minimum_age=18, maximum_age=90)
    lugar_nacimiento = fake.city()
    estado_civil = random.choice(estados_civiles)
    direccion = fake.address().replace("\n", ", ")
    telefono = str(fake.random_number(digits=9))
    while len(telefono) != 9:
        telefono = str(fake.random_number(digits=9))
    email = fake.email()
    ocupacion = fake.job()
    lugar_trabajo_estudio = fake.company()
    apoderado = fake.name()
    novedades = fake.sentence()

    cur.execute("""
        INSERT INTO paciente (
            paciente_dni, nombres, apellidos, fecha_de_nacimiento, lugar_de_nacimiento, 
            estado_civil, direccion, telefono, email, ocupacion, 
            lugar_trabajo_estudio, apoderado, novedades
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        str(dni), nombres, apellidos, nacimiento, lugar_nacimiento,
        estado_civil, direccion, str(telefono), email, ocupacion,
        lugar_trabajo_estudio, apoderado, novedades
    ))

    # Crear historia clínica relacionada
    fecha_creacion = fake.date_between(start_date='-2y', end_date='today')
    cur.execute("""
        INSERT INTO historia_clinica (fecha_creacion, paciente_dni)
        VALUES (%s, %s)
        RETURNING historia_clinica_id
    """, (fecha_creacion, str(dni)))
    historia_clinica_id = cur.fetchone()[0]

    # Puedes continuar aquí generando datos en otras tablas relacionadas usando este ID
    # Ejemplo: insertar antecedentes médicos, tratamientos, etc.

conn.commit()
cur.close()
conn.close()
