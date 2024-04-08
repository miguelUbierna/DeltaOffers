from abc import ABC, abstractmethod

# Definimos una clase abstracta en Python que actua como interfaz.
# En esta clase abstracta definimos los métodos que debe tener nuestra clase conctreta pero sin implementación.
# De esta manera, por norma general, si extenderemos la fucnionalidad de nuestra aplicación y añadimos nuevas universidades, esto nos será muy util.


class ScrapingInterface(ABC):

    @abstractmethod
    def obtener_titulos(self, param):
        pass

    @abstractmethod
    def obtener_estados(self, param):
        pass

    @abstractmethod
    def obtener_enlaces_subpagina(self, param):
        pass

    @abstractmethod
    def obtener_plazos_solicitud(self, param):
        pass

    @abstractmethod
    def obtener_universidad(self):
        pass

    @abstractmethod
    def obtener_categorias(self):
        pass

    @abstractmethod
    def añadir_fila(self):
        pass

    @abstractmethod
    def obtener_datos(self):
        pass
