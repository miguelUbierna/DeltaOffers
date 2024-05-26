import sys
import mysql.connector
from datetime import datetime
from PIL import Image


sys.path.append('C:\\Users\\Usuario\\Desktop\\DeltaOffers\\DataCollections')

from Scrapers.ScrapingUBU.scrapingUBU import UBUScraper  # nopep8
from Scrapers.ScrapingULE.scrapingULE import ULEScraper  # nopep8
from Scrapers.ScrapingUVA.scrapingUVA import UVAScraper  # nopep8


scraperUBU = UBUScraper()
scraperUBU.extraer_datos_paginas()
scraperUBU.tabla_limpia()
print(scraperUBU.ubu_general)
print(len(scraperUBU.ubu_general))
print(len(scraperUBU.ubu_general[0]))


scraperULE = ULEScraper()
scraperULE.extraer_datos_paginas()
scraperULE.tabla_limpia()
print(scraperULE.ule_general)
print(len(scraperULE.ule_general))
print(len(scraperULE.ule_general[0]))


link_uva_PDI = 'https://pdi.uva.es/1.convocatorias/index.html'
scraperPDI = UVAScraper(link_uva_PDI)
scraperPDI.obtener_datos()

print(scraperPDI.uva_general)
print(len(scraperPDI.uva_general))
print(len(scraperPDI.uva_general[0]))
print('************************')
print('************************')
print('************************')


link_UVA_PAS = 'https://pas.uva.es/1.convocatorias/'
scraperPAS = UVAScraper(link_UVA_PAS)
scraperPAS.obtener_datos()


print(scraperPAS.uva_general)
print(len(scraperPAS.uva_general))
print(len(scraperPAS.uva_general[0]))


conexion = mysql.connector.connect(
    host="delta-offers.mysql.database.azure.com",
    user="deltaadmin",
    password="Offers2002",
    database="convocatoriasdb"
)

cursor = conexion.cursor()

# Elimino todo el contenido actual de la tabla
delete = "DELETE FROM universidades"
cursor.execute(delete)

# Cambia la ruta a la ubicación de tu imagen
ruta_imagen = 'Images/ubuLogo.jpg'
with open(ruta_imagen, 'rb') as f:
    logo_ubu = f.read()

for fila in scraperUBU.ubu_general:
    if fila[4] == 'No especificada' and fila[5] == 'No especificada':

        fecha_fin = datetime.strptime(fila[6], "%Y-%m-%d").date()

        insert = "INSERT INTO universidades (titulo, plazo, enlace, descripcion,fecha_public,fecha_ini,fecha_fin,convocante,destinatarios,categoria,universidad,imagen_logo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        datos = (fila[0], fila[1], fila[2], fila[3], None, None,
                 fecha_fin, fila[7], fila[8], fila[9], fila[10], logo_ubu)
        cursor.execute(insert, datos)

    elif fila[4] != 'No especificada' and fila[5] == 'No especificada':

        fecha_publi = datetime.strptime(fila[4], "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(fila[6], "%Y-%m-%d").date()

        insert = "INSERT INTO universidades (titulo, plazo, enlace, descripcion,fecha_public,fecha_ini,fecha_fin,convocante,destinatarios,categoria,universidad,imagen_logo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        datos = (fila[0], fila[1], fila[2], fila[3], fecha_publi, None,
                 fecha_fin, fila[7], fila[8], fila[9], fila[10], logo_ubu)
        cursor.execute(insert, datos)

    elif fila[4] == 'No especificada' and fila[5] != 'No especificada':
        fecha_ini = datetime.strptime(fila[5], "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(fila[6], "%Y-%m-%d").date()

        insert = "INSERT INTO universidades (titulo, plazo, enlace, descripcion,fecha_public,fecha_ini,fecha_fin,convocante,destinatarios,categoria,universidad,imagen_logo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        datos = (fila[0], fila[1], fila[2], fila[3], None, fecha_ini,
                 fecha_fin, fila[7], fila[8], fila[9], fila[10], logo_ubu)
        cursor.execute(insert, datos)
    else:
        fecha_publi = datetime.strptime(fila[4], "%Y-%m-%d").date()
        fecha_ini = datetime.strptime(fila[5], "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(fila[6], "%Y-%m-%d").date()

        insert = "INSERT INTO universidades (titulo, plazo, enlace, descripcion,fecha_public,fecha_ini,fecha_fin,convocante,destinatarios,categoria,universidad,imagen_logo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        datos = (fila[0], fila[1], fila[2], fila[3], fecha_publi, fecha_ini,
                 fecha_fin, fila[7], fila[8], fila[9], fila[10], logo_ubu)
        cursor.execute(insert, datos)


ruta_imagen = 'Images/uleLogo.jpg'
with open(ruta_imagen, 'rb') as f:
    logo_ule = f.read()

for fila in scraperULE.ule_general:

    insert = "INSERT INTO universidades (titulo, enlace,fecha_public,categoria,tipo,fecha_ini,fecha_fin,plazo,nombre_plaza,convocatoria_asociada,descripcion,universidad,imagen_logo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    datos = (fila[0], fila[1], fila[2], fila[3], fila[4], fila[5],
             fila[6], fila[7], fila[8], fila[9], fila[10], fila[11], logo_ule)
    cursor.execute(insert, datos)

ruta_imagen = 'Images/uvaLogo.jpg'
with open(ruta_imagen, 'rb') as f:
    logo_uva = f.read()

for fila in scraperPDI.uva_general:
    if fila[1] == 'No especificado' and fila[2] == 'No especificado':

        insert = "INSERT INTO universidades (titulo, fecha_ini, fecha_fin, plazo,enlace,clasificacion,tipo,universidad,categoria,imagen_logo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        datos = (fila[0], None, None,
                 fila[3], fila[4], fila[5], fila[6], fila[7], fila[8], logo_uva)
        cursor.execute(insert, datos)
    elif fila[1] == 'No especificado' and fila[2] != 'No especificado':

        fecha_fin = datetime.strptime(fila[2], "%Y-%m-%d").date()
        insert = "INSERT INTO universidades (titulo, fecha_ini, fecha_fin, plazo,enlace,clasificacion,tipo,universidad,categoria,imagen_logo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        datos = (fila[0], None, fecha_fin,
                 fila[3], fila[4], fila[5], fila[6], fila[7], fila[8], logo_uva)
        cursor.execute(insert, datos)

    elif fila[1] != 'No especificado' and fila[2] == 'No especificado':
        fecha_ini = datetime.strptime(fila[1], "%Y-%m-%d").date()
        insert = "INSERT INTO universidades (titulo, fecha_ini, fecha_fin, plazo,enlace,clasificacion,tipo,universidad,categoria,imagen_logo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        datos = (fila[0], fecha_ini, None,
                 fila[3], fila[4], fila[5], fila[6], fila[7], fila[8], logo_uva)
        cursor.execute(insert, datos)
    else:
        fecha_ini = datetime.strptime(fila[1], "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(fila[2], "%Y-%m-%d").date()
        insert = "INSERT INTO universidades (titulo, fecha_ini, fecha_fin, plazo,enlace,clasificacion,tipo,universidad,categoria,imagen_logo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        datos = (fila[0], fecha_ini, fecha_fin,
                 fila[3], fila[4], fila[5], fila[6], fila[7], fila[8], logo_uva)
        cursor.execute(insert, datos)


for fila in scraperPAS.uva_general:
    if fila[1] == 'No especificado' and fila[2] == 'No especificado':

        insert = "INSERT INTO universidades (titulo, fecha_ini, fecha_fin, plazo,enlace,clasificacion,tipo,universidad,categoria,imagen_logo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        datos = (fila[0], None, None,
                 fila[3], fila[4], fila[5], fila[6], fila[7], fila[8], logo_uva)
        cursor.execute(insert, datos)
    elif fila[1] == 'No especificado' and fila[2] != 'No especificado':

        fecha_fin = datetime.strptime(fila[2], "%Y-%m-%d").date()
        insert = "INSERT INTO universidades (titulo, fecha_ini, fecha_fin, plazo,enlace,clasificacion,tipo,universidad,categoria,imagen_logo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        datos = (fila[0], None, fecha_fin,
                 fila[3], fila[4], fila[5], fila[6], fila[7], fila[8], logo_uva)
        cursor.execute(insert, datos)

    elif fila[1] != 'No especificado' and fila[2] == 'No especificado':
        fecha_ini = datetime.strptime(fila[1], "%Y-%m-%d").date()
        insert = "INSERT INTO universidades (titulo, fecha_ini, fecha_fin, plazo,enlace,clasificacion,tipo,universidad,categoria,imagen_logo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        datos = (fila[0], fecha_ini, None,
                 fila[3], fila[4], fila[5], fila[6], fila[7], fila[8], logo_uva)
        cursor.execute(insert, datos)
    else:
        fecha_ini = datetime.strptime(fila[1], "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(fila[2], "%Y-%m-%d").date()
        insert = "INSERT INTO universidades (titulo, fecha_ini, fecha_fin, plazo,enlace,clasificacion,tipo,universidad,categoria,imagen_logo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        datos = (fila[0], fecha_ini, fecha_fin,
                 fila[3], fila[4], fila[5], fila[6], fila[7], fila[8], logo_uva)
        cursor.execute(insert, datos)


conexion.commit()
cursor.close()
conexion.close()
