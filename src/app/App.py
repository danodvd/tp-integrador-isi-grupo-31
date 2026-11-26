from datetime import date
from flask import Flask, jsonify, request
from sqlalchemy.exc import IntegrityError

from src.db.Database import (
    CategoriaModel,
    EtiquetaModel,
    PreguntaModel,
    RespuestaModel,
    UsuarioModel,
    db,
)
from src.ia.AgenteDeRespuestasIA import AgenteDeRespuestasIA
from src.ia.models.ChatGPT import ChatGPT
from src.ia.models.Claude import Claude
from src.ia.models.Deepseek import Deepseek
from src.ia.models.Gemini import Gemini
from src.ia.models.Grok import Grok
from src.ia.models.Copilot import Copilot
from src.publication.Pregunta import Pregunta
from src.user.RolUsuario import RolUsuario
from src.user.Usuario import Usuario

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taller_isi.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


def seleccionar_llm(proveedor: str):
    proveedores = {
        "gemini": Gemini,
        "chatgpt": ChatGPT,
        "claude": Claude,
        "deepseek": Deepseek,
        "grok": Grok,
        "copilot": Copilot
    }
    clase_llm = proveedores.get(proveedor.lower())
    if not clase_llm:
        raise ValueError(f"Proveedor no soportado: {proveedor}")
    return clase_llm()


@app.post("/usuarios")
def crear_usuario():
    data = request.get_json() or {}
    try:
        rol = RolUsuario(data.get("rol", "usuarioGeneral"))
        usuario_dom = Usuario(
            nombre=data["nombre"],
            email=data["email"],
            password=data["password"],
            rol=rol,
        )
    except (KeyError, ValueError) as e:
        return jsonify({"error": f"Datos inválidos: {e}"}), 400

    nuevo = UsuarioModel(
        nombre=usuario_dom.getNombre(),
        email=usuario_dom.email,
        password_hash=usuario_dom._password_hash,
        salt=usuario_dom._salt,
        rol=rol.value,
    )
    try:
        db.session.add(nuevo)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "El email ya está registrado"}), 409

    return jsonify({"id": nuevo.id, "nombre": nuevo.nombre, "rol": nuevo.rol}), 201


@app.post("/preguntas")
def crear_pregunta():
    data = request.get_json() or {}
    if not data.get("titulo") or not data.get("cuerpo"):
        return jsonify({"error": "titulo y cuerpo son obligatorios"}), 400

    categoria = None
    if data.get("categoria"):
        categoria = CategoriaModel.query.filter_by(nombre=data["categoria"]).first()
        if not categoria:
            categoria = CategoriaModel(nombre=data["categoria"])
            db.session.add(categoria)

    etiquetas = []
    for nombre_etq in data.get("etiquetas", []):
        etq = EtiquetaModel.query.filter_by(nombre=nombre_etq).first()
        if not etq:
            etq = EtiquetaModel(nombre=nombre_etq)
            db.session.add(etq)
        etiquetas.append(etq)

    nueva_pregunta = PreguntaModel(
        titulo=data["titulo"],
        cuerpo=data["cuerpo"],
        fecha_publicacion=date.today(),
        categoria=categoria,
        etiquetas=etiquetas,
    )
    db.session.add(nueva_pregunta)
    db.session.commit()

    return jsonify({"id": nueva_pregunta.id, "titulo": nueva_pregunta.titulo}), 201


@app.post("/preguntas/<int:pregunta_id>/responder-ia")
def responder_con_ia(pregunta_id: int):
    pregunta_db = db.get_or_404(PreguntaModel, pregunta_id)
    data = request.get_json() or {}
    proveedor = data.get("modelo", "gemini")

    pregunta_dom = Pregunta(
        titulo=pregunta_db.titulo,
        cuerpo=pregunta_db.cuerpo,
        fecha_publicacion=pregunta_db.fecha_publicacion,
    )

    try:
        llm = seleccionar_llm(proveedor)
        agente = AgenteDeRespuestasIA(llm=llm, nombre=f"IA ({proveedor})", id_autor=0)
        respuesta_dom = agente.respuesta(pregunta_dom)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except KeyError as e:
        return jsonify({"error": f"Falta variable de entorno para API key: {e}"}), 500

    respuesta_db = RespuestaModel(
        cuerpo=respuesta_dom.cuerpo,
        aceptado=respuesta_dom.aceptado,
        fecha_publicacion=respuesta_dom.fecha_publicacion,
        id_autor=respuesta_dom.id_autor,
        nombre_autor=agente.getNombre(),
        pregunta_id=pregunta_db.id,
    )
    db.session.add(respuesta_db)
    db.session.commit()

    return jsonify({
        "id": respuesta_db.id,
        "autor": respuesta_db.nombre_autor,
        "cuerpo": respuesta_db.cuerpo,
        "fecha": respuesta_db.fecha_publicacion.isoformat(),
    }), 201


@app.get("/preguntas/<int:pregunta_id>")
def obtener_pregunta(pregunta_id: int):
    p = db.get_or_404(PreguntaModel, pregunta_id)
    return jsonify({
        "id": p.id,
        "titulo": p.titulo,
        "cuerpo": p.cuerpo,
        "categoria": p.categoria.nombre if p.categoria else None,
        "etiquetas": [e.nombre for e in p.etiquetas],
        "respuestas": [
            {
                "id": r.id,
                "autor": r.nombre_autor,
                "cuerpo": r.cuerpo,
                "aceptado": r.aceptado,
                "fecha": r.fecha_publicacion.isoformat(),
            }
            for r in p.respuestas
        ],
    })

    @app.patch("/respuestas/<int:respuesta_id>/aceptar")
    def aceptar_respuesta(respuesta_id: int):
        respuesta_db = db.get_or_404(RespuestaModel, respuesta_id)
        respuesta_db.aceptado = True
        db.session.commit()
        return jsonify({"id": respuesta_db.id, "aceptado": respuesta_db.aceptado})


if __name__ == "__main__":
    app.run(debug=True)