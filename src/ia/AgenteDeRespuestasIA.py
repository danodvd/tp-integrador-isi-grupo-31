from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from src.Autor import Autor
from src.ia.LLM import LLM
from src.publication.Respuesta import Respuesta

if TYPE_CHECKING:
    from src.publication.Pregunta import Pregunta


class AgenteDeRespuestasIA(Autor):
    def __init__(self, llm: LLM, nombre: str = "Agente IA", id_autor: int = 0) -> None:
        super().__init__(nombre)
        self._llm: LLM = llm
        self._id_autor: int = id_autor

    def respuesta(self, p: Pregunta) -> Respuesta:
        contenido_generado: str = self._llm.generarRespuesta(p)
        return Respuesta(
            aceptado=False,
            id_autor=self._id_autor,
            cuerpo=contenido_generado,
            fecha_publicacion=date.today(),
            pregunta=p,
        )