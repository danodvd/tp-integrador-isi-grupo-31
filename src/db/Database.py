from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

pregunta_etiqueta = db.Table(
    "pregunta_etiqueta",
    db.Column("pregunta_id", db.Integer, db.ForeignKey("preguntas.id"), primary_key=True),
    db.Column("etiqueta_id", db.Integer, db.ForeignKey("etiquetas.id"), primary_key=True),
)


class UsuarioModel(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.LargeBinary, nullable=False)
    salt = db.Column(db.LargeBinary, nullable=False)
    rol = db.Column(db.String(30), nullable=False)


class CategoriaModel(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    preguntas = db.relationship("PreguntaModel", back_populates="categoria")


class EtiquetaModel(db.Model):
    __tablename__ = "etiquetas"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    preguntas = db.relationship(
        "PreguntaModel", secondary=pregunta_etiqueta, back_populates="etiquetas"
    )


class PreguntaModel(db.Model):
    __tablename__ = "preguntas"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    cuerpo = db.Column(db.Text, nullable=False)
    fecha_publicacion = db.Column(db.Date, default=date.today, nullable=False)

    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=True)
    categoria = db.relationship("CategoriaModel", back_populates="preguntas")

    etiquetas = db.relationship(
        "EtiquetaModel", secondary=pregunta_etiqueta, back_populates="preguntas"
    )
    respuestas = db.relationship(
        "RespuestaModel", back_populates="pregunta", cascade="all, delete-orphan"
    )


class RespuestaModel(db.Model):
    __tablename__ = "respuestas"

    id = db.Column(db.Integer, primary_key=True)
    cuerpo = db.Column(db.Text, nullable=False)
    aceptado = db.Column(db.Boolean, default=False, nullable=False)
    fecha_publicacion = db.Column(db.Date, default=date.today, nullable=False)
    id_autor = db.Column(db.Integer, nullable=False)
    nombre_autor = db.Column(db.String(100), nullable=False)

    pregunta_id = db.Column(db.Integer, db.ForeignKey("preguntas.id"), nullable=False)
    pregunta = db.relationship("PreguntaModel", back_populates="respuestas")