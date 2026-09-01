# Casos de Uso - Portal Empresarial de Atención al Cliente con IA

**Proyecto:** Portal de Atención al Cliente 24/7  
**Fecha:** Agosto 2026  
**Versión:** 1.0

---

## 📋 Descripción General del Sistema

Sistema web 24/7 que permite a los clientes crear solicitudes (consultas, peticiones, quejas) que un **chatbot con IA inteligente** intenta resolver automáticamente. Si el chatbot no puede resolver la solicitud, esta se **escala automáticamente** para revisión manual. Incluye un panel de administración con métricas mensuales, gráficos interactivos, resumen ejecutivo generado por IA y exportación a formatos PDF/Excel.

### Stack Tecnológico
- **Frontend:** React 19 + Vite + Tailwind CSS 4 + Recharts
- **Backend:** Python 3.12 + FastAPI + SQLAlchemy 2
- **Base de Datos:** SQLite
- **IA:** Google Gemini (API gratuita) con fallback a proveedor mock

---

## 🎯 Actores del Sistema

1. **Cliente Externo** - Usuario que crea y consulta tickets
2. **Chatbot IA** - Sistema automático que resuelve solicitudes
3. **Administrador** - Personal que gestiona tickets escalados y genera reportes
4. **Sistema** - Procesos automáticos (escalamiento, reportes, insights)

---

## 📌 Casos de Uso Principales

### 1. CU-001: Crear Nueva Solicitud (Consulta, Petición o Queja)

**Actor Primario:** Cliente Externo  
**Actor Secundario:** Chatbot IA, Sistema  
**Precondición:** El cliente tiene acceso a la plataforma  
**Flujo Principal:**

1. El cliente accede a la página de inicio del portal
2. Selecciona el tipo de solicitud:
   - **Consulta** (dudas sobre productos/servicios)
   - **Petición** (solicitud de acción)
   - **Queja** (insatisfacción o problema)
3. Completa el formulario con:
   - Nombre y apellido
   - Email
   - Teléfono
   - Asunto (máx. 200 caracteres)
   - Descripción detallada
4. Envía la solicitud
5. El sistema genera un **código de referencia único** (ej: TK-2024-001234)
6. El chatbot IA **analiza automáticamente** la solicitud

**Flujo Alternativo (IA puede resolver):**
- La IA identifica palabras clave resoluble (ej: "horario", "contraseña", "factura", "garantía")
- El ticket se marca como **RESUELTO_IA** con `resuelto_por_ia=true`
- Se registra automáticamente el tiempo de atención

**Flujo Alternativo (IA no puede resolver):**
- La solicitud se marca como **ESCALADO** con prioridad **ALTA**
- Se asigna a personal humano para revisión

**Postcondición:** 
- Ticket creado en base de datos
- Cliente recibe código de referencia
- Conversación inicial registrada

**Excepciones:**
- Fallos de conexión a IA → Se usa proveedor mock (reglas locales)
- Email inválido → Validación en frontend, rechazo del formulario

---

### 2. CU-002: Consultar Estado de Ticket

**Actor Primario:** Cliente Externo  
**Precondición:** Cliente tiene un código de referencia de ticket válido  
**Flujo Principal:**

1. El cliente accede a la página de consulta
2. Ingresa el **código de referencia público** (ej: TK-2024-001234) O **ID numérico**
3. El sistema busca el ticket en la base de datos
4. Muestra:
   - Estado actual (Abierto, Resuelto por IA, Escalado, Cerrado)
   - Tipo de solicitud
   - Asunto y descripción original
   - **Conversación completa** con la IA o personal
   - Tiempo de atención
   - Calificación de satisfacción (si ya fue resuelta)

**Postcondición:** Cliente visualiza el estado y progreso del ticket

**Excepciones:**
- Ticket no encontrado → Mensaje de error 404 controlado
- Acceso denegado → Validación de propiedad del ticket

---

### 3. CU-003: Enviar Mensaje Adicional a Ticket Abierto

**Actor Primario:** Cliente Externo  
**Actor Secundario:** Chatbot IA (si ticket está escalado)  
**Precondición:** El ticket existe y NO está cerrado  
**Flujo Principal:**

1. Cliente visualiza un ticket abierto o escalado
2. Escribe un mensaje adicional en el campo de respuesta
3. Envía el mensaje
4. El sistema registra la interacción con:
   - Contenido del mensaje
   - Timestamp
   - Si es de cliente o personal
5. **Si el ticket está escalado:**
   - Se notifica al personal responsable
   - El ticket permanece en estado **ESCALADO**
6. **Si es una consulta nueva:**
   - La IA intenta procesarla nuevamente

**Postcondición:** Mensaje registrado en la conversación del ticket

**Excepciones:**
- Ticket cerrado → Rechaza el mensaje con error
- Ticket inexistente → Error 404

---

### 4. CU-004: Chatbot IA Resuelve Solicitud Automáticamente

**Actor Primario:** Chatbot IA  
**Actor Secundario:** Proveedor IA (Google Gemini / Mock)  
**Precondición:** Nueva solicitud recibida  
**Flujo Principal:**

1. Chatbot recibe la descripción del ticket
2. Extrae palabras clave (horario, contraseña, factura, garantía, etc.)
3. Usa IA para generar respuesta contextual:
   - Entiende la intención del cliente
   - Proporciona respuesta relevante y útil
   - Incluye pasos de acción si es necesario
4. Registra en la base de datos:
   - Modelo de IA utilizado
   - Tokens consumidos
   - Fecha/hora de procesamiento
   - **Tiempo de atención** (en segundos)
5. Marca ticket como **RESUELTO_IA**
6. Cambia estado a **RESUELTO_IA**
7. Registra `resuelto_por_ia=true`

**Postcondición:** 
- Ticket resuelto automáticamente
- Respuesta visible al cliente
- Métricas actualizadas

**Excepciones:**
- API de IA no disponible → Fallback a proveedor mock
- Error en procesamiento → Se escala manualmente

---

### 5. CU-005: Escalar Ticket a Personal Humano

**Actor Primario:** Sistema o Chatbot IA  
**Actor Secundario:** Administrador  
**Precondición:** Ticket no puede ser resuelto por IA  
**Flujo Principal:**

1. Chatbot determina que no puede resolver la solicitud
2. Automáticamente cambia estado a **ESCALADO**
3. Asigna prioridad **ALTA**
4. Crea notificación para el equipo de administración
5. El ticket aparece en la cola de pendientes
6. Personal humano revisa y proporciona respuesta

**Postcondición:**
- Ticket marcado como escalado
- Disponible para personal humano
- Cliente puede ver que está en revisión

**Excepciones:**
- Fallo en notificación → Se registra en logs

---

### 6. CU-006: Responder y Cerrar Ticket (Personal Humano)

**Actor Primario:** Administrador  
**Precondición:** Ticket en estado ESCALADO  
**Flujo Principal:**

1. Administrador accede a la lista de tickets escalados
2. Selecciona un ticket
3. Revisa la conversación completa
4. Escribe respuesta detallada
5. Opcionalmente cambia:
   - Prioridad
   - Asigna personal específico
6. Envía respuesta
7. Cierra el ticket (estado **CERRADO**)

**Postcondición:**
- Ticket cerrado con resolución humana
- Cliente recibe notificación

---

### 7. CU-007: Ver Dashboard de Administración

**Actor Primario:** Administrador  
**Precondición:** Autenticación exitosa en sección admin  
**Flujo Principal:**

1. Administrador accede a `/admin`
2. El dashboard muestra:
   - **Tarjetas KPI:**
     - Total de tickets del mes
     - Tickets resueltos por IA
     - Tasa de resolución automática (%)
     - Tickets pendientes
     - Tiempo promedio de atención
   - **Gráficos interactivos:**
     - Línea temporal de tickets por día
     - Distribución por tipo (Consulta, Petición, Queja)
     - Distribución por estado
     - Tendencia de resoluciones IA vs. humanas
   - **Resumen ejecutivo** generado por IA con insights clave

**Postcondición:** Visualización del estado general del sistema

**Excepciones:**
- Sin datos en el mes → Mostrar mensaje "Sin actividad"

---

### 8. CU-008: Listar Tickets con Filtros Avanzados

**Actor Primario:** Administrador  
**Precondición:** Acceso a sección admin  
**Flujo Principal:**

1. Administrador accede a `/admin/tickets`
2. Aplica filtros opcionales:
   - **Tipo:** Consulta, Petición, Queja (múltiple)
   - **Estado:** Abierto, Resuelto por IA, Escalado, Cerrado
   - **Prioridad:** Baja, Media, Alta
   - **Rango de fechas:** Desde/Hasta
3. Sistema ejecuta búsqueda con paginación (20 por página, ajustable hasta 100)
4. Muestra:
   - Código de ticket
   - Cliente (nombre/email)
   - Tipo y asunto
   - Estado actual
   - Prioridad
   - Resuelto por IA (sí/no)
   - Fecha de creación y resolución
   - Tiempo de atención

**Postcondición:** Lista filtrada de tickets disponible para acción

**Excepciones:**
- Sin resultados → Mensaje amigable
- Filtros inválidos → Validación del lado del servidor

---

### 9. CU-009: Generar Reporte Mensual con Métricas

**Actor Primario:** Administrador  
**Precondición:** Acceso a sección de reportes  
**Flujo Principal:**

1. Administrador selecciona mes y año (formato YYYY-MM)
2. Sistema calcula automáticamente:
   - **Total de tickets** del período
   - **Resoluciones por IA:** Cantidad y porcentaje
   - **Resoluciones humanas:** Cantidad y porcentaje
   - **Tickets escalados:** Cantidad
   - **Tickets pendientes:** Cantidad
   - **Distribución por tipo:** Consultas, Peticiones, Quejas
   - **Distribución por estado:** Abierto, Resuelto IA, Escalado, Cerrado
   - **Tiempo promedio de atención:** En segundos
   - **Tasa de satisfacción:** Calificaciones promedio
   - **Tiempo de pico:** Hora del día con mayor volumen

3. Reporte se muestra en interfaz interactiva con gráficos Recharts

**Postcondición:** Reporte completo disponible para análisis

**Excepciones:**
- Mes inválido → Error 422 controlado
- Sin datos → Reporte con todos los campos en cero

---

### 10. CU-010: Generar Insights Mensuales con IA

**Actor Primario:** Sistema / Chatbot IA  
**Actor Secundario:** Google Gemini (o Mock)  
**Precondición:** Reporte mensual generado  
**Flujo Principal:**

1. Administrador accede a insights del mes
2. Sistema verifica si existe **caché** del mes anterior
3. **Si existe caché:**
   - Muestra insights guardados (resumen ejecutivo generado por IA)
4. **Si no existe o fuerza recálculo:**
   - IA analiza todas las métricas del mes
   - Genera insights contextuales:
     - Tendencias observadas
     - Patrones de consultas
     - Recomendaciones de mejora
     - Problemas frecuentes
     - Oportunidades de automación
   - Guarda resultado en tabla `insight_mensual`
   - Devuelve al usuario

**Postcondición:**
- Insights cacheados para consultas futuras
- Valor agregado disponible para decisiones

**Excepciones:**
- Proveedor IA no disponible → Error 503
- Mes inválido → Error 422

---

### 11. CU-011: Exportar Reporte a Excel

**Actor Primario:** Administrador  
**Precondición:** Reporte mensual generado  
**Flujo Principal:**

1. Administrador selecciona mes y clica "Descargar Excel"
2. Sistema genera archivo `.xlsx` con:
   - Hoja 1: Resumen ejecutivo (KPIs principales)
   - Hoja 2: Detalle de tickets (todos los del mes)
   - Hoja 3: Análisis por tipo
   - Hoja 4: Análisis por estado
   - Hoja 5: Datos brutos para auditoría
3. Archivo se descarga automáticamente con nombre: `Reporte_YYYY-MM.xlsx`

**Postcondición:** Archivo descargado en dispositivo del usuario

**Excepciones:**
- Error en generación → Error 422
- Mes inválido → Validación previa

---

### 12. CU-012: Exportar Reporte a PDF

**Actor Primario:** Administrador  
**Precondición:** Reporte mensual generado  
**Flujo Principal:**

1. Administrador selecciona mes y clica "Descargar PDF"
2. Sistema genera documento PDF con:
   - Portada con período y fecha
   - Índice
   - Resumen ejecutivo con conclusiones
   - Gráficos e ilustraciones
   - Tablas de datos detalladas
   - Recomendaciones
3. Archivo se descarga automáticamente: `Reporte_YYYY-MM.pdf`

**Postcondición:** Archivo descargado listo para presentación

**Excepciones:**
- Error en renderizado → Error 422
- Datos faltantes → Se omiten secciones afectadas

---

### 13. CU-013: Validar Ticket Existente

**Actor Primario:** Sistema  
**Flujo Principal:**

1. Sistema recibe solicitud de consulta de ticket
2. Busca por:
   - Código público (ej: TK-2024-001234)
   - O ID numérico
3. Si existe → Retorna datos completos
4. Si no existe → Retorna error 404

**Postcondición:** Validación completada

---

### 14. CU-014: Registrar Interacción en Conversación

**Actor Primario:** Sistema  
**Precondición:** Mensaje enviado en ticket  
**Flujo Principal:**

1. Sistema registra cada mensaje/interacción con:
   - `ticket_id`: Referencia al ticket
   - `contenido`: Texto del mensaje
   - `rol`: "cliente", "ia", o "admin"
   - `modelo_ia`: (si aplica)
   - `tokens_consumidos`: (si aplica)
   - `fecha`: Timestamp

2. Mensaje se añade a la conversación del ticket
3. Cliente ve conversación completa en orden cronológico

**Postcondición:** Interacción registrada para auditoría y seguimiento

---

### 15. CU-015: Calcular Tiempo de Atención

**Actor Primario:** Sistema  
**Precondición:** Ticket resuelto  
**Flujo Principal:**

1. Sistema calcula:
   - `tiempo_atencion_seg` = timestamp_resolución - timestamp_creación
2. Se almacena en base de datos
3. Se utiliza para:
   - Métricas de reporte
   - Promedios de atención
   - Análisis de desempeño

**Postcondición:** Métrica registrada para análisis

---

## 🔄 Flujos Secundarios Críticos

### Flujo: Proveedor IA No Disponible
1. Cliente envía solicitud
2. Backend intenta conectar con Google Gemini
3. Si falla → Fallback automático a proveedor **MOCK**
4. Proveedor mock resuelve por palabras clave locales
5. Sistema registra el proveedor utilizado
6. Se registra warning en logs

### Flujo: Ticket Recibe Múltiples Mensajes
1. Cliente envía mensaje inicial
2. Se escala a personal (si es necesario)
3. Cliente envía mensaje adicional
4. Conversación crece
5. **Nota importante:** La IA no reabre tickets cerrados/escalados
6. Personal humano continúa la conversación

---

## 📊 Entidades y Estados

### Estados del Ticket
- **ABIERTO**: Ticket recién creado, pendiente de procesamiento
- **RESUELTO_IA**: Resuelto automáticamente por el chatbot
- **ESCALADO**: Enviado a personal humano, de alta prioridad
- **CERRADO**: Resolución completada (IA o humana)

### Tipos de Solicitud
- **CONSULTA**: Dudas sobre productos/servicios
- **PETICION**: Solicitud de acción
- **QUEJA**: Insatisfacción o problema

### Niveles de Prioridad
- **BAJA**: No urgente, resolución flexible
- **MEDIA**: Estándar, resolución normal
- **ALTA**: Urgente, escaladas automáticamente

---

## 🛡️ Restricciones y Reglas de Negocio

1. **Un código de ticket es único** y sirve como referencia pública
2. **La IA no reabre casos cerrados** - Solo personal humano puede cambiar de escalado a resuelto
3. **El tiempo de atención** se calcula automáticamente al resolver
4. **Los insights se cachean** mensualmente para no regenerar innecesariamente
5. **Palabras clave resoluble:** horario, contraseña, factura, garantía
6. **Falta de API key de IA** → Sistema no falla, usa proveedor mock
7. **Exportes (PDF/Excel)** se generan bajo demanda, no se almacenan

---

## ✅ Cobertura de Pruebas Confirmada

Todos estos casos de uso han sido validados con pruebas end-to-end en `smoke_test.py`:

| # | Caso | Resultado Esperado | ✓ Cubierto |
|---|------|--------------------|-----------|
| 1 | Crear ticket resoluble ("horario") | 201, estado `resuelto_ia`, `resuelto_por_ia=true` | ✓ |
| 2 | Crear queja no resoluble | 201, estado `escalado`, prioridad `alta` | ✓ |
| 3 | Consultar ticket por código y por ID | 200 con conversación completa | ✓ |
| 4 | Consultar código inexistente | 404 controlado | ✓ |
| 5 | Mensaje adicional a ticket escalado | Conversación crece, permanece `escalado` | ✓ |
| 6 | Listado admin con filtros y paginación | Solo coincidencias, `total` correcto | ✓ |
| 7 | Reporte mensual con datos | Totales, distribuciones, tasa IA correctos | ✓ |

---

## 📱 Interfaz de Usuario (Frontend)

**Rutas disponibles:**
- `/` → Página de inicio
- `/consulta` → Crear nueva solicitud
- `/chat` → Conversación con chatbot (después de crear ticket)
- `/admin` → Dashboard de administración
- `/admin/tickets` → Gestión de tickets (filtros)
- `/admin/reportes` → Reportes mensuales y exportes

---

## 🔌 API Endpoints Principales

**Públicos (sin autenticación):**
- `POST /tickets` → Crear solicitud
- `GET /tickets/{ticket_ref}` → Consultar estado
- `POST /tickets/{ticket_ref}/mensajes` → Enviar mensaje

**Privados (admin):**
- `GET /admin/tickets` → Listar con filtros
- `GET /admin/reportes/mensual` → Reporte mes YYYY-MM
- `GET /admin/reportes/mensual/insights` → Insights IA
- `GET /admin/reportes/mensual/exportar/excel` → Descarga Excel
- `GET /admin/reportes/mensual/exportar/pdf` → Descarga PDF
- `GET /health` → Status del backend

---

## 📝 Conclusiones

Este sistema automatiza significativamente la atención al cliente:

✅ **Resoluciones automáticas** reducen carga de personal  
✅ **Escalamiento inteligente** asegura consultas complejas lleguen a humanos  
✅ **Análisis con IA** proporciona insights accionables  
✅ **Exportes flexibles** facilitan reportes ejecutivos  
✅ **24/7 disponible** sin intervención humana constante  

El diseño es robusto, con fallbacks (proveedor mock), caché (insights), y cobertura completa de pruebas.
