import unittest
import sys
# Vamos a utilizar MagicMock que es utilizada para la creación de objetos simulados y de esta manera la facilitación de pruebas,¡.
from unittest.mock import Mock
from bs4 import BeautifulSoup
from datetime import date, datetime

sys.path.append('C:\\Users\\Usuario\\Desktop\\DeltaOffers\\DataCollections')

from Scrapers.ScrapingUVA.scrapingUVA import UVAScraper  # nopep8


class TestScrapingUVA(unittest.TestCase):

    link_UVA_PDI = 'https://pdi.uva.es/1.convocatorias/index.html'
    link_UVA_PAS = 'https://pas.uva.es/1.convocatorias/'

    def instance(self):

        scraper = UVAScraper(self.link_UVA_PDI)
        scraper.obtener_datos()
        return scraper

        # Test que comprueba si el scraping se ha realizado bien y por lo tanto se han obtenido convocatorias.
    def test_comprobar_convocatorias_existentes(self):
        scraper = self.instance()
        self.assertGreater(len(scraper.uva_general), 0)

    # Test que comprueba que se han obtenido bien todos los campos de esta universidad.
    def test_comprobar_campos_correctos(self):
        scraper = self.instance()

        for i in scraper.uva_general:
            self.assertEqual(len(i), 9)

    # Test que comprueba que hay un número de convocatorias mínimas (equivalente al número de cerradas)
    def test_comprobar_convocatorias_minimas(self):
        scraper = self.instance()

        self.assertGreaterEqual(len(scraper.uva_general), 5)

    # Test que comprueba que el número de convocatorias cerradas es el deseado
    def test_comprobar_convocatorias_cerradas(self):
        contador = 0
        scraper = self.instance()

        for i in range(len(scraper.uva_general)):
            if scraper.uva_general[i][3] == 'CONVOCATORIA CERRADA':
                contador += 1

        self.assertEqual(contador, 5)

    # Test que comprueba la obtención de la categoría de la convocatoria.
    def test_obtener_categorias_correctas(self):

        scraper = self.instance()
        scraper.obtener_categorias()

        self.assertIn('PDI', scraper.filas)

    # Test que comprueba la obtención de los plazos en los distintos casos que se pueden dar
    def test_obtener_plazos_correctos(self):
        scraper = self.instance()

        scraper.obtener_estados('No especificado', '2024-01-17')
        self.assertIn('NO ESPECIFICADO', scraper.filas)

        scraper.obtener_estados('2024-01-03', '2024-01-17')
        self.assertIn('CONVOCATORIA CERRADA', scraper.filas)

        scraper.obtener_estados('2024-01-03', '2025-04-17')
        self.assertIn('EN PLAZO', scraper.filas)

    # Test que comprueba que añadimos a nuestra estructura el valor correcto cuando hay fechas en los plazos que no estan definidas.
    def test_obtener_plazos_solicitud_fechas_no_definidas(self):

        scraper = UVAScraper(self.link_UVA_PDI)

        mock_contenedor = Mock()
        mock_contenedor.find.return_value.get_text.return_value = ''

        scraper.obtener_plazos_solicitud(mock_contenedor)

        self.assertIn("No especificado", scraper.filas)


if __name__ == '__main__':
    unittest.main()
