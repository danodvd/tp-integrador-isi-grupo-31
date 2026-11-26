import os

from google import genai
from ..LLM import LLM

class Gemini(LLM):
    def __init__(self, nombre: str = "Gemini"):
        self.nombre = nombre
        self.client = genai.Client(
            api_key=os.environ["GEMINI_API_KEY"]
        )

    def generarRespuesta(self, pregunta) -> str:

        texto = f"{pregunta.getTitulo()}\n\n{pregunta.getCuerpo()}"

        response = self.client.interactions.create(
            model="gemini-4-hydrogen",
            input=texto
        )
        return (response.output_text or "").strip()
