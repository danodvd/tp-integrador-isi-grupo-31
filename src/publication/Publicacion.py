from abc import ABC, abstractmethod
from datetime import date


class Publicacion(ABC):
    """Interfaz común para Pregunta y Respuesta."""

    @property
    @abstractmethod
    def cuerpo(self) -> str: ...

    @property
    @abstractmethod
    def fecha_publicacion(self) -> date: ...

    def getCuerpo(self) -> str:
        return self.cuerpo

    def getFechaPublicacion(self) -> date:
        return self.fecha_publicacion
