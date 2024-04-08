import unittest
import sys
# Vamos a utilizar MagicMock que es utilizada para la creación de objetos simulados y de esta manera la facilitación de pruebas,¡.
from unittest.mock import MagicMock

from datetime import date, datetime

sys.path.append('C:\\Users\\Usuario\\Desktop\\DeltaOffers')

from Scrapers.ScrapingULE.scrapingULE import ULEScraper  # nopep8


class TestScrapingULE(unittest.TestCase):
    def instance(self):
        scraper = ULEScraper()
        scraper.extraer_datos_paginas()
        scraper.tabla_limpia()
        return scraper

    def pruebas_none(self, param):
        scraper = ULEScraper()
        mock_contenedor = MagicMock()
        mock_contenedor.find.return_value = None
        if param == 1:
            scraper.obtener_categorias(mock_contenedor)
        elif param == 2:
            scraper.obtener_tipo(mock_contenedor)
        elif param == 3:
            param = ''
            scraper.obtener_nombre_plaza(mock_contenedor)
        elif param == 4:
            scraper.obtener_convocatoria_asociada(mock_contenedor)
        elif param == 5:
            scraper.obtener_descripciones(mock_contenedor)
        elif param == 6:
            scraper.obtener_documento(mock_contenedor)

        return scraper

    # Test que comprueba si el scraping se ha realizado bien y por lo tanto se han obtenido convocatorias.
    def test_comprobar_convocatorias_existentes(self):
        scraper = self.instance()
        self.assertGreater(len(scraper.ule_general), 0)

    # Test que comprueba que se han obtenido bien todos los campos de esta universidad.
    def test_comprobar_campos_correctos(self):
        scraper = self.instance()

        for i in scraper.ule_general:
            self.assertEqual(len(i), 12)

    # Test que comprueba que hay un número de convocatorias mínimas (equivalente al número de cerradas)
    def test_comprobar_convocatorias_minimas(self):
        scraper = self.instance()
        self.assertGreaterEqual(len(scraper.ule_general), 10)

    # Test que comprueba que el numero de convocatorias cerradas es el deseado
    def test_comprobar_convocatorias_cerradas(self):
        contador = 0
        scraper = self.instance()

        for i in range(len(scraper.ule_general)):
            if scraper.ule_general[i][7] == 'CONVOCATORIA CERRADA':
                contador += 1

        self.assertEqual(contador, 10)

    # Determinamos que se controla bien el caso de que en la página web no haya ninguna categoría asociada a una determinada convocatoria.
    # Le asignamos a esa convocatoria una categoría general
    def test_obtener_categorias_no_especificadas(self):

        scraper = self.pruebas_none(1)
        self.assertIn("GENERAL", scraper.fila)

    # Determinamos que se controla bien el caso de que en la página web no haya ningún tipo asociado a una determinada convocatoria.
    def test_obtener_tipo_no_especificado(self):
        scraper = self.pruebas_none(2)
        self.assertIn("No especificado", scraper.fila)

    # Determinamos que se controla bien el caso de que en la página web no haya ningún nombre de la plaza asociado a una determinada convocatoria.
    def test_obtener_nombre_plaza_no_especificado(self):
        scraper = self.pruebas_none(3)
        self.assertIn("No especificado", scraper.fila)

    # Determinamos que se controla bien el caso de que en la página web no haya ninguna convocatoria asociada a una determinada convocatoria.
    def test_obtener_convocatoria_asociada_no_especificada(self):
        scraper = self.pruebas_none(4)
        self.assertIn("No especificada", scraper.fila)

    # Determinamos que se controla bien el caso de que en la página web no haya ninguna convocatoria asociada a una determinada convocatoria.
    def test_obtener_descripcion_no_especificada(self):
        scraper = self.pruebas_none(5)
        self.assertIn("No especificada", scraper.fila)

    def test_obtener_documentos_no_especificados(self):
        scraper = self.pruebas_none(6)
        self.assertIn("No hay documentos adjuntos", scraper.fila)

    # Comprueba si la limpieza de la tabla se hace correctamente.
    def test_tabla_limpia(self):
        ubu_scraper = ULEScraper()
        ubu_scraper.ule_general = [[
            'Oferta\xa0Personal Docente'], ['Puesto\xa0Administrativo']]
        ubu_scraper.tabla_limpia()

        self.assertEqual(
            ubu_scraper.ule_general[0][0], 'Oferta Personal Docente')
        self.assertEqual(
            ubu_scraper.ule_general[1][0], 'Puesto Administrativo')

    def test_obtener_estados_correctos(self):
        scraper = ULEScraper()

        fecha_inicial = datetime.strptime(
            "2024-03-25T23:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
        fecha_fin = datetime.strptime(
            "2024-04-15T21:59:59Z", "%Y-%m-%dT%H:%M:%SZ")
        fecha_fin_cerrada = datetime.strptime(
            "2024-03-27T21:59:59Z", "%Y-%m-%dT%H:%M:%SZ")
        scraper.obtener_estados(fecha_inicial, fecha_fin)
        self.assertIn("EN PLAZO", scraper.fila)
        scraper.obtener_estados(fecha_inicial, fecha_fin_cerrada)
        self.assertIn("CONVOCATORIA CERRADA", scraper.fila)

    # Test que comprueba si hago una solicitud a un enlace no valido, no obtengo nada y salta una excepcion.
    def test_enlace_no_valido(self):
        ule_scraper = ULEScraper()
        cadena = 'enlaceNoValido'

        with self.assertRaises(Exception):
            ule_scraper.obtener_datos(cadena)

        self.assertEqual(ule_scraper.contador_cerradas, 0)


if __name__ == '__main__':
    unittest.main()
