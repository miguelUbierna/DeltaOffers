import requests
from bs4 import BeautifulSoup

titulos=[]
list_fechas_convocatorias=[]
categorias=[]
emisores=[]
enlaces=[]
convocante=[]
descripciones=[]


link_USAL='https://sede.usal.es/tablon/buscar/?title=&description=&categories=2&status=effective&fecha_ini=&fecha_fin='

response=requests.get(link_USAL)

if response.status_code == 200:
    soup=BeautifulSoup(response.text, 'lxml')

    etiqueta_pagina=soup.find('tbody')

    etiquetas_titulo=etiqueta_pagina.find_all('td',class_='title')

    
    etiquetas_fecha=etiqueta_pagina.find_all('td',class_='publication_date')

    for item in etiquetas_fecha:
        fecha_publi=item.get_text(strip=True)
        list_fechas_convocatorias.append(fecha_publi)

    for item in etiquetas_titulo:
        titulo=item.find('a').get_text(strip=True)
        titulos.append(titulo)

        enlace_subpagina= 'https://sede.usal.es'+ item.find('a')['href']
        enlaces.append(enlace_subpagina)

    
        respuesta_subpagina=requests.get(enlace_subpagina)
        
        if respuesta_subpagina.status_code==200:
            sub_soup=BeautifulSoup(respuesta_subpagina.text, 'lxml')

            list_items= sub_soup.find_all('li', class_='list-group-item')

            for contador,item in zip(range(len(list_items)),list_items):
                if contador==0 :
                    if 'Personal Técnico, de Gestión y de Administración y Servicios'== item.find('span').find('span').get_text(strip=True):
                        categorias.append('PAS')
                    else:
                        categoria=item.find('span').get_text(strip=True)
                        categorias.append(categoria)
                elif contador==1:
                        emisor=item.find('span').get_text(strip=True)
                        emisores.append(emisor)
                elif contador==4:
                        descripcion=item.find('span').get_text(strip=True)
                        descripciones.append(descripcion)
for i in range(len(titulos)):
    convocante.append('Universidad de Salamanca')

print(titulos)
print(list_fechas_convocatorias)
print(enlaces)
print(categorias)
print(emisores)
print(convocante)
print(descripciones)

print(len(titulos))
print(len(list_fechas_convocatorias))
print(len(enlaces))
print(len(categorias))
print(len(emisores))
print(len(convocante))
print(len(descripciones))

print(titulos[0])
print(list_fechas_convocatorias[0])
print(enlaces[0])
print(categorias[0])
print(emisores[0])
print(convocante[0])
print(descripciones[0])