# Especificación de la API REST
## Portal Empresarial de Atención al Cliente con IA

**Documento:** OpenAPI / REST API Specification  
**Versión:** 1.0  
**Fecha:** Agosto 31, 2026  
**Estado:** ✅ Aprobado para Desarrollo  
**Herramienta:** FastAPI (auto-documentada en /docs y /redoc)

---

## 📋 Índice

1. Información General
2. Autenticación
3. Endpoints Públicos (/tickets)
4. Endpoints Privados (/admin)
5. Códigos de Respuesta HTTP
6. Schemas (Modelos de Datos)
7. Ejemplos de Uso
8. Limitaciones y Rate Limiting

---

## 1️⃣ Información General

### Base URL

```
Desarrollo:   http://localhost:8000
Staging:      https://api-staging.example.com
Producción:   https://api.example.com
```

### Versionamiento

**Versión Actual:** 1.0  
**Esquema de URL:** No versionado (v1 implícito)

### Documentación Interactiva

- **Swagger UI:** `/docs` (http://localhost:8000/docs)
- **ReDoc:** `/redoc` (http://localhost:8000/redoc)
- **OpenAPI Schema:** `/openapi.json`

### Headers Globales

```
Content-Type: application/json
Accept: application/json
Accept-Encoding: gzip, deflate
User-Agent: [Cliente HTTP]
```

### Rate Limiting (Futuro Fase 2)

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1693550400
```

---

## 2️⃣ Autenticación

### Endpoints Públicos (SIN Autenticación)

```
POST /tickets              ✅ Abierto
GET /tickets/{ticket_ref}  ✅ Abierto
POST /tickets/{ref}/mensajes  ✅ Abierto
```

### Endpoints Privados (Requieren Autenticación Fase 2)

```
GET /admin/tickets                           🔐 Requiere Auth
GET /admin/reportes/mensual                  🔐 Requiere Auth
GET /admin/reportes/mensual/insights         🔐 Requiere Auth
GET /admin/reportes/mensual/exportar/excel   🔐 Requiere Auth
GET /admin/reportes/mensual/exportar/pdf     🔐 Requiere Auth
```

### Método de Autenticación (Futuro)

```
Authorization: Bearer {token_jwt}
```

### Health Check (Sin Autenticación)

```
GET /health  ✅ Público
```

---

## 3️⃣ ENDPOINTS PÚBLICOS (/tickets)

---

### 📌 POST /tickets
**Crear Nueva Solicitud**

**Descripción:**  
Crea nueva solicitud (consulta, petición o queja) sin requerir autenticación. La solicitud se procesa automáticamente con IA.

**Método HTTP:** `POST`

**URL:** `/tickets`

**Headers Requeridos:**
```
Content-Type: application/json
```

**Body (Request):**
```json
{
  "cliente": {
    "nombre": "Juan Pérez López",
    "email": "juan.perez@example.com",
    "telefono": "+34 555 123 4567"
  },
  "tipo": "CONSULTA",
  "asunto": "¿Cuál es el horario de atención?",
  "descripcion": "Quisiera saber cuál es el horario de atención al cliente durante la semana..."
}
```

**Campos Requeridos:**
| Campo | Tipo | Validación | Ejemplo |
|-------|------|-----------|---------|
| cliente.nombre | string | Min 2, Max 100 | "Juan Pérez" |
| cliente.email | string | Email válido, unique | "juan@example.com" |
| cliente.telefono | string | Max 20 | "+34 555 123" |
| tipo | enum | CONSULTA, PETICION, QUEJA | "CONSULTA" |
| asunto | string | Min 1, Max 200 | "Horario de atención" |
| descripcion | string | Min 1, Max 5000 | "Descripción detallada..." |

**Response Success (201 Created):**
```json
{
  "id": 1,
  "codigo": "TK-2026-001234",
  "cliente_id": 1,
  "tipo": "CONSULTA",
  "asunto": "¿Cuál es el horario de atención?",
  "descripcion": "Quisiera saber...",
  "estado": "RESUELTO_IA",
  "prioridad": "MEDIA",
  "resuelto_por_ia": true,
  "tiempo_atencion_seg": 45,
  "fecha_creacion": "2026-08-20T14:30:00Z",
  "fecha_resolucion": "2026-08-20T14:30:45Z",
  "satisfaccion": null,
  "cliente": {
    "nombre": "Juan Pérez López",
    "email": "juan.perez@example.com",
    "telefono": "+34 555 123 4567"
  },
  "interacciones": [
    {
      "id": 1,
      "contenido": "¿Cuál es el horario de atención?",
      "rol": "cliente",
      "fecha": "2026-08-20T14:30:00Z"
    },
    {
      "id": 2,
      "contenido": "Nuestro horario es lunes a viernes 9:00-18:00 UTC.",
      "rol": "ia",
      "modelo_ia": "gemini-3.6-flash",
      "tokens_consumidos": 125,
      "fecha": "2026-08-20T14:30:45Z"
    }
  ]
}
```

**Response Errors:**

| Código | Escenario | Body |
|--------|-----------|------|
| **400** | Email inválido | `{"detail": "Email formato inválido"}` |
| **400** | Campo requerido faltante | `{"detail": "Asunto es requerido"}` |
| **400** | Tipo inválido | `{"detail": "tipo debe ser CONSULTA, PETICION o QUEJA"}` |
| **422** | Validación Pydantic falla | `{"detail": [...validation errors]}` |
| **503** | IA y DB no disponible | `{"detail": "Servicio no disponible, intente más tarde"}` |

**Latencia Esperada:**
- P50: ~2 segundos (incluye procesamiento IA)
- P95: ~30 segundos (timeout máximo de IA)
- Espera: Cliente debe esperar respuesta

**Ejemplo cURL:**
```bash
curl -X POST http://localhost:8000/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "cliente": {
      "nombre": "Juan Pérez",
      "email": "juan@example.com",
      "telefono": "+34 555 123"
    },
    "tipo": "CONSULTA",
    "asunto": "Horario",
    "descripcion": "¿Cuál es el horario?"
  }'
```

**Ejemplo Python:**
```python
import requests

url = "http://localhost:8000/tickets"
payload = {
    "cliente": {
        "nombre": "Juan Pérez",
        "email": "juan@example.com",
        "telefono": "+34 555 123"
    },
    "tipo": "CONSULTA",
    "asunto": "Horario",
    "descripcion": "¿Cuál es el horario?"
}

response = requests.post(url, json=payload)
if response.status_code == 201:
    ticket = response.json()
    print(f"Ticket creado: {ticket['codigo']}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

---

### 📌 GET /tickets/{ticket_ref}
**Consultar Ticket (Cliente)**

**Descripción:**  
Obtiene estado completo y conversación de un ticket usando código público.

**Método HTTP:** `GET`

**URL:** `/tickets/TK-2026-001234`

**Parámetros Path:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| ticket_ref | string | Código público (TK-YYYY-XXXXX) o ID numérico |

**Query Parameters:**
```
Ninguno (no hay filtros)
```

**Headers:**
```
(Ninguno requerido)
```

**Response Success (200 OK):**
```json
{
  "id": 1,
  "codigo": "TK-2026-001234",
  "cliente": {
    "nombre": "Juan Pérez López",
    "email": "juan.perez@example.com",
    "telefono": "+34 555 123 4567"
  },
  "tipo": "CONSULTA",
  "asunto": "¿Cuál es el horario de atención?",
  "descripcion": "Quisiera saber cuál es el horario...",
  "estado": "RESUELTO_IA",
  "prioridad": "MEDIA",
  "resuelto_por_ia": true,
  "tiempo_atencion_seg": 45,
  "fecha_creacion": "2026-08-20T14:30:00Z",
  "fecha_resolucion": "2026-08-20T14:30:45Z",
  "satisfaccion": null,
  "interacciones": [
    {
      "id": 1,
      "contenido": "¿Cuál es el horario?",
      "rol": "cliente",
      "fecha": "2026-08-20T14:30:00Z"
    },
    {
      "id": 2,
      "contenido": "Nuestro horario es de 9:00-18:00",
      "rol": "ia",
      "modelo_ia": "gemini-3.6-flash",
      "tokens_consumidos": 125,
      "fecha": "2026-08-20T14:30:45Z"
    }
  ]
}
```

**Response Errors:**

| Código | Escenario |
|--------|-----------|
| **404** | Ticket no encontrado |
| **400** | Parámetro inválido |

**Latencia Esperada:**
- P50: <100ms (índice en código)
- P95: <200ms

**Ejemplo cURL:**
```bash
curl -X GET http://localhost:8000/tickets/TK-2026-001234
```

---

### 📌 POST /tickets/{ticket_ref}/mensajes
**Enviar Mensaje a Ticket**

**Descripción:**  
Permite cliente agregar mensaje adicional a conversación abierta.

**Método HTTP:** `POST`

**URL:** `/tickets/TK-2026-001234/mensajes`

**Parámetros Path:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| ticket_ref | string | Código público o ID numérico |

**Body (Request):**
```json
{
  "mensaje": "Muchas gracias por la información, ¿tenéis más detalles sobre tarifa?"
}
```

**Campos:**
| Campo | Tipo | Validación |
|-------|------|-----------|
| mensaje | string | Min 1, Max 5000 |

**Response Success (200 OK):**
```json
{
  "id": 1,
  "codigo": "TK-2026-001234",
  "cliente": {...},
  "tipo": "CONSULTA",
  "estado": "ESCALADO",  // Permanece escalado
  "interacciones": [
    {...mensajes previos...},
    {
      "id": 4,
      "contenido": "Muchas gracias por...",
      "rol": "cliente",
      "fecha": "2026-08-20T14:35:00Z"
    }
  ]
}
```

**Response Errors:**

| Código | Escenario |
|--------|-----------|
| **404** | Ticket no encontrado |
| **400** | Mensaje vacío o muy largo |
| **422** | Validación falla |

**Latencia Esperada:**
- P50: <200ms

**Ejemplo cURL:**
```bash
curl -X POST http://localhost:8000/tickets/TK-2026-001234/mensajes \
  -H "Content-Type: application/json" \
  -d '{
    "mensaje": "¿Tenéis más detalles?"
  }'
```

---

## 4️⃣ ENDPOINTS PRIVADOS (/admin)

---

### 📌 GET /admin/tickets
**Listar Tickets con Filtros**

**Descripción:**  
Lista tickets con filtros, búsqueda y paginación. Requiere autenticación admin.

**Método HTTP:** `GET`

**URL:** `/admin/tickets`

**Query Parameters:**
| Parámetro | Tipo | Opcional | Default | Validación |
|-----------|------|----------|---------|-----------|
| tipo | enum | ✅ Sí | — | CONSULTA, PETICION, QUEJA |
| estado | enum | ✅ Sí | — | ABIERTO, RESUELTO_IA, ESCALADO, CERRADO |
| prioridad | enum | ✅ Sí | — | BAJA, MEDIA, ALTA |
| fecha_desde | date | ✅ Sí | — | YYYY-MM-DD |
| fecha_hasta | date | ✅ Sí | — | YYYY-MM-DD |
| pagina | int | ✅ Sí | 1 | ≥ 1 |
| tamanio_pagina | int | ✅ Sí | 20 | 1-100 |

**Headers Requeridos:**
```
Authorization: Bearer {token}  (Futuro)
```

**Response Success (200 OK):**
```json
{
  "total": 250,
  "pagina": 1,
  "tamanio_pagina": 20,
  "items": [
    {
      "id": 10,
      "codigo": "TK-2026-000010",
      "cliente_nombre": "María García",
      "cliente_email": "maria@example.com",
      "tipo": "QUEJA",
      "estado": "ESCALADO",
      "prioridad": "ALTA",
      "asunto": "Problema con factura",
      "resuelto_por_ia": false,
      "tiempo_atencion_seg": null,
      "fecha_creacion": "2026-08-20T10:00:00Z",
      "fecha_resolucion": null,
      "satisfaccion": null
    },
    {
      "id": 9,
      "codigo": "TK-2026-000009",
      "cliente_nombre": "Pedro López",
      "cliente_email": "pedro@example.com",
      "tipo": "CONSULTA",
      "estado": "RESUELTO_IA",
      "prioridad": "MEDIA",
      "asunto": "Horario de atención",
      "resuelto_por_ia": true,
      "tiempo_atencion_seg": 45,
      "fecha_creacion": "2026-08-20T09:30:00Z",
      "fecha_resolucion": "2026-08-20T09:30:45Z",
      "satisfaccion": 5
    }
  ]
}
```

**Ejemplos de Queries:**

```bash
# Todos los tickets escalados de alta prioridad
GET /admin/tickets?estado=ESCALADO&prioridad=ALTA

# Tickets resueltos en agosto (pagina 2)
GET /admin/tickets?estado=RESUELTO_IA&fecha_desde=2026-08-01&fecha_hasta=2026-08-31&pagina=2

# Quejas solo (todas las prioridades)
GET /admin/tickets?tipo=QUEJA

# Últimas 50 (página grande)
GET /admin/tickets?tamanio_pagina=50
```

**Response Errors:**

| Código | Escenario |
|--------|-----------|
| **401** | No autenticado (Futuro) |
| **403** | No autorizado (Futuro) |
| **422** | Parámetro inválido (tipo, estado, etc.) |

**Latencia Esperada:**
- P50: <200ms
- P95: <500ms (con índices)

---

### 📌 GET /admin/reportes/mensual
**Obtener Reporte Mensual**

**Descripción:**  
Calcula métricas mensuales: total, IA%, tiempo promedio, distribuciones.

**Método HTTP:** `GET`

**URL:** `/admin/reportes/mensual`

**Query Parameters:**
| Parámetro | Tipo | Obligatorio | Validación |
|-----------|------|-------------|-----------|
| mes | string | ✅ Sí | YYYY-MM (ej: 2026-08) |

**Response Success (200 OK):**
```json
{
  "periodo": "2026-08",
  "metricas": {
    "total_tickets": 250,
    "total_consultas": 150,
    "total_peticiones": 60,
    "total_quejas": 40,
    "tickets_resueltos_ia": 175,
    "tickets_escalados": 50,
    "tickets_cerrados": 25,
    "tickets_abiertos": 0,
    "tasa_resolucion_ia": 70.0,
    "tiempo_promedio_atencion_seg": 120.5,
    "tiempo_min_atencion_seg": 5,
    "tiempo_max_atencion_seg": 3600,
    "satisfaccion_promedio": 4.2,
    "tickets_pendientes": 0,
    "distribucion_tipo": {
      "CONSULTA": 150,
      "PETICION": 60,
      "QUEJA": 40
    },
    "distribucion_estado": {
      "ABIERTO": 0,
      "RESUELTO_IA": 175,
      "ESCALADO": 50,
      "CERRADO": 25
    },
    "distribucion_prioridad": {
      "BAJA": 50,
      "MEDIA": 150,
      "ALTA": 50
    }
  }
}
```

**Response Errors:**

| Código | Escenario | Body |
|--------|-----------|------|
| **401** | No autenticado | `{"detail": "No autenticado"}` |
| **422** | Mes inválido | `{"detail": "mes debe ser formato YYYY-MM"}` |

**Ejemplo cURL:**
```bash
curl -X GET "http://localhost:8000/admin/reportes/mensual?mes=2026-08" \
  -H "Authorization: Bearer {token}"
```

**Latencia Esperada:**
- P50: <1 segundo
- P95: <5 segundos (con BD grande)

---

### 📌 GET /admin/reportes/mensual/insights
**Obtener Insights Mensuales (IA)**

**Descripción:**  
Genera análisis con IA o retorna desde caché. Permite forzar recálculo.

**Método HTTP:** `GET`

**URL:** `/admin/reportes/mensual/insights`

**Query Parameters:**
| Parámetro | Tipo | Opcional | Default | Validación |
|-----------|------|----------|---------|-----------|
| mes | string | ❌ No | — | YYYY-MM |
| recalcular | boolean | ✅ Sí | false | true/false |

**Response Success (200 OK):**
```json
{
  "periodo": "2026-08",
  "contenido": {
    "resumen_ejecutivo": "Agosto fue un mes con actividad estable. Se procesaron 250 tickets con tasa de resolución automática del 70%, superando meta. Reducción de quejas respecto a julio (-15%).",
    "tendencias": [
      "Mayor volumen de consultas sobre horarios (27% del total)",
      "Reducción consistente de quejas a partir de semana 3",
      "Pico de peticiones los martes y miércoles"
    ],
    "problemas_identificados": [
      "Problema recurrente de facturación (15 casos)",
      "Demora en escalamiento de quejas (promedio 2 horas)",
      "Insuficiencia de información en peticiones (requiere follow-up)"
    ],
    "recomendaciones": [
      "Automatizar más preguntas sobre horarios (ganancia potencial: 40 tickets/mes)",
      "Revisar proceso de facturación (issue crítica)",
      "Implementar template de respuesta para peticiones",
      "Reducir tiempo de revisión de quejas escaladas"
    ],
    "comparacion_mes_anterior": {
      "diferencia_tickets": "+12% respecto a julio",
      "diferencia_ia_rate": "+5% (65% vs 70%)",
      "diferencia_tiempo_promedio": "-15 segundos (135s vs 120s)"
    }
  },
  "fecha_generacion": "2026-08-31T23:59:00Z",
  "generado_por_ia": true,
  "cached": false
}
```

**Response Errors:**

| Código | Escenario |
|--------|-----------|
| **401** | No autenticado |
| **422** | Mes inválido |
| **503** | IA no disponible (Gemini error) |

**Ejemplo cURL:**
```bash
# Primera consulta (genera IA)
curl -X GET "http://localhost:8000/admin/reportes/mensual/insights?mes=2026-08"

# Consulta posterior (desde caché)
curl -X GET "http://localhost:8000/admin/reportes/mensual/insights?mes=2026-08"

# Fuerza regeneración
curl -X GET "http://localhost:8000/admin/reportes/mensual/insights?mes=2026-08&recalcular=true"
```

**Latencia Esperada:**
- P50 (caché): <100ms
- P50 (primera vez): <10 segundos (incluye IA)
- P95: <30 segundos

---

### 📌 GET /admin/reportes/mensual/exportar/excel
**Descargar Reporte en Excel**

**Descripción:**  
Genera y descarga archivo Excel (.xlsx) con reporte mensual.

**Método HTTP:** `GET`

**URL:** `/admin/reportes/mensual/exportar/excel`

**Query Parameters:**
| Parámetro | Tipo | Obligatorio |
|-----------|------|-------------|
| mes | string | ✅ Sí (YYYY-MM) |

**Response Success (200 OK):**
```
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename="Reporte_2026-08.xlsx"

[Archivo binario Excel]
```

**Contenido del Excel:**
- Hoja 1: Resumen ejecutivo (KPIs)
- Hoja 2: Detalles de tickets
- Hoja 3: Análisis por tipo
- Hoja 4: Análisis por estado
- Hoja 5: Datos brutos

**Response Errors:**

| Código | Escenario |
|--------|-----------|
| **401** | No autenticado |
| **422** | Mes inválido |

**Latencia Esperada:**
- P50: <5 segundos
- P95: <10 segundos

**Ejemplo cURL:**
```bash
curl -X GET "http://localhost:8000/admin/reportes/mensual/exportar/excel?mes=2026-08" \
  --output "Reporte_2026-08.xlsx"
```

---

### 📌 GET /admin/reportes/mensual/exportar/pdf
**Descargar Reporte en PDF**

**Descripción:**  
Genera y descarga archivo PDF profesional con reporte mensual.

**Método HTTP:** `GET`

**URL:** `/admin/reportes/mensual/exportar/pdf`

**Query Parameters:**
| Parámetro | Tipo | Obligatorio |
|-----------|------|-------------|
| mes | string | ✅ Sí (YYYY-MM) |

**Response Success (200 OK):**
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="Reporte_2026-08.pdf"

[Archivo binario PDF]
```

**Contenido del PDF:**
- Portada con período y fecha
- Índice
- Resumen ejecutivo (1 página)
- Gráficos e ilustraciones (2-3 páginas)
- Tablas detalladas (5+ páginas)
- Recomendaciones y conclusiones

**Response Errors:**

| Código | Escenario |
|--------|-----------|
| **401** | No autenticado |
| **422** | Mes inválido |

**Latencia Esperada:**
- P50: <10 segundos
- P95: <15 segundos

**Ejemplo cURL:**
```bash
curl -X GET "http://localhost:8000/admin/reportes/mensual/exportar/pdf?mes=2026-08" \
  --output "Reporte_2026-08.pdf"
```

---

## 5️⃣ Endpoint de Infraestructura

### 📌 GET /health
**Health Check**

**Descripción:**  
Verifica estado del sistema. Útil para monitoring y load balancer.

**Método HTTP:** `GET`

**URL:** `/health`

**Response (200 OK):**
```json
{
  "status": "ok",
  "timestamp": "2026-08-31T23:59:59Z",
  "version": "1.0.0"
}
```

**Latencia Esperada:**
- <10ms (sin lógica compleja)

---

## 6️⃣ Códigos de Respuesta HTTP

### Códigos 2xx (Éxito)

| Código | Uso | Descripción |
|--------|-----|-------------|
| **200** | GET, POST (actualización) | Solicitud exitosa, respuesta con datos |
| **201** | POST (creación) | Recurso creado exitosamente |
| **204** | DELETE | Sin contenido (recurso eliminado) |

### Códigos 4xx (Error del Cliente)

| Código | Uso | Descripción |
|--------|-----|-------------|
| **400** | Validación | Solicitud malformada (parámetro inválido) |
| **401** | Autenticación | Credenciales faltantes/inválidas |
| **403** | Autorización | Usuario autenticado pero sin permisos |
| **404** | Recurso | Recurso no encontrado (ticket inexistente) |
| **409** | Conflicto | Email duplicado en creación cliente |
| **422** | Validación | Entidad no procesable (Pydantic) |
| **429** | Rate Limit | Demasiadas solicitudes (Futuro) |

### Códigos 5xx (Error del Servidor)

| Código | Uso | Descripción |
|--------|-----|-------------|
| **500** | Error General | Error interno no controlado |
| **502** | Gateway | Bad gateway (proxy error) |
| **503** | Unavailable | Servicio no disponible (IA offline) |
| **504** | Timeout | Gateway timeout (solicitud tardó >60s) |

### Formato de Error

```json
{
  "detail": "Mensaje descriptivo del error en español"
}
```

---

## 7️⃣ Schemas (Modelos de Datos)

### Schema: TicketCreate (Request)

```json
{
  "cliente": {
    "nombre": "string (2-100)",
    "email": "string (email válido)",
    "telefono": "string (max 20)"
  },
  "tipo": "enum: CONSULTA | PETICION | QUEJA",
  "asunto": "string (1-200)",
  "descripcion": "string (1-5000)"
}
```

### Schema: TicketDetalle (Response)

```json
{
  "id": "integer",
  "codigo": "string (TK-YYYY-XXXXX)",
  "cliente_id": "integer",
  "tipo": "enum",
  "asunto": "string",
  "descripcion": "string",
  "estado": "enum: ABIERTO | RESUELTO_IA | ESCALADO | CERRADO",
  "prioridad": "enum: BAJA | MEDIA | ALTA",
  "resuelto_por_ia": "boolean",
  "tiempo_atencion_seg": "integer | null",
  "fecha_creacion": "datetime",
  "fecha_resolucion": "datetime | null",
  "satisfaccion": "integer (1-5) | null",
  "cliente": {
    "nombre": "string",
    "email": "string",
    "telefono": "string"
  },
  "interacciones": [
    {
      "id": "integer",
      "contenido": "string",
      "rol": "enum: cliente | ia | admin",
      "modelo_ia": "string | null",
      "tokens_consumidos": "integer | null",
      "fecha": "datetime"
    }
  ]
}
```

### Schema: MensajeCreate (Request)

```json
{
  "mensaje": "string (1-5000)"
}
```

### Schema: PaginaTickets (Response)

```json
{
  "total": "integer",
  "pagina": "integer",
  "tamanio_pagina": "integer",
  "items": [
    {...TicketDetalle...}
  ]
}
```

### Schema: ReporteMensualOut (Response)

```json
{
  "periodo": "string (YYYY-MM)",
  "metricas": {
    "total_tickets": "integer",
    "total_consultas": "integer",
    "total_peticiones": "integer",
    "total_quejas": "integer",
    "tickets_resueltos_ia": "integer",
    "tickets_escalados": "integer",
    "tickets_cerrados": "integer",
    "tasa_resolucion_ia": "float (0-100)",
    "tiempo_promedio_atencion_seg": "float",
    "satisfaccion_promedio": "float (1-5)",
    "distribucion_tipo": {...},
    "distribucion_estado": {...},
    "distribucion_prioridad": {...}
  }
}
```

---

## 8️⃣ Limitaciones y Rate Limiting

### Límites Actuales (Fase 1)

| Límite | Valor | Aplicado A |
|--------|-------|-----------|
| Tamaño máx. de solicitud | 1 MB | Todos los POST |
| Descripción máxima | 5000 caracteres | POST /tickets |
| Asunto máximo | 200 caracteres | POST /tickets |
| Items por página | 1-100 | GET /admin/tickets |
| Timeout API | 30 segundos | POST /tickets (IA) |
| Conexiones simultáneas | 100 | Servidor |

### Rate Limiting (Futuro Fase 2)

```
100 solicitudes por minuto por IP
1000 solicitudes por hora por usuario
Retry-After header en respuesta 429
```

### CORS (Cross-Origin Resource Sharing)

```
Access-Control-Allow-Origin: * (Desarrollo)
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

---

## 9️⃣ Testing y Validación

### Swagger UI
```
http://localhost:8000/docs
- Interfaz interactiva
- Try it out para cada endpoint
- Documentación automática
```

### Herramientas Recomendadas

- **Postman:** Colección de API
- **curl:** Testing desde CLI
- **pytest:** Testing automatizado
- **Locust:** Load testing
- **JMeter:** Performance testing

---

## 🔟 Versionamiento Futuro

**v2.0 Previsto:**
- Autenticación OAuth2
- WebSocket para updates en tiempo real
- Batch operations
- Filtering avanzado
- Sorting por múltiples campos
- Search full-text en tickets

---

**Documento:** Especificación de la API REST  
**Versión:** 1.0  
**Fecha:** Agosto 31, 2026  
**Estado:** ✅ Aprobado para Desarrollo  
**Última Revisión:** Agosto 31, 2026  
**Próxima Revisión:** Después de implementar Fase 2
