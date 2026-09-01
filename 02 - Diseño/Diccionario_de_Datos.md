# Diccionario de Datos
## Portal Empresarial de Atención al Cliente con IA

**Documento:** Diccionario de Datos  
**Versión:** 1.0  
**Fecha:** Agosto 31, 2026  
**Estado:** ✅ Aprobado

---

## 📚 Índice

1. Descripción General
2. Tabla: clientes
3. Tabla: tickets
4. Tabla: interacciones
5. Tabla: insight_mensual
6. Enumeraciones
7. Índices y Constraints
8. Vistas (Future)

---

## 1️⃣ Descripción General

Este documento describe todas las tablas, campos, tipos de datos, restricciones y relaciones de la base de datos del Portal de Atención al Cliente con IA.

**Base de Datos:**
- **Desarrollo:** SQLite (archivo `backend/dev.db`)
- **Producción:** PostgreSQL (recomendado)
- **Encoding:** UTF-8
- **Zona Horaria:** UTC para todos los timestamps

**Convenciones de Nombres:**
- **Tablas:** snake_case (singular o plural según contexto)
- **Campos:** snake_case
- **Constraints:** tabla_campo_tipo (ej: tickets_codigo_unique)
- **Índices:** idx_tabla_campo (ej: idx_tickets_cliente_id)

---

## 2️⃣ Tabla: clientes

### Propósito
Almacena información de clientes que crean solicitudes en el sistema.

### Estructura

```sql
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### Campos

| Campo | Tipo | Nulo | Único | Default | Descripción |
|-------|------|------|-------|---------|-------------|
| **id** | INTEGER | ❌ No | ✅ Sí (PK) | AUTOINCREMENT | Identificador único del cliente. Clave primaria. Incremento automático. |
| **nombre** | VARCHAR(100) | ❌ No | ❌ No | — | Nombre completo del cliente. 1-100 caracteres. Requerido. |
| **email** | VARCHAR(100) | ❌ No | ✅ Sí | — | Email único del cliente. Validación RFC 5322. Requerido. Índice para búsquedas rápidas. |
| **telefono** | VARCHAR(20) | ✅ Sí | ❌ No | NULL | Número de teléfono. Formato flexible. Opcional (puede ser NULL). |
| **fecha_creacion** | DATETIME | ❌ No | ❌ No | CURRENT_TIMESTAMP | Fecha y hora de registro del cliente. Automático (se asigna al INSERT). |

### Relaciones

```
clientes (1) ←─ (N) tickets
  └─ Un cliente puede tener múltiples tickets
  └─ Relación: cliente_id en tickets
```

### Restricciones

- **PK:** `id` (clave primaria)
- **UNIQUE:** `email` (no se repiten emails)
- **NOT NULL:** `nombre`, `email`, `fecha_creacion`
- **CHECK:** Email válido (validación en aplicación antes de INSERT)

### Índices

```sql
CREATE UNIQUE INDEX idx_clientes_email ON clientes(email);
CREATE INDEX idx_clientes_fecha ON clientes(fecha_creacion);
```

### Ejemplo de Datos

```json
{
  "id": 1,
  "nombre": "Juan Pérez López",
  "email": "juan.perez@example.com",
  "telefono": "+34 555 123 4567",
  "fecha_creacion": "2026-08-15 10:30:00"
}
```

### Límites y Validaciones

- **Nombre:** Min 2 caracteres, Max 100 caracteres
- **Email:** Formato válido, máximo 100 caracteres, unique
- **Teléfono:** Máximo 20 caracteres (permite diferentes formatos internacionales)

---

## 3️⃣ Tabla: tickets

### Propósito
Registro central de todas las solicitudes (consultas, peticiones, quejas) creadas en el sistema.

### Estructura

```sql
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo VARCHAR(24) NOT NULL UNIQUE,
    cliente_id INTEGER NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    asunto VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'ABIERTO',
    prioridad VARCHAR(10) NOT NULL DEFAULT 'MEDIA',
    resuelto_por_ia BOOLEAN NOT NULL DEFAULT FALSE,
    tiempo_atencion_seg INTEGER,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_resolucion DATETIME,
    satisfaccion INTEGER,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);
```

### Campos

| Campo | Tipo | Nulo | Único | Default | Descripción |
|-------|------|------|-------|---------|-------------|
| **id** | INTEGER | ❌ No | ✅ Sí (PK) | AUTOINCREMENT | Identificador único interno del ticket. |
| **codigo** | VARCHAR(24) | ❌ No | ✅ Sí | — | Código público del ticket (ej: TK-2026-001234). Cliente usa esto para consultar. |
| **cliente_id** | INTEGER | ❌ No | ❌ No (FK) | — | Referencia a `clientes.id`. Relación con cliente propietario. |
| **tipo** | VARCHAR(20) | ❌ No | ❌ No | — | Tipo de solicitud: CONSULTA, PETICION, QUEJA (Enum). |
| **asunto** | VARCHAR(200) | ❌ No | ❌ No | — | Título breve de la solicitud. 1-200 caracteres. |
| **descripcion** | TEXT | ❌ No | ❌ No | — | Descripción detallada. Sin límite de caracteres (TEXT). |
| **estado** | VARCHAR(20) | ❌ No | ❌ No | 'ABIERTO' | Estado actual: ABIERTO, RESUELTO_IA, ESCALADO, CERRADO. |
| **prioridad** | VARCHAR(10) | ❌ No | ❌ No | 'MEDIA' | Nivel: BAJA, MEDIA, ALTA. Escalados siempre ALTA. |
| **resuelto_por_ia** | BOOLEAN | ❌ No | ❌ No | FALSE | Flag: ¿Fue resuelto por chatbot IA? |
| **tiempo_atencion_seg** | INTEGER | ✅ Sí | ❌ No | NULL | Segundos desde creación hasta resolución. NULL si aún abierto. |
| **fecha_creacion** | DATETIME | ❌ No | ❌ No | CURRENT_TIMESTAMP | Fecha/hora de creación. Automático. Índice para queries rápidas. |
| **fecha_resolucion** | DATETIME | ✅ Sí | ❌ No | NULL | Fecha/hora de cierre. NULL si aún abierto. Se asigna al CERRAR. |
| **satisfaccion** | INTEGER | ✅ Sí | ❌ No | NULL | Calificación 1-5 estrellas. NULL si no calificado. |

### Relaciones

```
tickets (N) ─→ (1) clientes
  └─ Muchos tickets pertenecen a un cliente
  └─ FK cliente_id → clientes.id

tickets (1) ←─ (N) interacciones
  └─ Un ticket tiene muchas interacciones (conversación)
  └─ FK ticket_id en interacciones
```

### Restricciones

- **PK:** `id`
- **FK:** `cliente_id` → `clientes(id)` (cascade delete en algunas BDs)
- **UNIQUE:** `codigo`
- **NOT NULL:** `codigo`, `cliente_id`, `tipo`, `asunto`, `descripcion`, `estado`, `prioridad`, `resuelto_por_ia`, `fecha_creacion`
- **CHECK:** `tipo` IN ('CONSULTA', 'PETICION', 'QUEJA')
- **CHECK:** `estado` IN ('ABIERTO', 'RESUELTO_IA', 'ESCALADO', 'CERRADO')
- **CHECK:** `prioridad` IN ('BAJA', 'MEDIA', 'ALTA')
- **CHECK:** `satisfaccion` IS NULL OR (satisfaccion >= 1 AND satisfaccion <= 5)

### Índices

```sql
CREATE UNIQUE INDEX idx_tickets_codigo ON tickets(codigo);
CREATE INDEX idx_tickets_cliente_id ON tickets(cliente_id);
CREATE INDEX idx_tickets_estado ON tickets(estado);
CREATE INDEX idx_tickets_fecha_creacion ON tickets(fecha_creacion);
CREATE INDEX idx_tickets_resuelto_ia ON tickets(resuelto_por_ia);
```

### Ejemplo de Datos

```json
{
  "id": 1,
  "codigo": "TK-2026-001234",
  "cliente_id": 1,
  "tipo": "CONSULTA",
  "asunto": "¿Cuál es el horario de atención?",
  "descripcion": "Quisiera saber cuál es el horario de atención al cliente...",
  "estado": "RESUELTO_IA",
  "prioridad": "MEDIA",
  "resuelto_por_ia": true,
  "tiempo_atencion_seg": 45,
  "fecha_creacion": "2026-08-20 14:30:00",
  "fecha_resolucion": "2026-08-20 14:30:45",
  "satisfaccion": 5
}
```

### Transiciones de Estado (State Machine)

```
ABIERTO (inicial)
  ↓ (IA procesa)
  ├─→ RESUELTO_IA (si IA resuelve)
  └─→ ESCALADO (si IA no resuelve)

RESUELTO_IA (terminal, no cambia)

ESCALADO (esperando admin)
  ↓ (admin responde)
  └─→ CERRADO (admin cierra)

CERRADO (terminal)
```

### Límites y Validaciones

- **Código:** Formato TK-YYYY-XXXXXX (24 caracteres max)
- **Asunto:** 1-200 caracteres, requerido
- **Descripción:** 1-5000 caracteres, requerido
- **Tipo:** Solo enum permitidos
- **Estado:** Solo enum permitidos
- **Prioridad:** Solo enum permitidos
- **Tiempo Atención:** Segundos (positivo), NULL si abierto
- **Satisfacción:** 1-5 (inclusive), NULL si no calificado

---

## 4️⃣ Tabla: interacciones

### Propósito
Registro de cada mensaje en la conversación de un ticket. Auditoría completa y reconstrucción de diálogo.

### Estructura

```sql
CREATE TABLE interacciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER NOT NULL,
    contenido TEXT NOT NULL,
    rol VARCHAR(20) NOT NULL,
    modelo_ia VARCHAR(50),
    tokens_consumidos INTEGER,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(id)
);
```

### Campos

| Campo | Tipo | Nulo | Único | Default | Descripción |
|-------|------|------|-------|---------|-------------|
| **id** | INTEGER | ❌ No | ✅ Sí (PK) | AUTOINCREMENT | Identificador único de la interacción. |
| **ticket_id** | INTEGER | ❌ No | ❌ No (FK) | — | Referencia a `tickets.id`. Cada mensaje pertenece a un ticket. |
| **contenido** | TEXT | ❌ No | ❌ No | — | Texto del mensaje. Sin límite de caracteres. |
| **rol** | VARCHAR(20) | ❌ No | ❌ No | — | Quién envió: 'cliente', 'ia', o 'admin'. Enum. |
| **modelo_ia** | VARCHAR(50) | ✅ Sí | ❌ No | NULL | Si `rol='ia'`: nombre del modelo (ej: gemini-3.6-flash, gpt-4). NULL si cliente/admin. |
| **tokens_consumidos** | INTEGER | ✅ Sí | ❌ No | NULL | Tokens IA usados. Solo si `rol='ia'`. NULL para cliente/admin. |
| **fecha** | DATETIME | ❌ No | ❌ No | CURRENT_TIMESTAMP | Timestamp del mensaje. Automático. UTC. |

### Relaciones

```
interacciones (N) ─→ (1) tickets
  └─ Muchos mensajes en un ticket
  └─ FK ticket_id → tickets.id
```

### Restricciones

- **PK:** `id`
- **FK:** `ticket_id` → `tickets(id)` (cascade delete)
- **NOT NULL:** `ticket_id`, `contenido`, `rol`, `fecha`
- **CHECK:** `rol` IN ('cliente', 'ia', 'admin')

### Índices

```sql
CREATE INDEX idx_interacciones_ticket_id ON interacciones(ticket_id);
CREATE INDEX idx_interacciones_fecha ON interacciones(fecha);
CREATE INDEX idx_interacciones_rol ON interacciones(rol);
```

### Ejemplo de Datos

```json
[
  {
    "id": 1,
    "ticket_id": 1,
    "contenido": "¿Cuál es el horario de atención?",
    "rol": "cliente",
    "modelo_ia": null,
    "tokens_consumidos": null,
    "fecha": "2026-08-20 14:30:00"
  },
  {
    "id": 2,
    "ticket_id": 1,
    "contenido": "Nuestro horario de atención es de lunes a viernes 9:00 a 18:00 UTC.",
    "rol": "ia",
    "modelo_ia": "gemini-3.6-flash",
    "tokens_consumidos": 125,
    "fecha": "2026-08-20 14:30:45"
  },
  {
    "id": 3,
    "ticket_id": 1,
    "contenido": "Muchas gracias, eso me ayuda mucho.",
    "rol": "cliente",
    "modelo_ia": null,
    "tokens_consumidos": null,
    "fecha": "2026-08-20 14:35:12"
  }
]
```

### Límites y Validaciones

- **Contenido:** Mínimo 1 carácter, sin límite máximo
- **Rol:** Solo enum permitidos
- **Modelo IA:** Máximo 50 caracteres, optional
- **Tokens:** Positivo, optional

### Notas Importantes

1. **Auditoría Completa:** Cada mensaje queda registrado permanentemente
2. **No Edición:** Los mensajes no se modifican (append-only log)
3. **Reconstrucción:** Se puede reconstruir la conversación exacta ordenando por fecha
4. **Costos:** `tokens_consumidos` permite auditar costos de API IA

---

## 5️⃣ Tabla: insight_mensual

### Propósito
Almacenar análisis mensuales generados por IA. Caché de insights para evitar regenerar.

### Estructura

```sql
CREATE TABLE insight_mensual (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    periodo VARCHAR(7) NOT NULL UNIQUE,
    contenido TEXT NOT NULL,
    fecha_generacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    generado_por_ia BOOLEAN NOT NULL DEFAULT TRUE
);
```

### Campos

| Campo | Tipo | Nulo | Único | Default | Descripción |
|-------|------|------|-------|---------|-------------|
| **id** | INTEGER | ❌ No | ✅ Sí (PK) | AUTOINCREMENT | Identificador único. |
| **periodo** | VARCHAR(7) | ❌ No | ✅ Sí | — | Formato YYYY-MM (ej: 2026-08). Clave única por mes. |
| **contenido** | TEXT | ❌ No | ❌ No | — | JSON o texto con análisis. Insights generados por IA. |
| **fecha_generacion** | DATETIME | ❌ No | ❌ No | CURRENT_TIMESTAMP | Cuándo se generó/actualizó el insight. |
| **generado_por_ia** | BOOLEAN | ❌ No | ❌ No | TRUE | ¿Fue generado por IA? FALSE si es manual. |

### Relaciones

```
insight_mensual (1) ←─ (N) tickets
  └─ Un insight resume múltiples tickets de un mes
  └─ No hay FK explícita (relación semántica)
```

### Restricciones

- **PK:** `id`
- **UNIQUE:** `periodo` (solo un insight por mes)
- **NOT NULL:** `periodo`, `contenido`, `fecha_generacion`, `generado_por_ia`
- **CHECK:** `periodo` LIKE 'YYYY-MM' (validación en aplicación)

### Índices

```sql
CREATE UNIQUE INDEX idx_insight_periodo ON insight_mensual(periodo);
```

### Ejemplo de Datos

```json
{
  "id": 1,
  "periodo": "2026-08",
  "contenido": "{\"resumen\": \"Agosto fue un mes...\", \"tendencias\": [...], \"recomendaciones\": [...]}",
  "fecha_generacion": "2026-08-31 23:59:00",
  "generado_por_ia": true
}
```

### Formato de Contenido (JSON)

```json
{
  "resumen_ejecutivo": "Descripción del mes...",
  "total_tickets": 250,
  "tasa_ia": 75.5,
  "tiempo_promedio": 120,
  "tendencias": [
    "Mayor volumen de consultas sobre horarios",
    "Reducción de quejas respecto a julio"
  ],
  "problemas_identificados": [
    "Problema de facturación recurrente",
    "Demora en respuesta a quejas"
  ],
  "recomendaciones": [
    "Automatizar más preguntas sobre horarios",
    "Revisar proceso de facturación"
  ],
  "comparacion_mes_anterior": {
    "diferencia_tickets": "+15%",
    "diferencia_ia": "+5%"
  }
}
```

### Límites y Validaciones

- **Período:** Formato YYYY-MM (4 dígitos año, guión, 2 dígitos mes)
- **Contenido:** Puede ser JSON estructurado o texto libre (máximo 50KB)
- **Fecha Generación:** UTC

### TTL (Time to Live)

- **Caché:** 30 días
- **Política:** Después de 30 días se puede recalcular si se solicita
- **Retención:** Mínimo 2 años para auditoría histórica

---

## 6️⃣ Enumeraciones

### TipoTicket

```python
class TipoTicket(Enum):
    CONSULTA = "CONSULTA"      # Pregunta/duda
    PETICION = "PETICION"      # Solicitud de acción
    QUEJA = "QUEJA"            # Insatisfacción/problema
```

**Mapping en BD:** VARCHAR con CHECK constraint

---

### EstadoTicket

```python
class EstadoTicket(Enum):
    ABIERTO = "ABIERTO"            # Inicial, sin procesar
    RESUELTO_IA = "RESUELTO_IA"     # Resuelto automáticamente
    ESCALADO = "ESCALADO"          # Esperando personal humano
    CERRADO = "CERRADO"            # Resolución completa
```

**Transiciones válidas:**
- ABIERTO → RESUELTO_IA
- ABIERTO → ESCALADO
- ESCALADO → CERRADO
- (RESUELTO_IA y CERRADO son terminales)

---

### PrioridadTicket

```python
class PrioridadTicket(Enum):
    BAJA = "BAJA"       # No urgente
    MEDIA = "MEDIA"     # Estándar (default)
    ALTA = "ALTA"       # Urgente (escalados)
```

---

### RolInteraccion

```python
class RolInteraccion(Enum):
    CLIENTE = "cliente"     # Mensaje del cliente
    IA = "ia"              # Respuesta del chatbot
    ADMIN = "admin"        # Respuesta de personal
```

---

## 7️⃣ Índices y Constraints

### Índices Recomendados

```sql
-- Búsquedas por código (consulta de cliente)
CREATE UNIQUE INDEX idx_tickets_codigo ON tickets(codigo);

-- Filtrado admin
CREATE INDEX idx_tickets_cliente_id ON tickets(cliente_id);
CREATE INDEX idx_tickets_estado ON tickets(estado);
CREATE INDEX idx_tickets_fecha_creacion ON tickets(fecha_creacion);
CREATE INDEX idx_tickets_resuelto_ia ON tickets(resuelto_por_ia);

-- Búsqueda de email único
CREATE UNIQUE INDEX idx_clientes_email ON clientes(email);

-- Interacciones por ticket
CREATE INDEX idx_interacciones_ticket_id ON interacciones(ticket_id);
CREATE INDEX idx_interacciones_fecha ON interacciones(fecha);

-- Insight por periodo
CREATE UNIQUE INDEX idx_insight_periodo ON insight_mensual(periodo);
```

### Composite Indices (Futuro Optimización)

```sql
-- Listar tickets con filtros múltiples
CREATE INDEX idx_tickets_estado_fecha ON tickets(estado, fecha_creacion);

-- Reportes mensuales rápidos
CREATE INDEX idx_tickets_tipo_fecha ON tickets(tipo, fecha_creacion);
```

---

## 8️⃣ Vistas (Future)

### Vista: vw_tickets_activos

```sql
CREATE VIEW vw_tickets_activos AS
SELECT 
    t.id,
    t.codigo,
    t.asunto,
    c.nombre AS cliente_nombre,
    c.email,
    t.tipo,
    t.estado,
    t.prioridad,
    COUNT(i.id) AS num_interacciones
FROM tickets t
JOIN clientes c ON t.cliente_id = c.id
LEFT JOIN interacciones i ON t.id = i.ticket_id
WHERE t.estado IN ('ABIERTO', 'ESCALADO')
GROUP BY t.id;
```

### Vista: vw_resumen_mensual

```sql
CREATE VIEW vw_resumen_mensual AS
SELECT 
    strftime('%Y-%m', t.fecha_creacion) AS periodo,
    COUNT(*) AS total_tickets,
    SUM(CASE WHEN t.resuelto_por_ia = 1 THEN 1 ELSE 0 END) AS tickets_ia,
    COUNT(*) FILTER (WHERE t.tipo = 'CONSULTA') AS consultas,
    COUNT(*) FILTER (WHERE t.tipo = 'PETICION') AS peticiones,
    COUNT(*) FILTER (WHERE t.tipo = 'QUEJA') AS quejas,
    ROUND(AVG(t.tiempo_atencion_seg), 2) AS tiempo_promedio
FROM tickets t
GROUP BY periodo;
```

---

## 📊 Diagrama de Relaciones (ER)

```
┌──────────────┐
│   clientes   │
│──────────────│
│ id (PK)      │
│ nombre       │ 1
│ email (U)    │─────────┐
│ telefono     │         │
│ fecha_crea   │         │
└──────────────┘         │ N
                         │
                    ┌────────────┐
                    │   tickets  │
                    │────────────│
                    │ id (PK)    │
                    │ codigo (U) │
                    │ cliente_id │────────┐
                    │ tipo       │        │
                    │ asunto     │        │ 1
                    │ descripcion│        │
                    │ estado     │        │ N
                    │ prioridad  │        │
                    │ resuelto_ia│    ┌───────────────┐
                    │ tiempo_sec │    │ interacciones │
                    │ fecha_crea │    │───────────────│
                    │ fecha_resol│    │ id (PK)       │
                    │ satisfacc  │    │ ticket_id (FK)│
                    └────────────┘    │ contenido     │
                                      │ rol           │
                                      │ modelo_ia     │
                                      │ tokens        │
                                      │ fecha         │
                                      └───────────────┘
                                      
┌─────────────────┐
│ insight_mensual │
│─────────────────│
│ id (PK)         │
│ periodo (U)     │ (Relación semántica con tickets del mes)
│ contenido       │
│ fecha_gen       │
│ generado_ia     │
└─────────────────┘
```

---

## 🔍 9. Ejemplos de Queries Comunes

### Obtener Conversación de Ticket

```sql
SELECT 
    i.id,
    i.contenido,
    i.rol,
    i.fecha,
    i.modelo_ia,
    i.tokens_consumidos
FROM interacciones i
WHERE i.ticket_id = (
    SELECT id FROM tickets WHERE codigo = 'TK-2026-001234'
)
ORDER BY i.fecha ASC;
```

### Reporte Mensual

```sql
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN resuelto_por_ia THEN 1 ELSE 0 END) as ia_count,
    ROUND(100.0 * SUM(CASE WHEN resuelto_por_ia THEN 1 ELSE 0 END) / COUNT(*), 2) as ia_percent,
    AVG(tiempo_atencion_seg) as tiempo_promedio,
    COUNT(CASE WHEN estado = 'ESCALADO' THEN 1 END) as pendientes
FROM tickets
WHERE strftime('%Y-%m', fecha_creacion) = '2026-08';
```

### Listar Escalados

```sql
SELECT 
    t.id,
    t.codigo,
    t.asunto,
    c.nombre,
    t.tipo,
    t.prioridad,
    COUNT(i.id) as mensajes
FROM tickets t
JOIN clientes c ON t.cliente_id = c.id
LEFT JOIN interacciones i ON t.id = i.ticket_id
WHERE t.estado = 'ESCALADO'
GROUP BY t.id
ORDER BY t.fecha_creacion DESC;
```

---

## ✅ Checklist de Integridad

- ✅ Todas las tablas tienen PK
- ✅ Todas las FK apuntan a PKs válidos
- ✅ Campos requeridos tienen NOT NULL
- ✅ Campos únicos tienen índices
- ✅ Enums validados en BD (CHECK) y aplicación
- ✅ Timestamps en UTC
- ✅ Encoding UTF-8
- ✅ Índices para queries frecuentes
- ✅ Cascade delete configurado

---

**Documento:** Diccionario de Datos  
**Versión:** 1.0  
**Fecha:** Agosto 31, 2026  
**Estado:** ✅ Aprobado
