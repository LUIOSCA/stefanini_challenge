# Stefanini Backend Challenge

Proyecto de ejemplo para la prueba técnica: API REST de gestión de usuarios.

---

**Contenido**

- **Descripción**
- **Requisitos**
- **Instalación y ejecución local**
- **Variables de entorno**
- **Ejemplos de llamadas (cURL)**
- **Pruebas**
- **Despliegue (Supabase / GCP)**
- **Imágenes y Postman**
- **Contacto**

---

## Descripción

API REST construida con FastAPI que implementa CRUD para usuarios. El proyecto está organizado con una estructura modular (DDD-like):

- `app/core/` — configuración, base de datos y logging
- `app/api/v1/users/` — modelos, esquemas, rutas y lógica de acceso a datos del dominio Users

El objetivo es un proyecto profesional, testeable y listo para desplegar en GCP (Cloud Build) o ejecutar localmente con Docker.

## Requisitos

- Python 3.11+ (se probó con 3.13 en el entorno de CI local)
- Virtualenv o venv
- Dependencias: ver `requirements.txt`

## Instalación y ejecución local

1. Clona el repositorio y entra en la carpeta:

```bash
git clone git@github.com:LUIOSCA/stefanini_challenge.git
cd stefanini-backend-challenge
```

2. Crea y activa un entorno virtual, instala dependencias:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\\Scripts\\activate     # Windows PowerShell
pip install -r requirements.txt
```

3. Configura las variables de entorno:
Crea un archivo `.env` basado en `.env.example`:
```bash
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/dbname
# Edita .env y pega la cadena de conexión de Supabase
```

Nota: Si tu contraseña contiene caracteres especiales (p.ej. `*`) debes url-encodificarlos (ej: `*` → `%2A`).

4. Ejecuta la aplicación (uvicorn):

```bash
uvicorn app.main:app --reload
```


La API quedará disponible en `https://stefanini-users-service-1055540780592.us-central1.run.app`. 
La documentación interactiva en `https://stefanini-users-service-1055540780592.us-central1.run.app/docs`.
Accede a la documentación local en: http://localhost:8000/docs

## Variables de entorno relevantes

- `DATABASE_URL` — URL de la BD (ejemplo en `.env.example`):
  - Para SQLAlchemy async: `postgresql+asyncpg://user:pass@host:port/dbname`
  - Para `asyncpg` directo: `postgresql://user:pass@host:port/dbname`
- `LOG_LEVEL` — nivel de log (`INFO`, `DEBUG`, ...)

## Endpoints principales (ejemplos cURL)

Crear usuario

```bash
curl -s -X POST https://stefanini-users-service-1055540780592.us-central1.run.app/users/ \\
  -H "Content-Type: application/json" \\
  -d '{"username":"jdoe","email":"jdoe@example.com","first_name":"John","last_name":"Doe","role":"user","active":true}'
```

Listar usuarios

```bash
curl -s https://stefanini-users-service-1055540780592.us-central1.run.app/users/
```

Obtener usuario por id

```bash
curl -s https://stefanini-users-service-1055540780592.us-central1.run.app/users/b1e9fbb2-aefe-45dc-8757-80104b19c547
```

Actualizar usuario

```bash
curl -s -X PUT https://stefanini-users-service-1055540780592.us-central1.run.app/users/b1e9fbb2-aefe-45dc-8757-80104b19c547 \\
  -H "Content-Type: application/json" \\
  -d '{"first_name":"Jane","role":"admin"}'
```

Eliminar usuario

```bash
curl -s -X DELETE https://stefanini-users-service-1055540780592.us-central1.run.app/users/b1e9fbb2-aefe-45dc-8757-80104b19c547
```

Respuestas de ejemplo:

- OK (200): `{ "detail": "User successfully deleted" }`
- Not found (404): `{ "detail": "User not found" }`
- Invalid UUID (400): `{ "detail": "Invalid user_id" }`

## Pruebas

La suite de tests usa `pytest` y fixtures `pytest-asyncio`.

Ejecutar tests (local):

```bash
.venv\\Scripts\\python.exe -m pytest -v
```

Se incluyen casos de creación, validación de duplicados y flujo CRUD completo.

## Despliegue en producción GCP

Swagger UI: https://stefanini-users-service-1055540780592.us-central1.run.app/docs

Estado CI/CD: El pipeline en Cloud Build garantiza que cada despliegue pase por la suite de pruebas automatizadas.

Supabase (base de datos sql posgresql)

- Crea un proyecto en Supabase y copia la `DATABASE_URL` en `.env`.
- Si usas PgBouncer / pooler, recuerda `connect_args={"statement_cache_size": 0}` en SQLAlchemy para evitar errores duplicados de prepared statements.

GCP / Cloud Build

- El repositorio incluye `Dockerfile` y `cloudbuild.yaml` de ejemplo.
- Para construir y desplegar con Cloud Build (requiere `gcloud` y permisos):

```bash
gcloud builds submit --config cloudbuild.yaml .
```

O construir localmente con Docker:

```bash
docker build -t stefanini-backend-challenge .
docker run -e DATABASE_URL="${DATABASE_URL}" -p 8000:8000 stefanini-backend-challenge
```


Evidencias de Funcionamiento

```markdown
![Postman - Crear usuario](docs/postman.png)
![Supabase - Config](docs/postgresql_supabase.png)
![GCP - Cloud Build](docs/cloud_run_ci_cd.png)
![Pytest](pytest.png)
![Documentación - Swagger](docs/Swagger.png)

```

## Convenciones y notas de calidad

- Se prefieren docstrings (explicativos) sobre comentarios excesivos en línea.
- El logging básico está configurado en `app/core/logger.py` y se integra en `app/main.py`.
- Las pruebas se ejecutan en SQLite temporal para velocidad; la app está preparada para Postgres en producción.

