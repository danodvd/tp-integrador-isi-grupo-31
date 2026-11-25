from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from publicacion import Publicacion

if TYPE_CHECKING:
    from respuesta import Respuesta


class Pregunta(Publicacion):
    def __init__(self, titulo: str, cuerpo: str, fecha_publicacion: date):
        self.titulo = titulo
        self._cuerpo = cuerpo
        self._fecha_publicacion = fecha_publicacion
        self._respuestas: list[Respuesta] = []

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

    # Respuestas
    @property
    def respuestas(self) -> list[Respuesta]:
        # Copia, para que no se modifique la lista interna desde afuera
        return list(self._respuestas)

    def agregar_respuesta(self, respuesta: Respuesta) -> None:
        if not any(r is respuesta for r in self._respuestas):
            self._respuestas.append(respuesta)
        # Mantiene sincronizada la relación bidireccional
        if respuesta.pregunta is not self:
            respuesta.pregunta = self

    def quitar_respuesta(self, respuesta: Respuesta) -> None:
        self._respuestas = [r for r in self._respuestas if r is not respuesta]
