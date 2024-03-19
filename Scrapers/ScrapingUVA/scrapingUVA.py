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

# NOTAS: LA UVA, UTILIZA EN SUS WEBS DEL PDI Y PAS JAVASCRIPT DINÁMICO, ESTO QUIERE DECIR QUE VOY A TENER QUE UTILZIAR SELENIUM.
# PARA PODER OBTENER CORRECTAMENTE EL CÓDIGO HTML. LAS ETIQUETAS JS ESTAN CARGADAS DE MANERA DINÁMICA.

titulos = []
list_inicio = []
list_fin = []
tipos = []
clasificaciones = []
estados = []
enlaces = []
convocantes = []
categorias = []

uva_general = []
contador = 0


class UVAScraper:

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
        if fecha_ini == 'No especificado' or fecha_fin == 'No especificado':
            self.filas.append('NO ESPECIFICADO')
        else:
            fecha_actual = datetime.now().date()

            fecha_ini_convertida = datetime.strptime(
                fecha_ini, '%d/%m/%Y').date()

            fecha_fin_convertida = datetime.strptime(
                fecha_fin, '%d/%m/%Y').date()

            if fecha_ini_convertida <= fecha_actual and fecha_actual < fecha_fin_convertida:
                self.filas.append('EN PLAZO')
            else:
                self.filas.append('CONVOCATORIA CERRADA')

    def obtener_plazos_solicitud(self, item):
        if item.find('span', id='fechainicio').get_text(strip=True) == '':
            fecha_inicio_solicitud = 'No especificado'
            self.filas.append(fecha_inicio_solicitud)
        if item.find('span', id='fechafin').get_text(strip=True) == '':
            fecha_fin_solicitud = 'No especificado'
            self.filas.append(fecha_fin_solicitud)
        else:
            fecha_inicio_solicitud = item.find(
                'span', id='fechainicio').get_text(strip=True)
            fecha_inicio_solicitud = fecha_inicio_solicitud.replace(
                'Desde ', '')
            self.filas.append(fecha_inicio_solicitud)

            fecha_fin_solicitud = item.find(
                'span', id='fechafin').get_text(strip=True)
            fecha_fin_solicitud = fecha_fin_solicitud.replace('Hasta ', '')
            self.filas.append(fecha_fin_solicitud)

        self.obtener_estados(fecha_inicio_solicitud, fecha_fin_solicitud)

    def obtener_enlaces_subpagina(self, item):
        enlace_subpagina = item.find(
            'a', class_='uva-convocatoria-link')['href']
        self.filas.append(enlace_subpagina)
        return enlace_subpagina

    def obtener_universidad(self):
        self.filas.append('Universidad de Valladolid')

    def obtener_categoria(self):
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
                    etiqueta_subpagina = sub_soup.find_all(
                        'div', class_='uva-convocatoria-contenido')

                    for sub_item in etiqueta_subpagina:
                        etiq_tipo_clasificacion = sub_item.find_all(
                            'div', class_='uva-convocatoria-contenido-tipo')

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
                self.obtener_categoria()

                if self.filas[3] == 'EN PLAZO':
                    self.añadir_fila()
                elif self.filas[3] == 'CONVOCATORIA CERRADA':
                    if self.contador_cerradas < 10:
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
