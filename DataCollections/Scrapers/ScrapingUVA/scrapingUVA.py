import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
# A veces el html tarda un tiempo en cargar, con esto hacemos que hasta que cierto elemento no cargue.
# No realizaremos ninguna operacion.
# Vamos a esperar.
from selenium.webdriver.support.ui import WebDriverWait
# A que ciertos elementos cumplan una condición.
from selenium.webdriver.support import expected_conditions as EC
# Que viene dada por ciertos elementos html.
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from datetime import datetime
import sys


# NOTAS: LA UVA, UTILIZA EN SUS WEBS DEL PDI Y PAS JAVASCRIPT DINÁMICO, ESTO QUIERE DECIR QUE VOY A TENER QUE UTILZIAR SELENIUM.
# PARA PODER OBTENER CORRECTAMENTE EL CÓDIGO HTML. LAS ETIQUETAS JS ESTAN CARGADAS DE MANERA DINÁMICA.

# sys.path.append('C:\\Users\\Usuario\\Desktop\\DeltaOffers\\DataCollections')

# La guía de estilos Pep8 indica que los 'imports' tienen que estar al inicio del fichero, sin embargo, hay ocasiones en las que nos interesa 'saltarnos' esa guía de estilos.
# Este es uno de los casos y es por ello que a las líneas que no se quiera que sigan esta guía se las podrá agregar el siguiente comentario:
from ...Interfaces.scrapingInterface import ScrapingInterface  # nopep8


# Anteriormente, dado que la web de las convocatorias del PDI Y PAS de la UVA eran distintas, utilizaba dos clases diferentes.
# Al darme cuenta de que la estructura de ambas es monolítica, decido implementar una clase con una instancia por cada tipo de convocatoria.
# Esta refactorización consigue eliminar la duplicidad de código.

class UVAScraper(ScrapingInterface):

    def __init__(self, enlace):
        self.enlace = enlace
        self.filas = []
        self.uva_general = []
        self.contador_cerradas = 0

    def obtener_titulos(self, item):
        titulo = item.find(
            'a', class_='uva-convocatoria-link').get_text(strip=True)
        self.filas.append(titulo)

    def obtener_estados(self, fecha_ini, fecha_fin):
        # En ocasiones la web 'scrapeada' no nos indica alguna de las fechas y por lo tanto no podemos conocer si la oferta está en plazo o no.
        if fecha_ini == 'No especificado' or fecha_fin == 'No especificado':
            self.filas.append('NO ESPECIFICADO')
        else:
            fecha_actual = datetime.now().date()

            fecha_ini_convertida = datetime.strptime(
                fecha_ini, "%Y-%m-%d").date()

            fecha_fin_convertida = datetime.strptime(
                fecha_fin, "%Y-%m-%d").date()

            if fecha_ini_convertida <= fecha_actual and fecha_actual < fecha_fin_convertida:
                self.filas.append('EN PLAZO')
            else:
                self.filas.append('CONVOCATORIA CERRADA')

    def obtener_plazos_solicitud(self, item):
        if item.find('span', id='fechainicio').get_text(strip=True) == '':
            fecha_inicio_formateada = 'No especificado'
            self.filas.append(fecha_inicio_formateada)
        if item.find('span', id='fechafin').get_text(strip=True) == '':
            fecha_fin_formateada = 'No especificado'
            self.filas.append(fecha_fin_formateada)
        else:
            fecha_inicio_solicitud = item.find(
                'span', id='fechainicio').get_text(strip=True)
            fecha_inicio_solicitud = fecha_inicio_solicitud.replace(
                'Desde ', '')
            fecha_inicio_solicitud = datetime.strptime(
                fecha_inicio_solicitud, '%d/%m/%Y')
            fecha_inicio_formateada = fecha_inicio_solicitud.strftime(
                '%Y-%m-%d')
            self.filas.append(fecha_inicio_formateada)

            fecha_fin_solicitud = item.find(
                'span', id='fechafin').get_text(strip=True)
            fecha_fin_solicitud = fecha_fin_solicitud.replace('Hasta ', '')
            fecha_fin_solicitud = datetime.strptime(
                fecha_fin_solicitud, '%d/%m/%Y')
            fecha_fin_formateada = fecha_fin_solicitud.strftime('%Y-%m-%d')
            self.filas.append(fecha_fin_formateada)

        self.obtener_estados(fecha_inicio_formateada, fecha_fin_formateada)

    def obtener_enlaces_subpagina(self, item):
        enlace_subpagina = item.find(
            'a', class_='uva-convocatoria-link')['href']
        self.filas.append(enlace_subpagina)
        return enlace_subpagina

    def obtener_universidad(self):
        self.filas.append('Universidad de Valladolid')

    def obtener_categorias(self):
        # En función del enlace que se pase por parámetro, determinamos si es una convocatoria PDI o PAS.
        if self.enlace == 'https://pdi.uva.es/1.convocatorias/index.html':
            self.filas.append('PDI')
        else:
            self.filas.append('PAS')

    def añadir_fila(self):
        self.uva_general.append(list(self.filas))
        self.filas.clear()

    def obtener_datos(self):
        contador = 0
        try:

            # INDICO EL WEB DRIVER, interfaz que proporciona una API de alto nivel para controlar navegadores web de manera programática.
            driver = webdriver.Firefox()
            # Link para extraer data.

            # Para enviar una solicitud a la página y como resultado nos da una respuesta.
            driver.get(self.enlace)

            # De esta manera, nos aseguramos que el acceso a los elementos deseados es correcto.
            # Experamos 5 segundos hasta que se cumpla la condición de que encontremos esa clase.
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'uva-convocatoria-link'))
            )
            # Obtengo el HTML.
            html = driver.page_source

            soup = BeautifulSoup(html, 'lxml')

            etiqueta_pagina = soup.find_all('p', class_='uva-convocatoria')

            for item in etiqueta_pagina:
                self.obtener_titulos(item)
                self.obtener_plazos_solicitud(item)

                enlace_subpagina = self.obtener_enlaces_subpagina(item)
                respuesta_subpagina = requests.get(enlace_subpagina)
                respuesta_subpagina.encoding = 'utf-8'

                if respuesta_subpagina.status_code == 200:

                    sub_soup = BeautifulSoup(
                        respuesta_subpagina.text, 'lxml')

                    # Hago esperas cada vez que accedo a hacer el scraping de las subpaginas para simular el comportamiento humano
                    # time.sleep(3)

                    etiqueta_subpagina = sub_soup.find_all(
                        'div', class_='uva-convocatoria-contenido')

                    for sub_item in etiqueta_subpagina:
                        etiq_tipo_clasificacion = sub_item.find_all(
                            'div', class_='uva-convocatoria-contenido-tipo')
                        # He tenido que realizar este flujo dado que para obtener distintos atributos, la estructura html era la misma.
                        for i in etiq_tipo_clasificacion:
                            if contador % 2 == 0:
                                tipo = i.find('span').get_text(strip=True)
                            else:
                                clasificacion = i.find_all('span')
                                if len(clasificacion) <= 1:
                                    self.filas.append('No determinado')
                                else:
                                    self.filas.append(
                                        clasificacion[1].get_text(strip=True))
                            contador += 1

                        self.filas.append(tipo.replace('Tipo: ', ''))
                self.obtener_universidad()
                self.obtener_categorias()

                # Por si al usuario le interesaría, añado a mi estructura las 10 convocatorias cerradas más recientes de la web.
                if self.filas[3] == 'EN PLAZO':
                    self.añadir_fila()
                elif self.filas[3] == 'CONVOCATORIA CERRADA':
                    if self.contador_cerradas < 5:
                        self.añadir_fila()
                        self.contador_cerradas += 1
                    else:
                        self.contador_cerradas += 1

        except WebDriverException as wde:
            print("Se ha ocasionado un error con el Web Driver:", wde)
        except Exception as e:
            print("Ha ocurrido un error insesperado:", e)
        finally:
            driver.quit()
