import src.app.App as app_module
from src.ia.LLM import LLM


class ProviderSimulado(LLM):
    def __init__(self, etiqueta: str):
        self.etiqueta = etiqueta

    def generarRespuesta(self, pregunta) -> str:
        return f"[{self.etiqueta}] Respuesta a '{pregunta.getTitulo()}'"


def test_flujo_integrado_completo(client, monkeypatch):
    monkeypatch.setattr(
        app_module,
        "seleccionar_llm",
        lambda nombre: ProviderSimulado(nombre.upper()),
    )

    res_user = client.post(
        "/usuarios",
        json={
            "nombre": "Danilo",
            "email": "danilo@integracion.com",
            "password": "123",
            "rol": "usuarioGeneral",
        },
    )
    assert res_user.status_code == 201

    res_preg = client.post(
        "/preguntas",
        json={
            "titulo": "Arquitectura en capas",
            "cuerpo": "¿Cómo separar dominio, persistencia y API?",
            "categoria": "Arquitectura",
            "etiquetas": ["Flask", "SQLAlchemy"],
        },
    )
    assert res_preg.status_code == 201
    pregunta_id = res_preg.get_json()["id"]

    r1 = client.post(f"/preguntas/{pregunta_id}/responder-ia", json={"modelo": "gemini"})
    r2 = client.post(f"/preguntas/{pregunta_id}/responder-ia", json={"modelo": "claude"})
    assert r1.status_code == 201
    assert r2.status_code == 201

    res_detalle = client.get(f"/preguntas/{pregunta_id}")
    assert res_detalle.status_code == 200
    detalle = res_detalle.get_json()

    assert detalle["categoria"] == "Arquitectura"
    assert set(detalle["etiquetas"]) == {"Flask", "SQLAlchemy"}
    assert len(detalle["respuestas"]) == 2
    assert detalle["respuestas"][0]["autor"] == "IA (gemini)"
    assert detalle["respuestas"][1]["autor"] == "IA (claude)"