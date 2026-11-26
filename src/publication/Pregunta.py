from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Optional

from src.publication.Categoria import Categoria
from src.publication.Etiqueta import Etiqueta
from src.publication.Publicacion import Publicacion

if TYPE_CHECKING:
    from src.publication.Respuesta import Respuesta


class Pregunta(Publicacion):
    def __init__(
        self,
        titulo: str,
        cuerpo: str,
        fecha_publicacion: date,
        categoria: Optional[Categoria] = None,
        etiquetas: Optional[list[Etiqueta]] = None,
    ):
        self.titulo = titulo
        self._cuerpo = cuerpo
        self._fecha_publicacion = fecha_publicacion
        self.categoria: Optional[Categoria] = categoria
        self._etiquetas: list[Etiqueta] = list(etiquetas) if etiquetas else []
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

    @property
    def etiquetas(self) -> list[Etiqueta]:
        return list(self._etiquetas)

    def agregar_etiqueta(self, etiqueta: Etiqueta) -> None:
        if not any(e is etiqueta for e in self._etiquetas):
            self._etiquetas.append(etiqueta)

    def quitar_etiqueta(self, etiqueta: Etiqueta) -> None:
        self._etiquetas = [e for e in self._etiquetas if e is not etiqueta]

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

    def getTitulo(self) -> str:
        return self.titulo
