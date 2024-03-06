import requests
from bs4 import BeautifulSoup

titulos=[]
descripciones=[]
list_fechas_convocatorias=[]
list_inicio=[]
list_fin=[]
convocantes=[]
destinatarios=[]
estados=[]
enlaces=[]
categorias=[]

ubu_general=[]



#Link para extraer data
link_UBU='https://www.ubu.es/trabaja-en-la-ubu'
#Para enviar una solicitud a la pagina y como resultado nos da una respuesta
response=requests.get(link_UBU)

#Comprobamos si la solicitud fue exitosa
if response.status_code == 200:
    #El response.text es para obtner el texto de esa respuesta/resultado que me envio la página
    #La variable soup es importante porque es la que nos va a permitir obtener elementos en una página web
    #El parser es lxml para obtener el código HTML de la respuesta obtenida.
    soup=BeautifulSoup(response.text, 'lxml')
    #Para obtener el código HTML con un buen formato utilizo el método prettify
    #print(soup.prettify())
    #Para buscar un elemento por su tag
    etiqueta_pagina = soup.find_all('div',class_='views-field views-field-field---last-application-date')
    
    for item in etiqueta_pagina:
        titulo=item.find('div',class_='field-content').get_text(strip=True)
        titulos.append(titulo)
        estado=item.find('div').get_text(strip=True)
        estados.append(estado)
        
        #PROCESO DE OBTENCIÓN DE SUBPÁGINA
        enlace_subpagina='https://www.ubu.es'+item.find('a')['href']
        enlaces.append(enlace_subpagina)
        respuesta_subpagina=requests.get(enlace_subpagina)
        #PROCESO DE OBTENCIÓN DE SUBPÁGINA
            
        if respuesta_subpagina.status_code==200:
                sub_soup=BeautifulSoup(respuesta_subpagina.text, 'lxml')
                contenedores_subpagina = sub_soup.find_all('article')
                
                for contenedor in contenedores_subpagina:
                    descripcion=contenedor.find('div',class_='field-item even',property='content:encoded').p.get_text(strip=True)
                    texto_limpio_descripcion = descripcion.replace('\xa0', ' ')
                    descripciones.append(texto_limpio_descripcion)
                    
                    fecha_convocatoria=contenedor.find('span', class_='date-display-single')['content']
                    list_fechas_convocatorias.append(fecha_convocatoria)
                    
                    
                    if str(contenedor.find('div', class_='field field-name-field-presentation-date field-type-datetime field-label-above').find('span')['class'])!="['date-display-single']":

                        
                        fecha_inicio_solicitud=contenedor.find('span', class_='date-display-start')['content']
                        list_inicio.append(fecha_inicio_solicitud)

                        fecha_fin_solicitud=contenedor.find('span', class_='date-display-end')['content']
                        list_fin.append(fecha_fin_solicitud)
                        
                    else:
                        list_inicio.append('No Especificada')
                        fecha_fin_solicitud=contenedor.find('div',class_='field field-name-field-presentation-date field-type-datetime field-label-above').find('span', class_='date-display-single')['content']
                        list_fin.append(fecha_fin_solicitud)
                    
                    if contenedor.find('div',class_='field field-name-field-receiver field-type-text-long field-label-above') != None:
                        contenedor_destinatarios=contenedor.find('div',class_='field field-name-field-receiver field-type-text-long field-label-above').find('div',class_='field-item even').get_text(strip=True)
                        destinatarios.append(contenedor_destinatarios)
                    else:
                        destinatarios.append('No se han encontrado destinatarios')
                    
                    categoria=contenedor.find('div',class_='field-item odd').a.get_text(strip=True)
                    
                    if categoria=='Convocatorias personal docente' or categoria=='Investigación: adscritas a proyectos':
                        categorias.append('PDI')
                    elif categoria=='Convocatorias PAS':
                        categorias.append('PAS')
                    else:
                        categorias.append('No especificada')
                    
        else:
            print(f'La solicitud ha fallado y su código de estado es el {respuesta_subpagina.status_code}')        

else: 
    print(f'La solicitud ha fallado y su código de estado es el {response.status_code}')
    


print(len(titulos))
print(len(descripciones))
print(len(list_fechas_convocatorias))
print(len(list_inicio))
print(len(list_fin))
print(len(destinatarios))
print(len(estados))
print(len(enlaces))
print(len(categorias))




ubu_general.append(titulos)
ubu_general.append(descripciones)
ubu_general.append(list_fechas_convocatorias)
ubu_general.append(list_inicio)
ubu_general.append(list_fin)
ubu_general.append(destinatarios)
ubu_general.append(estados)
ubu_general.append(enlaces)
ubu_general.append(categorias)

for i in range(len(titulos)):
    convocantes.append('Universidad de Burgos')

ubu_general.append(convocantes)
print('***************************************************************')

print(ubu_general)
