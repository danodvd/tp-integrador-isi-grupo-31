Proyecto Integrador de **Ingeniería de Software I** — Grupo 31.

Aplicación backend desarrollada en Python que modela una comunidad de preguntas y respuestas siguiendo el diagrama de clases UML del dominio, incorporando persistencia relacional en SQLite y generación automática de respuestas mediante distintos proveedores de modelos de lenguaje (LLMs) desacoplados con el patrón **Strategy**.

## Funcionalidades

- **Gestión de usuarios y roles:** Registro de usuarios con roles (`usuarioGeneral` y `admin`) y almacenamiento seguro de contraseñas mediante *hashing* PBKDF2 con *salt* aleatorio.
- **Publicaciones:** Creación y consulta de preguntas y respuestas implementando la interfaz `Publicacion` y la jerarquía de `Autor`.
- **Clasificación:** Asociación de preguntas con una `Categoria` y múltiples `Etiqueta` (relación muchos a muchos) con control de duplicados.
- **Agente de respuestas con IA:** `AgenteDeRespuestasIA` (subclase de `Autor`) recibe cualquier estrategia que implemente `LLM` (`Gemini`, `ChatGPT`, `Claude`, `DeepSeek`, `Grok`, `Copilot` o un proveedor simulado) para generar y enlazar respuestas automáticamente.
- **Persistencia en base de datos:** Mapeo objeto-relacional con SQLAlchemy sobre SQLite (`taller_isi.db`), con creación automática de tablas al iniciar la aplicación.
- **API REST:** Exposición de operaciones principales mediante endpoints HTTP en formato JSON.

## Tecnologías utilizadas

- Python 3.11+
- Flask
- Flask-SQLAlchemy / SQLAlchemy
- SQLite
- Pytest
- SDKs de IA: `google-genai`, `openai`, `anthropic`

## Requisitos e instalación

1. **Clonar el repositorio:**

```bash
git clone <https://github.com/danodvd/tp-integrador-isi-grupo-31>
cd tp-integrador-isi-grupo-31
```

2. **Instalar las dependencias:**

```bash
pip install flask flask-sqlalchemy google-genai openai anthropic pytest
```

*(En distribuciones basadas en Arch Linux, también se pueden instalar desde los repositorios del sistema con `pacman`.)*

3. **Configurar las variables de entorno:**

Exportar la clave del proveedor de IA que se quiera utilizar antes de iniciar el servidor:

```bash
export GEMINI_API_KEY="api-key"
export OPENAI_API_KEY="api-key"
export ANTHROPIC_API_KEY="api-key"
export DEEPSEEK_API_KEY="api-key"
export XAI_API_KEY="api-key"
export COPILOT_API_KEY="api-key"
```

*(Solo es obligatorio definir la variable correspondiente al modelo que se vaya a consultar).*

## Ejecución

Iniciar el servidor de desarrollo desde la carpeta raíz del proyecto:

```bash
python -m src.app.App
```

El servidor quedará escuchando en:

```text
[http://127.0.0.1:5000](http://127.0.0.1:5000)
```

Al ejecutarse por primera vez, SQLAlchemy crea el archivo `taller_isi.db` con todas las tablas necesarias de manera automática.

## API REST

Los endpoints disponibles son:

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/health` | Verificar el estado del servidor |
| `POST` | `/usuarios` | Registrar un nuevo usuario (`nombre`, `email`, `password`, `rol`) |
| `POST` | `/preguntas` | Publicar una pregunta con `categoria` y lista de `etiquetas` opcionales |
| `GET` | `/preguntas/<id>` | Consultar el detalle de una pregunta junto con sus etiquetas y respuestas |
| `POST` | `/preguntas/<id>/responder-ia` | Generar y persistir una respuesta mediante `AgenteDeRespuestasIA` (`{"modelo": "gemini"}`) |

### Ejemplo de uso con `curl`

```bash
# 1. Crear una pregunta
curl -X POST [http://127.0.0.1:5000/preguntas](http://127.0.0.1:5000/preguntas) \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Patrón Strategy en Python",
    "cuerpo": "¿Cómo desacoplar distintos proveedores de LLM?",
    "categoria": "Ingeniería de Software",
    "etiquetas": ["UML", "Patrones"]
  }'

# 2. Generar una respuesta automática con IA
curl -X POST [http://127.0.0.1:5000/preguntas/1/responder-ia](http://127.0.0.1:5000/preguntas/1/responder-ia) \
  -H "Content-Type: application/json" \
  -d '{"modelo": "gemini"}'
```

## Pruebas automatizadas

La suite de tests unitarios y de integración está implementada con `pytest`. Utiliza una base de datos SQLite en memoria (`sqlite:///:memory:`) y proveedores simulados para validar tanto las reglas del dominio como los endpoints sin consumir cuota de API ni modificar `taller_isi.db`.

Ejecutar todas las pruebas desde la raíz:

```bash
python -m pytest -v
```

## Estructura del proyecto

```text
tp-integrador-isi-grupo-31/
├── src/
│   ├── app/
│   │   └── App.py                  # Servidor Flask y definición de endpoints REST
│   ├── db/
│   │   └── Database.py             # Modelos SQLAlchemy y configuración de SQLite
│   ├── ia/
│   │   ├── models/                 # Estrategias concretas de proveedores LLM
│   │   │   ├── ChatGPT.py
│   │   │   ├── Claude.py
│   │   │   ├── Copilot.py
│   │   │   ├── Deepseek.py
│   │   │   ├── Gemini.py
│   │   │   └── Grok.py
│   │   ├── AgenteDeRespuestasIA.py # Agente heredado de Autor que usa Strategy
│   │   └── LLM.py                  # Interfaz abstracta de estrategia LLM
│   ├── publication/
│   │   ├── Categoria.py            # Categoría con control de unicidad
│   │   ├── Etiqueta.py             # Etiqueta con control de unicidad
│   │   ├── Pregunta.py             # Publicación de tipo pregunta
│   │   ├── Publicacion.py          # Interfaz base de publicaciones
│   │   └── Respuesta.py            # Publicación de tipo respuesta
│   ├── user/
│   │   ├── RolUsuario.py           # Enumeración de roles del sistema
│   │   └── Usuario.py              # Usuario con autenticación y hashing PBKDF2
│   └── Autor.py                    # Clase base para autores de publicaciones
├── tests/                          # Pruebas unitarias y de integración con pytest
│   ├── conftest.py
│   ├── test_answers_api.py
│   ├── test_auth_api.py
│   ├── test_categories_tags_api.py
│   ├── test_questions_api.py
│   ├── test_users_admin_api.py
│   └── test_web_integration.py
├── .gitignore
└── README.md
```

## Integrantes — Grupo 31

- **Danilo Valentín Domínguez**
- **Facundo Dorado Escudero**
- **Matías Giannoni** 
