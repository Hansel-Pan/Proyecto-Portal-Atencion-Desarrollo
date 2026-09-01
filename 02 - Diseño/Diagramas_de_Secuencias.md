# Diagramas de Secuencias
## Portal Empresarial de Atención al Cliente con IA

**Documento:** Diagramas de Secuencia (Sequence Diagrams)  
**Versión:** 1.0  
**Fecha:** Agosto 31, 2026  
**Estado:** ✅ Aprobado

---

## 📋 Índice

1. Crear Ticket (Flujo Principal)
2. Consultar Ticket
3. Enviar Mensaje
4. Procesar Resolución IA
5. Generar Reporte
6. Generar Insights
7. Fallos y Recuperación

---

## 1️⃣ Crear Ticket (CU-001)

### Escenario: Cliente crea nueva consulta

```
Cliente           Frontend         Backend          IA Service        DB
  │                  │                │                  │             │
  │  1. Completa      │                │                  │             │
  │  formulario       │                │                  │             │
  ├─────────────────►│                │                  │             │
  │                  │                │                  │             │
  │                  │ 2. Valida      │                  │             │
  │                  │ (frontend)     │                  │             │
  │                  │                │                  │             │
  │                  │ 3. POST /tickets                  │             │
  │                  │ {nombre, email, │                  │             │
  │                  │  tipo, asunto...}                 │             │
  │                  ├───────────────►│                  │             │
  │                  │                │                  │             │
  │                  │                │ 4. Valida Pydantic             │
  │                  │                │                  │             │
  │                  │                │ 5. Busca cliente               │
  │                  │                ├───────────────────────────────►│
  │                  │                │◄───────────────────────────────┤
  │                  │                │   cliente (existente o nuevo)  │
  │                  │                │                  │             │
  │                  │                │ 6. Genera código único         │
  │                  │                │ (TK-2026-XXXXX)                │
  │                  │                │                  │             │
  │                  │                │ 7. INSERT ticket               │
  │                  │                ├───────────────────────────────►│
  │                  │                │◄───────────────────────────────┤
  │                  │                │         ticket.id = 1          │
  │                  │                │                  │             │
  │                  │                │ 8. INSERT interacción (cliente)│
  │                  │                ├───────────────────────────────►│
  │                  │                │◄───────────────────────────────┤
  │                  │                │                  │             │
  │                  │                │ 9. procesar_solicitud()        │
  │                  │                ├──────────────────►│             │
  │                  │                │                  │             │
  │                  │                │                  │ 10. factory.crear_proveedor()
  │                  │                │                  │  (Gemini)  │
  │                  │                │                  │             │
  │                  │                │                  │ 11. generar_respuesta()
  │                  │                │                  │  [API call] │
  │                  │                │                  │             │
  │                  │  ┌─ 30 seg ───┐                  │             │
  │                  │  │  timeout    │                  │             │
  │                  │  └─────────────┘                  │             │
  │                  │                │◄──────────────────┤             │
  │                  │                │    respuesta IA   │             │
  │                  │                │   tokens=125      │             │
  │                  │                │                  │             │
  │                  │  ┌─ ¿Resuelve? ┐                 │             │
  │                  │  │  SÍ → RESUELTO_IA             │             │
  │                  │  │  NO → ESCALADO (ALTA)         │             │
  │                  │  └─────────────┘                  │             │
  │                  │                │ 12. UPDATE ticket estado       │
  │                  │                ├───────────────────────────────►│
  │                  │                │◄───────────────────────────────┤
  │                  │                │                  │             │
  │                  │                │ 13. INSERT interacción (IA)    │
  │                  │                │ + modelo_ia + tokens           │
  │                  │                ├───────────────────────────────►│
  │                  │                │◄───────────────────────────────┤
  │                  │                │                  │             │
  │                  │ 14. TicketDetalle                 │             │
  │                  │◄───────────────┤                  │             │
  │                  │                │                  │             │
  │  15. Modal éxito │                │                  │             │
  │  + código        │                │                  │             │
  │◄─────────────────┤                │                  │             │
  │                  │                │                  │             │
```

**Puntos Críticos:**
- ✅ Validación frontend preventiva
- ✅ Re-validación backend con Pydantic
- ✅ Generación de código único
- ✅ Transacción atómica (INSERT ticket + interacción)
- ✅ Procesamiento IA asincrónico
- ✅ Fallback a Mock si IA falla (timeout 30s)
- ✅ Decisión automática: resuelve o escala

---

## 2️⃣ Consultar Ticket (CU-002)

### Escenario: Cliente consulta estado de ticket existente

```
Cliente           Frontend         Backend          DB
  │                  │                │              │
  │  1. Ingresa       │                │              │
  │  código           │                │              │
  ├─────────────────►│                │              │
  │                  │                │              │
  │                  │ 2. GET /tickets/{ref}         │
  │                  ├───────────────►│              │
  │                  │                │              │
  │                  │                │ 3. SELECT * FROM tickets
  │                  │                │ WHERE codigo = ?  │
  │                  │                ├─────────────────►│
  │                  │                │◄─────────────────┤
  │                  │                │  ticket record   │
  │                  │                │              │
  │                  │                │ 4. SELECT * FROM interacciones
  │                  │                │ WHERE ticket_id = ?  │
  │                  │                ├─────────────────►│
  │                  │                │◄─────────────────┤
  │                  │                │  [interacción 1, 2, 3...]
  │                  │                │              │
  │                  │                │ 5. SELECT cliente data
  │                  │                ├─────────────────►│
  │                  │                │◄─────────────────┤
  │                  │                │  cliente info    │
  │                  │                │              │
  │                  │ 6. TicketDetalle               │
  │                  │ {                              │
  │                  │   codigo,                      │
  │                  │   cliente_nombre,              │
  │                  │   estado,                      │
  │                  │   interacciones: [...]         │
  │                  │ }                              │
  │                  │◄───────────────┤               │
  │                  │                │               │
  │  7. Renderiza    │                │               │
  │  ChatPage        │                │               │
  │  + Conversacion  │                │               │
  │◄─────────────────┤                │               │
  │                  │                │               │
```

**Puntos Críticos:**
- ✅ Búsqueda por código único (índice)
- ✅ JOIN con cliente
- ✅ Conversación ordenada cronológicamente
- ✅ Error 404 si no existe

---

## 3️⃣ Enviar Mensaje Adicional (CU-003)

### Escenario: Cliente envía mensaje a ticket abierto/escalado

```
Cliente           Frontend         Backend          DB
  │                  │                │              │
  │  1. Lee mensaje   │                │              │
  │  + clica enviar   │                │              │
  ├─────────────────►│                │              │
  │                  │                │              │
  │                  │ 2. POST /tickets/{ref}/mensajes
  │                  │ {mensaje: "..."}  │              │
  │                  ├───────────────►│              │
  │                  │                │              │
  │                  │                │ 3. Valida ticket existe
  │                  │                │              │
  │                  │                │ 4. INSERT interacción
  │                  │                │ rol='cliente'  │
  │                  │                ├─────────────────►│
  │                  │                │◄─────────────────┤
  │                  │                │ interacción.id   │
  │                  │                │              │
  │                  │ 5. TicketDetalle (actualizado)
  │                  │◄───────────────┤              │
  │                  │                │              │
  │  6. Muestra      │                │              │
  │  nuevo mensaje   │                │              │
  │  en conversación │                │              │
  │◄─────────────────┤                │              │
  │                  │                │              │

NOTA: Estado NO cambia (si ESCALADO, permanece ESCALADO)
      Admin debe intervenir manualmente
```

**Puntos Críticos:**
- ✅ Validación de ticket abierto/escalado/resuelto
- ✅ Mensaje se agrega a conversación
- ✅ Timestamp automático
- ✅ Estado NO cambia (diferencia importante)

---

## 4️⃣ Procesar Resolución IA (CU-004, CU-005)

### Escenario: IA Decide: Resolver o Escalar

```
Sistema         IA Service        DB
  │                  │             │
  │ 1. procesar_solicitud()        │
  ├─────────────────►│             │
  │                  │             │
  │                  │ 2. generar_respuesta()
  │                  │ (Timeout 30s)  │
  │                  │             │
  │         ┌─ IA Procesa ─┐       │
  │         │ (Google API) │       │
  │         └──────────────┘       │
  │                  │             │
  │◄─────────────────┤             │
  │  respuesta_json  │             │
  │  + tokens        │             │
  │                  │             │
  │ ┌─ ANÁLISIS ─┐   │             │
  │ │ ¿Resuelve? │   │             │
  │ │ (keywords) │   │             │
  │ └────────────┘   │             │
  │                  │             │
  │         SÍ → RAMA 1             │
  │         NO → RAMA 2             │

═══════════════════════════════════════════════════════════

RAMA 1: RESUELVE POR IA

Sistema         IA Service       DB
  │                 │            │
  │ ┌─ Acción ─┐    │            │
  │ │ UPDATE   │    │            │
  │ │ estado=  │    │            │
  │ │RESUELTO_IA
  │ │ resuelto_│    │            │
  │ │por_ia=1  │    │            │
  │ └──────────┘    │            │
  │                 │            │
  │                 │ 1. UPDATE tickets
  │                 ├───────────►│
  │                 │◄───────────┤
  │                 │            │
  │                 │ 2. INSERT interacción
  │                 │ rol='ia', modelo, tokens
  │                 ├───────────►│
  │                 │◄───────────┤
  │                 │            │
  │                 │ 3. UPDATE tiempo_atencion
  │                 ├───────────►│
  │                 │◄───────────┤
  │                 │            │

═══════════════════════════════════════════════════════════

RAMA 2: ESCALA A PERSONAL

Sistema         IA Service       DB
  │                 │            │
  │ ┌─ Acción ─┐    │            │
  │ │ UPDATE   │    │            │
  │ │ estado=  │    │            │
  │ │ESCALADO  │    │            │
  │ │ prioridad│    │            │
  │ │=ALTA     │    │            │
  │ └──────────┘    │            │
  │                 │            │
  │                 │ 1. UPDATE tickets
  │                 │ (estado, prioridad)
  │                 ├───────────►│
  │                 │◄───────────┤
  │                 │            │
  │                 │ 2. INSERT interacción
  │                 │ rol='ia' + respuesta
  │                 │ (por qué escaló)
  │                 ├───────────►│
  │                 │◄───────────┤
  │                 │            │
  │ 3. Notificación │            │
  │    a Admin      │            │
  │    (via panel)  │            │
  │                 │            │
```

**Puntos Críticos:**
- ✅ Timeout máximo 30 segundos
- ✅ Fallback a Mock si IA falla
- ✅ Decisión basada en palabras clave o IA
- ✅ Registro de modelo y tokens
- ✅ Cálculo automático tiempo_atencion
- ✅ Escalados siempre ALTA prioridad

---

## 5️⃣ Generar Reporte Mensual (CU-009)

### Escenario: Admin solicita reporte de agosto 2026

```
Admin            Frontend        Backend         DB
  │                 │              │             │
  │ 1. Selecciona   │              │             │
  │ mes: 2026-08    │              │             │
  ├────────────────►│              │             │
  │                 │              │             │
  │                 │ 2. GET /admin/reportes/mensual
  │                 │ ?mes=2026-08  │             │
  │                 ├─────────────►│             │
  │                 │              │             │
  │                 │              │ 3. Valida formato YYYY-MM
  │                 │              │             │
  │                 │              │ 4. calcular_metricas()
  │                 │              │             │
  │                 │              │ 5. SELECT COUNT(*) total
  │                 │              │ WHERE fecha BETWEEN
  │                 │              ├────────────►│
  │                 │              │◄────────────┤
  │                 │              │  total: 250 │
  │                 │              │             │
  │                 │              │ 6. SELECT SUM(resuelto_ia)
  │                 │              ├────────────►│
  │                 │              │◄────────────┤
  │                 │              │  ia_count: 175
  │                 │              │             │
  │                 │              │ 7. SELECT AVG(tiempo)
  │                 │              ├────────────►│
  │                 │              │◄────────────┤
  │                 │              │  promedio: 120.5 seg
  │                 │              │             │
  │                 │              │ 8. SELECT * distribuido
  │                 │              │ por tipo/estado
  │                 │              ├────────────►│
  │                 │              │◄────────────┤
  │                 │              │  consultas: 150
  │                 │              │  peticiones: 60
  │                 │              │  quejas: 40
  │                 │              │             │
  │                 │              │ 9. Genera ReporteMensualOut
  │                 │              │    {
  │                 │              │      total: 250,
  │                 │              │      ia%: 70.0,
  │                 │              │      tiempo_prom: 120.5,
  │                 │              │      ...
  │                 │              │    }
  │                 │              │             │
  │                 │ 10. JSON ReporteMensualOut
  │                 │◄─────────────┤             │
  │                 │              │             │
  │  11. Renderiza  │              │             │
  │  gráficos con   │              │             │
  │  Recharts       │              │             │
  │◄────────────────┤              │             │
  │  - Línea        │              │             │
  │  - Pie          │              │             │
  │  - Barras       │              │             │
  │                 │              │             │
```

**Puntos Críticos:**
- ✅ Validación de formato mes (YYYY-MM)
- ✅ Aggregaciones SQL eficientes
- ✅ Performance < 5 segundos
- ✅ Manejo de meses sin datos
- ✅ Índices en fecha_creacion y resuelto_por_ia

---

## 6️⃣ Generar Insights con IA (CU-010)

### Escenario: Admin solicita insights (posible caché)

```
Admin            Frontend        Backend        IA Service      DB
  │                 │              │                 │           │
  │ 1. Clica         │              │                 │           │
  │ "Insights"       │              │                 │           │
  ├────────────────►│              │                 │           │
  │                 │              │                 │           │
  │                 │ 2. GET /admin/reportes/mensual/insights
  │                 │ ?mes=2026-08                    │           │
  │                 ├─────────────►│                 │           │
  │                 │              │                 │           │
  │                 │              │ 3. insights_service.generar_insight()
  │                 │              │                 │           │
  │                 │              │ 4. CHECK caché  │           │
  │                 │              ├──────────────────────────────►│
  │                 │              │◄──────────────────────────────┤
  │                 │              │   Existe en insight_mensual?  │
  │                 │              │                 │           │
  │    ┌──── SÍ ────┐              │                 │           │
  │    │ (RETURN    │              │                 │           │
  │    │  cached)   │              │                 │           │
  │    └────────────┘              │                 │           │
  │                 │              │                 │           │
  │                 │     ┌────────────────────────────►           │
  │                 │     │       SELECT contenido FROM            │
  │                 │     │       insight_mensual WHERE            │
  │                 │     │       periodo='2026-08'                │
  │                 │     │◄────────────────────────────            │
  │                 │     │         cached_insight                 │
  │                 │     │                 │           │           │
  │    ┌──── NO ────┐     │                 │           │           │
  │    │ (Generar)  │     │                 │           │           │
  │    └────────────┘     │                 │           │           │
  │                 │              │                 │           │
  │                 │              │ 5. reporte_service.calcular_metricas()
  │                 │              ├─────────────────────────────►│
  │                 │              │◄─────────────────────────────┤
  │                 │              │         metricas_json        │
  │                 │              │                 │           │
  │                 │              │ 6. IA.generar_insights()    │
  │                 │              │ (Prompt + metricas)          │
  │                 │              ├────────────────►│           │
  │                 │              │                 │           │
  │                 │              │        ┌─ Google API ─┐     │
  │                 │              │        │ (Gemini)      │     │
  │                 │              │        └───────────────┘     │
  │                 │              │                 │           │
  │                 │              │◄────────────────┤           │
  │                 │              │  análisis_texto │           │
  │                 │              │  (español)      │           │
  │                 │              │                 │           │
  │                 │              │ 7. INSERT insight_mensual    │
  │                 │              │ periodo=2026-08              │
  │                 │              │ contenido=análisis_texto     │
  │                 │              ├──────────────────────────────►│
  │                 │              │◄──────────────────────────────┤
  │                 │              │                 │           │
  │                 │ 8. JSON insight_result         │           │
  │                 │ {                              │           │
  │                 │   insight: "...",              │           │
  │                 │   cached: false                │           │
  │                 │ }                              │           │
  │                 │◄─────────────┤                 │           │
  │                 │              │                 │           │
  │  9. Muestra     │              │                 │           │
  │  análisis en    │              │                 │           │
  │  card / modal   │              │                 │           │
  │◄────────────────┤              │                 │           │
  │                 │              │                 │           │
```

**Puntos Críticos:**
- ✅ Check de caché antes de generar
- ✅ Caché por período (YYYY-MM)
- ✅ Generación de IA en background (podría ser async)
- ✅ TTL: 30 días (después se puede recalcular)
- ✅ Flag recalcular=true fuerza regeneración

---

## 7️⃣ Fallos y Recuperación

### Escenario A: API Gemini No Disponible

```
Sistema        chatbot_service    Gemini API      Mock Provider      DB
  │                 │                 │                 │            │
  │ 1. procesar_solicitud()           │                 │            │
  ├────────────────►│                 │                 │            │
  │                 │                 │                 │            │
  │                 │ 2. Llama Gemini │                 │            │
  │                 ├────────────────►│                 │            │
  │                 │                 │                 │            │
  │         ┌─ TIMEOUT 30s ┐          │                 │            │
  │         │ O ERROR 503  │          │                 │            │
  │         └──────────────┘          │                 │            │
  │                 │◄────────────────┤                 │            │
  │                 │   ❌ Connection Error             │            │
  │                 │                 │                 │            │
  │                 │ 3. Fallback → MockProvider        │            │
  │                 ├──────────────────────────────────►│            │
  │                 │                 │                 │            │
  │                 │                 │ 4. generar_respuesta()        │
  │                 │                 │ (Palabras clave locales)      │
  │                 │                 │◄──────────────────────────────┤
  │                 │                 │   respuesta_mock              │
  │                 │                 │   + tokens=0 (mock)           │
  │                 │                 │                 │            │
  │                 │ 5. Continúa normalmente           │            │
  │                 │    (UPDATE tickets,               │            │
  │                 │     INSERT interacciones)         │            │
  │                 │                 │                 │            │
  │                 │ 6. Log WARNING: "Proveedor IA no disponible"  │
  │                 │    Usó Mock en lugar de Gemini    │            │
  │                 │                 │                 │            │
  │                 ├──────────────────────────────────────────────►│
  │                 │                 │                 │   [LOG]    │
  │                 │                 │                 │            │
```

**Recuperación:**
- ✅ Fallback automático a Mock
- ✅ Sistema NO falla
- ✅ Respuesta menos sofisticada pero funcional
- ✅ Log de warning para auditoría
- ✅ Siguiente solicitud reintenta Gemini

### Escenario B: Ticket No Encontrado

```
Cliente           Frontend         Backend          DB
  │                 │              │             │
  │ 1. Ingresa      │              │             │
  │ código 404      │              │             │
  ├────────────────►│              │             │
  │                 │              │             │
  │                 │ 2. GET /tickets/TK-INVALID
  │                 ├─────────────►│             │
  │                 │              │             │
  │                 │              │ 3. SELECT WHERE codigo='TK-INVALID'
  │                 │              ├────────────►│
  │                 │              │◄────────────┤
  │                 │              │   NULL     │
  │                 │              │             │
  │                 │              │ 4. raise HTTPException(404)
  │                 │              │ "Ticket no encontrado"
  │                 │              │             │
  │                 │ 5. JSON Error             │
  │                 │ {                         │
  │                 │   "detail": "Ticket no   │
  │                 │    encontrado"            │
  │                 │ }                         │
  │                 │◄─────────────┤             │
  │                 │              │             │
  │  6. Muestra     │              │             │
  │  mensaje error  │              │             │
  │  amigable       │              │             │
  │◄────────────────┤              │             │
  │                 │              │             │
```

**Recuperación:**
- ✅ Validación en backend
- ✅ Error 404 controlado
- ✅ Mensaje amigable al usuario
- ✅ No crash de API

---

## 📊 Tabla de Secuencias

| # | Caso | Actores | Duración | Éxito | Fallo |
|---|------|---------|----------|-------|-------|
| 1 | Crear Ticket | Cliente, IA | ~2s (IA 30s timeout) | RESUELTO_IA o ESCALADO | Mock fallback |
| 2 | Consultar | Cliente | <200ms (P50) | TicketDetalle | 404 |
| 3 | Enviar Mensaje | Cliente | <200ms | Interacción agregada | Ticket no existe |
| 4 | Procesar IA | Sistema | <30s | Resuelto o Escalado | Fallback Mock |
| 5 | Reporte | Admin | <5s | JSON con KPIs | Mes inválido 422 |
| 6 | Insights | Admin | <10s (1a vez) | Análisis IA | IA no disponible 503 |
| 7 | Exportar | Admin | <10s (Excel) / <15s (PDF) | Archivo descargado | Error 422 |

---

**Documento:** Diagramas de Secuencias  
**Versión:** 1.0  
**Fecha:** Agosto 31, 2026  
**Estado:** ✅ Aprobado para Implementación
