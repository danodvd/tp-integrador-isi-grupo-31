class LLM:
    def generarRespuesta(self, pregunta):
        raise NotImplementedError("Cada IA tiene que implementar este metodo")


class Gemini(LLM):
    def generarRespuesta(self, pregunta):
        return "Respuesta de Gemini a: " + pregunta.getCuerpo()


class ChatGPT(LLM):
    def generarRespuesta(self, pregunta):
        return "Respuesta de ChatGPT a: " + pregunta.getCuerpo()


class Claude(LLM):
    def generarRespuesta(self, pregunta):
        return "Respuesta de Claude a: " + pregunta.getCuerpo()
