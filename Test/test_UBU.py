import unittest
import sys
# Vamos a utilizar MagicMock que es utilizada para la creación de objetos simulados y de esta manera la facilitación de pruebas,¡.
from unittest.mock import MagicMock
from bs4 import BeautifulSoup
from datetime import date, datetime

sys.path.append('C:\\Users\\Usuario\\Desktop\\DeltaOffers')

from Scrapers.ScrapingUBU.scrapingUBU import UBUScraper  # nopep8


class TestScrapingUBU(unittest.TestCase):

    def instance(self):
        scraper = UBUScraper()
        scraper.extraer_datos_paginas()
        scraper.tabla_limpia()
        return scraper

    def pruebas_none(self, param):
        scraper = UBUScraper()
        mock_contenedor = MagicMock()
        mock_contenedor.find.return_value = None
        if param == 1:
            scraper.obtener_descripciones(mock_contenedor)
        elif param == 2:
            scraper.obtener_fechas_convocatorias(mock_contenedor)
        elif param == 3:
            param = ''
            scraper.obtener_convocantes(mock_contenedor, param)
        elif param == 4:
            scraper.obtener_destinatarios(mock_contenedor)

        return scraper

    # Test que comprueba si el scraping se ha realizado bien y por lo tanto se han obtenido convocatorias.
    def test_comprobar_convocatorias_existentes(self):
        scraper = self.instance()
        self.assertGreater(len(scraper.ubu_general), 0)

    # Test que comprueba que se han obtenido bien todos los campos de esta universidad.
    def test_comprobar_campos_correctos(self):
        scraper = self.instance()

        for i in scraper.ubu_general:
            self.assertEqual(len(i), 11)

    # Test que comprueba que hay un número de convocatorias mínimas (equivalente al número de cerradas)
    def test_comprobar_convocatorias_minimas(self):
        scraper = self.instance()

        self.assertGreaterEqual(len(scraper.ubu_general), 10)

    # Test que comprueba que el numero de convocatorias cerradas es el deseado
    def test_comprobar_convocatorias_cerradas(self):
        contador = 0
        scraper = self.instance()

        for i in range(len(scraper.ubu_general)):
            if scraper.ubu_general[i][1] == 'CONVOCATORIA CERRADA':
                contador += 1

        self.assertEqual(contador, 10)

    # Test que comprueba si el indicador de plazo que expone la universidad en su web esta correcto.
    def test_indicador_plazo(self):
        fecha_actual = date.today()
        scraper = self.instance()
        for fila in scraper.ubu_general:
            if fila[1] == 'EN PLAZO':
                fecha_fin_plazo = datetime.strptime(fila[6], "%Y-%m-%d")
                if fecha_actual <= fecha_fin_plazo.date():
                    plazo = 'EN PLAZO'
                else:
                    plazo = 'El PLAZO NO SE HA OBTENIDO CORRECTAMENTE'

        self.assertEqual(plazo, 'EN PLAZO')

    # Determinamos que se controla bien el caso de que en la página web no haya ninguna descripción asociada a una determinada convocatoria.
    def test_obtener_descripciones_sin_descripcion_presente(self):

        scraper = self.pruebas_none(1)
        self.assertIn("No especificada", scraper.filas)

    # Determinamos que se controla bien el caso de que en la página web no haya ninguna fecha de convocatoria asociada a una determinada convocatoria.
    def test_obtener_fechas_convocatorias_sin_fecha(self):
        scraper = self.pruebas_none(2)
        self.assertIn("No especificada", scraper.filas)

    # Determinamos que se controla bien el caso de que en la página web no haya ningun convocante asociado a una determinada convocatoria.
    def test_obtener_convocantes_no_existentes(self):

        scraper = self.pruebas_none(3)
        self.assertIn("No especificado", scraper.filas)

    # Determinamos que se controla bien el caso de que en la página web no haya ningun destinatario asociado a una determinada convocatoria.
    def test_obtener_destinatarios_no_existentes(self):

        scraper = self.pruebas_none(4)
        self.assertIn('No se han encontrado destinatarios', scraper.filas)

    # Test que comprueba que controlamos el flujo de que aparezca una categoría de las no vistas hasta ahora.
    def test_controlar_categorias_inusuales(self):
        scraper = UBUScraper()
        mock_categoria = MagicMock()
        mock_categoria.find.a.get_text.return_value = 'Esta categoria no la conozco'
        scraper.obtener_categorias(mock_categoria)

        self.assertIn("No especificada", scraper.filas)

    # Test que comprueba si hago una solicitud a un enlace no valido, no obtengo nada y salta una excepcion.
    def test_enlace_no_valido(self):
        ubu_scraper = UBUScraper()
        cadena = 'enlaceNoValido'

        with self.assertRaises(Exception):
            ubu_scraper.obtener_datos(cadena)

        self.assertEqual(ubu_scraper.contador_cerradas, 0)

    # Comprueba si la limpieza de la tabla se hace correctamente.
    def test_tabla_limpia(self):
        ubu_scraper = UBUScraper()
        ubu_scraper.ubu_general = [[
            'Oferta\xa0Personal Docente'], ['• Puesto Administrativo']]
        ubu_scraper.tabla_limpia()

        self.assertEqual(
            ubu_scraper.ubu_general[0][0], 'Oferta Personal Docente')
        self.assertEqual(
            ubu_scraper.ubu_general[1][0], ' Puesto Administrativo')


if __name__ == '__main__':
    unittest.main()
