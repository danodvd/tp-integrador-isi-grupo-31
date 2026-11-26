import os

from anthropic import Anthropic
from ..LLM import LLM

class Claude(LLM):
    def __init__(self, nombre: str = "Claude"):
        self.nombre = nombre
        self.client =  Anthropic(
            api_key=os.environ["ANTHROPIC_API_KEY"]
        )

    def generarRespuesta(self, pregunta) -> str:

        texto = f"{pregunta.getTitulo()}\n\n{pregunta.getCuerpo()}"

        response = self.client.messages.create(
            model="claude-opus-5-5",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": texto
                }
            ]
        )
        return (response.content[0].text or "").strip()
