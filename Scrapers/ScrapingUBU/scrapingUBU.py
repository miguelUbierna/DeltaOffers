import requests
from bs4 import BeautifulSoup


class UBUScraper:
    def __init__(self):
        self.titulos = []
        self.estados = []
        self.descripciones = []
        self.list_fechas_convocatorias = []
        self.list_inicio = []
        self.list_fin = []
        self.convocantes = []
        self.destinatarios = []
        self.categorias = []
        self.enlaces = []
        self.universidad = []
        self.ubu_general = []
        self.contador_cerradas = 0

    def obtener_titulos(self, item):
        titulo = item.find(
            'div', class_='field-content').find('a').get_text(strip=True)
        self.titulos.append(titulo)

    def obtener_estados(self, item):
        estado = item.find('div').get_text(strip=True)
        # En el momento en el que estoy haciendo el scraping, no hay ninguna convocatoria en resolución.
        # Como no se, cual será el contenido de este tipo de etiquetas, si el estado de la convocatoria,
        # No es ni en plazo ni cerrado, automaticamente podré como estado: "EN RESOLUCIÓN"
        if estado != 'EN PLAZO' and estado != 'CONVOCATORIA CERRADA':
            self.estados.append('EN RESOLUCIÓN')
        else:
            self.estados.append(estado)

    def obtener_enlaces_subpagina(self, item):
        # Proceso de obtención de subpágina.
        enlace_subpagina = 'https://www.ubu.es' + item.find('a')['href']
        self.enlaces.append(enlace_subpagina)
        respuesta_subpagina = requests.get(enlace_subpagina)
        return respuesta_subpagina

    def obtener_descripciones(self, contenedor):
        descripcion = contenedor.find('div', class_='field-item even', property='content:encoded').p.get_text(
            strip=True)
        self.descripciones.append(descripcion)

    def obtener_fechas_convocatorias(self, contenedor):
        fecha_convocatoria = contenedor.find(
            'span', class_='date-display-single')['content']
        self.list_fechas_convocatorias.append(fecha_convocatoria)

    def obtener_plazos_solicitud(self, contenedor):
        if str(contenedor.find('div', class_='field field-name-field-presentation-date field-type-datetime '
                               'field-label-above').find('span')['class']) != "['date-display-single']":

            fecha_inicio_solicitud = contenedor.find(
                'span', class_='date-display-start')['content']
            self.list_inicio.append(fecha_inicio_solicitud)

            fecha_fin_solicitud = contenedor.find(
                'span', class_='date-display-end')['content']
            self.list_fin.append(fecha_fin_solicitud)

        else:
            self.list_inicio.append('No Especificada')
            fecha_fin_solicitud = contenedor.find('div', class_='field field-name-field-presentation-date '
                                                  'field-type-datetime field-label-above').find(
                'span', class_='date-display-single')['content']
            self.list_fin.append(fecha_fin_solicitud)

    def obtener_convocantes(self, contenedor, convocante):
        if contenedor.find('div', class_='field field-name-field-convener field-type-text-long field-label-above') == None:
            self.convocantes.append('No especificado')
        else:
            contenedor_convocante = contenedor.find(
                'div', class_='field field-name-field-convener field-type-text-long field-label-above').find_all('p')
            for item in contenedor_convocante:
                convocante += item.get_text(strip=True) + ' '
            self.convocantes.append(convocante)

    def obtener_destinatarios(self, contenedor):
        if contenedor.find('div', class_='field field-name-field-receiver field-type-text-long field-label-above') \
                is not None:
            contenedor_destinatarios = contenedor.find(
                'div', class_='field field-name-field-receiver field-type-text-long field-label-above').find(
                'div', class_='field-item even').get_text(strip=True)
            self.destinatarios.append(contenedor_destinatarios)
        else:
            self.destinatarios.append('No se han encontrado destinatarios')

    def obtener_categorias(self, contenedor):
        categoria = contenedor.find(
            'div', class_='field-item odd').a.get_text(strip=True)

        if categoria == 'Convocatorias personal docente' or categoria == 'Investigación: adscritas a proyectos':
            self.categorias.append('PDI')
        elif categoria == 'Convocatorias PAS':
            self.categorias.append('PAS')
        else:
            self.categorias.append('No especificada')

    def obtener_universidad(self):
        for _ in range(len(self.titulos)):
            self.universidad.append('Universidad de Burgos')

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

                else:
                    print(f'La solicitud ha fallado y su código de estado es el {
                        respuesta_subpagina.status_code}')

        else:
            print(f'La solicitud ha fallado y su código de estado es el {
                response.status_code}')

    def añadir_a_estructura_general(self):
        self.ubu_general.append(self.titulos)
        self.ubu_general.append(self.estados)
        self.ubu_general.append(self.descripciones)
        self.ubu_general.append(self.list_fechas_convocatorias)
        self.ubu_general.append(self.list_inicio)
        self.ubu_general.append(self.list_fin)
        self.ubu_general.append(self.convocantes)
        self.ubu_general.append(self.destinatarios)
        self.ubu_general.append(self.categorias)
        self.ubu_general.append(self.enlaces)
        self.ubu_general.append(self.universidad)

        return self.ubu_general

    def tabla_limpia(self):
        for fila in self.ubu_general:
            for i, item in enumerate(fila):
                fila[i] = item.replace('\xa0', ' ')

    def contar_convocatorias_cerradas(self):
        for item in self.estados:
            if item == 'CONVOCATORIA CERRADA':
                self.contador_cerradas += 1
            else:
                # Si encuentro una abierta, o en proceso, vuelvo a empezar a contar
                self.contador_cerradas = 0
        # Si he recorrido 30 convocatorias y no he encontrado ninguna abierta, suponemos que ya no quedarán mas abiertas.
        if self.contador_cerradas >= 30:
            return True
        else:
            return False

    def extraer_datos_paginas(self):
        contador_paginas = 0
        # Link para extraer los datos.
        link_ubu = 'https://www.ubu.es/trabaja-en-la-ubu'
        while not self.contar_convocatorias_cerradas():
            if contador_paginas == 0:
                self.obtener_datos(link_ubu)
            else:
                link_ubu_siguientes_paginas = 'https://www.ubu.es/trabaja-en-la-ubu?field_term_interest_tid=109&page=' + \
                    str(contador_paginas)
                self.obtener_datos(link_ubu_siguientes_paginas)
                link_ubu_siguientes_paginas = ''
            contador_paginas += 1


scraper = UBUScraper()
scraper.extraer_datos_paginas()
scraper.obtener_universidad()
scraper.añadir_a_estructura_general()
scraper.tabla_limpia()


print(scraper.titulos)
print(scraper.estados)
print(scraper.descripciones)
print(scraper.list_fechas_convocatorias)
print(scraper.list_inicio)
print(scraper.list_fin)
print(scraper.convocantes)
print(scraper.destinatarios)
print(scraper.categorias)
print(scraper.enlaces)
print(scraper.universidad)


print(len(scraper.titulos))
print(len(scraper.estados))
print(len(scraper.descripciones))
print(len(scraper.list_fechas_convocatorias))
print(len(scraper.list_inicio))
print(len(scraper.list_fin))
print(len(scraper.convocantes))
print(len(scraper.destinatarios))
print(len(scraper.categorias))
print(len(scraper.enlaces))
print(len(scraper.universidad))


print(scraper.titulos[11])
print(scraper.estados[11])
print(scraper.descripciones[11])
print(scraper.list_fechas_convocatorias[11])
print(scraper.list_inicio[11])
print(scraper.list_fin[11])
print(scraper.convocantes[11])
print(scraper.destinatarios[11])
print(scraper.categorias[11])
print(scraper.enlaces[11])
print(scraper.universidad[11])
