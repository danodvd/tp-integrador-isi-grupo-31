from datetime import date
import pytest

import src.app.App as app_module
from src.db.Database import RespuestaModel
from src.ia.AgenteDeRespuestasIA import AgenteDeRespuestasIA
from src.ia.LLM import LLM
from src.publication.Pregunta import Pregunta
from src.publication.Respuesta import Respuesta


class MockProvider(LLM):
    def generarRespuesta(self, pregunta) -> str:
        return f"Explicación sobre: {pregunta.getTitulo()}"


def test_responder_con_ia_endpoint(client, app, monkeypatch):
    monkeypatch.setattr(app_module, "seleccionar_llm", lambda _: MockProvider())

    res_p = client.post(
        "/preguntas",
        json={"titulo": "UML y Python", "cuerpo": "¿Cómo modelar herencia?"},
    )
    pregunta_id = res_p.get_json()["id"]

    res_r = client.post(
        f"/preguntas/{pregunta_id}/responder-ia",
        json={"modelo": "gemini"},
    )

    assert res_r.status_code == 201
    data = res_r.get_json()
    assert data["autor"] == "IA (gemini)"
    assert data["cuerpo"] == "Explicación sobre: UML y Python"

    with app.app_context():
        resp_db = RespuestaModel.query.filter_by(pregunta_id=pregunta_id).first()
        assert resp_db is not None
        assert resp_db.aceptado is False


def test_responder_pregunta_inexistente_devuelve_404(client):
    res = client.post("/preguntas/999/responder-ia", json={"modelo": "gemini"})
    assert res.status_code == 404


def test_seleccionar_llm_rechaza_proveedor_desconocido():
    with pytest.raises(ValueError):
        app_module.seleccionar_llm("modelo_inexistente")


def test_agente_y_relacion_bidireccional_dominio():
    pregunta = Pregunta("Polimorfismo", "¿Cómo funciona?", date.today())
    agente = AgenteDeRespuestasIA(llm=MockProvider(), nombre="Bot ISI", id_autor=0)

    respuesta = agente.respuesta(pregunta)

    assert isinstance(respuesta, Respuesta)
    assert respuesta.pregunta is pregunta
    assert respuesta in pregunta.respuestas
    assert agente.getNombre() == "Bot ISI"