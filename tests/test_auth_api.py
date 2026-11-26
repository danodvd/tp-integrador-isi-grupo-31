import hmac
import pytest

from src.db.Database import UsuarioModel
from src.user.RolUsuario import RolUsuario
from src.user.Usuario import Usuario


def test_autenticacion_usuario_dominio():
    usuario = Usuario("Ada", "ada@unrc.edu.ar", "secreto123", RolUsuario.usuarioGeneral)

    assert usuario.autenticar("ada@unrc.edu.ar", "secreto123") is True
    assert usuario.autenticar("ada@unrc.edu.ar", "clave_mala") is False
    assert usuario.autenticar("otro@unrc.edu.ar", "secreto123") is False

    with pytest.raises(AttributeError):
        _ = usuario.password


def test_hash_persistido_en_db_corresponde_a_password(client, app):
    client.post(
        "/usuarios",
        json={
            "nombre": "Grace",
            "email": "grace@unrc.edu.ar",
            "password": "hopper_pass",
        },
    )

    with app.app_context():
        usuario_db = UsuarioModel.query.filter_by(email="grace@unrc.edu.ar").first()
        assert usuario_db is not None
        hash_calculado = Usuario._hash("hopper_pass", usuario_db.salt)
        assert hmac.compare_digest(usuario_db.password_hash, hash_calculado)