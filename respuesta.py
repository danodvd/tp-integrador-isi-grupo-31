from __future__ import annotations

from datetime import date
from typing import Optional

from publicacion import Publicacion
from pregunta import Pregunta


class Respuesta(Publicacion):
    def __init__(self, aceptado: bool, id_autor: int, cuerpo: str,
                 fecha_publicacion: date, pregunta: Optional[Pregunta] = None):
        self.aceptado = bool(aceptado)
        self.id_autor = id_autor
        self._cuerpo = cuerpo
        self._fecha_publicacion = fecha_publicacion
        self._pregunta: Optional[Pregunta] = None
        self.pregunta = pregunta  # Relación 0..* a 1 con Pregunta

    # Propiedades de la interfaz Publicacion
    @property
    def cuerpo(self) -> str:
        return self._cuerpo

    @cuerpo.setter
    def cuerpo(self, valor: str) -> None:
        self._cuerpo = valor

    @property
    def fecha_publicacion(self) -> date:
        return self._fecha_publicacion

    @fecha_publicacion.setter
    def fecha_publicacion(self, valor: date) -> None:
        self._fecha_publicacion = valor

    # Relación con Pregunta
    @property
    def pregunta(self) -> Optional[Pregunta]:
        return self._pregunta

    @pregunta.setter
    def pregunta(self, nueva: Optional[Pregunta]) -> None:
        anterior = self._pregunta
        if anterior is nueva:
            return
        if anterior is not None:
            anterior.quitar_respuesta(self)
        self._pregunta = nueva
        if nueva is not None:
            nueva.agregar_respuesta(self)
