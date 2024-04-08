import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import sys

sys.path.append('C:\\Users\\Usuario\\Desktop\\DeltaOffers')

# La guía de estilos Pep8 indica que los 'imports' tienen que estar al inicio del fichero, sin embargo, hay ocasiones en las que nos interesa 'saltarnos' esa guía de estilos.
# Este es uno de los casos y es por ello que a las líneas que no se quiera que sigan esta guía se las podrá agregar el siguiente comentario:
from Interfaces.scrapingInterface import ScrapingInterface  # nopep8


class ULEScraper(ScrapingInterface):
    def __init__(self):
        self.fila = []
        self.ule_general = []
        self.contador_primeras_cerradas = 0
        self.contador_cerradas = 0
        self.palabras_no_deseadas = ['provisional', 'definitiva',
                                     'aprobados', 'admitidos', 'desierto', 'plantilla', 'superado']

    def obtener_titulos(self, item):
        titulo = item.find(
            'div', class_='list-item-content').get_text(strip=True)
        self.fila.append(titulo)

    def obtener_enlaces_subpagina(self, item):
        enlace_subpagina = 'https://www.unileon.es' + item.find('a')['href']
        self.fila.append(enlace_subpagina)
        return enlace_subpagina

    def obtener_fechas_convocatorias(self, sub_soup):
        fecha_conv = sub_soup.find(
            'div', class_='field field--name-node-post-date field--type-ds field--label-hidden field--item').get_text(strip=True)
        dia, fecha = fecha_conv.split(', ')
        fecha_conv = datetime.strptime(fecha, "%d/%m/%Y - %H:%M")
        fecha_conv_limpia = fecha_conv.strftime("%Y-%m-%d")
        self.fila.append(fecha_conv_limpia)

    def obtener_categorias(self, sub_soup):
        # En ocasiones, esta web no me indica la categoría. Esta discrepancia la resuelvo asignandole a mi campo una categoria 'GENERAL'.
        if sub_soup.find('div', class_='field field--name-field-announcement-target field--type-list-string field--label-above') == None:
            self.fila.append('GENERAL')
        elif 'General' == sub_soup.find('div', class_='field field--name-field-announcement-target field--type-list-string field--label-above').find('div', class_='field--item').get_text(strip=True):
            self.fila.append('GENERAL')
        elif 'P.A.S. Laboral' == sub_soup.find('div', class_='field field--name-field-announcement-target field--type-list-string field--label-above').find('div', class_='field--item').get_text(strip=True):
            self.fila.append('PAS')
        else:
            self.fila.append('GENERAL')

    def obtener_tipo(self, sub_soup):
        # Controlo el caso de que haya campos en la web que no aparezcan en alguna convocatoria.
        if sub_soup.find('div', class_='field field--name-field-type field--type-list-string field--label-above') == None:
            self.fila.append('No especificado')
        else:
            tipo = sub_soup.find('div', class_='field field--name-field-type field--type-list-string field--label-above').find(
                'div', class_='field--item').get_text(strip=True)
            self.fila.append(tipo)

    def obtener_estados(self, fecha_ini, fecha_fin):
        fecha_actual = datetime.now()
        # Ya que esta web no nos indica si una oferta está en plazo o no. Asignaremos el plazo nosotros a partir de la comparación entre la fecha actual y los plazos.
        if fecha_ini <= fecha_actual and fecha_fin > fecha_actual:
            self.fila.append('EN PLAZO')
        else:
            self.fila.append('CONVOCATORIA CERRADA')

    def obtener_plazos_solicitud(self, sub_soup):

        # A la hora de obtener los plazos de solititud, convertiremos el campo a un estilo mas legible, ya pensando en el atractivo de nuestro frontend.
        fecha_inicio_solicitud = sub_soup.find(
            'div', class_='field field--name-field-announcement-date field--type-datetime field--label-above').find('time')['datetime']
        fecha_inicio_solicitud = datetime.strptime(
            fecha_inicio_solicitud, "%Y-%m-%dT%H:%M:%SZ")
        fecha_inicio_limpia = fecha_inicio_solicitud.strftime("%Y-%m-%d")
        self.fila.append(fecha_inicio_limpia)

        fecha_fin_solicitud = sub_soup.find(
            'div', class_='field field--name-field-announcement-deadline field--type-datetime field--label-above').find('time')['datetime']
        fecha_fin_solicitud = datetime.strptime(
            fecha_fin_solicitud, "%Y-%m-%dT%H:%M:%SZ")
        fecha_fin_limpia = fecha_fin_solicitud.strftime("%Y-%m-%d")
        self.fila.append(fecha_fin_limpia)

        self.obtener_estados(fecha_inicio_solicitud, fecha_fin_solicitud)

    def obtener_nombre_plaza(self, sub_soup):
        # En ocasiones, el nombre de la plaza no está indicado. Añadimos una comprobación para solucionar esta discrepancia.
        if None == sub_soup.find('div', class_='field field--name-field-positions field--type-string-long field--label-above'):
            self.fila.append('No especificado')
        else:
            nombre_plaza = sub_soup.find('div', class_='field field--name-field-positions field--type-string-long field--label-above').find(
                'div', class_='field--item').get_text(strip=True)
            self.fila.append(nombre_plaza)

    def obtener_convocatoria_asociada(self, sub_soup):
        # En ocasiones, la convocatoria asociada no esta especificada en la web. Añadimos una comprobación para solucionar esta discrepancia.
        if sub_soup.find('div', class_='field field--name-field-associated-announcement field--type-string-long field--label-above') == None:
            self.fila.append('No especificada')
        else:
            conv_asociada = sub_soup.find('div', class_='field field--name-field-associated-announcement field--type-string-long field--label-above').find(
                'div', class_='field--item').get_text(strip=True)
            self.fila.append(conv_asociada)

    def obtener_descripciones(self, sub_soup):
        # En ocasiones, la descripción no esta especificada en la web. Añadimos una comprobación para solucionar esta discrepancia.
        if sub_soup.find('div', class_='field field--name-body field--type-text-with-summary field--label-hidden field--item') == None:
            self.fila.append('No especificada')
        else:
            descripcion = sub_soup.find(
                'div', class_='field field--name-body field--type-text-with-summary field--label-hidden field--item').get_text(strip=True)
            self.fila.append(descripcion)

    def obtener_documento(self, sub_soup):
        documento = ' '
        # En ocasiones, no hay documentos adjuntos asociados a una oferta. Añadimos una comprobación para solucionar esta discrepancia.
        if sub_soup.find('div', class_='field field--name-upload field--type-file field--label-hidden field--items') == None:
            self.fila.append('No hay documentos adjuntos')
        else:
            lista_documentos = sub_soup.find(
                'div', class_='field field--name-upload field--type-file field--label-hidden field--items').find_all('span', class_='file-link')

            for item in lista_documentos:
                documento += item.get_text(strip=True) + ' '
            self.fila.append(documento)

    def obtener_universidad(self):
        self.fila.append('Universidad de Leon')

    def añadir_fila(self):
        self.ule_general.append(list(self.fila))
        self.fila.clear()

    def obtener_datos(self, link_ule):
        response = requests.get(link_ule)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            etiqueta_pagina = soup.find_all(
                'td', class_='views-field views-field-created views-field-title')

            for item in etiqueta_pagina:
                self.obtener_titulos(item)

                enlace_subpagina = self.obtener_enlaces_subpagina(item)
                respuesta_subpagina = requests.get(enlace_subpagina)

                if respuesta_subpagina.status_code == 200:
                    sub_soup = BeautifulSoup(respuesta_subpagina.text, 'lxml')

                    # Hago esperas cada vez que accedo a hacer el scraping de las subpaginas para simular el comportamiento humano
                    # time.sleep(3)

                    self.obtener_fechas_convocatorias(sub_soup)
                    self.obtener_categorias(sub_soup)
                    self.obtener_tipo(sub_soup)
                    self.obtener_plazos_solicitud(sub_soup)
                    self.obtener_nombre_plaza(sub_soup)
                    self.obtener_convocatoria_asociada(sub_soup)
                    self.obtener_descripciones(sub_soup)
                    self.obtener_universidad()
                    self.obtener_documento(sub_soup)

                    # En esta sección del código, realizo comprobaciones de las ofertas que se añadirán a mi estructura.
                    # Además, implemento contadores para añadir algunas convocatorias cerradas por si fuesen de interés para el usuario.
                    fila_minusculas = self.fila[12].lower()
                    # Cojo las primeras 10 convocatorias cerradas por si el usuario quiere ver las convocatorias cerradas recientemente.
                    if self.fila[7] == 'CONVOCATORIA CERRADA' and self.contador_primeras_cerradas < 10:
                        self.fila.pop()
                        self.añadir_fila()
                        self.contador_cerradas += 1
                        self.contador_primeras_cerradas += 1
                    # Cuento cuántas son las cerradas para determinar la condicion de parada de mi programa.
                    elif self.fila[7] == 'CONVOCATORIA CERRADA' and self.contador_primeras_cerradas >= 10:
                        self.fila.clear()
                        self.contador_cerradas += 1
                    # Si los documentos adjuntos no contienen las palabras no deseadas y la convocatoria está en plazo,  añadimos a la estructura ULE general.
                    elif self.fila[7] != 'CONVOCATORIA CERRADA':

                        lista_no_deseadas = []
                        # Utilizo una estructura de datos con las palabras no deseadas de tal manera que, para futuras implemenatciones, si se desean añadir más palabras no deseadas.
                        # Solo tendremos que añadirlas a esa estructura.
                        for palabra in self.palabras_no_deseadas:
                            # Si encuentro alguna no desada
                            if palabra in fila_minusculas:
                                lista_no_deseadas.append(palabra)
                        if len(lista_no_deseadas) == 0:
                            self.fila.pop()
                            self.añadir_fila()
                            # Pongo el contador de cerradas a cero para que el programa no acabe hasta que encuentre 30 convocatorias cerradas seguidas. En este caso suponemos que ya no habrá mas convocatorias en plazo.
                            self.contador_cerradas = 0
                        else:
                            self.fila.clear()
                    else:
                        self.fila.clear()
                else:
                    print(f'La solicitud ha fallado y su código de estado es el {
                        respuesta_subpagina.status_code}')
        else:
            print(f'La solicitud ha fallado y su código de estado es el {
                response.status_code}')

    def extraer_datos_paginas(self):
        contador_paginas = 0
        link_ule = 'https://www.unileon.es/actualidad/convocatorias'

        # Determino la condición de parada, al encontrar 30 convocatorias cerradas seguidas.
        while self.contador_cerradas < 30:
            if contador_paginas == 0:
                self.obtener_datos(link_ule)
            else:
                link_ule_siguientes_paginas = f'https://www.unileon.es/actualidad/convocatorias?page={
                    contador_paginas}'
                self.obtener_datos(link_ule_siguientes_paginas)
            contador_paginas += 1

    def tabla_limpia(self):
        # Realizo una limpieza de mi estructura para la eliminación de caracteres no deseados.
        for fila in self.ule_general:
            for i, item in enumerate(fila):
                fila[i] = item.replace('\xa0', ' ')


'''
scraper = ULEScraper()
scraper.extraer_datos_paginas()
scraper.tabla_limpia()
print(scraper.ule_general)
print(len(scraper.ule_general))
print(len(scraper.ule_general[0]))
'''
