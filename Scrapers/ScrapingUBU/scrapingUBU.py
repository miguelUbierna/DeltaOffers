import requests
from bs4 import BeautifulSoup


class UBUScraper:
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
        if contenedor.find('div', class_='field-item even', property='content:encoded').p == None:
            descripcion = 'No especificada'
        else:
            descripcion = contenedor.find('div', class_='field-item even', property='content:encoded').p.get_text(
                strip=True)
        self.filas.append(descripcion)

    def obtener_fechas_convocatorias(self, contenedor):
        fecha_convocatoria = contenedor.find(
            'span', class_='date-display-single')['content']
        self.filas.append(fecha_convocatoria)

    def obtener_plazos_solicitud(self, contenedor):
        if str(contenedor.find('div', class_='field field-name-field-presentation-date field-type-datetime '
                               'field-label-above').find('span')['class']) != "['date-display-single']":

            fecha_inicio_solicitud = contenedor.find(
                'span', class_='date-display-start')['content']
            self.filas.append(fecha_inicio_solicitud)

            fecha_fin_solicitud = contenedor.find(
                'span', class_='date-display-end')['content']
            self.filas.append(fecha_fin_solicitud)

        else:
            self.filas.append('No Especificada')
            fecha_fin_solicitud = contenedor.find('div', class_='field field-name-field-presentation-date '
                                                  'field-type-datetime field-label-above').find(
                'span', class_='date-display-single')['content']
            self.filas.append(fecha_fin_solicitud)

    def obtener_convocantes(self, contenedor, convocante):
        if contenedor.find('div', class_='field field-name-field-convener field-type-text-long field-label-above') == None:
            self.filas.append('No especificado')
        else:
            contenedor_convocante = contenedor.find(
                'div', class_='field field-name-field-convener field-type-text-long field-label-above').find_all('p')
            for item in contenedor_convocante:
                convocante += item.get_text(strip=True) + ' '
            self.filas.append(convocante)

    def obtener_destinatarios(self, contenedor):
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
            'div', class_='field-item odd').a.get_text(strip=True)

        if categoria == 'Convocatorias personal docente' or categoria == 'Investigación: adscritas a proyectos':
            self.filas.append('PDI')
        elif categoria == 'Convocatorias PAS':
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
                    contenedores_subpagina = sub_soup.find_all('article')

                    for contenedor in contenedores_subpagina:
                        self.obtener_descripciones(contenedor)
                        self.obtener_fechas_convocatorias(contenedor)
                        self.obtener_plazos_solicitud(contenedor)
                        self.obtener_convocantes(contenedor, convocante)
                        self.obtener_destinatarios(contenedor)
                        self.obtener_categorias(contenedor)
                    self.obtener_universidad()

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
        for fila in self.ubu_general:
            for i, item in enumerate(fila):
                fila[i] = item.replace('\xa0', ' ')

    def extraer_datos_paginas(self):
        contador_paginas = 0
        # Link para extraer los datos.
        link_ubu = 'https://www.ubu.es/trabaja-en-la-ubu'
        while self.contador_cerradas < 30:
            if contador_paginas == 0:
                self.obtener_datos(link_ubu)
                # Meter aqui algo para que rompa el bucle
            else:
                link_ubu_siguientes_paginas = 'https://www.ubu.es/trabaja-en-la-ubu?field_term_interest_tid=109&page=' + \
                    str(contador_paginas)
                self.obtener_datos(
                    link_ubu_siguientes_paginas)
                link_ubu_siguientes_paginas = ''
                # Meter aqui algo que rompa el bucle
            contador_paginas += 1


scraper = UBUScraper()
scraper.extraer_datos_paginas()
# Una vez que se rompe el bucle, meter aqui algo para limpiar mi estructura
print(scraper.ubu_general)
print(len(scraper.ubu_general))
print(len(scraper.ubu_general[0]))
scraper.tabla_limpia()
