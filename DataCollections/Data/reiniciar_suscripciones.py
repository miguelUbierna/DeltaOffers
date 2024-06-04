import mysql.connector

conexion = mysql.connector.connect(
    host="delta-offers.mysql.database.azure.com",
    user="deltaadmin",
    password="Offers2002",
    database="convocatoriasdb"
)

cursor = conexion.cursor()

# Elimino todo el contenido actual de la tabla
update = "UPDATE suscripciones SET num_avisos = 0"

cursor.execute(update)
conexion.commit()
cursor.close()
conexion.close()
