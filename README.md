# Genio Backend — API REST

Backend del proyecto **Genio**, una aplicación de trivia/quiz interactiva. Desarrollado con **Django 4.2** y **Django REST Framework**, con soporte para SQLite en desarrollo y **Azure SQL Server** en producción.

---

## Tabla de Contenidos

- [Tecnologías](#tecnologías)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Configuración e Instalación](#configuración-e-instalación)
- [Variables de Entorno](#variables-de-entorno)
- [Base de Datos](#base-de-datos)
- [Modelos](#modelos)
- [API — Endpoints](#api--endpoints)
  - [Usuarios](#usuarios--apiusuarios)
  - [Categorías](#categorías--apicategorias)
  - [Preguntas](#preguntas--apipreguntas)
  - [Rondas](#rondas--apirondas)
  - [Diseños](#diseños--apidesign)
- [Arquitectura de la Aplicación](#arquitectura-de-la-aplicación)
- [Despliegue en Azure](#despliegue-en-azure)

---

## Tecnologías

| Paquete | Versión | Propósito |
|---|---|---|
| Django | >=4.2, <5.0 | Framework web principal |
| djangorestframework | latest | Construcción de la API REST |
| django-cors-headers | latest | Manejo de CORS |
| django-environ | latest | Gestión de variables de entorno (.env) |
| mssql-django | latest | Soporte para Azure SQL Server |
| pyodbc | latest | Driver ODBC para SQL Server |
| requests | latest | Utilidades HTTP |
| python-dateutil | latest | Parseo de fechas |

---

## Estructura del Proyecto

```
Genio_Backend/
├── manage.py                   # Punto de entrada de comandos Django
├── requirements.txt            # Dependencias del proyecto
├── db.sqlite3                  # Base de datos SQLite (solo desarrollo)
├── core/                       # Configuración central del proyecto
│   ├── settings.py             # Configuración Django (BD, apps, middleware)
│   ├── urls.py                 # Router principal de URLs
│   └── wsgi.py                 # Punto de entrada WSGI
└── apps/                       # Módulos de la aplicación
    ├── categoria/              # Gestión de categorías de preguntas
    ├── usuario/                # Gestión de usuarios y autenticación
    ├── pregunta/               # Banco de preguntas
    ├── ronda/                  # Rondas de juego
    ├── pregunta_ronda/         # Relación intermedia pregunta-ronda
    └── diseno/                 # Diseños y personalización visual
```

Cada módulo en `apps/` sigue la estructura estándar de Django:
```
<app>/
├── models.py       # Definición del modelo de datos
├── serializers.py  # Serialización para la API
├── views.py        # Lógica de negocio (ViewSets)
├── urls.py         # Rutas del módulo
├── admin.py        # Configuración del panel admin
└── migrations/     # Historial de migraciones de BD
```

---

## Configuración e Instalación

### Requisitos previos
- Python 3.10+
- ODBC Driver 18 for SQL Server (solo para producción/Azure)

### Pasos

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd Genio_Backend

# 2. Crear y activar entorno virtual
python -m venv venv
.\venv\Scripts\activate       # Windows
source venv/bin/activate      # Linux/macOS

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear el archivo .env en la raíz del proyecto (ver sección Variables de Entorno)

# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear superusuario (opcional)
python manage.py createsuperuser

# 7. Iniciar el servidor de desarrollo
python manage.py runserver
```

---

## Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu_clave_secreta_django
DEBUG=True

# Solo necesario para producción con Azure SQL
DB_NAME=nombre_base_de_datos
DB_HOST=servidor.database.windows.net
```

> En desarrollo, si `WEBSITE_HOSTNAME` no está definido (no es Azure), la aplicación usa **SQLite** automáticamente.

---

## Base de Datos

La aplicación detecta automáticamente el entorno y selecciona la base de datos correspondiente:

| Entorno | Motor | Descripción |
|---|---|---|
| **Desarrollo** | `django.db.backends.sqlite3` | Archivo local `db.sqlite3` |
| **Producción (Azure)** | `mssql` | Azure SQL Server con Managed Identity |

### Configuración de producción (Azure SQL)
- **Motor**: `mssql` con ODBC Driver 18
- **Esquema**: `genio`
- **Autenticación**: `ActiveDirectoryMsi` (Managed Identity, sin contraseña)
- **Puerto**: `1433`

---

## Modelos

### `tbl_categoria` — Categorías

| Campo | Tipo | Descripción |
|---|---|---|
| `id_categoria` | AutoField (PK) | Identificador único |
| `nombre` | CharField(100) | Nombre de la categoría (único) |
| `descripcion` | TextField | Descripción |
| `puntaje` | FloatField | Puntos por respuesta correcta |
| `tiempo_limite` | IntegerField | Segundos por pregunta (default: 10) |

---

### `tbl_usuario` — Usuarios

| Campo | Tipo | Descripción |
|---|---|---|
| `id_usuarios` | AutoField (PK) | Identificador único |
| `identificador` | CharField(100) | Nombre o alias (único) |
| `correo` | EmailField(255) | Correo electrónico (único) |
| `telefono` | CharField(20) | Teléfono (único, opcional) |
| `estado` | BooleanField | Activo/Inactivo (default: True) |
| `fecha_creacion` | DateTimeField | Fecha de registro (auto) |
| `permisos` | BooleanField | Permisos administrativos (default: False) |
| `codigo_diseno` | CharField(20) | Código del diseño asignado |

---

### `tbl_preguntas` — Preguntas

| Campo | Tipo | Descripción |
|---|---|---|
| `id_pregunta` | AutoField (PK) | Identificador único |
| `id_categoria` | ForeignKey → `tbl_categoria` | Categoría de la pregunta |
| `codigo` | CharField(20) | Código de diseño asociado (indexado) |
| `pregunta` | TextField | Texto de la pregunta |
| `respuesta_correcta` | BooleanField | Verdadero/Falso |
| `explicacion` | TextField | Explicación de la respuesta |

---

### `tbl_rondas` — Rondas de Juego

| Campo | Tipo | Descripción |
|---|---|---|
| `id_ronda` | AutoField (PK) | Identificador único |
| `id_usuarios` | ForeignKey → `tbl_usuario` | Usuario que jugó |
| `puntaje_total` | FloatField | Puntaje obtenido en la ronda |
| `fecha_jugado` | DateTimeField | Fecha/hora de la partida (auto) |
| `preguntas` | ManyToManyField (through) | Preguntas jugadas via `tbl_pregunta_ronda` |

---

### `tbl_pregunta_ronda` — Relación Pregunta-Ronda (tabla intermedia)

| Campo | Tipo | Descripción |
|---|---|---|
| `pregunta` | ForeignKey → `tbl_preguntas` | Pregunta asociada |
| `ronda` | ForeignKey → `tbl_rondas` | Ronda asociada |
| `estado_respuesta` | BooleanField | Si fue respondida correctamente |
| `fecha_respondida` | DateTimeField | Timestamp de la respuesta (auto) |

> Restricción única: `(pregunta, ronda)` — una pregunta no puede repetirse en la misma ronda.

---

### `tbl_disenos` — Diseños / Temas Visuales

| Campo | Tipo | Descripción |
|---|---|---|
| `code` | CharField(20) (PK) | Código único del diseño |
| `nombre` | CharField(100) | Nombre del diseño |
| `color_primario` | CharField(20) | Color principal (hex) |
| `fuente` | CharField(100) | Fuente tipográfica |
| `fondo_nombre_archivo` | CharField(255) | Nombre del archivo de fondo |
| `fondo_url` | TextField | URL o Base64 del fondo |
| `logo_nombre_archivo` | CharField(255) | Nombre del archivo de logo |
| `logo_url` | TextField | URL o Base64 del logo |
| `fecha_expiracion` | BigIntegerField | Expiración en timestamp ms (nullable) |
| `app_titulo` | CharField(200) | Título de la app |
| `app_subtitulo` | CharField(200) | Subtítulo de la app |
| `app_tagline` | TextField | Tagline descriptivo |
| `icono_victoria_url` | TextField | Icono de victoria (URL) |
| `icono_fallaste_url` | TextField | Icono de derrota (URL) |
| `icono_v_url` | TextField | Icono respuesta correcta (URL) |
| `icono_f_url` | TextField | Icono respuesta incorrecta (URL) |
| `created_at` | BigIntegerField | Creación en timestamp ms |
| `updated_at` | BigIntegerField | Última actualización en timestamp ms |

---

### `tbl_preguntas_diseno` — Preguntas de un Diseño

| Campo | Tipo | Descripción |
|---|---|---|
| `diseno` | ForeignKey → `tbl_disenos` | Diseño al que pertenece |
| `pregunta_id` | IntegerField | ID local asignado por el frontend |
| `pregunta` | TextField | Texto de la pregunta |
| `respuesta` | BooleanField | Verdadero/Falso |
| `explicacion` | TextField | Explicación |
| `categoria` | IntegerField | Categoría numérica (default: 1) |

> Restricción única: `(diseno, pregunta_id)`.

---

## API — Endpoints

URL base de producción: `https://geniobackend-faawf6f0hbewfdbj.centralus-01.azurewebsites.net`

Panel de administración: `/admin/`

---

### Usuarios — `/api/usuarios/`

#### `GET /api/usuarios/`
Lista todos los usuarios registrados.

**Respuesta `200`:**
```json
[
  {
    "id_usuarios": 1,
    "identificador": "juan123",
    "correo": "juan@example.com",
    "telefono": "5551234567",
    "estado": true,
    "fecha_creacion": "2024-01-15T10:00:00Z",
    "permisos": false,
    "codigo_diseno": "DKPWLA"
  }
]
```

---

#### `POST /api/usuarios/`
Crea un nuevo usuario.

**Body:**
```json
{
  "identificador": "juan123",
  "correo": "juan@example.com",
  "telefono": "5551234567",
  "permisos": false,
  "codigo_diseno": "DKPWLA"
}
```

---

#### `GET /api/usuarios/{id}/`
Obtiene un usuario por ID.

---

#### `PUT/PATCH /api/usuarios/{id}/`
Actualiza un usuario.

---

#### `DELETE /api/usuarios/{id}/`
Elimina un usuario.

---

#### `POST /api/usuarios/login_simple/`
Busca un usuario por correo electrónico (login básico sin contraseña).

**Body:**
```json
{ "email": "juan@example.com" }
```

**Respuesta `200`:**
```json
{
  "id_usuarios": 1,
  "identificador": "juan123",
  "correo": "juan@example.com"
}
```

**Respuesta `404`:**
```json
{ "error": "Usuario no encontrado" }
```

---

#### `POST /api/usuarios/acceso_directo/`
Login con registro automático. Si el usuario no existe, lo crea. Si ya existe y viene `codigo_diseno`, lo actualiza.

**Body:**
```json
{
  "email": "juan@example.com",
  "identificador": "juan123",
  "telefono": "5551234567",
  "recibir_apostemos": false,
  "codigo_diseno": "DKPWLA"
}
```

**Respuesta `200` (usuario existente) / `201` (usuario nuevo):**
```json
{
  "id_usuarios": 1,
  "identificador": "juan123",
  "correo": "juan@example.com",
  "codigo_diseno": "DKPWLA",
  "nuevo_registro": false
}
```

---

#### `POST /api/usuarios/{id}/desactivar/`
Desactiva la cuenta de un usuario (establece `estado = False`).

**Respuesta `200`:**
```json
{ "message": "Cuenta desactivada correctamente" }
```

---

#### `GET /api/usuarios/{id}/rondas/`
Obtiene todas las rondas jugadas por un usuario específico.

---

#### `GET /api/usuarios/ranking/`
Retorna el top 20 de jugadores y la posición del usuario actual (opcional).

**Query Params:**

| Parámetro | Tipo | Descripción |
|---|---|---|
| `user_id` | int | (Opcional) ID del usuario para incluir su posición |

**Respuesta `200`:**
```json
{
  "top_20": [
    {
      "rank": 1,
      "name": "juan123",
      "score": 850.0,
      "avatarIcon": "person",
      "avatarColor": "#13ec5b"
    }
  ],
  "user_rank": {
    "rank": 5,
    "name": "pedro456",
    "score": 600.0
  }
}
```

---

### Categorías — `/api/categorias/`

CRUD estándar sobre `tbl_categoria`.

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/categorias/` | Lista todas las categorías |
| POST | `/api/categorias/` | Crea una categoría |
| GET | `/api/categorias/{id}/` | Obtiene una categoría |
| PUT/PATCH | `/api/categorias/{id}/` | Actualiza una categoría |
| DELETE | `/api/categorias/{id}/` | Elimina una categoría |

**Ejemplo de objeto categoría:**
```json
{
  "id_categoria": 1,
  "nombre": "Historia",
  "descripcion": "Preguntas sobre historia mundial",
  "puntaje": 10.0,
  "tiempo_limite": 15
}
```

---

### Preguntas — `/api/preguntas/`

#### `GET /api/preguntas/`
Lista todas las preguntas. Acepta filtro por código de diseño:

**Query Params:**

| Parámetro | Tipo | Descripción |
|---|---|---|
| `codigo` | string | Filtra por código de diseño (se normaliza a mayúsculas) |

```
GET /api/preguntas/?codigo=DKPWLA
```

---

#### `POST /api/preguntas/`
Crea una pregunta individual.

---

#### `GET/PUT/PATCH/DELETE /api/preguntas/{id}/`
Operaciones CRUD estándar sobre una pregunta.

---

#### `POST /api/preguntas/sync/`
Sincroniza (reemplaza) **todas** las preguntas de un código de diseño en una sola operación atómica (delete + bulk insert).

**Body:**
```json
{
  "code": "DKPWLA",
  "preguntas": [
    {
      "id": 1,
      "pregunta": "¿La Tierra es redonda?",
      "respuesta": true,
      "explicacion": "La Tierra tiene forma geoide.",
      "categoria": 1
    }
  ]
}
```

**Respuesta `200`:**
```json
{
  "success": true,
  "code": "DKPWLA",
  "preguntasGuardadas": 1,
  "preguntas": [
    {
      "id": 42,
      "codigo": "DKPWLA",
      "pregunta": "¿La Tierra es redonda?",
      "respuesta": true,
      "explicacion": "La Tierra tiene forma geoide.",
      "categoria": 1
    }
  ]
}
```

---

### Rondas — `/api/rondas/`

#### `POST /api/rondas/iniciar_juego/`
Inicia una nueva ronda de juego. Selecciona 10 preguntas aleatorias de la categoría indicada, crea la ronda y registra las preguntas en la tabla intermedia.

**Body:**
```json
{
  "id_usuario": 1,
  "id_categoria": 2,
  "codigo": "DKPWLA"
}
```

> Si `codigo` se omite o está vacío, se usan preguntas globales (sin código).  
> Se requieren exactamente **10 preguntas** disponibles; si hay menos, retorna error.

**Respuesta `201`:**
```json
{
  "ronda_id": 15,
  "preguntas": [
    {
      "id_pregunta": 42,
      "codigo": "DKPWLA",
      "pregunta": "¿La Tierra es redonda?",
      "respuesta_correcta": true,
      "explicacion": "La Tierra tiene forma geoide."
    }
  ],
  "puntos_categoria": 10.0,
  "tiempo_categoria": 15
}
```

---

#### `PATCH /api/rondas/{id}/finalizar/`
Finaliza una ronda guardando el puntaje total obtenido.

**Body:**
```json
{ "puntaje_total": 80.0 }
```

**Respuesta `200`:**
```json
{ "status": "Ronda actualizada" }
```

---

#### Rutas CRUD estándar de Rondas

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/rondas/` | Lista todas las rondas |
| POST | `/api/rondas/` | Crea una ronda |
| GET | `/api/rondas/{id}/` | Obtiene una ronda |
| PUT/PATCH | `/api/rondas/{id}/` | Actualiza una ronda |
| DELETE | `/api/rondas/{id}/` | Elimina una ronda |

---

### Diseños — `/api/design/`

Gestiona los diseños visuales (temas) de la aplicación. El identificador de cada diseño es su **código** (`code`), no un ID numérico.

---

#### `POST /api/design/sync/`
Operación principal. Sincroniza un diseño completo con todas sus preguntas. Realiza un upsert del diseño y reemplaza todas sus preguntas (delete + bulk insert) en una transacción atómica.

**Body:**
```json
{
  "code": "DKPWLA",
  "payload": {
    "code": "DKPWLA",
    "nombre_diseno": "Tema Corporativo",
    "color_primario": "#FF5733",
    "fuente": "Roboto",
    "fondo_url_o_base64": "https://cdn.example.com/fondo.jpg",
    "fondo_nombre_archivo": "fondo.jpg",
    "logo_url_o_base64": "https://cdn.example.com/logo.png",
    "logo_nombre_archivo": "logo.png",
    "fecha_expiracion": 1893456000000,
    "app_titulo": "Trivia Express",
    "app_subtitulo": "¿Cuánto sabes?",
    "app_tagline": "El juego de preguntas más rápido",
    "icono_victoria_url": "https://cdn.example.com/win.png",
    "icono_fallaste_url": "https://cdn.example.com/lose.png",
    "icono_v_url": "https://cdn.example.com/correct.png",
    "icono_f_url": "https://cdn.example.com/wrong.png",
    "preguntas": [
      {
        "id": 1,
        "pregunta": "¿La Tierra es redonda?",
        "respuesta": true,
        "explicacion": "La Tierra tiene forma geoide.",
        "categoria": 1
      }
    ]
  },
  "queuedAt": 1700000000000,
  "status": "PENDING"
}
```

**Respuesta `200`:**
```json
{
  "success": true,
  "code": "DKPWLA",
  "message": "Diseño sincronizado exitosamente.",
  "preguntasGuardadas": 1,
  "timestamp": 1700000000123
}
```

---

#### `GET /api/design/{code}/`
Obtiene un diseño completo con sus preguntas anidadas.

**Respuesta `200`:**
```json
{
  "code": "DKPWLA",
  "nombre": "Tema Corporativo",
  "color_primario": "#FF5733",
  "fuente": "Roboto",
  "fondo_url": "https://...",
  "logo_url": "https://...",
  "app_titulo": "Trivia Express",
  "app_subtitulo": "¿Cuánto sabes?",
  "app_tagline": "El juego de preguntas más rápido",
  "preguntas": [
    {
      "id": 1,
      "pregunta": "¿La Tierra es redonda?",
      "respuesta": true,
      "explicacion": "La Tierra tiene forma geoide.",
      "categoria": 1
    }
  ]
}
```

---

#### `DELETE /api/design/{code}/`
Elimina un diseño y sus preguntas (cascade).

---

#### `GET /api/design/{code}/questions/`
Lista todas las preguntas de un diseño, ordenadas por `pregunta_id`.

**Respuesta `200`:**
```json
{
  "success": true,
  "code": "DKPWLA",
  "preguntas": [
    {
      "id": 1,
      "pregunta": "¿La Tierra es redonda?",
      "respuesta": true,
      "explicacion": "La Tierra tiene forma geoide.",
      "categoria": 1
    }
  ]
}
```

---

#### `PUT /api/design/{code}/questions/`
Reemplaza todas las preguntas de un diseño (delete + bulk insert).

**Body:** Lista de preguntas (mismo formato que en `sync`).

---

## Arquitectura de la Aplicación

```
Frontend (App móvil / Web)
        │
        │  HTTP/HTTPS (JSON)
        ▼
┌─────────────────────────────────┐
│         Django REST API         │
│                                 │
│  /api/usuarios/   UsuariosViewSet  │
│  /api/categorias/ CategoriaViewSet │
│  /api/preguntas/  PreguntasViewSet │
│  /api/rondas/     RondasViewSet    │
│  /api/design/     DisenioViewSet   │
└────────────┬────────────────────┘
             │  Django ORM
             ▼
┌─────────────────────────────────┐
│          Base de Datos          │
│                                 │
│  Dev:  SQLite (db.sqlite3)      │
│  Prod: Azure SQL Server         │
│        (esquema: genio)         │
└─────────────────────────────────┘
```

### Flujo de una partida

```
1. Frontend llama POST /api/rondas/iniciar_juego/
   → Se crean 10 preguntas aleatorias filtradas por categoría y código
   → Se crea tbl_rondas con puntaje_total = 0
   → Se crean 10 registros en tbl_pregunta_ronda
   → Retorna ronda_id + preguntas + tiempo + puntos por pregunta

2. Usuario responde preguntas en el frontend (lógica local)

3. Frontend llama PATCH /api/rondas/{ronda_id}/finalizar/
   → Se guarda el puntaje total en tbl_rondas

4. Frontend llama GET /api/usuarios/ranking/ para mostrar tabla de posiciones
```

---

## Despliegue en Azure

La aplicación está desplegada en **Azure App Service**:

- **URL de producción**: `https://geniobackend-faawf6f0hbewfdbj.centralus-01.azurewebsites.net`
- **Base de datos**: Azure SQL Server con autenticación por Managed Identity (sin contraseñas en código)
- **Detección de entorno**: Automática mediante la variable `WEBSITE_HOSTNAME` (presente solo en App Service)

### Comandos útiles post-despliegue

```bash
# Aplicar migraciones en producción
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic --noinput
```
