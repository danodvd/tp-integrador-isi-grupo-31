import hashlib
import hmac
import os

from autor import Autor
from rol_usuario import RolUsuario


class Usuario(Autor):
    def __init__(self, nombre: str, email: str, password: str, rol: RolUsuario):
        super().__init__(nombre)
        self.email = email
        self._salt = b""
        self._password_hash = None
        self.password = password  # usa el setter (guarda hash)
        self.rol = rol

    @staticmethod
    def _hash(password: str, salt: bytes) -> bytes:
        return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)

    @property
    def password(self):
        raise AttributeError("La contraseña no se puede leer")

    @password.setter
    def password(self, valor) -> None:
        if valor is None:
            self._password_hash = None
            return
        self._salt = os.urandom(16)
        self._password_hash = self._hash(valor, self._salt)

    def is_admin(self) -> bool:
        return self.rol == RolUsuario.ADMIN

    def autenticar(self, email: str, password: str) -> bool:
        if self.email is None or self._password_hash is None or password is None:
            return False
        return (self.email == email and
                hmac.compare_digest(self._password_hash, self._hash(password, self._salt)))
