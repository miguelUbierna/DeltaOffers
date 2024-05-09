import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import sys

sys.path.append('C:\\Users\\Usuario\\Desktop\\DeltaOffers\\DataCollections')


# La guía de estilos Pep8 indica que los 'imports' tienen que estar al inicio del fichero, sin embargo, hay ocasiones en las que nos interesa 'saltarnos' esa guía de estilos.
# Este es uno de los casos y es por ello que a las líneas que no se quiera que sigan esta guía se las podrá agregar el siguiente comentario:
from Interfaces.scrapingInterface import ScrapingInterface  # nopep8


class UBUScraper(ScrapingInterface):
    def __init__(self):
        self.filas = []
        self.ubu_general = []
        self.contador_cerradas = 0

    def obtener_titulos(self, item):
        titulo = item.find(
            'div', class_='field-content').find('a').get_text(strip=True)
        self.filas.append(titulo)

    def obtener_estados(self, item):
        estado = item.find('div').get_text(strip=True)
        self.filas.append(estado)

    def obtener_enlaces_subpagina(self, item):
        # Proceso de obtención de subpágina.
        enlace_subpagina = 'https://www.ubu.es' + item.find('a')['href']
        self.filas.append(enlace_subpagina)
        respuesta_subpagina = requests.get(enlace_subpagina)
        return respuesta_subpagina

    def obtener_descripciones(self, contenedor):
        # Controlo en el caso de que la descripción no aparezca en la web a la que hago el scraping. Este tipo de condiciones son muy útiles para asegurarnos
        # de que aunque en la web falten determinados campos, nosotros nos aseguraremos una estructura uniforme.
        if contenedor.find('div', class_='field-item even', property='content:encoded') == None:
            descripcion = 'No especificada'
        else:
            descripcion = contenedor.find('div', class_='field-item even', property='content:encoded').p.get_text(
                strip=True)
        self.filas.append(descripcion)

    def obtener_fechas_convocatorias(self, contenedor):

        if contenedor.find('span', class_='date-display-single') == None:
            self.filas.append('No especificada')
        else:
            fecha_convocatoria = contenedor.find(
                'span', class_='date-display-single')['content']
            fecha_convocatoria = datetime.strptime(
                fecha_convocatoria, "%Y-%m-%dT%H:%M:%S%z")
            fecha_convocatoria_limpia = fecha_convocatoria.strftime("%Y-%m-%d")
            self.filas.append(fecha_convocatoria_limpia)

    def obtener_plazos_solicitud(self, contenedor):

        # Esta comprobación la hago debido que en ocasiones, en la web a la que estoy haciendo scraping, no me aparece la fecha de inicio de la solicutud del plazo de presentación.
        if str(contenedor.find('div', class_='field field-name-field-presentation-date field-type-datetime '
                               'field-label-above').find('span')['class']) != "['date-display-single']":

            fecha_inicio_solicitud = contenedor.find(
                'span', class_='date-display-start')['content']
            fecha_inicio_solicitud = datetime.strptime(
                fecha_inicio_solicitud, "%Y-%m-%dT%H:%M:%S%z")
            fecha_inicio_limpia = fecha_inicio_solicitud.strftime("%Y-%m-%d")
            self.filas.append(fecha_inicio_limpia)

            fecha_fin_solicitud = contenedor.find(
                'span', class_='date-display-end')['content']
            fecha_fin_solicitud = datetime.strptime(
                fecha_fin_solicitud, "%Y-%m-%dT%H:%M:%S%z")
            fecha_fin_limpia = fecha_fin_solicitud.strftime("%Y-%m-%d")
            self.filas.append(fecha_fin_limpia)

        else:
            self.filas.append('No especificada')
            fecha_fin_solicitud = contenedor.find('div', class_='field field-name-field-presentation-date '
                                                  'field-type-datetime field-label-above').find(
                'span', class_='date-display-single')['content']
            fecha_fin_solicitud = datetime.strptime(
                fecha_fin_solicitud, "%Y-%m-%dT%H:%M:%S%z")
            fecha_fin_limpia = fecha_fin_solicitud.strftime("%Y-%m-%d")
            self.filas.append(fecha_fin_limpia)

    def obtener_convocantes(self, contenedor, convocante):

        # En ocasiones, en la web el campo de convocantes sale vacio, por esta razón, añado a mi estructura un campo indicando que el convocante no se ha especificado.
        if contenedor.find('div', class_='field field-name-field-convener field-type-text-long field-label-above') == None:
            self.filas.append('No especificado')
        else:
            contenedor_convocante = contenedor.find(
                'div', class_='field field-name-field-convener field-type-text-long field-label-above').find_all('p')
            for item in contenedor_convocante:
                convocante += item.get_text(strip=True) + ' '
            self.filas.append(convocante)

    def obtener_destinatarios(self, contenedor):
        # Compruebo que ese campo no este vacío. Si lo está, añado a mi estructura un texto explicativo.
        if contenedor.find('div', class_='field field-name-field-receiver field-type-text-long field-label-above') \
                is not None:
            contenedor_destinatarios = contenedor.find(
                'div', class_='field field-name-field-receiver field-type-text-long field-label-above').find(
                'div', class_='field-item even').get_text(strip=True)
            self.filas.append(contenedor_destinatarios)
        else:
            self.filas.append('No se han encontrado destinatarios')

    def obtener_categorias(self, contenedor):
        categoria = contenedor.find(
            'div', class_='field field-name-field-term-interest field-type-taxonomy-term-reference field-label-above').get_text(strip=True)

        # Si encuentro una categoría atípica hasta lo que nos hemos encontrado hasta el momento en la web, indico que la categoría no está especificada.
        # Hasta ahora no se han encontrado mas categorías con un formato concreto
        if 'Convocatorias personal docente' in categoria or 'Convocatorias personal investigador' in categoria:
            self.filas.append('PDI')
        elif 'Convocatorias PAS' in categoria:
            self.filas.append('PAS')
        else:
            self.filas.append('No especificada')

    def obtener_universidad(self):
        self.filas.append('Universidad de Burgos')

    def añadir_fila(self):
        self.ubu_general.append(list(self.filas))
        self.filas.clear()

    def obtener_datos(self, link):
        convocante = ''
        # Para enviar una solicitud a la página y como resultado nos da una respuesta
        response = requests.get(link)

        # Comprobamos si la solicitud fue exitosa.
        if response.status_code == 200:
            # El response.text es para obtener el texto de esa respuesta/resultado que me envió la pagina.
            # La variable soup es importante porque es la que nos va a permitir obtener elementos en una página web.
            # El parser es lxml para obtener el código HTML de la respuesta obtenida.
            soup = BeautifulSoup(response.text, 'lxml')

            # Para buscar un elemento por su etiqueta.
            etiqueta_pagina = soup.find_all(
                'div', class_='views-field views-field-field---last-application-date')

            for item in etiqueta_pagina:
                self.obtener_titulos(item)
                self.obtener_estados(item)
                respuesta_subpagina = self.obtener_enlaces_subpagina(item)

                if respuesta_subpagina.status_code == 200:
                    sub_soup = BeautifulSoup(respuesta_subpagina.text, 'lxml')

                    # Hago esperas cada vez que accedo a hacer el scraping de las subpaginas para simular el comportamiento humano
                    # time.sleep(3)
                    contenedores_subpagina = sub_soup.find_all('article')

                    for contenedor in contenedores_subpagina:
                        self.obtener_descripciones(contenedor)
                        self.obtener_fechas_convocatorias(contenedor)
                        self.obtener_plazos_solicitud(contenedor)
                        self.obtener_convocantes(contenedor, convocante)
                        self.obtener_destinatarios(contenedor)
                        self.obtener_categorias(contenedor)
                    self.obtener_universidad()

                    # Con esto contrlo el hecho de mostrar las 10 primeras convocatorias cerradas por si fuese de interés para el usuario.
                    if self.filas[1] == 'EN PLAZO' or self.filas[1] == 'EN RESOLUCION':
                        self.añadir_fila()
                    elif self.filas[1] == 'CONVOCATORIA CERRADA':
                        if self.contador_cerradas < 10:
                            self.añadir_fila()
                            self.contador_cerradas += 1
                        else:
                            self.contador_cerradas += 1
                else:
                    print(f'La solicitud ha fallado y su código de estado es el {
                        respuesta_subpagina.status_code}')

        else:
            print(f'La solicitud ha fallado y su código de estado es el {
                response.status_code}')

    def tabla_limpia(self):
        # Función la cual es utilizada para realizar una limpieza de mi estructura de datos ante caracteres no deseados a la hora de realizar el scraping.
        for fila in self.ubu_general:
            for i, item in enumerate(fila):
                fila[i] = item.replace('\xa0', ' ')
                fila[i] = fila[i].replace('• ', ' ')

    def extraer_datos_paginas(self):
        contador_paginas = 0
        # Link para extraer los datos.
        link_ubu = 'https://www.ubu.es/trabaja-en-la-ubu'

        # Con esto determino la condición de parada del proceso de scraping a la web de esta universidad.
        while self.contador_cerradas < 30:
            if contador_paginas == 0:
                self.obtener_datos(link_ubu)
            else:
                link_ubu_siguientes_paginas = 'https://www.ubu.es/trabaja-en-la-ubu?field_term_interest_tid=109&page=' + \
                    str(contador_paginas)
                self.obtener_datos(
                    link_ubu_siguientes_paginas)
                link_ubu_siguientes_paginas = ''
            contador_paginas += 1
