from bs4 import BeautifulSoup
import requests
from selenium import webdriver
#A veces el html tarda un tiempo en cargar, con esto hacemos que hasta que cierto elemento no cargue. no realizaremos ninguna operacion.
#Vamos a esperar
from selenium.webdriver.support.ui import WebDriverWait
#A que ciertos elementos cumplan una condicion
from selenium.webdriver.support import expected_conditions as EC
#Que viene dada por ciertos elementos html
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException


#NOTAS: LA UVA, UTILIZA EN SUS WEBS DEL PDI Y PAS JAVASCRIPT DINAMICO, ESTO QUIERE DECIR QUE VOY A TENER QUE UTILZIAR SELENIUM 
# PARA PODER OBTENER CORRECTAMENTE EL CÓDIGO HTML. LAS ETIQUETAS JS ESTAN CARGADAS DE MANERA DINAMICA.

titulos=[]
list_inicio=[]
list_fin=[]
tipos=[]
clasificaciones=[]
estados=[]
enlaces=[]
convocantes=[]
categorias=[]

uva_general=[]
contador=0

#UVA PDI

try:

    #INDICO EL WEB DRIVER, interfaz que proporciona una API de alto nivel para controlar navegadores web de manera programática.
    driver = webdriver.Firefox()
    #Link para extraer data
    link_UVA='https://pdi.uva.es/1.convocatorias/'

    #Para enviar una solicitud a la pagina y como resultado nos da una respuesta
    driver.get(link_UVA)

    #Experamos 5 segundos hasta que se cumpla la condicion de que encontremos esa clase
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'uva-convocatoria-link'))
    )
    #Obtengo el HTML
    html = driver.page_source
    
    soup=BeautifulSoup(html, 'lxml')

    etiqueta_pagina = soup.find_all('p',class_='uva-convocatoria')

    for item in etiqueta_pagina:
        titulo=item.find('a', class_='uva-convocatoria-link').get_text(strip=True)
        titulos.append(titulo)

        fecha_inicio_solicitud=item.find('span', id='fechainicio').get_text(strip=True)
        list_inicio.append(fecha_inicio_solicitud)

        fecha_fin_solicitud=item.find('span', id='fechafin').get_text(strip=True)
        list_fin.append(fecha_fin_solicitud)


        if None != item.find('span', class_='estado abierto'): 
            if 'abierto'== item.find('span', class_='estado abierto').get_text(strip=True) :
                estados.append('EN PLAZO')
        elif None !=item.find('span', class_='estado proceso'):
            if 'en proceso'== item.find('span', class_='estado proceso').get_text(strip=True):
                estados.append('EN PROCESO')
        elif None !=item.find('span', class_='estado cerrado'):
            if 'cerrado'== item.find('span', class_='estado cerrado').get_text(strip=True):
                estados.append('CONVOCATORIA CERRADA')

        enlace_subpagina=item.find('a', class_='uva-convocatoria-link')['href']
        enlaces.append(enlace_subpagina)

        respuesta_subpagina=requests.get(enlace_subpagina)

        if respuesta_subpagina.status_code==200:
                
                sub_soup=BeautifulSoup(respuesta_subpagina.text, 'lxml')
                etiqueta_subpagina = sub_soup.find_all('div',class_='uva-convocatoria-contenido')

                for sub_item in etiqueta_subpagina:
                    etiq_tipo_clasificacion = sub_item.find_all('div',class_='uva-convocatoria-contenido-tipo')

                    for i in etiq_tipo_clasificacion:
                        if contador % 2 ==0 : #Si es par el contador
                            tipo=i.find('span').get_text(strip=True)
                        else:
                            clasificacion=i.find_all('span')
                            if len(clasificacion) <= 1:
                                clasificaciones.append('No determinado')
                            else:
                                clasificaciones.append(clasificacion[1].get_text(strip=True))
                        contador+=1
                    tipos.append(tipo.replace('Tipo: ', ''))
                    
        
except WebDriverException as wde:
    print("Se ha ocasionado un error con el Web Driver:", wde)
except Exception as e:
    print("Ha ocurrido un error insesperado:", e)
finally:
    driver.quit()

for i in range(len(titulos)):
    convocantes.append('Universidad de Valladolid')
for i in range(len(titulos)):
    categorias.append('PDI')

print(titulos)
print(list_inicio)
print(list_fin)
print(estados)
print(convocantes)
print(enlaces)
print(tipos)
print(clasificaciones)
print(categorias)

        
print(len(titulos))
print(len(list_inicio))
print(len(list_fin))
print(len(estados))
print(len(convocantes))
print(len(enlaces))
print(len(tipos))
print(len(clasificaciones))
print(len(categorias))


print(titulos[2])
print(list_inicio[2])
print(list_fin[2])
print(estados[2])
print(convocantes[2])
print(enlaces[2])
print(tipos[2])
print(clasificaciones[2])
print(categorias[2])

