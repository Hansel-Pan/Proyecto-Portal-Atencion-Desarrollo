# Visión y Alcance del Proyecto
## Portal Empresarial de Atención al Cliente con IA

**Documento:** Visión y Alcance  
**Versión:** 1.0  
**Fecha:** Agosto 31, 2026  

---

## 📌 1. Declaración de Visión

### Visión Estratégica

**"Transformar la atención al cliente mediante un portal web 24/7 que automatiza la resolución de consultas con inteligencia artificial, reduce tiempos de respuesta y proporciona insights accionables para mejora continua."**

### Enunciado de Valor

El Portal Empresarial de Atención al Cliente con IA permite a las empresas:

✅ **Atender a los clientes 24/7** sin necesidad de personal humano constante  
✅ **Automatizar resoluciones** del 70%+ de consultas mediante IA inteligente  
✅ **Escalar casos complejos** de forma automática e inteligente  
✅ **Visualizar métricas** en tiempo real para tomar decisiones informadas  
✅ **Generar insights** automáticos con recomendaciones de mejora  
✅ **Exportar reportes** profesionales en PDF y Excel  

---

## 🎯 2. Objetivos del Proyecto

### Objetivos Principales

1. **Automatización de Atención**
   - Objetivo: Resolver el 70%+ de consultas automáticamente con IA
   - Métrica: Tasa de resolución IA ≥ 70%
   - Plazo: Mes 1 en producción

2. **Disponibilidad 24/7**
   - Objetivo: Sistema disponible sin interrupciones
   - Métrica: Uptime ≥ 99.9%
   - Plazo: Desde lanzamiento

3. **Reducción de Tiempo de Respuesta**
   - Objetivo: Atender solicitudes en < 120 segundos promedio
   - Métrica: Tiempo promedio de atención ≤ 120 seg
   - Plazo: Optimización continua

4. **Satisfacción del Cliente**
   - Objetivo: Calificación promedio ≥ 4/5 estrellas
   - Métrica: Promedio de ratings de satisfacción
   - Plazo: Mes 2-3

5. **Inteligencia de Negocio**
   - Objetivo: Generar insights actionables para mejora
   - Métrica: Recomendaciones implementadas / Recomendaciones totales
   - Plazo: Mes 2 en adelante

6. **Facilidad de Uso**
   - Objetivo: Interfaz intuitiva para clientes y administradores
   - Métrica: Tasa de adopción, feedback positivo
   - Plazo: Desde lanzamiento

---

## 🔍 3. Alcance del Proyecto

### Funcionalidades Incluidas (IN SCOPE)

#### 3.1 Portal para Clientes
- ✅ Crear solicitudes (Consultas, Peticiones, Quejas)
- ✅ Consultar estado de solicitudes por código o ID
- ✅ Enviar mensajes adicionales en conversación abierta
- ✅ Visualizar conversación completa con chatbot/personal
- ✅ Validación de datos en formulario (email, teléfono, etc.)

#### 3.2 Chatbot IA
- ✅ Procesamiento automático de solicitudes
- ✅ Resolución de consultas frecuentes mediante palabras clave
- ✅ Generación de respuestas contextuales con IA
- ✅ Escalamiento automático de casos complejos
- ✅ Soporte para múltiples proveedores IA (Gemini, OpenAI, Ollama)
- ✅ Fallback a proveedor mock si IA no disponible
- ✅ Registro de modelo IA y tokens consumidos

#### 3.3 Panel de Administración
- ✅ Dashboard con KPIs y gráficos interactivos
- ✅ Visualización de tickets escalados pendientes
- ✅ Listado de tickets con filtros avanzados (tipo, estado, prioridad, fechas)
- ✅ Paginación de resultados (1-100 items)
- ✅ Respuesta a tickets escalados
- ✅ Cierre de tickets

#### 3.4 Reportes y Exportes
- ✅ Generación de reporte mensual con métricas
- ✅ Cálculo automático de:
  - Total de tickets por tipo/estado
  - Tasa de resolución IA vs. humana
  - Tiempo promedio de atención
  - Distribuciones gráficas
  - Tendencias mensuales
- ✅ Generación de insights automáticos con IA
- ✅ Caché de insights por mes
- ✅ Exportación a Excel (.xlsx con 5 hojas)
- ✅ Exportación a PDF (formato profesional)

#### 3.5 Base de Datos
- ✅ Almacenamiento de clientes
- ✅ Almacenamiento de tickets con estados
- ✅ Registro de conversaciones (interacciones)
- ✅ Auditoría de acciones (quién, qué, cuándo)
- ✅ Cálculo de métricas en tiempo real

#### 3.6 Infraestructura
- ✅ API REST bien documentada (Swagger)
- ✅ Frontend responsive (React + Tailwind)
- ✅ Dockerización de backend
- ✅ Gestor de dependencias (pip para Python, pnpm para JS)

---

### Funcionalidades Excluidas (OUT OF SCOPE)

#### ❌ No Incluidas en Fase 1
- ❌ Autenticación OAuth2 con SSO
- ❌ Integración con sistemas CRM externos
- ❌ Soporte de chat en vivo (video/audio)
- ❌ Transferencia de conversación entre agentes
- ❌ SLA automático de resolución
- ❌ Encriptación de datos en tránsito (HTTPS se recomienda en prod)
- ❌ Backup automático de base de datos
- ❌ Notificaciones por email/SMS
- ❌ Chatbot multiidioma (solo español/inglés)
- ❌ Integración de redes sociales

#### 📌 Nota
Estas funcionalidades pueden incluirse en versiones futuras según demanda y recursos.

---

## 📊 4. Stakeholders y Usuarios

### Usuarios Primarios

#### 4.1 Clientes Externos
- **Descripción:** Personas que buscan resolver consultas, peticiones o reportar quejas
- **Necesidades:**
  - Acceso rápido y fácil (sin registro)
  - Respuestas automáticas rápidas
  - Seguimiento de estado en tiempo real
  - Comunicación clara y profesional

#### 4.2 Administradores/Personal de Soporte
- **Descripción:** Empleados que gestionan tickets escalados y generan reportes
- **Necesidades:**
  - Visibilidad de casos escalados
  - Filtros y búsqueda avanzada
  - Respuesta rápida a casos
  - Métricas y reportes detallados

#### 4.3 Ejecutivos/Gestores
- **Descripción:** Líderes que toman decisiones estratégicas
- **Necesidades:**
  - Dashboard con KPIs clave
  - Insights de IA para mejora
  - Exportes profesionales
  - Trazabilidad de métricas

### Stakeholders Secundarios

- **Gerencia de Tecnología:** Mantenimiento, seguridad, escalabilidad
- **Finanzas:** ROI, costos de infraestructura
- **Área de Calidad:** Cumplimiento de estándares
- **Proveedor IA:** Google (Gemini) u otros

---

## 🌍 5. Restricciones del Proyecto

### Restricciones Técnicas

| Restricción | Descripción | Impacto |
|-------------|-------------|--------|
| **Base de Datos** | SQLite en desarrollo, migración a PostgreSQL en producción | Desarrollo local rápido, producción escalable |
| **Proveedor IA** | Google Gemini (capa gratuita) como default, fallback mock | Costo bajo, cuota limitada diaria |
| **Frontend** | React 19 + Vite, sin universal server-side rendering | Performance optimizada, SPA |
| **Backend** | Python 3.12 + FastAPI (no otras versiones) | Performance async, desarrollo rápido |
| **Navegador** | Chrome, Firefox, Safari, Edge (últimas 2 versiones) | Compatibilidad moderna |

### Restricciones de Negocio

| Restricción | Descripción | Impacto |
|-------------|-------------|--------|
| **Autenticación** | Sin autenticación en clientes (acceso público), solo código de ticket | Acceso sin fricción, auditoría recomendada futuro |
| **Escalamiento** | Manual por personal, sin automatización de asignación | Simplicidad inicial, mejora futura |
| **Exportes** | Generados bajo demanda, no almacenados | Seguridad de datos, latencia aceptable |
| **Idioma** | Español primario, textos fijos en backend | Soporte multi-idioma futuro |

### Restricciones de Recursos

| Restricción | Descripción | Impacto |
|-------------|-------------|--------|
| **Equipo** | 1-2 desarrolladores, 1 diseñador, 1 QA | Sprints de 2 semanas, MVP primero |
| **Presupuesto** | Capa gratuita de Gemini, hosting económico | Limitaciones de volumen, optimización necesaria |
| **Tiempo** | MVP en 4 semanas, mejoras posteriores | Priorización clara de features |

---

## 🎨 6. Límites del Sistema

### Límites Funcionales

**Palabras Clave Resolubles (Proveedor Mock):**
- horario (información de horarios)
- contraseña (reset de contraseña)
- factura (estado de factura)
- garantía (información de garantía)

**Límites de Volumen:**
- Máximo 1,000 tickets/día en desarrollo
- Máximo 100 items en listado paginado
- Máximo 50 MB por archivo exportado

**Límites Temporales:**
- Timeout de API: 30 segundos
- Session de usuario: 24 horas
- Cache de insights: 30 días

---

## 🚀 7. Fases de Implementación

### Fase 1: MVP (Producto Mínimo Viable) - Semanas 1-4

**Objetivos:**
- Sistema base completamente funcional
- Autenticación básica (sin OAuth2)
- Chatbot con IA funcionando
- Dashboard con KPIs básicos

**Entregables:**
- Backend API completo
- Frontend con 6 rutas
- Base de datos SQLite
- Documentación completa

**Criterio de Éxito:**
- ✅ Smoke test con 48 checks pasando
- ✅ 70%+ de consultas resueltas por IA
- ✅ Dashboard visualizando métricas
- ✅ Exportes funcionando

### Fase 2: Mejoras y Optimización - Semanas 5-8

**Objectives:**
- Autenticación mejorada (OAuth2)
- Optimización de performance
- Más proveedores IA
- Dashboard avanzado

**Entregables:**
- Seguridad mejorada
- APIs optimizadas
- Documentación de admin
- Capacitación de usuarios

### Fase 3: Producción - Semanas 9+

**Objectives:**
- Deployment en producción
- Monitoreo 24/7
- Soporte al cliente
- Mejora continua

---

## 📈 8. Criterios de Éxito

### Métricas de Corto Plazo (Mes 1)

| Métrica | Meta | Verificación |
|---------|------|-------------|
| Uptime | ≥ 99.9% | Monitoreo automatizado |
| Resolución IA | ≥ 70% | Reporte mensual |
| Tiempo promedio | ≤ 120 seg | Cálculo en DB |
| Disponibilidad API | ≥ 99% | Health check |
| Usuarios activos | ≥ 100 | Analytics |

### Métricas de Mediano Plazo (Mes 3)

| Métrica | Meta | Verificación |
|---------|------|-------------|
| Satisfacción | ≥ 4.0 / 5 | Ratings de usuarios |
| Escalamientos correctos | ≥ 90% | Análisis manual |
| Adopción | ≥ 80% de usuarios | Encuesta |
| Performance | P95 < 500ms | Profiling |

---

## 🛡️ 9. Riesgos y Mitigación

### Riesgos Técnicos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|--------|-----------|
| API Gemini no disponible | MEDIA | ALTO | Proveedor mock fallback automático |
| Pérdida de datos SQLite | BAJA | CRÍTICO | Backup diario recomendado, migrar a PostgreSQL |
| Performance lenta | BAJA | MEDIO | Índices en BD, caching de reportes |
| Seguridad vulnerada | BAJA | CRÍTICO | Validación input, HTTPS en prod, auditoría |

### Riesgos de Negocio

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|--------|-----------|
| Baja adopción de usuarios | MEDIA | ALTO | UX/UI intuitiva, capacitación, marketing interno |
| Expectativas IA sobrevaloradas | MEDIA | MEDIO | Comunicación clara de limitaciones, demos realistas |
| Costos IA aumentan | BAJA | MEDIO | Proveedores alternativos, modelo hybrid human-AI |

---

## 📋 10. Supuestos y Dependencias

### Supuestos Clave

1. ✅ Clientes tienen acceso a internet 24/7
2. ✅ Google Gemini API disponible (capa gratuita)
3. ✅ Servidor hosting disponible 24/7
4. ✅ Base de datos SQLite suficiente para Fase 1
5. ✅ Personal de soporte disponible durante horario laboral
6. ✅ No hay requisitos de cumplimiento normativo especiales (GDPR, HIPAA)

### Dependencias Externas

- 🔗 Google Cloud (Gemini API)
- 🔗 Hosting provider (AWS, Heroku, etc.)
- 🔗 Node.js y Python runtimes disponibles
- 🔗 NPM/PyPI accesibles

---

## 📅 11. Cronograma de Alto Nivel

```
Agosto 2026:
├─ Semana 1-2: Desarrollo backend + BD
├─ Semana 2-3: Desarrollo frontend
├─ Semana 3-4: Testing e integración
└─ Semana 4: MVP listo

Septiembre 2026:
├─ Semana 1-2: Optimización y bugs
├─ Semana 3: UAT (pruebas de usuario)
└─ Semana 4: Preparación producción

Octubre 2026:
├─ Semana 1: Deploy producción
├─ Semana 2-4: Monitoreo y mejoras
└─ Roadmap Fase 2
```

---

## 🎓 12. Definición de Términos Clave

| Término | Definición |
|---------|-----------|
| **Ticket** | Registro de una solicitud de cliente (consulta, petición o queja) |
| **Resolución IA** | Respuesta generada automáticamente por chatbot sin intervención humana |
| **Escalamiento** | Transferencia de ticket a personal humano para revisión |
| **Interacción** | Mensaje individual en la conversación (cliente, IA, o admin) |
| **Insight** | Análisis generado por IA con recomendaciones de mejora |
| **KPI** | Key Performance Indicator (métrica de desempeño clave) |
| **Uptime** | Porcentaje de tiempo que el sistema está disponible y funcional |

---

## ✅ 13. Criterios de Aceptación del Proyecto

El proyecto se considerará exitoso cuando:

1. ✅ **Funcionalidad:** Todos los 15 casos de uso implementados y validados
2. ✅ **Performance:** 99%+ uptime en primera semana de producción
3. ✅ **Calidad:** Smoke test 48/48 checks pasando
4. ✅ **Usabilidad:** 4.0+ estrellas en rating de clientes
5. ✅ **Documentación:** Completa, actualizada, accesible
6. ✅ **Seguridad:** Sin vulnerabilidades críticas identificadas
7. ✅ **Adopción:** 80%+ de usuarios activos en mes 2

---

## 📝 14. Gobernanza y Aprobaciones

### Partes Autorizadas

| Rol | Nombre | Aprobación |
|-----|--------|-----------|
| Product Manager | — | ✅ |
| Gestor Técnico | — | ✅ |
| Stakeholder Ejecutivo | — | ✅ |

### Historial de Cambios

| Versión | Fecha | Cambios | Autor |
|---------|-------|---------|-------|
| 1.0 | 31-ago-2026 | Documento inicial | Análisis |
| — | — | — | — |

---

## 🔗 15. Referencias y Documentos Relacionados

- ✅ [Casos_de_Uso.md](../01%20-%20Análisis/Casos_de_Uso.md) - Descripción detallada de 15 casos
- ✅ [Especificacion_Requerimientos_Software.md](./Especificacion_Requerimientos_Software.md) - Requisitos funcionales y no funcionales
- ✅ [README.md](../../03%20-%20Desarrollo/README.md) - Instrucciones técnicas
- ✅ [Matriz_Trazabilidad.md](../01%20-%20Análisis/Matriz_Trazabilidad.md) - Requisitos vs componentes

---

## 📞 Información del Documento

**Documento:** Vision y Alcance del Proyecto  
**Versión:** 1.0  
**Fecha de Creación:** Agosto 31, 2026  
**Última Actualización:** Agosto 31, 2026  
**Estado:** ✅ Aprobado para Fase 1  
**Próxima Revisión:** Después de MVP (4 semanas)

---

**Aprobado:** ✅  
**Listo para Desarrollo:** ✅
