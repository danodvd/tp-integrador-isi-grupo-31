import os

from openai import OpenAI
from ..LLM import LLM

class Grok(LLM):
    def __init__(self, nombre: str = "Grok"):
        self.nombre = nombre
        self.client = OpenAI(
            api_key=os.environ["XAI_API_KEY"],
            base_url="https://api.x.ai/v1"
        )

    def generarRespuesta(self, pregunta) -> str:

        texto = f"{pregunta.getTitulo()}\n\n{pregunta.getCuerpo()}"

        response = self.client.responses.create(
            model="grok-4.7",
            input=texto
        )

        return (response.output_text or "").strip()