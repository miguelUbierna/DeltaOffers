import requests
from bs4 import BeautifulSoup
from datetime import datetime

list_fechas_convocatorias = []
titulos = []
enlaces = []
categorias = []
tipos = []
list_inicio = []
list_fin = []
convocantes = []
nombre_plazas = []
convocatorias_asociadas = []
estados = []
descripciones = []
documentos_adjuntos = []


ule_general = []


def determinar_plazo(fecha_fin):
    fecha_actual = datetime.now()

    fecha_fin_convertida = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M:%SZ')

    if fecha_fin_convertida > fecha_actual:
        estados.append('EN PLAZO')
    else:
        estados.append('CONVOCATORIA CERRADA')


def obtener_datos(link_ule):
    response = requests.get(link_ule)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')

        etiqueta_pagina = soup.find_all(
            'td', class_='views-field views-field-created views-field-title')

        for item in etiqueta_pagina:

            fechas_publicacion = item.find(
                'div', class_='list-datetime bold uppercase font-green-jungle list-datetime-list').get_text(strip=True)
            list_fechas_convocatorias.append(fechas_publicacion)

            titulo = item.find(
                'div', class_='list-item-content').get_text(strip=True)
            titulos.append(titulo)

            enlace_subpagina = 'https://www.unileon.es'+item.find('a')['href']
            enlaces.append(enlace_subpagina)

            respuesta_subpagina = requests.get(enlace_subpagina)

            if respuesta_subpagina.status_code == 200:
                sub_soup = BeautifulSoup(respuesta_subpagina.text, 'lxml')

                if sub_soup.find('div', class_='field field--name-field-announcement-target field--type-list-string field--label-above') == None:
                    categorias.append('GENERAL')
                elif 'General' == sub_soup.find('div', class_='field field--name-field-announcement-target field--type-list-string field--label-above').find('div', class_='field--item').get_text(strip=True):
                    categorias.append('GENERAL')
                elif 'P.A.S. Laboral' == sub_soup.find('div', class_='field field--name-field-announcement-target field--type-list-string field--label-above').find('div', class_='field--item').get_text(strip=True):
                    categorias.append('PAS')
                else:
                    categorias.append('GENERAL')

                if sub_soup.find('div', class_='field field--name-field-type field--type-list-string field--label-above') == None:
                    tipos.append('No especificado')
                else:
                    tipo = sub_soup.find('div', class_='field field--name-field-type field--type-list-string field--label-above').find(
                        'div', class_='field--item').get_text(strip=True)
                    tipos.append(tipo)

                fecha_inicio_solicitud = sub_soup.find(
                    'div', class_='field field--name-field-announcement-date field--type-datetime field--label-above').find('time')['datetime']
                list_inicio.append(fecha_inicio_solicitud)

                fecha_fin_solicitud = sub_soup.find(
                    'div', class_='field field--name-field-announcement-deadline field--type-datetime field--label-above').find('time')['datetime']
                list_fin.append(fecha_fin_solicitud)

                determinar_plazo(fecha_fin_solicitud)

                if None == sub_soup.find('div', class_='field field--name-field-positions field--type-string-long field--label-above'):
                    nombre_plazas.append('No especificado')
                else:
                    nombre_plaza = sub_soup.find('div', class_='field field--name-field-positions field--type-string-long field--label-above').find(
                        'div', class_='field--item').get_text(strip=True)
                    nombre_plazas.append(nombre_plaza)

                if sub_soup.find('div', class_='field field--name-field-associated-announcement field--type-string-long field--label-above') == None:
                    convocatorias_asociadas.append('No especificado')
                else:
                    conv_asociada = sub_soup.find('div', class_='field field--name-field-associated-announcement field--type-string-long field--label-above').find(
                        'div', class_='field--item').get_text(strip=True)
                    convocatorias_asociadas.append(conv_asociada)

                if sub_soup.find('div', class_='field field--name-body field--type-text-with-summary field--label-hidden field--item') == None:
                    descripciones.append('No especificado')
                else:
                    descripcion = sub_soup.find(
                        'div', class_='field field--name-body field--type-text-with-summary field--label-hidden field--item').get_text(strip=True)
                    descripciones.append(descripcion)

                documento = ' '
                if sub_soup.find('div', class_='field field--name-upload field--type-file field--label-hidden field--items') == None:
                    documentos_adjuntos.append('No hay documentos adjuntos')
                else:
                    lista_documentos = sub_soup.find(
                        'div', class_='field field--name-upload field--type-file field--label-hidden field--items').find_all('span', class_='file-link')

                    for item in lista_documentos:
                        documento += item.get_text(strip=True) + ' '
                    documentos_adjuntos.append(documento)


def extraer_datos_paginas():
    contador_paginas = 0
    # Link para extraer los datos.
    link_ule = 'https://www.unileon.es/actualidad/convocatorias'
    while contador_paginas < 4:
        if contador_paginas == 0:
            obtener_datos(link_ule)
        else:
            link_ule_siguientes_paginas = 'https://www.unileon.es/actualidad/convocatorias?page=' + \
                str(contador_paginas)
            obtener_datos(link_ule_siguientes_paginas)
            link_ule_siguientes_paginas = ''
        contador_paginas += 1


extraer_datos_paginas()

for i in range(len(titulos)):
    convocantes.append('Universidad de León')

'''
print(list_fechas_convocatorias)
print(titulos)
print(enlaces)
print(categorias)
print(tipos)
print(list_inicio)
print(list_fin)
print(convocantes)
print(nombre_plazas)
print(convocatorias_asociadas)
print(estados)

print(len(list_fechas_convocatorias))
print(len(titulos))
print(len(enlaces))
print(len(categorias))
print(len(tipos))
print(len(list_inicio))
print(len(list_fin))
print(len(convocantes))
print(len(nombre_plazas))
print(len(convocatorias_asociadas))
print(len(estados))


print(list_fechas_convocatorias[0])
print(titulos[0])
print(enlaces[0])
print(categorias[0])
print(tipos[0])
print(list_inicio[0])
print(list_fin[0])
print(convocantes[0])
print(nombre_plazas[0])
print(convocatorias_asociadas[0])
print(estados[0])
'''


for item in titulos:
    print(item)

print('*************************')
for item in convocatorias_asociadas:
    print(item)

print('*************************')
for item in descripciones:
    print(item)

print('*************************')
print(estados)

print('*************************')
print('*************************')
print('*************************')

for item in documentos_adjuntos:
    print(item)
