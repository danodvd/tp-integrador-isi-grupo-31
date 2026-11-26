from datetime import date

from src.publication.Pregunta import Pregunta
from src.publication.Publicacion import Publicacion


def test_crear_y_obtener_pregunta_api(client):
    res_post = client.post(
        "/preguntas",
        json={
            "titulo": "¿Qué es el patrón Strategy?",
            "cuerpo": "Necesito desacoplar varios proveedores de LLM.",
            "categoria": "Diseño",
            "etiquetas": ["Patrones", "IA"],
        },
    )

    assert res_post.status_code == 201
    pregunta_id = res_post.get_json()["id"]

    res_get = client.get(f"/preguntas/{pregunta_id}")
    assert res_get.status_code == 200
    data = res_get.get_json()
    assert data["titulo"] == "¿Qué es el patrón Strategy?"
    assert data["categoria"] == "Diseño"
    assert set(data["etiquetas"]) == {"Patrones", "IA"}
    assert data["respuestas"] == []


def test_obtener_pregunta_inexistente_devuelve_404(client):
    res = client.get("/preguntas/9999")
    assert res.status_code == 404


def test_pregunta_implementa_publicacion():
    p = Pregunta("Título", "Contenido", date.today())
    assert isinstance(p, Publicacion)
    assert p.getTitulo() == "Título"
    assert p.getCuerpo() == "Contenido"