Read [](file:///c%3A/Users/garodriguez/OneDrive%20-%20Canadian%20Bank%20Note%20Company%2C%20Ltd/Escritorio/Genio/Genio_Backend/core/urls.py)

Read [](file:///c%3A/Users/garodriguez/OneDrive%20-%20Canadian%20Bank%20Note%20Company%2C%20Ltd/Escritorio/Genio/Genio_Backend/apps/ronda/urls.py)

Read [](file:///c%3A/Users/garodriguez/OneDrive%20-%20Canadian%20Bank%20Note%20Company%2C%20Ltd/Escritorio/Genio/Genio_Backend/apps/categoria/urls.py)

Read [](file:///c%3A/Users/garodriguez/OneDrive%20-%20Canadian%20Bank%20Note%20Company%2C%20Ltd/Escritorio/Genio/Genio_Backend/apps/usuario/urls.py)

Read [](file:///c%3A/Users/garodriguez/OneDrive%20-%20Canadian%20Bank%20Note%20Company%2C%20Ltd/Escritorio/Genio/Genio_Backend/apps/categoria/views.py)

Read [](file:///c%3A/Users/garodriguez/OneDrive%20-%20Canadian%20Bank%20Note%20Company%2C%20Ltd/Escritorio/Genio/Genio_Backend/apps/usuario/views.py#1-1), lines 1 to 80

Read [](file:///c%3A/Users/garodriguez/OneDrive%20-%20Canadian%20Bank%20Note%20Company%2C%20Ltd/Escritorio/Genio/Genio_Backend/apps/pregunta_ronda/views.py)

Read [](file:///c%3A/Users/garodriguez/OneDrive%20-%20Canadian%20Bank%20Note%20Company%2C%20Ltd/Escritorio/Genio/Genio_Backend/apps/usuario/views.py#50-50), lines 50 to 80

Read [](file:///c%3A/Users/garodriguez/OneDrive%20-%20Canadian%20Bank%20Note%20Company%2C%20Ltd/Escritorio/Genio/Genio_Backend/apps/usuario/views.py#110-110), lines 110 to 127

Aquí tienes el resumen completo de todos los endpoints:

---

## API Endpoints — Genio Backend

**Base URL:** `https://geniobackend-faawf6f0hbewfdbj.centralus-01.azurewebsites.net`

---

### 👤 USUARIOS — `/api/usuarios/`

| Método | URL | Qué hace |
|---|---|---|
| `POST` | `/api/usuarios/acceso_directo/` | Login + registro automático. Crea usuario si no existe. **Úsalo para el flujo de entrada del jugador.** |
| `POST` | `/api/usuarios/login_simple/` | Busca usuario por email. Solo lectura. |
| `GET` | `/api/usuarios/{id}/rondas/` | Historial de rondas de un usuario. |
| `POST` | `/api/usuarios/{id}/desactivar/` | Desactiva la cuenta del usuario. |
| `GET` | `/api/usuarios/ranking/?user_id={id}` | Top 20 + posición del usuario dado. |

**Payload `acceso_directo`:**
```json
POST /api/usuarios/acceso_directo/
{
  "email": "jugador@mail.com",
  "identificador": "Carlos",
  "telefono": "5551234567",
  "recibir_apostemos": false
}
```
**Respuesta:**
```json
{ "id_usuarios": 3, "identificador": "Carlos", "correo": "jugador@mail.com", "nuevo_registro": true }
```

---

### 🏷️ CATEGORÍAS — `/api/categorias/`

| Método | URL | Qué hace |
|---|---|---|
| `GET` | `/api/categorias/` | Lista todas las categorías (nombre, puntaje, tiempo_limite). |
| `GET` | `/api/categorias/{id}/` | Detalle de una categoría. |

---

### 🎮 RONDAS — `/api/rondas/`

| Método | URL | Qué hace |
|---|---|---|
| `POST` | `/api/rondas/iniciar_juego/` | Crea una ronda y devuelve 10 preguntas aleatorias. |
| `PATCH` | `/api/rondas/{id}/finalizar/` | Guarda el puntaje final de la ronda. |

**Payload `iniciar_juego`:**
```json
POST /api/rondas/iniciar_juego/
{ "id_usuario": 3, "id_categoria": 1 }
```
**Respuesta:**
```json
{
  "ronda_id": 12,
  "preguntas": [ { "id_pregunta": 5, "pregunta": "...", "respuesta_correcta": true, "explicacion": "..." } ],
  "puntos_categoria": 10.0,
  "tiempo_categoria": 15
}
```

**Payload `finalizar`:**
```json
PATCH /api/rondas/12/finalizar/
{ "puntaje_total": 80.5 }
```

---

### ❓ PREGUNTAS DEL JUEGO — `/api/preguntas/`

| Método | URL | Qué hace |
|---|---|---|
| `GET` | `/api/preguntas/?codigo=DKPWLA` | Lista preguntas de un código de diseño. |
| `POST` | `/api/preguntas/sync/` | **Inserta** preguntas a un código (no borra las existentes). |

**Payload `sync`:**
```json
POST /api/preguntas/sync/
{
  "code": "DKPWLA",
  "preguntas": [
    { "id": 1, "pregunta": "¿...?", "respuesta": true, "explicacion": "...", "categoria": 1 }
  ]
}
```
**Respuesta:**
```json
{ "success": true, "code": "DKPWLA", "preguntasGuardadas": 1, "preguntas": [...] }
```

---

### 🎨 DISEÑOS — `/api/design/`

| Método | URL | Qué hace |
|---|---|---|
| `POST` | `/api/design/sync/` | Upsert completo de diseño (colores, fuente, fondo, logo) + reemplaza todas sus preguntas. |
| `GET` | `/api/design/{code}/` | Carga diseño completo con sus preguntas. |
| `DELETE` | `/api/design/{code}/` | Elimina diseño y todas sus preguntas. |
| `GET` | `/api/design/{code}/questions/` | Solo las preguntas del diseño. |
| `PUT` | `/api/design/{code}/questions/` | Reemplaza todas las preguntas del diseño. |

**Payload `design/sync/`** (diseño completo):
```json
POST /api/design/sync/
{
  "code": "ABC123",
  "payload": {
    "code": "ABC123",
    "nombre_diseno": "Banco Central",
    "color_primario": "#f5821f",
    "fuente": "Plus Jakarta Sans",
    "preguntas": [ { "id": 1, "pregunta": "...", "respuesta": true, "explicacion": "...", "categoria": 1 } ],
    "fondo_url_o_base64": "data:image/jpeg;base64,...",
    "fondo_nombre_archivo": "abc123_fondo.jpg",
    "logo_url_o_base64": "<svg>...</svg>",
    "logo_nombre_archivo": "abc123_logo.svg",
    "fecha_expiracion": 1743339600000
  },
  "queuedAt": 1743339600000,
  "status": "PENDING"
}
```

**Payload `PUT /api/design/{code}/questions/`** (solo preguntas):
```json
[
  { "id": 1, "pregunta": "...", "respuesta": false, "explicacion": "...", "categoria": 1 }
]
```

---

### Cuándo usar cada uno

| Acción del frontend | Endpoint a llamar |
|---|---|
| Jugador entra con Google/email | `POST /api/usuarios/acceso_directo/` |
| Mostrar categorías al jugador | `GET /api/categorias/` |
| Jugador empieza trivia | `POST /api/rondas/iniciar_juego/` |
| Jugador termina trivia | `PATCH /api/rondas/{id}/finalizar/` |
| Mostrar ranking | `GET /api/usuarios/ranking/?user_id={id}` |
| Admin crea/edita diseño | `POST /api/design/sync/` |
| Admin agrega preguntas (CSV/manual) | `POST /api/preguntas/sync/` |
| Admin reemplaza preguntas | `PUT /api/design/{code}/questions/` |
| Cargar diseño existente | `GET /api/design/{code}/` |
| Cargar preguntas de un código | `GET /api/preguntas/?codigo={code}` |