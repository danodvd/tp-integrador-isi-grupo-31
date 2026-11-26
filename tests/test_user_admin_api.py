from src.db.Database import UsuarioModel
from src.user.RolUsuario import RolUsuario
from src.user.Usuario import Usuario


def test_crear_usuario_general_api(client, app):
    res = client.post(
        "/usuarios",
        json={
            "nombre": "Danilo",
            "email": "danilo@unrc.edu.ar",
            "password": "123",
            "rol": "usuarioGeneral",
        },
    )

    assert res.status_code == 201
    data = res.get_json()
    assert data["nombre"] == "Danilo"
    assert data["rol"] == "usuarioGeneral"

    with app.app_context():
        usuario_db = UsuarioModel.query.filter_by(email="danilo@unrc.edu.ar").first()
        assert usuario_db is not None
        assert usuario_db.rol == "usuarioGeneral"


def test_crear_usuario_admin_y_verificar_rol(client, app):
    res = client.post(
        "/usuarios",
        json={
            "nombre": "Admin ISI",
            "email": "admin@unrc.edu.ar",
            "password": "root",
            "rol": "admin",
        },
    )

    assert res.status_code == 201
    assert res.get_json()["rol"] == "admin"

    admin_dom = Usuario("Admin ISI", "admin@unrc.edu.ar", "root", RolUsuario.ADMIN)
    user_dom = Usuario("User ISI", "user@unrc.edu.ar", "123", RolUsuario.usuarioGeneral)

    assert admin_dom.is_admin() is True
    assert admin_dom.getRol() == RolUsuario.ADMIN
    assert user_dom.is_admin() is False