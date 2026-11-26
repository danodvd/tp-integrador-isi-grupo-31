import os

from openai import OpenAI
from ..LLM import LLM


class ChatGPT(LLM):

    def __init__(self, nombre: str = "ChatGPT"):
        self.client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"]
        )
        self.nombre = nombre

    def generarRespuesta(self, pregunta) -> str:

        texto = f"{pregunta.getTitulo()}\n\n{pregunta.getCuerpo()}"

        response = self.client.responses.create(
            model="gpt-6.2-sol",
            input=texto
        )

        return (response.output_text or "").strip()