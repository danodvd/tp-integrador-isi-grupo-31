import pytest

import src.app.App as app_module
from src.db.Database import db
from src.publication.Categoria import Categoria
from src.publication.Etiqueta import Etiqueta

app_module.app.config.update(
    TESTING=True,
    SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
)
app_module.app.extensions.pop("sqlalchemy", None)
db.init_app(app_module.app)


@pytest.fixture(autouse=True)
def limpiar_estado_dominio():
    Categoria.nombres_usados.clear()
    Etiqueta.nombres_usados.clear()
    yield
    Categoria.nombres_usados.clear()
    Etiqueta.nombres_usados.clear()


@pytest.fixture
def app():
    flask_app = app_module.app
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()