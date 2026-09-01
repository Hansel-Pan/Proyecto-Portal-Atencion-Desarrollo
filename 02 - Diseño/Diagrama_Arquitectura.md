# Diagrama de Arquitectura del Sistema
## Portal Empresarial de Atención al Cliente con IA

**Documento:** Arquitectura de Software  
**Versión:** 1.0  
**Fecha:** Agosto 31, 2026  
**Estado:** ✅ Aprobado

---

## 📐 1. Arquitectura General del Sistema

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CAPA DE PRESENTACIÓN (Frontend)                     │
│                                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Inicio    │  │   Crear      │  │   Consulta   │  │  Dashboard   │    │
│  │  /          │  │  Solicitud   │  │  Tickets     │  │  /admin      │    │
│  │             │  │  /consulta   │  │  /chat       │  │             │    │
│  └─────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  React 19 + Vite + Tailwind CSS + React Router                       │  │
│  │  - Single Page Application (SPA)                                     │  │
│  │  - Client-side routing                                              │  │
│  │  - State management (useState, Context API)                         │  │
│  │  - Real-time updates (polling/WebSocket futura)                     │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                        HTTP/HTTPS (REST API)
                                 │
┌────────────────────────────────┴────────────────────────────────────────────┐
│                    CAPA DE APLICACIÓN (Backend)                             │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  FastAPI 0.100+ - API REST Asincrónica                              │  │
│  │  - Validación automática con Pydantic                               │  │
│  │  - Documentación Swagger en /docs                                   │  │
│  │  - Manejo de CORS y middlewares                                     │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  ROUTERS (Controladores)                                             │  │
│  │                                                                      │  │
│  │  ┌─────────────────────────────────────────────────────────────┐   │  │
│  │  │  /tickets (Público)                                        │   │  │
│  │  │  - POST /tickets → Crear solicitud                        │   │  │
│  │  │  - GET /tickets/{ref} → Consultar estado                 │   │  │
│  │  │  - POST /tickets/{ref}/mensajes → Enviar mensaje          │   │  │
│  │  └─────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  │  ┌─────────────────────────────────────────────────────────────┐   │  │
│  │  │  /admin (Privado)                                          │   │  │
│  │  │  - GET /admin/tickets → Listar con filtros               │   │  │
│  │  │  - GET /admin/reportes/mensual → Reporte KPIs            │   │  │
│  │  │  - GET /admin/reportes/mensual/insights → Análisis IA    │   │  │
│  │  │  - GET /admin/reportes/exportar/excel → Descargar        │   │  │
│  │  │  - GET /admin/reportes/exportar/pdf → Descargar          │   │  │
│  │  └─────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  │  ┌─────────────────────────────────────────────────────────────┐   │  │
│  │  │  /health (Infraestructura)                                 │   │  │
│  │  │  - GET /health → Status del sistema                       │   │  │
│  │  └─────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  SERVICES (Lógica de Negocio)                                        │  │
│  │                                                                      │  │
│  │  ticket_service.py              reporte_service.py                 │  │
│  │  ├─ crear_ticket()              ├─ calcular_metricas()             │  │
│  │  ├─ obtener_ticket()            ├─ generar_reporte_mensual()       │  │
│  │  ├─ responder_mensaje()         └─ analytics()                     │  │
│  │  └─ listar_tickets()                                               │  │
│  │                                  insights_service.py                │  │
│  │  chatbot_service.py             ├─ generar_insight()              │  │
│  │  ├─ procesar_solicitud()        ├─ cachear_insight()              │  │
│  │  ├─ resolver_con_ia()           └─ recalcular_insight()           │  │
│  │  └─ escalar_ticket()                                               │  │
│  │                                  exporte_service.py                │  │
│  │                                  ├─ generar_excel()                │  │
│  │                                  └─ generar_pdf()                  │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  MÓDULO IA (Proveedores)                                             │  │
│  │                                                                      │  │
│  │  ProveedorIA (Abstract Base Class)                                  │  │
│  │  ├─ gemini_provider.py (Google Gemini - default)                  │  │
│  │  ├─ openai_provider.py (OpenAI GPT)                               │  │
│  │  ├─ ollama_provider.py (Local LLM)                                │  │
│  │  └─ mock_provider.py (Fallback - reglas locales)                 │  │
│  │                                                                      │  │
│  │  Factory Pattern: IA.factory.crear_proveedor(AI_PROVIDER)         │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────┬──────────────────────────────────────────┘
                                  │
                    SQLAlchemy ORM (Connection Pool)
                                  │
┌─────────────────────────────────┴──────────────────────────────────────────┐
│              CAPA DE DATOS (Persistencia)                                   │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  SQLite (Desarrollo) / PostgreSQL (Producción)                       │  │
│  │                                                                      │  │
│  │  ┌─────────────────────────────────────────────────────────────┐   │  │
│  │  │  Tabla: clientes                                           │   │  │
│  │  │  ├─ id (PK)                                                │   │  │
│  │  │  ├─ nombre                                                 │   │  │
│  │  │  ├─ email (UNIQUE)                                         │   │  │
│  │  │  ├─ telefono                                               │   │  │
│  │  │  └─ fecha_creacion                                         │   │  │
│  │  └─────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  │  ┌─────────────────────────────────────────────────────────────┐   │  │
│  │  │  Tabla: tickets                                            │   │  │
│  │  │  ├─ id (PK)                                                │   │  │
│  │  │  ├─ codigo (UNIQUE, Índice)                                │   │  │
│  │  │  ├─ cliente_id (FK, Índice)                                │   │  │
│  │  │  ├─ tipo (ENUM: CONSULTA, PETICION, QUEJA)               │   │  │
│  │  │  ├─ estado (ENUM: ABIERTO, RESUELTO_IA, ESCALADO)        │   │  │
│  │  │  ├─ prioridad (ENUM: BAJA, MEDIA, ALTA)                  │   │  │
│  │  │  ├─ resuelto_por_ia (BOOLEAN)                             │   │  │
│  │  │  ├─ tiempo_atencion_seg (INTEGER)                         │   │  │
│  │  │  ├─ fecha_creacion (Índice)                               │   │  │
│  │  │  ├─ fecha_resolucion                                      │   │  │
│  │  │  └─ satisfaccion (1-5)                                    │   │  │
│  │  └─────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  │  ┌─────────────────────────────────────────────────────────────┐   │  │
│  │  │  Tabla: interacciones                                      │   │  │
│  │  │  ├─ id (PK)                                                │   │  │
│  │  │  ├─ ticket_id (FK, Índice)                                │   │  │
│  │  │  ├─ contenido (TEXT)                                       │   │  │
│  │  │  ├─ rol (ENUM: cliente, ia, admin)                        │   │  │
│  │  │  ├─ modelo_ia (VARCHAR: gemini-3.6-flash, gpt-4, etc.)   │   │  │
│  │  │  ├─ tokens_consumidos (INTEGER)                           │   │  │
│  │  │  └─ fecha (DateTime)                                      │   │  │
│  │  └─────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  │  ┌─────────────────────────────────────────────────────────────┐   │  │
│  │  │  Tabla: insight_mensual                                    │   │  │
│  │  │  ├─ id (PK)                                                │   │  │
│  │  │  ├─ periodo (VARCHAR: YYYY-MM, UNIQUE)                    │   │  │
│  │  │  ├─ contenido (TEXT/JSON)                                 │   │  │
│  │  │  ├─ fecha_generacion                                      │   │  │
│  │  │  └─ generado_por_ia (BOOLEAN)                             │   │  │
│  │  └─────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🌐 2. Arquitectura de Red

```
┌──────────────────────┐
│   Internet / Usuario │
└──────────────┬───────┘
               │
               │ HTTPS:443
               │
┌──────────────┴───────────────────────────┐
│         Load Balancer (Futuro)            │
└──────────────┬───────────────────────────┘
               │
        ┌──────┴──────┐
        │             │
    HTTP:80      HTTP:80
        │             │
┌───────┴─┐       ┌───┴──────┐
│ Frontend │       │ Backend  │
│ (React)  │       │(FastAPI) │
│ :5173    │       │ :8000    │
└───────┬─┘       └───┬──────┘
        │             │
        │             │ SQLAlchemy
        │             │
        └─────┬───────┘
              │
        ┌─────┴──────┐
        │             │
    SQLite       PostgreSQL (Prod)
  (dev.db)       (puerto 5432)
```

---

## 🏗️ 3. Arquitectura de Capas (Layered Architecture)

```
LAYER 1: PRESENTATION (UI)
├─ React Components
├─ Pages (6 rutas)
├─ Layout & Navigation
└─ Styling (Tailwind CSS)

        ↓ HTTP/JSON

LAYER 2: API GATEWAY
├─ FastAPI Router
├─ Middleware (CORS, Error Handling)
├─ Request Validation (Pydantic)
└─ Response Serialization

        ↓ Function Calls

LAYER 3: BUSINESS LOGIC
├─ Services (5 servicios)
├─ Chatbot Logic
├─ Report Generation
├─ Export Generation
└─ Data Aggregation

        ↓ ORM Calls

LAYER 4: DATA ACCESS
├─ SQLAlchemy ORM
├─ Database Connection Pool
├─ Query Building
└─ Transaction Management

        ↓ SQL Queries

LAYER 5: DATABASE
├─ SQLite (Desarrollo)
├─ PostgreSQL (Producción)
├─ Tables (4 tablas)
├─ Indices (6 índices)
└─ Constraints (Referencial + Domain)
```

---

## 🔄 4. Patrón de Flujo de Datos

### 4.1 Crear Ticket (POST /tickets)

```
Cliente Frontend
    │
    ├─ Llena formulario en ConsultaPage.jsx
    │
    ├─ Valida en cliente (validación preventiva)
    │
    ├─ POST /tickets → Backend
    │
    ├─ API recibe JSON con TicketCreate schema
    │
    ├─ FastAPI valida con Pydantic (auto)
    │
    ├─ router.crear_ticket() → ticket_service
    │
    ├─ ticket_service.crear_ticket():
    │   ├─ Busca cliente por email (o crea)
    │   ├─ Genera código único
    │   ├─ INSERT INTO tickets
    │   ├─ INSERT INTO interacciones (mensaje cliente)
    │   └─ COMMIT
    │
    ├─ chatbot_service.procesar_solicitud():
    │   ├─ Lee descripción del ticket
    │   ├─ Llama a factory IA → obtiene proveedor
    │   ├─ IA.generar_respuesta()
    │   │   ├─ SI resuelve → UPDATE ticket SET estado=RESUELTO_IA
    │   │   └─ NO → UPDATE ticket SET estado=ESCALADO
    │   ├─ INSERT INTO interacciones (respuesta IA)
    │   └─ Calcula tiempo_atencion_seg
    │
    ├─ Response JSON TicketDetalle
    │
    └─ Frontend recibe código + muestra modal de éxito
```

### 4.2 Consultar Ticket (GET /tickets/{ref})

```
Cliente Frontend
    │
    ├─ Ingresa código en ChatPage.jsx
    │
    ├─ GET /tickets/{ticket_ref} → Backend
    │
    ├─ router.consultar_ticket() → ticket_service
    │
    ├─ ticket_service.obtener_ticket():
    │   ├─ SELECT * FROM tickets WHERE codigo=?
    │   ├─ SELECT * FROM interacciones WHERE ticket_id=?
    │   ├─ JOIN con cliente
    │   └─ Retorna TicketDetalle
    │
    ├─ Response JSON con conversación completa
    │
    └─ Frontend renderiza en ChatPage + Conversacion.jsx
```

### 4.3 Generar Reporte (GET /admin/reportes/mensual?mes=2026-08)

```
Admin (Browser)
    │
    ├─ Selecciona mes en AdminReportePage.jsx
    │
    ├─ GET /admin/reportes/mensual?mes=2026-08
    │
    ├─ router.reporte_mensual() → reporte_service
    │
    ├─ reporte_service.calcular_metricas():
    │   ├─ SELECT COUNT(*) FROM tickets WHERE fecha ∈ mes
    │   ├─ SELECT SUM(resuelto_por_ia=1) / total * 100
    │   ├─ SELECT AVG(tiempo_atencion_seg)
    │   ├─ SELECT * distribuido por tipo/estado
    │   ├─ Genera objeto Metricas
    │   └─ RETURN ReporteMensualOut
    │
    ├─ Response JSON con todos los KPIs
    │
    └─ Frontend renderiza gráficos (Recharts)
        └─ Línea, Pie, Barras interactivas
```

### 4.4 Generar Insights (GET /admin/reportes/mensual/insights?mes=2026-08)

```
Admin (Browser)
    │
    ├─ Clica en "Insights" en AdminReportePage.jsx
    │
    ├─ GET /admin/reportes/mensual/insights?mes=2026-08
    │
    ├─ router.insights_mensuales() → insights_service
    │
    ├─ insights_service.generar_insight():
    │   ├─ CHECK: ¿Existe en insight_mensual?
    │   │   ├─ SÍ (y recalcular=false) → RETURN cached
    │   │   └─ NO → Generar
    │   │
    │   ├─ reporte_service.calcular_metricas() → obtiene KPIs
    │   │
    │   ├─ IA.generar_insights(metricas):
    │   │   ├─ Prompt: "Analiza estos datos y genera insights"
    │   │   ├─ Google Gemini procesa
    │   │   └─ Retorna texto análisis en español
    │   │
    │   ├─ INSERT INTO insight_mensual (periodo, contenido)
    │   │
    │   └─ RETURN {"insight": "...", "cached": false}
    │
    ├─ Response JSON con análisis
    │
    └─ Frontend muestra en card
```

---

## 🔌 5. Patrón de Diseño: Factory Pattern (IA)

```
┌─────────────────────────────┐
│   app/ai/factory.py         │
│  ProveedorFactory           │
│                             │
│  crear_proveedor(nombre):   │
│    ├─ IF nombre == "gemini" │
│    │  └─ return Gemini()    │
│    ├─ IF nombre == "openai" │
│    │  └─ return OpenAI()    │
│    ├─ IF nombre == "ollama" │
│    │  └─ return Ollama()    │
│    └─ ELSE                  │
│       └─ return Mock()      │
│                             │
└────────┬────────────────────┘
         │
    ┌────┴───────────────────────────────────────┐
    │                                            │
    ▼                                            ▼
┌─────────────────────────┐      ┌─────────────────────────┐
│   GeminiProvider        │      │   MockProvider          │
│                         │      │                         │
│   generar_respuesta()   │      │   generar_respuesta()   │
│   ├─ API call Gemini    │      │   ├─ Palabras clave     │
│   ├─ Timeout: 30s       │      │   ├─ Reglas locales     │
│   ├─ tokens_consumidos  │      │   ├─ Respuesta fija     │
│   └─ modelo: "gemini-"  │      │   └─ Sin IA real        │
│                         │      │                         │
└─────────────────────────┘      └─────────────────────────┘
```

---

## 🔐 6. Capas de Seguridad

```
┌──────────────────────────────────────────────────┐
│  CAPA 1: VALIDACIÓN INPUT                         │
│  ├─ Pydantic schemas validan tipos               │
│  ├─ Email regex validado                         │
│  ├─ Sanitización de texto (no HTML/JS)           │
│  └─ Rango de valores controlado                  │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│  CAPA 2: PARAMETRIZED QUERIES                    │
│  ├─ SQLAlchemy ORM (no SQL strings)              │
│  ├─ Prevención SQL Injection                     │
│  └─ Prepared statements automáticos              │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│  CAPA 3: AUTENTICACIÓN (FUTURO)                  │
│  ├─ JWT tokens para admin                        │
│  ├─ Session management                           │
│  └─ Refresh tokens automáticos                   │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│  CAPA 4: AUTORIZACIÓN                            │
│  ├─ Role-based access control (RBAC)            │
│  ├─ Cliente vs Admin endpoints                   │
│  └─ Validación de propiedad                      │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│  CAPA 5: AUDITORÍA & LOGGING                     │
│  ├─ Registra cada acción                         │
│  ├─ Timestamps en UTC                            │
│  ├─ No guarda datos sensibles                    │
│  └─ Retención 90+ días                           │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│  CAPA 6: ENCRIPTACIÓN (PRODUCCIÓN)               │
│  ├─ HTTPS/TLS para transmisión                   │
│  ├─ Datos sensibles encriptados en reposo        │
│  └─ API keys en variables de entorno             │
└──────────────────────────────────────────────────┘
```

---

## 📦 7. Dependencias y Componentes Externos

```
┌────────────────────────────────────────────────────┐
│       SERVICIOS EXTERNOS                            │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │  Google Gemini API                           │ │
│  │  ├─ gemini-3.6-flash                         │ │
│  │  ├─ Cuota: Capa gratuita (60 reqs/min)       │ │
│  │  └─ Fallback: Mock provider                  │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │  OpenAI API (Opcional Fase 2)                │ │
│  │  └─ gpt-4, gpt-3.5-turbo                     │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │  Ollama Local (Opcional)                     │ │
│  │  └─ Mistral, Llama 2, etc.                   │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │  Email Service (Futuro)                      │ │
│  │  └─ SendGrid, AWS SES, etc.                  │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## 🗄️ 8. Modelo de Componentes Backend

```
app/
├── __init__.py
│
├── main.py
│   └─ FastAPI app creation, lifespan, middleware
│
├── core/
│   └── config.py
│       └─ Settings (env vars, CORS origins, defaults)
│
├── db/
│   ├── __init__.py
│   ├── base.py
│       └─ Base declarative class, metadata
│   ├── session.py
│       └─ SQLAlchemy engine, sessionmaker, get_db()
│
├── models/
│   ├── __init__.py
│   ├── cliente.py
│       └─ Modelo Cliente
│   ├── ticket.py
│       └─ Modelo Ticket
│   ├── interaccion.py
│       └─ Modelo Interacción
│   ├── insight_mensual.py
│       └─ Modelo InsightMensual
│   └── enums.py
│       └─ Enums (TipoTicket, EstadoTicket, etc.)
│
├── schemas/
│   ├── __init__.py
│   ├── ticket.py
│       ├─ TicketCreate (input)
│       ├─ TicketDetalle (output)
│       ├─ PaginaTickets (output paginado)
│       └─ MensajeCreate (input)
│   └── reporte.py
│       ├─ ReporteMensualOut
│       └─ MetricasOut
│
├── services/
│   ├── __init__.py
│   ├── ticket_service.py
│       ├─ crear_ticket()
│       ├─ obtener_ticket()
│       ├─ responder_mensaje()
│       ├─ listar_tickets()
│       ├─ escalar_ticket()
│       └─ calcular_tiempo_atencion()
│   ├── chatbot_service.py
│       ├─ procesar_solicitud()
│       ├─ resolver_con_ia()
│       └─ escalar_si_no_resoluble()
│   ├── reporte_service.py
│       ├─ calcular_metricas()
│       └─ generar_reporte_mensual()
│   ├── insights_service.py
│       ├─ generar_insight()
│       ├─ obtener_cached()
│       └─ recalcular_insight()
│   └── exporte_service.py
│       ├─ generar_excel()
│       └─ generar_pdf()
│
├── ai/
│   ├── __init__.py
│   ├── base.py
│       └─ Abstract ProveedorIA class
│   ├── factory.py
│       └─ ProveedorFactory.crear_proveedor()
│   ├── gemini_provider.py
│       └─ GeminiProvider (default)
│   ├── openai_provider.py
│       └─ OpenAIProvider
│   ├── ollama_provider.py
│       └─ OllamaProvider
│   ├── mock_provider.py
│       └─ MockProvider (fallback)
│   └── prompts.py
│       ├─ SISTEMA_PROMPT
│       ├─ PROMPT_INSIGHTS
│       └─ PROMPT_CLASIFICACION
│
└── routers/
    ├── __init__.py
    ├── tickets.py
    │   ├─ POST /tickets
    │   ├─ GET /tickets/{ref}
    │   └─ POST /tickets/{ref}/mensajes
    └── admin.py
        ├─ GET /admin/tickets
        ├─ GET /admin/reportes/mensual
        ├─ GET /admin/reportes/mensual/insights
        ├─ GET /admin/reportes/mensual/exportar/excel
        └─ GET /admin/reportes/mensual/exportar/pdf
```

---

## 🎨 9. Modelo de Componentes Frontend

```
src/
├── main.jsx
│   └─ React.StrictMode + ReactDOM.createRoot()
│
├── App.jsx
│   └─ BrowserRouter + Routes
│
├── App.css
│   └─ Estilos globales
│
├── index.css
│   └─ Tailwind directives
│
├── api/
│   └── client.js
│       ├─ API base URL
│       ├─ POST /tickets
│       ├─ GET /tickets/{ref}
│       ├─ POST /tickets/{ref}/mensajes
│       ├─ GET /admin/tickets
│       ├─ GET /admin/reportes/mensual
│       ├─ GET /admin/reportes/mensual/insights
│       └─ Exportes
│
├── components/
│   ├── Layout.jsx
│   │   └─ Navbar, Footer, Wrapper
│   ├── Conversacion.jsx
│   │   └─ Muestra mensajes en orden
│   └── badges.jsx
│       └─ Estado de ticket (color, texto)
│
└── pages/
    ├── InicioPage.jsx
    │   └─ Página inicial, nav a crear ticket
    ├── ConsultaPage.jsx
    │   └─ Formulario para crear solicitud
    ├── ChatPage.jsx
    │   └─ Visualización de conversación
    ├── AdminDashboardPage.jsx
    │   ├─ KPIs (cards)
    │   └─ Gráficos (Recharts)
    ├── AdminTicketsPage.jsx
    │   ├─ Filtros
    │   └─ Tabla paginada
    └── AdminReportePage.jsx
        ├─ Selector de mes
        ├─ Reporte visual
        ├─ Insights
        └─ Botones exportar (Excel, PDF)
```

---

## ⚙️ 10. Flujo de Despliegue (Deployment)

```
DESARROLLO
├─ Frontend: localhost:5173 (pnpm dev)
├─ Backend: localhost:8000 (uvicorn --reload)
└─ DB: dev.db (SQLite)

STAGING
├─ Frontend: CDN (static)
├─ Backend: Docker container (FastAPI)
├─ DB: PostgreSQL cloud
└─ Env: staging.env

PRODUCCIÓN
├─ Frontend: CDN + nginx
├─ Backend: Docker Kubernetes
├─ DB: PostgreSQL cluster (replicación)
└─ Env: production.env (secretos en vault)
```

---

## 📊 11. Estadísticas de Arquitectura

| Aspecto | Valor |
|---------|-------|
| Capas | 5 (Presentation, API, Business, Access, DB) |
| Servicios | 5 (ticket, chatbot, reporte, insights, exporte) |
| Routers | 2 (tickets, admin) |
| Endpoints | 7 |
| Modelos ORM | 4 |
| Tablas | 4 |
| Índices | 6 |
| Proveedores IA | 4 (Gemini, OpenAI, Ollama, Mock) |
| Componentes Frontend | 8 (Layout, 6 pages, badges) |
| Reutilización | 85%+ (código DRY) |

---

## ✅ 12. Principios Arquitectónicos Aplicados

✅ **Separación de Concerns:** Cada capa tiene responsabilidad específica  
✅ **DRY (Don't Repeat Yourself):** Código reutilizable en services  
✅ **SOLID Principles:** Factory pattern, dependency injection  
✅ **Stateless Design:** Frontend SPA, backend stateless (fácil escalado)  
✅ **Fallback Mechanisms:** Mock provider si IA falla  
✅ **Async/Await:** FastAPI nativo asincrónico  
✅ **Type Safety:** Pydantic validation, TypeScript (futuro)  
✅ **Resilience:** Retry logic, timeout handling  

---

**Documento:** Diagrama de Arquitectura  
**Versión:** 1.0  
**Fecha:** Agosto 31, 2026  
**Estado:** ✅ Aprobado para Implementación
