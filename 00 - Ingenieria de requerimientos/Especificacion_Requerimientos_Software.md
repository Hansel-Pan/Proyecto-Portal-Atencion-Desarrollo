# Especificación de Requerimientos de Software
## Portal Empresarial de Atención al Cliente con IA

**Documento:** ERS (Especificacion Requerimientos Software)  
**Versión:** 1.0  
**Fecha:** Agosto 31, 2026  

---

## 📋 Índice de Contenidos

1. Introducción
2. Descripción General del Producto
3. Requisitos Funcionales
4. Requisitos No Funcionales
5. Requisitos de Interfaz
6. Requisitos de Datos
7. Requisitos de Seguridad
8. Requisitos de Confiabilidad
9. Requisitos de Rendimiento
10. Atributos de Calidad
11. Restricciones de Implementación
12. Matriz de Trazabilidad

---

## 1️⃣ Introducción

### 1.1 Propósito

Este documento especifica los requisitos completos de software para el **Portal Empresarial de Atención al Cliente con IA**. Incluye requisitos funcionales, no funcionales, interfaces, datos, seguridad y calidad. Sirve como contrato entre stakeholders y equipo de desarrollo.

### 1.2 Audiencia

- Desarrolladores backend y frontend
- Gestores de proyecto
- Personal de QA/Testing
- Stakeholders de negocio
- Arquitectos de software

### 1.3 Alcance del Documento

Especifica todos los requisitos técnicos derivados de los 15 casos de uso documentados. Excluye documentación de deployment, operaciones y soporte.

### 1.4 Convenciones y Terminología

- **REQ-FN-XXX:** Requisito Funcional (Functional)
- **REQ-NF-XXX:** Requisito No Funcional (Non-Functional)
- **REQ-INT-XXX:** Requisito de Interfaz
- **REQ-DATA-XXX:** Requisito de Datos
- **REQ-SEC-XXX:** Requisito de Seguridad
- **MUST:** Obligatorio
- **SHOULD:** Altamente recomendado
- **MAY:** Opcional para versión futura

---

## 2️⃣ Descripción General del Producto

### 2.1 Perspectiva del Producto

Sistema web de dos capas (frontend + backend) que automatiza atención al cliente mediante chatbot IA. Usuarios sin registro pueden crear solicitudes, consultar estado y enviar mensajes. Administradores visualizan métricas, gestionan casos escalados y exportan reportes.

### 2.2 Funcionamiento del Producto

```
Cliente → Crea Ticket → IA Procesa → Resuelve O Escala
                              ↓
                      Admin Revisa → Responde → Cierra
                              ↓
                      Métricas → Reporte → Insights → Exportes
```

### 2.3 Usuarios y Características

| Usuario | Características Clave | Volumen Esperado |
|---------|----------------------|-----------------|
| Cliente | Crear/consultar tickets, chat | 1,000+ diarios |
| Admin | Gestionar, reportar, exportar | 10-20 diarios |
| Ejecutivo | Dashboard, insights | 5-10 diarios |

### 2.4 Ambiente de Operación

- **Frontend:** Navegador moderno (Chrome, Firefox, Safari, Edge)
- **Backend:** Servidor Linux/Windows con Python 3.12+
- **Base de Datos:** SQLite (dev), PostgreSQL (producción)
- **Conectividad:** Internet 24/7, HTTPS recomendado

### 2.5 Dependencias y Restricciones

- Google Gemini API disponible
- Node.js 18+ y Python 3.12+ instalados
- Hosting con 2+ GB RAM mínimo

---

## 3️⃣ Requisitos Funcionales

### 3.1 Módulo: Creación de Solicitudes

#### REQ-FN-001: Crear Nueva Solicitud (MUST)
- **Descripción:** Cliente puede crear nueva solicitud sin autenticación
- **Entrada:** Nombre, email, teléfono, tipo (Consulta/Petición/Queja), asunto, descripción
- **Proceso:** 
  1. Validar datos (email válido, campos requeridos)
  2. Generar código único (TK-YYYY-XXXXXX)
  3. Guardar en base de datos
  4. Enviar a procesamiento IA
- **Salida:** Código de referencia, confirmación visual
- **Datos:** Crear registro en tabla `clientes` (si no existe) y `tickets`
- **Errores:** Email inválido → mensaje de error; Campos vacíos → validación frontend
- **Verificación:** Smoke test CU-001

#### REQ-FN-002: Generar Código Único de Ticket (MUST)
- **Descripción:** Cada ticket recibe código único, público e inmutable
- **Formato:** `TK-YYYY-XXXXXX` (ej: TK-2026-001234)
- **Garantía:** No puede repetirse, indexado en BD
- **Uso:** Cliente consulta ticket usando este código
- **Implementación:** Algoritmo incremental en base de datos

#### REQ-FN-003: Validar Entrada de Formulario (MUST)
- **Email:** Formato válido, requerido
- **Teléfono:** Formato básico, requerido
- **Asunto:** 1-200 caracteres, requerido
- **Descripción:** 1-5000 caracteres, requerido
- **Tipo:** Debe ser Consulta, Petición o Queja
- **Feedback:** Mensajes de error específicos en español

#### REQ-FN-004: Guardar Solicitud en Base de Datos (MUST)
- **Tabla:** `tickets`, `clientes`, `interacciones`
- **Campos:** id, codigo, cliente_id, tipo, asunto, descripcion, estado, prioridad, fecha_creacion, etc.
- **Indexación:** codigo (único), cliente_id, estado, fecha_creacion
- **Transacción:** Atómica (todo o nada)

---

### 3.2 Módulo: Procesamiento IA

#### REQ-FN-005: Procesar Solicitud con Chatbot IA (MUST)
- **Descripción:** IA analiza solicitud automáticamente después de creación
- **Entrada:** Descripción del ticket
- **Proveedores Soportados:** Google Gemini (default), OpenAI, Ollama, Mock
- **Proceso:**
  1. Detectar palabras clave resoluble (horario, contraseña, factura, garantía)
  2. Generar respuesta contextual
  3. Registrar modelo y tokens
  4. Decidir: Resolver O Escalar
- **Salida:** Respuesta y decisión de acción
- **Fallback:** Si IA falla → Proveedor Mock automático
- **Verificación:** Smoke test CU-004

#### REQ-FN-006: Resolver Automáticamente (MUST)
- **Condición:** IA identifica solicitud como resoluble
- **Acción:** 
  1. Cambiar estado a `RESUELTO_IA`
  2. Establecer `resuelto_por_ia = true`
  3. Registrar respuesta como interacción
  4. Calcular tiempo de atención
- **Límite de Tiempo:** Máximo 30 segundos para generar respuesta
- **Notificación:** Email a cliente (opcional en Fase 1)

#### REQ-FN-007: Usar Múltiples Proveedores IA (MUST)
- **Gemini:** `AI_PROVIDER=gemini` (default)
- **OpenAI:** `AI_PROVIDER=openai` con API key
- **Ollama:** `AI_PROVIDER=ollama` local
- **Mock:** `AI_PROVIDER=mock` reglas locales, sin API
- **Configuración:** Via `.env` en backend
- **Switching:** Cambiar provider reiniciando servidor

#### REQ-FN-008: Fallback Automático a Mock (MUST)
- **Cuándo:** IA principal falla (timeout, API error, sin key)
- **Acción:** Usar proveedor Mock automáticamente
- **Log:** Registrar warning en logs
- **Resultado:** Sistema NO falla, continúa operativo
- **User Impact:** Respuesta menos sofisticada pero funcional

#### REQ-FN-009: Registrar Tokens Consumidos (MUST)
- **Campo:** `interacciones.tokens_consumidos`
- **Valor:** Número exacto de tokens usados
- **Uso:** Auditoría de costos, optimización
- **Null:** Permitido si proveedor no reporta tokens

#### REQ-FN-010: Guardar Modelo IA Utilizado (MUST)
- **Campo:** `interacciones.modelo_ia`
- **Ejemplos:** "gemini-3.6-flash", "gpt-4", "ollama-mistral"
- **Uso:** Trazabilidad, análisis de performance

---

### 3.3 Módulo: Escalamiento

#### REQ-FN-011: Escalar Ticket Automáticamente (MUST)
- **Condición:** IA no puede resolver
- **Acción:**
  1. Cambiar estado a `ESCALADO`
  2. Establecer prioridad a `ALTA`
  3. Crear notificación para admin
  4. Ticket aparece en cola de pendientes
- **Sin Intervención:** Totalmente automático
- **Tiempo:** Instantáneo (< 1 segundo)

#### REQ-FN-012: Asignar Prioridad Automática (MUST)
- **Escalados:** Siempre `ALTA`
- **Resueltos IA:** `MEDIA` (default)
- **Quejas:** `ALTA` (default)
- **Cambio Manual:** Admin puede cambiar después

#### REQ-FN-013: Crear Notificación de Escalamiento (SHOULD)
- **Destinatario:** Equipo de administración
- **Canal:** Panel admin (visible en listado)
- **Futura Mejora:** Notificación por email/SMS

---

### 3.4 Módulo: Consulta de Tickets

#### REQ-FN-014: Consultar Ticket por Código Público (MUST)
- **Entrada:** Código de ticket (ej: TK-2026-001234)
- **Salida:**
  - Estado actual
  - Tipo y asunto
  - Descripción original
  - Conversación completa
  - Tiempo de atención
  - Fecha de creación/resolución
  - Calificación de satisfacción
- **Validación:** 404 si no existe
- **Verificación:** Smoke test CU-002

#### REQ-FN-015: Consultar Ticket por ID Numérico (MUST)
- **Entrada:** ID numérico del ticket (ej: 12345)
- **Salida:** Misma información que REQ-FN-014
- **Restricción:** Uso interno o admin

#### REQ-FN-016: Mostrar Conversación Completa (MUST)
- **Contenido:** Todos los mensajes en orden cronológico
- **Campos:** contenido, rol (cliente/ia/admin), timestamp
- **Formato:** Conversación legible, estilos visuales por rol
- **Scroll:** Autodesplazarse al final

#### REQ-FN-017: Mostrar Estado de Ticket (MUST)
- **Estados Posibles:**
  - `ABIERTO`: Recién creado, pendiente IA
  - `RESUELTO_IA`: Resuelto automáticamente
  - `ESCALADO`: En cola para admin
  - `CERRADO`: Resolución completada
- **Visualización:** Badge de color por estado
- **Actualización:** En tiempo real si es posible

---

### 3.5 Módulo: Envío de Mensajes

#### REQ-FN-018: Enviar Mensaje Adicional a Ticket Abierto (MUST)
- **Condición:** Ticket en estado ABIERTO, RESUELTO_IA o ESCALADO
- **Entrada:** Texto del mensaje (1-5000 caracteres)
- **Proceso:**
  1. Validar ticket existe
  2. Crear registro en `interacciones`
  3. Registrar rol = "cliente"
  4. Timestamp automático
- **Salida:** Mensaje aparece en conversación
- **Errores:** 404 si ticket no existe, 400 si ticket cerrado
- **Verificación:** Smoke test CU-003

#### REQ-FN-019: Registrar Interacción de Cliente (MUST)
- **Tabla:** `interacciones`
- **Campos:** ticket_id, contenido, rol, fecha, cliente_id (opcional)
- **Auditoría:** Permanente, no se puede eliminar

#### REQ-FN-020: Ticket Permanece en Escalado (MUST)
- **Restricción:** Mensaje de cliente NO cambia estado
- **Ticket ESCALADO:** Permanece `ESCALADO` (admin debe resolver)
- **Behavior:** Diferencia respecto a sistema típico

---

### 3.6 Módulo: Gestión de Admin

#### REQ-FN-021: Listar Tickets (MUST)
- **Filtros Soportados:**
  - Tipo: Consulta, Petición, Queja (múltiple)
  - Estado: Abierto, Resuelto IA, Escalado, Cerrado
  - Prioridad: Baja, Media, Alta
  - Rango de fechas: Desde y Hasta
- **Paginación:**
  - Página (desde 1)
  - Tamaño: 1-100 items (default 20)
  - Total de registros retornado
- **Ordenamiento:** Fecha descendente (default)
- **Validación:** Parámetros válidos según tipo enum
- **Verificación:** Smoke test CU-008

#### REQ-FN-022: Filtro de Tipo (MUST)
- **Valores:** CONSULTA, PETICION, QUEJA
- **Múltiple:** Soporta filtrar por varios tipos
- **Null:** Equivale a "sin filtro"

#### REQ-FN-023: Filtro de Estado (MUST)
- **Valores:** ABIERTO, RESUELTO_IA, ESCALADO, CERRADO
- **Múltiple:** Soporta varios estados
- **Restricción:** Admin típicamente verá ESCALADO

#### REQ-FN-024: Filtro de Prioridad (MUST)
- **Valores:** BAJA, MEDIA, ALTA
- **Uso:** Priorizar casos urgentes
- **Default:** Mostrar todas (si no se filtra)

#### REQ-FN-025: Filtro de Fechas (MUST)
- **Parámetros:** fecha_desde, fecha_hasta
- **Formato:** YYYY-MM-DD
- **Lógica:** Inclusivo en ambos extremos
- **Validación:** fecha_desde ≤ fecha_hasta

#### REQ-FN-026: Paginación (MUST)
- **Parámetro:** pagina (1-based), tamanio_pagina (1-100)
- **Default:** pagina=1, tamanio_pagina=20
- **Total:** Campo `total` en respuesta
- **Cálculo:** (Total + tamanio_pagina - 1) / tamanio_pagina = total_paginas

#### REQ-FN-027: Responder a Ticket Escalado (MUST)
- **Condición:** Ticket en estado ESCALADO
- **Entrada:** Mensaje de respuesta
- **Proceso:**
  1. Validar ticket existe y está escalado
  2. Crear interacción con rol="admin"
  3. Guardar timestamp
- **Salida:** Mensaje aparece en conversación
- **Verificación:** Smoke test CU-006

#### REQ-FN-028: Cerrar Ticket (MUST)
- **Condición:** Admin responde ticket escalado
- **Acción:** Cambiar estado a CERRADO
- **Campo:** fecha_resolucion = ahora
- **Cálculo:** tiempo_atencion_seg = fecha_resolucion - fecha_creacion
- **Cierre:** Conversación finaliza para cliente

#### REQ-FN-029: Cambiar Prioridad Manual (SHOULD)
- **Permiso:** Solo admin
- **Valores:** BAJA, MEDIA, ALTA
- **Trigger:** No automático, decisión manual
- **Log:** Registrar cambio

---

### 3.7 Módulo: Reportes

#### REQ-FN-030: Generar Reporte Mensual (MUST)
- **Entrada:** Mes en formato YYYY-MM
- **Validación:** Formato válido, mes no futuro
- **Proceso:** Agregación SQL de tickets del mes
- **Salida:** Objeto `ReporteMensual` con todas las métricas
- **Performance:** < 5 segundos incluso con 10,000+ tickets
- **Caché:** Opcional para meses pasados
- **Verificación:** Smoke test CU-009

#### REQ-FN-031: Calcular Total de Tickets (MUST)
- **Campo:** `total_tickets`
- **Fórmula:** COUNT(*) WHERE fecha_creacion en mes
- **Subcategorías:**
  - `total_consultas`: COUNT(*) WHERE tipo=CONSULTA
  - `total_peticiones`: COUNT(*) WHERE tipo=PETICION
  - `total_quejas`: COUNT(*) WHERE tipo=QUEJA

#### REQ-FN-032: Calcular Tasa de Resolución IA (MUST)
- **Campo:** `tasa_resolucion_ia`
- **Fórmula:** (COUNT(*) WHERE resuelto_por_ia=true) / total_tickets * 100
- **Precisión:** 2 decimales
- **Rango:** 0-100%
- **Ejemplo:** "72.45%" = 72 IA, 28 humanas de 100 tickets

#### REQ-FN-033: Calcular Tiempo Promedio de Atención (MUST)
- **Campo:** `tiempo_promedio_atencion_seg`
- **Fórmula:** AVG(tiempo_atencion_seg) for tickets resueltos
- **Unidad:** Segundos
- **Rango:** 1-infinito
- **Ejemplo:** 84.5 segundos = ~1.4 minutos

#### REQ-FN-034: Distribuir por Estado (MUST)
- **Campos:** 
  - `resuelto_ia_count`: Tickets RESUELTO_IA
  - `escalado_count`: Tickets ESCALADO
  - `cerrado_count`: Tickets CERRADO
  - `abierto_count`: Tickets ABIERTO (usualmente 0 en mes cerrado)
- **Validación:** Suma = total_tickets

#### REQ-FN-035: Contar Tickets Pendientes (MUST)
- **Campo:** `tickets_pendientes`
- **Condición:** Estado != CERRADO en mes actual
- **Uso:** Identificar backlog

#### REQ-FN-036: Distribución Visual (MUST)
- **Gráfico 1:** Línea temporal (tickets/día)
- **Gráfico 2:** Pie (tipo de solicitud)
- **Gráfico 3:** Barras (estado)
- **Gráfico 4:** Línea (tendencia IA vs humana)
- **Librería:** Recharts (React)

#### REQ-FN-037: Generar Insights con IA (MUST)
- **Trigger:** Admin solicita insights
- **Input:** Todas las métricas del mes
- **Proveedor:** Google Gemini (mismo que tickets)
- **Output:** Texto en español con análisis y recomendaciones
- **Caché:** Almacenar por mes en tabla `insight_mensual`
- **TTL:** 30 días (después se puede recalcular)
- **Recálculo:** Parámetro `recalcular=true` fuerza regeneración
- **Verificación:** Smoke test CU-010

#### REQ-FN-038: Contenido de Insights (SHOULD)
- Tendencias observadas en el mes
- Patrones de consultas frecuentes
- Problemas identificados
- Recomendaciones de mejora
- Oportunidades de automatización
- Comparación con mes anterior (si existe)

---

### 3.8 Módulo: Exportes

#### REQ-FN-039: Exportar Reporte a Excel (MUST)
- **Formato:** .xlsx (Microsoft Excel 2007+)
- **Nombre:** Reporte_YYYY-MM.xlsx
- **Contenido:**
  - Hoja 1: Resumen ejecutivo (KPIs)
  - Hoja 2: Detalles de tickets (todos del mes)
  - Hoja 3: Análisis por tipo
  - Hoja 4: Análisis por estado
  - Hoja 5: Datos brutos
- **Estilos:** Colores, negrita, bordes
- **Performance:** < 10 segundos incluso con 10,000 registros
- **Descarga:** Automática al cliente
- **Verificación:** Smoke test CU-011

#### REQ-FN-040: Contenido Hoja 1 (Excel) (MUST)
- Período: YYYY-MM
- KPIs: Total, IA%, Tiempo promedio, Satisfacción
- Gráficos: Pastel (tipo), Barras (estado)
- Fuente: Calibri 11pt, centrado

#### REQ-FN-041: Contenido Hoja 2 (Excel) (MUST)
- Columnas: ID, Código, Cliente, Tipo, Estado, Prioridad, IA, Tiempo seg, Satisfacción
- Filas: Todos los tickets del mes
- Totales: Pie de página con COUNT y PROMEDIO
- Filtros: Habilitados en header (Excel autofilter)

#### REQ-FN-042: Exportar Reporte a PDF (MUST)
- **Formato:** PDF (ISO 32000-1)
- **Nombre:** Reporte_YYYY-MM.pdf
- **Contenido:**
  - Portada con encabezado y período
  - Índice
  - Resumen ejecutivo (1 página)
  - Gráficos e ilustraciones (2-3 páginas)
  - Tablas detalladas (5+ páginas)
  - Recomendaciones y conclusiones
- **Página:** A4, márgenes 20mm
- **Estilo:** Profesional, colores corporativos
- **Performance:** < 15 segundos incluso con 10,000 registros
- **Descarga:** Automática al cliente
- **Verificación:** Smoke test CU-012

#### REQ-FN-043: Validación de Mes en Exportes (MUST)
- **Formato:** YYYY-MM (ej: 2026-08)
- **Validación:**
  - Largo exacto: 7 caracteres
  - Separador: Guión en posición 4
  - Año: 4 dígitos, 2000-2099
  - Mes: 2 dígitos, 01-12
- **Error:** 422 Unprocessable Entity si inválido

---

### 3.9 Módulo: Datos y Auditoría

#### REQ-FN-044: Registrar Cada Interacción (MUST)
- **Tabla:** `interacciones`
- **Campos:** ticket_id, contenido, rol, modelo_ia, tokens, fecha
- **Rol Permitido:** "cliente", "ia", "admin"
- **Timestamp:** Automático, zona horaria UTC
- **Permanente:** No se puede eliminar
- **Auditoría:** Permite reconstruir conversación exacta

#### REQ-FN-045: Calcular Tiempo de Atención (MUST)
- **Cuándo:** Ticket se resuelve
- **Fórmula:** fecha_resolucion - fecha_creacion (en segundos)
- **Campo:** `tickets.tiempo_atencion_seg`
- **Nulo:** Null si ticket aún abierto
- **Precisión:** Segundos (sin decimales)

#### REQ-FN-046: Indexar Campos de Búsqueda Frecuente (MUST)
- `tickets.codigo` (único)
- `tickets.cliente_id`
- `tickets.estado`
- `tickets.fecha_creacion`
- `interacciones.ticket_id`
- **Beneficio:** Consultas < 100ms incluso con 100,000+ registros

#### REQ-FN-047: Validar Unicidad de Código (MUST)
- **Constraint:** UNIQUE en base de datos
- **Error:** Si se intenta duplicar → DB rechaza
- **Algoritmo:** Incremental o UUID
- **Colisiones:** Imposibles (garantizado por BD)

---

## 4️⃣ Requisitos No Funcionales

### 4.1 Rendimiento

#### REQ-NF-001: Latencia de API (MUST)
- **P50 (mediana):** < 200ms
- **P95 (percentil 95):** < 500ms
- **P99 (percentil 99):** < 1s
- **Método:** Profiling con herramientas (pytest-benchmark)
- **Exclusiones:** Exportes (hasta 15s permitido)

#### REQ-NF-002: Throughput (MUST)
- **Solicitudes concurrentes:** ≥ 100 simultáneas
- **Requests/segundo:** ≥ 10 req/s sin degradación
- **Test:** Load testing con Locust

#### REQ-NF-003: Tiempo de Respuesta IA (MUST)
- **Máximo:** 30 segundos para generar respuesta
- **Timeout:** Fallback a Mock si excede
- **Métrica:** Registrar en logs

#### REQ-NF-004: Exportes (MUST)
- **Excel:** < 10 segundos para 10,000 registros
- **PDF:** < 15 segundos para 10,000 registros
- **Streaming:** Permitido para archivos grandes

---

### 4.2 Disponibilidad y Confiabilidad

#### REQ-NF-005: Uptime (MUST)
- **Objetivo:** 99.9% (máximo 43 minutos downtime/mes)
- **Medición:** Automated health checks cada 5 minutos
- **SLA:** Incluir en contrato de hosting

#### REQ-NF-006: Recuperación ante Fallos (MUST)
- **Validación de Datos:** Antes de guardar en BD
- **Transacciones:** Atómicas (todo o nada)
- **Rollback:** Automático si error
- **Fallback IA:** Proveedor Mock si Gemini falla
- **Logs:** Registrar todo error para análisis

#### REQ-NF-007: Manejo de Errores (MUST)
- **HTTP 4xx:** Para errores de cliente (validación)
  - 400: Bad Request
  - 404: Not Found
  - 422: Unprocessable Entity
- **HTTP 5xx:** Para errores de servidor
  - 500: Internal Server Error (genérico)
  - 503: Service Unavailable (IA no disponible)
- **Mensajes:** En español, descriptivos

#### REQ-NF-008: Backup y Recuperación (SHOULD)
- **Frecuencia:** Diaria
- **Estrategia:** Backup de base de datos + archivos estáticos
- **Retención:** 30 días mínimo
- **RTO (Recovery Time Objective):** < 1 hora
- **RPO (Recovery Point Objective):** < 1 día

---

### 4.3 Escalabilidad

#### REQ-NF-009: Escalabilidad Horizontal (SHOULD)
- **Arquitectura:** Stateless (sin estado en servidor)
- **Sessions:** Usar JWT o similar (futuro)
- **BD:** Preparado para replicación (PostgreSQL)
- **Caché:** Redis para Fase 2 (opcional)

#### REQ-NF-010: Crecimiento de Datos (MUST)
- **Año 1:** ~ 1 millón de tickets
- **Tamaño BD:** SQLite ~ 500MB, PostgreSQL ~ 2GB
- **Migración:** Plan de SQLite a PostgreSQL documentado

---

### 4.4 Usabilidad

#### REQ-NF-011: Interfaz Intuitiva (MUST)
- **Navegación:** Menú claro, breadcrumbs
- **Formularios:** Validación en tiempo real
- **Iconos:** SVG claros, etiquetados
- **Colores:** Accessible (WCAG AA mínimo)
- **Responsive:** Mobile-first, funciona en tablet/desktop

#### REQ-NF-012: Accesibilidad (SHOULD)
- **WCAG 2.1 Level A:** Obligatorio
- **WCAG 2.1 Level AA:** Recomendado
- **Screen Readers:** Etiquetas ARIA
- **Teclado:** Navegación sin ratón

#### REQ-NF-013: Idioma (MUST)
- **UI:** Español latinoamericano
- **Mensajes:** Claros, sin jerga técnica
- **Validaciones:** Texto descriptivo
- **Errores:** Soluciones sugeridas

#### REQ-NF-014: Responsividad (MUST)
- **Breakpoints:** 320px (mobile), 768px (tablet), 1024px (desktop)
- **Prueba:** Navegadores populares en cada tamaño
- **Touch:** Botones ≥ 44x44px en mobile

---

### 4.5 Compatibilidad

#### REQ-NF-015: Navegadores Soportados (MUST)
- Chrome 120+
- Firefox 121+
- Safari 17+
- Edge 120+
- Opera 106+
- Versiones 2 años atrás mínimo

#### REQ-NF-016: Sistemas Operativos (MUST)
- **Frontend:** Windows 10+, macOS 10.15+, Linux (Ubuntu 20.04+)
- **Backend:** Linux (recomendado), Windows con WSL2

#### REQ-NF-017: Versiones de Software (MUST)
- Python 3.12+ (no 3.11 ni anteriores)
- Node.js 18+ (no 16 ni anteriores)
- SQLite 3.35+ (incluso en Python)
- FastAPI 0.100+

---

### 4.6 Mantenibilidad

#### REQ-NF-018: Documentación de Código (MUST)
- **Docstrings:** Todas las funciones backend
- **Comentarios:** Lógica compleja explicada
- **README:** Instrucciones de setup
- **API Docs:** Swagger/OpenAPI automático en FastAPI

#### REQ-NF-019: Estructura Modular (MUST)
- **Separación:** routers, services, models, schemas, db
- **Reutilización:** Código DRY (Don't Repeat Yourself)
- **Testing:** Unidades testeable

#### REQ-NF-020: Control de Versiones (MUST)
- **Git:** Commits pequeños, mensajes descriptivos
- **Branching:** feature/, bugfix/, main
- **Tag:** Versión semántica (v0.1.0, v1.0.0)

---

### 4.7 Portabilidad

#### REQ-NF-021: Docker (SHOULD)
- **Imagen:** Backend en contenedor Docker
- **Compose:** docker-compose.yml para orquestación
- **Volúmenes:** Base de datos persistente

#### REQ-NF-022: Dependencias Externas (MUST)
- **requirements.txt:** Python
- **package.json:** Node.js
- **Versions:** Pinned (no floating versions)
- **Lockfiles:** pnpm-lock.yaml y pip.lock

---

## 5️⃣ Requisitos de Interfaz

### 5.1 Interfaz de Usuario (Frontend)

#### REQ-INT-001: Página de Inicio (MUST)
- **URL:** `/`
- **Componente:** InicioPage.jsx
- **Contenido:**
  - Bienvenida y descripción del sistema
  - Botones: "Crear Solicitud", "Consultar Ticket"
  - FAQ o información adicional
- **Diseño:** Hero section + cards

#### REQ-INT-002: Página de Crear Solicitud (MUST)
- **URL:** `/consulta`
- **Componente:** ConsultaPage.jsx
- **Formulario:**
  - Nombre (text, requerido)
  - Email (email, requerido, validado)
  - Teléfono (tel, requerido)
  - Tipo (radio: Consulta/Petición/Queja)
  - Asunto (text, 200 char max)
  - Descripción (textarea, 5000 char max)
  - Botón: "Enviar"
- **Validación:** Real-time en frontend
- **Feedback:** Spinner mientras se procesa IA
- **Success:** Modal con código de ticket

#### REQ-INT-003: Página de Chat (MUST)
- **URL:** `/chat`
- **Componente:** ChatPage.jsx
- **Contenido:**
  - Campo para ingresar código ticket
  - O redirigir desde `/consulta` con código
  - Mostrar conversación en Conversacion.jsx
  - Campo para enviar mensaje
- **Actualización:** En tiempo real si es posible

#### REQ-INT-004: Dashboard Admin (MUST)
- **URL:** `/admin`
- **Componente:** AdminDashboardPage.jsx
- **KPIs:**
  - Total tickets mes
  - % IA
  - Tiempo promedio
  - Pendientes
- **Gráficos:** Recharts (línea, pie, barras)
- **Resumen IA:** Texto con insights

#### REQ-INT-005: Gestión de Tickets Admin (MUST)
- **URL:** `/admin/tickets`
- **Componente:** AdminTicketsPage.jsx
- **Filtros:** Tipo, Estado, Prioridad, Fechas
- **Tabla:** Listado paginado de tickets
- **Acciones:** Click para abrir, responder, cerrar

#### REQ-INT-006: Reportes y Exportes (MUST)
- **URL:** `/admin/reportes`
- **Componente:** AdminReportePage.jsx
- **Inputs:** Selector de mes (YYYY-MM)
- **Botones:** "Ver Reporte", "Excel", "PDF", "Insights"
- **Visualización:** Gráficos interactivos

#### REQ-INT-007: Componente Layout (MUST)
- **Componente:** Layout.jsx
- **Contenido:** Navbar, navegación, footer
- **Elementos:** Logo, menú, breadcrumbs

#### REQ-INT-008: Badges de Estado (MUST)
- **Componente:** badges.jsx
- **Estilos:** Color por estado
  - ABIERTO: Azul
  - RESUELTO_IA: Verde
  - ESCALADO: Naranja
  - CERRADO: Gris

---

### 5.2 Interfaz de API

#### REQ-INT-009: Documentación Swagger (MUST)
- **URL:** http://localhost:8000/docs
- **Auto-generada:** FastAPI crea automáticamente
- **Contenido:** Todos los endpoints, parámetros, ejemplos
- **Prueba:** Try-it-out para testear desde UI

#### REQ-INT-010: Formato JSON (MUST)
- **Request/Response:** JSON puro
- **Content-Type:** application/json
- **Encoding:** UTF-8
- **Schemas:** Validados con Pydantic

#### REQ-INT-011: Respuesta de Error (MUST)
```json
{
  "detail": "Mensaje de error descriptivo en español"
}
```

#### REQ-INT-012: Respuesta de Éxito (MUST)
```json
{
  "data": {...},
  "status": "success"
}
```

---

## 6️⃣ Requisitos de Datos

### 6.1 Modelo de Datos

#### REQ-DATA-001: Tabla Clientes (MUST)
```sql
CREATE TABLE clientes (
  id INTEGER PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  telefono VARCHAR(20),
  fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### REQ-DATA-002: Tabla Tickets (MUST)
```sql
CREATE TABLE tickets (
  id INTEGER PRIMARY KEY,
  codigo VARCHAR(24) UNIQUE NOT NULL,
  cliente_id INTEGER NOT NULL FOREIGN KEY,
  tipo ENUM('CONSULTA', 'PETICION', 'QUEJA') NOT NULL,
  asunto VARCHAR(200) NOT NULL,
  descripcion TEXT NOT NULL,
  estado ENUM('ABIERTO', 'RESUELTO_IA', 'ESCALADO', 'CERRADO') DEFAULT 'ABIERTO',
  prioridad ENUM('BAJA', 'MEDIA', 'ALTA') DEFAULT 'MEDIA',
  resuelto_por_ia BOOLEAN DEFAULT FALSE,
  tiempo_atencion_seg INTEGER,
  fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
  fecha_resolucion DATETIME,
  satisfaccion INTEGER CHECK(satisfaccion >= 1 AND satisfaccion <= 5)
);
```

#### REQ-DATA-003: Tabla Interacciones (MUST)
```sql
CREATE TABLE interacciones (
  id INTEGER PRIMARY KEY,
  ticket_id INTEGER NOT NULL FOREIGN KEY,
  contenido TEXT NOT NULL,
  rol ENUM('cliente', 'ia', 'admin') NOT NULL,
  modelo_ia VARCHAR(50),
  tokens_consumidos INTEGER,
  fecha DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### REQ-DATA-004: Tabla InsightMensual (MUST)
```sql
CREATE TABLE insight_mensual (
  id INTEGER PRIMARY KEY,
  periodo VARCHAR(7) UNIQUE NOT NULL,  -- YYYY-MM
  contenido TEXT NOT NULL,  -- JSON
  fecha_generacion DATETIME DEFAULT CURRENT_TIMESTAMP,
  generado_por_ia BOOLEAN DEFAULT TRUE
);
```

### 6.2 Integridad de Datos

#### REQ-DATA-005: Validación de Entradas (MUST)
- **Frontend:** Validación en tiempo real
- **Backend:** Re-validación de todos los inputs
- **BD:** Constraints y checks

#### REQ-DATA-006: Normalización (MUST)
- **3NF:** Tercera forma normal
- **Índices:** En campos frecuentemente consultados
- **Redundancia:** Minimal

#### REQ-DATA-007: Referencial (MUST)
- **FK clientes:** No puede eliminarse si tiene tickets
- **FK tickets:** Interacciones solo si ticket existe
- **Cascada:** Configurar según política

---

## 7️⃣ Requisitos de Seguridad

### 7.1 Autenticación y Autorización

#### REQ-SEC-001: Acceso Público a Tickets (MUST)
- **Clientes:** Sin autenticación
- **Método:** Solo código de ticket (público)
- **Seguridad:** Códigos únicos, difíciles de adivinar
- **Nota:** Futura autenticación recomendada (OAuth2)

#### REQ-SEC-002: Acceso Admin (SHOULD)
- **Clientes Admin:** Requiere autenticación (Fase 2)
- **Método:** Username/password o OAuth2
- **Sesión:** JWT o session cookie
- **Renovación:** Expirar después de inactividad

---

### 7.2 Validación y Sanitización

#### REQ-SEC-003: Validar Todos los Inputs (MUST)
- **Email:** Formato RFC 5322
- **Teléfono:** Formato básico (no debe contener SQL)
- **Texto Libre:** Remover HTML/JavaScript
- **Números:** Rango válido

#### REQ-SEC-004: Prevenir SQL Injection (MUST)
- **Método:** Parameterized queries (SQLAlchemy)
- **No concat:** Nunca concatenar SQL strings
- **Test:** Intentar inyectar SQL, debe fallar

#### REQ-SEC-005: Prevenir XSS (MUST)
- **Escapar:** Todos los datos del usuario
- **Contexto:** HTML, JavaScript, URL según contexto
- **Frontend:** Usar librerías seguras (React escapa por defecto)

---

### 7.3 Encriptación

#### REQ-SEC-006: HTTPS en Producción (MUST)
- **Certificado:** SSL/TLS válido
- **Redirección:** HTTP → HTTPS automático
- **Cipher:** Uso de suites seguras
- **Renovación:** Automática (Let's Encrypt recomendado)

#### REQ-SEC-007: Datos Sensibles (SHOULD)
- **Email:** Encriptar en reposo (Fase 2)
- **Teléfono:** Enmascarar en logs
- **API Keys:** Nunca en repositorio, usar .env

---

### 7.4 Auditoría

#### REQ-SEC-008: Logging de Acciones (MUST)
- **Qué:** Cada creación, lectura, modificación, eliminación
- **Cuándo:** Timestamp exacto
- **Quién:** User (cliente/admin/sistema)
- **Dónde:** Archivo o base de datos de logs
- **Retención:** Mínimo 90 días

#### REQ-SEC-009: Logs de Seguridad (MUST)
- **Intentos Fallidos:** Login (Fase 2)
- **Cambios de Estado:** Quién escaló/cerró ticket
- **Acceso Admin:** Quién accedió a qué
- **Alertas:** Patrones sospechosos (futuro)

#### REQ-SEC-010: No Registrar Datos Sensibles (MUST)
- **Passwords:** Nunca en logs
- **API Keys:** Máscara primeros/últimos caracteres
- **Tokens:** Solo primeros 10 caracteres
- **Tarjetas:** Nunca, ni siquiera parcial

---

## 8️⃣ Requisitos de Confiabilidad

#### REQ-CONF-001: Validación de Datos Antes de Guardar (MUST)
- **Reglas:** Definidas en schemas Pydantic
- **Casteo:** Seguro, con defaults
- **Errores:** Mensajes claros

#### REQ-CONF-002: Transacciones (MUST)
- **ACID:** Atomicidad, Consistencia, Aislamiento, Durabilidad
- **Rollback:** Automático si error
- **Locks:** Evitar race conditions

#### REQ-CONF-003: Monitoreo (SHOULD)
- **Uptime Monitors:** Pingdom, StatusPage
- **Error Tracking:** Sentry o Rollbar
- **Performance:** New Relic o DataDog (Fase 2)
- **Alertas:** Notificar a oncall engineer

---

## 9️⃣ Requisitos de Rendimiento

*(Amplificación de sección 4.1)*

#### REQ-PERF-001: Índices de BD (MUST)
- **tickets.codigo:** Búsqueda rápida por código
- **tickets.cliente_id:** Listar por cliente
- **tickets.estado:** Filtrar por estado
- **interacciones.ticket_id:** Conversación completa

#### REQ-PERF-002: Caché de Reportes (SHOULD)
- **Insights:** Cacheado por mes (30 días)
- **KPIs:** Recalcular si nuevo ticket en mes
- **Invalidación:** Automática al mes cambiar

#### REQ-PERF-003: Query Optimization (MUST)
- **Lazy Loading:** Interacciones solo si se solicitan
- **Paginación:** Siempre límite de resultados
- **Agregaciones:** En BD, no en app

---

## 🔟 Atributos de Calidad

#### REQ-CALIDAD-001: Cobertura de Tests (MUST)
- **Unidad:** ≥ 80% de funciones críticas
- **Integración:** ≥ 60% de endpoints
- **Smoke Test:** 48 checks end-to-end pasan

#### REQ-CALIDAD-002: Code Review (MUST)
- **Antes de Merge:** Mínimo 1 aprobación
- **Estilo:** Usar linter (ESLint, Pylint)
- **Duplicación:** Mantener < 5%

#### REQ-CALIDAD-003: Definición de Hecho (MUST)
- Código compilado sin warnings
- Pruebas unitarias pasan (>80%)
- Code review aprobado
- Documentación actualizada
- Smoke test pasa

---

## 1️⃣1️⃣ Restricciones de Implementación

#### REQ-IMP-001: Lenguajes Permitidos (MUST)
- **Backend:** Python 3.12+
- **Frontend:** JavaScript/TypeScript (React)
- **BD:** SQL (SQLite/PostgreSQL)

#### REQ-IMP-002: Librerías Aprobadas (MUST)
- **Backend:** FastAPI, SQLAlchemy, Pydantic
- **Frontend:** React, React Router, Tailwind, Recharts
- **IA:** OpenAI SDK, Google Generative AI, Ollama SDK

#### REQ-IMP-003: Arquitectura (MUST)
- **Frontend:** SPA (Single Page Application)
- **Backend:** RESTful API stateless
- **BD:** Relacional (SQL)
- **Pattern:** Separación clara de capas

---

## 1️⃣2️⃣ Matriz de Trazabilidad

| ID | Requisito | Tipo | Prioridad | Caso de Uso | Componente | Estado |
|----|-----------|----- |-----------|------------|-----------|--------|
| REQ-FN-001 | Crear solicitud | Funcional | MUST | CU-001 | ConsultaPage | ✅ |
| REQ-FN-005 | Procesar IA | Funcional | MUST | CU-004 | chatbot_service | ✅ |
| REQ-NF-001 | Latencia API | No-Funcional | MUST | Todos | API | ⚠️ |
| REQ-SEC-003 | Validar inputs | Seguridad | MUST | Todos | Backend | ✅ |
| REQ-PERF-001 | Índices BD | Performance | MUST | Todos | DB | ✅ |

---

## 📝 Historial de Cambios

| Versión | Fecha | Cambios | Autor |
|---------|-------|---------|-------|
| 1.0 | 31-ago-2026 | Documento inicial | Ingeniería |
| — | — | — | — |

---

**Documento:** Especificación de Requerimientos de Software  
**Versión:** 1.0  
**Fecha:** Agosto 31, 2026  
**Estado:** ✅ Aprobado para Desarrollo  

**Próxima Revisión:** Después de iteración 2 (2 semanas)
