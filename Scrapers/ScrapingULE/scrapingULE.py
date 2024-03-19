import requests
from bs4 import BeautifulSoup
from datetime import datetime


class ULEScraper:
    def __init__(self):
        self.fila = []
        self.ule_general = []
        self.contador_primeras_cerradas = 0
        self.contador_cerradas = 0

    def obtener_fechas_convocatorias(self, item):
        fechas_publicacion = item.find(
            'div', class_='list-datetime bold uppercase font-green-jungle list-datetime-list').get_text(strip=True)
        self.fila.append(fechas_publicacion)

    def obtener_titulos(self, item):
        titulo = item.find(
            'div', class_='list-item-content').get_text(strip=True)
        self.fila.append(titulo)

    def obtener_enlaces_subpagina(self, item):
        enlace_subpagina = 'https://www.unileon.es' + item.find('a')['href']
        self.fila.append(enlace_subpagina)
        return enlace_subpagina

    def obtener_categorias(self, sub_soup):
        if sub_soup.find('div', class_='field field--name-field-announcement-target field--type-list-string field--label-above') == None:
            self.fila.append('GENERAL')
        elif 'General' == sub_soup.find('div', class_='field field--name-field-announcement-target field--type-list-string field--label-above').find('div', class_='field--item').get_text(strip=True):
            self.fila.append('GENERAL')
        elif 'P.A.S. Laboral' == sub_soup.find('div', class_='field field--name-field-announcement-target field--type-list-string field--label-above').find('div', class_='field--item').get_text(strip=True):
            self.fila.append('PAS')
        else:
            self.fila.append('GENERAL')

    def obtener_tipo(self, sub_soup):
        if sub_soup.find('div', class_='field field--name-field-type field--type-list-string field--label-above') == None:
            self.fila.append('No especificado')
        else:
            tipo = sub_soup.find('div', class_='field field--name-field-type field--type-list-string field--label-above').find(
                'div', class_='field--item').get_text(strip=True)
            self.fila.append(tipo)

    def obtener_estados(self, fecha_fin):
        fecha_actual = datetime.now()

        fecha_fin_convertida = datetime.strptime(
            fecha_fin, '%Y-%m-%dT%H:%M:%SZ')

        if fecha_fin_convertida > fecha_actual:
            self.fila.append('EN PLAZO')
        else:
            self.fila.append('CONVOCATORIA CERRADA')

    def obtener_plazos_solicitud(self, sub_soup):
        fecha_inicio_solicitud = sub_soup.find(
            'div', class_='field field--name-field-announcement-date field--type-datetime field--label-above').find('time')['datetime']
        self.fila.append(fecha_inicio_solicitud)

        fecha_fin_solicitud = sub_soup.find(
            'div', class_='field field--name-field-announcement-deadline field--type-datetime field--label-above').find('time')['datetime']
        self.fila.append(fecha_fin_solicitud)

        self.obtener_estados(fecha_fin_solicitud)

    def obtener_nombre_plaza(self, sub_soup):
        if None == sub_soup.find('div', class_='field field--name-field-positions field--type-string-long field--label-above'):
            self.fila.append('No especificado')
        else:
            nombre_plaza = sub_soup.find('div', class_='field field--name-field-positions field--type-string-long field--label-above').find(
                'div', class_='field--item').get_text(strip=True)
            self.fila.append(nombre_plaza)

    def obtener_convocatoria_asociada(self, sub_soup):
        if sub_soup.find('div', class_='field field--name-field-associated-announcement field--type-string-long field--label-above') == None:
            self.fila.append('No especificado')
        else:
            conv_asociada = sub_soup.find('div', class_='field field--name-field-associated-announcement field--type-string-long field--label-above').find(
                'div', class_='field--item').get_text(strip=True)
            self.fila.append(conv_asociada)

    def obtener_descripciones(self, sub_soup):
        if sub_soup.find('div', class_='field field--name-body field--type-text-with-summary field--label-hidden field--item') == None:
            self.fila.append('No especificado')
        else:
            descripcion = sub_soup.find(
                'div', class_='field field--name-body field--type-text-with-summary field--label-hidden field--item').get_text(strip=True)
            self.fila.append(descripcion)

    def obtener_documento(self, sub_soup):
        documento = ' '
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
                self.obtener_fechas_convocatorias(item)
                enlace_subpagina = self.obtener_enlaces_subpagina(item)
                respuesta_subpagina = requests.get(enlace_subpagina)

                if respuesta_subpagina.status_code == 200:
                    sub_soup = BeautifulSoup(respuesta_subpagina.text, 'lxml')
                    self.obtener_categorias(sub_soup)
                    self.obtener_tipo(sub_soup)
                    self.obtener_plazos_solicitud(sub_soup)
                    self.obtener_nombre_plaza(sub_soup)
                    self.obtener_convocatoria_asociada(sub_soup)
                    self.obtener_descripciones(sub_soup)
                    self.obtener_universidad(sub_soup)
                    self.obtener_documento(sub_soup)

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
                    elif (not ('provisional' in fila_minusculas or 'definitiva' in fila_minusculas or 'aprobados' in fila_minusculas or 'admitidos' in fila_minusculas or 'desierto' in fila_minusculas or 'plantilla' in fila_minusculas or 'superado' in fila_minusculas)) and (self.fila[7] != 'CONVOCATORIA CERRADA'):
                        self.fila.pop()
                        self.añadir_fila()
                        # Pongo el contador de cerradas a cero para que el programa no acabe hasta que encuentre 30 convocatorias cerradas seguidas. En este caso suponemos que ya no habrá mas convocatorias en plazo.
                        self.contador_cerradas = 0
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

        while self.contador_cerradas < 30:
            if contador_paginas == 0:
                self.obtener_datos(link_ule)
            else:
                link_ule_siguientes_paginas = f'https://www.unileon.es/actualidad/convocatorias?page={
                    contador_paginas}'
                self.obtener_datos(link_ule_siguientes_paginas)
            contador_paginas += 1

    def tabla_limpia(self):
        for fila in self.ule_general:
            for i, item in enumerate(fila):
                fila[i] = item.replace('\xa0', ' ')


scraper = ULEScraper()
scraper.extraer_datos_paginas()
scraper.tabla_limpia()
print(scraper.ule_general)
print(len(scraper.ule_general))
print(len(scraper.ule_general[0]))
