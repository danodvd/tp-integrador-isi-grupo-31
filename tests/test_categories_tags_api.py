import pytest

from src.db.Database import CategoriaModel, EtiquetaModel
from src.publication.Categoria import Categoria
from src.publication.Etiqueta import Etiqueta


def test_reutilizacion_de_categorias_y_etiquetas_en_api(client, app):
    client.post(
        "/preguntas",
        json={
            "titulo": "Pregunta 1",
            "cuerpo": "Cuerpo 1",
            "categoria": "Ingeniería de Software",
            "etiquetas": ["UML", "Python"],
        },
    )
    client.post(
        "/preguntas",
        json={
            "titulo": "Pregunta 2",
            "cuerpo": "Cuerpo 2",
            "categoria": "Ingeniería de Software",
            "etiquetas": ["Python", "Flask"],
        },
    )

    with app.app_context():
        assert CategoriaModel.query.count() == 1
        assert EtiquetaModel.query.count() == 3


def test_dominio_rechaza_categorias_y_etiquetas_duplicadas():
    cat = Categoria("Bases de Datos")
    etq = Etiqueta("SQLAlchemy")

    assert cat.getNombre() == "Bases de Datos"
    assert etq.getNombre() == "SQLAlchemy"

    with pytest.raises(ValueError):
        Categoria("Bases de Datos")

    with pytest.raises(ValueError):
        Etiqueta("SQLAlchemy")