import requests
from bs4 import BeautifulSoup
from datetime import datetime



titulos=[]
list_fechas_convocatorias=[]
list_inicio=[]
list_fin=[]
convocantes=[]
nombre_plazas=[]
estados=[]
enlaces=[]
categorias=[]

ule_general=[]

def determinar_plazo (fecha_fin):
    fecha_actual=datetime.now()

    fecha_fin_convertida = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M:%SZ')

    if fecha_fin_convertida > fecha_actual:
        estados.append('EN PLAZO')
    else:
        estados.append('CONVOCATORIA CERRADA')


link_ULE='https://www.unileon.es/actualidad/convocatorias'

response=requests.get(link_ULE)

if response.status_code == 200:
    soup=BeautifulSoup(response.text, 'lxml')

    etiqueta_pagina=soup.find_all('td',class_='views-field views-field-created views-field-title')

    for item in etiqueta_pagina:
       
        fechas_publicacion=item.find('div',class_='list-datetime bold uppercase font-green-jungle list-datetime-list').get_text(strip=True)
        list_fechas_convocatorias.append(fechas_publicacion)

        titulo=item.find('div',class_='list-item-content').get_text(strip=True)
        titulos.append(titulo)
        
        enlace_subpagina='https://www.unileon.es'+item.find('a')['href']
        enlaces.append(enlace_subpagina)

        respuesta_subpagina=requests.get(enlace_subpagina)

        if respuesta_subpagina.status_code==200:
            sub_soup=BeautifulSoup(respuesta_subpagina.text, 'lxml')

            if sub_soup.find('div',class_='field field--name-field-announcement-target field--type-list-string field--label-above') == None:
                categorias.append('GENERAL')
            elif 'General'==sub_soup.find('div',class_='field field--name-field-announcement-target field--type-list-string field--label-above').find('div', class_='field--item').get_text(strip=True):
                categorias.append('GENERAL')
            elif 'P.A.S. Laboral'==sub_soup.find('div',class_='field field--name-field-announcement-target field--type-list-string field--label-above').find('div', class_='field--item').get_text(strip=True):
                categorias.append('PAS')
            else:
                categorias.append('GENERAL')

            fecha_inicio_solicitud=sub_soup.find('div', class_='field field--name-field-announcement-date field--type-datetime field--label-above').find('time')['datetime']
            list_inicio.append(fecha_inicio_solicitud)

            fecha_fin_solicitud=sub_soup.find('div', class_='field field--name-field-announcement-deadline field--type-datetime field--label-above').find('time')['datetime']
            list_fin.append(fecha_fin_solicitud)

            determinar_plazo(fecha_fin_solicitud)



            if None == sub_soup.find('div',class_='field field--name-field-positions field--type-string-long field--label-above'):
                nombre_plazas.append('No especificado')
            else:
                nombre_plaza=sub_soup.find('div',class_='field field--name-field-positions field--type-string-long field--label-above').find('div',class_='field--item').get_text(strip=True)
                nombre_plazas.append(nombre_plaza)



for i in range(len(titulos)):
    convocantes.append('Universidad de León')

print(titulos)
print(list_fechas_convocatorias)
print(enlaces)
print(categorias)
print(list_inicio)
print(list_fin)
print(convocantes)
print(nombre_plazas)
print(estados)


print(len(titulos))
print(len(list_fechas_convocatorias))
print(len(enlaces))
print(len(categorias))
print(len(list_inicio))
print(len(list_fin))
print(len(convocantes))
print(len(nombre_plazas))
print(len(estados))

print(titulos[0])
print(list_fechas_convocatorias[0])
print(enlaces[0])
print(categorias[0])
print(list_inicio[0])
print(list_fin[0])
print(convocantes[0])
print(nombre_plazas[0])
print(estados[0])


