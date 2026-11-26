import os

from openai import OpenAI
from ..LLM import LLM

class Deepseek(LLM):
    def __init__(self, nombre: str = "DeepSeek"):
        self.nombre = nombre
        self.client = OpenAI(
            api_key=os.environ["DEEPSEEK_API_KEY"],
            base_url="https://api.deepseek.com"
        )

    def generarRespuesta(self, pregunta) -> str:

        texto = f"{pregunta.getTitulo()}\n\n{pregunta.getCuerpo()}"

        response = self.client.chat.completions.create(
            model="deepseek-flash",
            messages=[
                {"role": "user", "content": texto}
            ]
        )
        return (response.choices[0].message.content or "").strip()
