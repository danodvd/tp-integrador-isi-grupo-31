from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.publication.Pregunta import Pregunta
    
class LLM(ABC):

    @abstractmethod
    def generarRespuesta(self, pregunta) -> str:
        pass