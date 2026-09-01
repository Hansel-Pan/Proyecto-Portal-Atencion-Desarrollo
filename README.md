# Portal Empresarial de Atención al Cliente con IA

Sistema de atención 24/7: los clientes crean solicitudes (consultas, peticiones, quejas) que un chatbot con IA intenta resolver automáticamente; si no puede, el ticket se escala para revisión manual. Incluye panel de administración con métricas mensuales, gráficos, resumen ejecutivo generado por IA y exportación a PDF/Excel.

## Stack

- **Frontend**: React 19 + Vite + Tailwind CSS 4 + Recharts + React Router
- **Backend**: Python 3.12 + FastAPI + SQLAlchemy 2
- **Base de datos**: SQLite (archivo `backend/dev.db`, se crea sola al arrancar)
- **IA**: Google Gemini (`gemini-3.6-flash`, capa gratuita) con proveedor `mock` sin API key para desarrollo

## Estructura

```
proyectoIA/
├── backend/
│   ├── smoke_test.py              # prueba de humo end-to-end (48 checks)
│   └── app/
│       ├── core/config.py         # configuración (.env)
│       ├── db/                    # engine, sesión, base declarativa
│       ├── models/                # SQLAlchemy: clientes, tickets, interacciones, insights
│       ├── schemas/               # Pydantic
│       ├── ai/                    # proveedores LLM: gemini/openai/ollama/mock
│       ├── services/              # chatbot, tickets, reportes, insights, exportes
│       └── routers/               # /tickets (público) y /admin (reportes)
└── src/                           # frontend React
    ├── api/client.js
    ├── components/
    └── pages/                     # solicitud, consulta, chat, dashboard, tickets, reportes
```

## Puesta en marcha

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt   # Linux/Mac: .venv/bin/pip
copy .env.example .env                           # Linux/Mac: cp
```

No hay que crear tablas a mano: al iniciar el servidor se generan automáticamente en SQLite.

```bash
.venv\Scripts\uvicorn app.main:app --reload      # docs: http://localhost:8000/docs
```

### Frontend

```bash
pnpm install
pnpm dev        # http://localhost:5173
```

## Configurar Gemini (capa gratuita)

1. Entra en **https://aistudio.google.com/apikey** con una cuenta de Google.
2. Pulsa *Create API key* → copia la clave (empieza con `AIza...`). No requiere tarjeta.
3. Pega la clave en `backend/.env`:

```env
GEMINI_API_KEY=AIza...tu_clave
AI_PROVIDER=gemini
```

4. Reinicia el backend.

Notas de la capa gratuita (verificado ago-2026):

- Modelo por defecto: `gemini-3.6-flash` (`gemini-2.5-flash` ya no se ofrece a usuarios nuevos). Alternativas con más cuota diaria: `gemini-flash-lite-latest` o `gemini-3.1-flash-lite`.
- Si no hay clave o está vacía, el sistema **no falla**: cae automáticamente al proveedor `mock` (reglas locales) y registra un warning.
- Cada interacción guarda modelo y tokens consumidos en la tabla `interacciones`.

## Probar la IA sin API key

El proveedor `mock` resuelve por palabras clave (`horario`, `contraseña`, `factura`,
`garantía`) y escala todo lo demás. Útil para demostrar el flujo completo sin gastar cuota.

## Prueba de humo

```bash
cd backend && .venv\Scripts\python smoke_test.py
```

Cubre creación de tickets (resueltos y escalados), chat multi-turno, filtros,
reporte mensual, insights con caché, recálculo, mes vacío e inválido, y ambos exportes.
Usa su propia BD temporal en memoria temporal, no toca `dev.db`.

## Casos de prueba mínimos del sistema (Paso 7)

| # | Caso | Resultado esperado | Estado |
|---|------|--------------------|--------|
| 1 | Crear ticket con palabra clave resoluble ("horario") | 201, estado `resuelto_ia`, `resuelto_por_ia=true`, tiempo de atención calculado, 2 interacciones | Cubierto |
| 2 | Crear queja no resoluble | 201, estado `escalado`, prioridad `alta`, respuesta de escalamiento | Cubierto |
| 3 | Consultar ticket por código público y por ID numérico | 200 con conversación completa | Cubierto |
| 4 | Consultar código inexistente | 404 controlado | Cubierto |
| 5 | Mensaje adicional a un ticket escalado | Conversación crece; el ticket permanece `escalado` (la IA no reabre casos humanos) | Cubierto |
| 6 | Listado admin con filtros tipo+estado y paginación | Solo coincidencias, `total` correcto | Cubierto |
| 7 | Reporte mensual con datos | Totales, distribuciones, tasa IA, pendientes correctos | Cubierto |
| 8 | Reporte de mes vacío | 200 con `total_tickets=0`, tasa 0, sin errores de división | Cubierto |
| 9 | Formato de mes inválido | 422 con mensaje claro | Cubierto |
| 10 | Insights primera generación | Resumen + hallazgos + recomendaciones persistidos en caché | Cubierto |
| 11 | Insights segunda llamada | Servido desde caché (`generado_en` intacto, sin gasto de tokens) | Cubierto |
| 12 | `recalcular=true` | Regenera y sobrescribe el informe | Cubierto |
| 13 | Insights de mes vacío | Mensaje determinista sin llamar a la IA | Cubierto |
| 14 | Fallo del proveedor de IA (chatbot) | Ticket escalado con mensaje técnico; nunca se pierde la solicitud | Cubierto |
| 15 | Confianza IA bajo el umbral (<0.7) | Escala aunque la IA diga poder resolver | Cubierto |
| 16 | Respuesta IA malformada / JSON inválido | Parseo tolerante o escalamiento seguro | Cubierto |
| 17 | Exportar Excel | xlsx válido (firma PK) con hojas Resumen/Tickets/Insights | Cubierto |
| 18 | Exportar PDF | PDF válido (firma %PDF-) con métricas e insights | Cubierto |
| 19 | Exportar con mes inválido | 422 | Cubierto |

**Casos sugeridos para siguientes iteraciones** (requieren funcionalidad nueva):

- Agente resuelve manualmente un ticket escalado → endpoint `PATCH /admin/tickets/{id}` (pendiente de implementar).
- Calificación de satisfacción del cliente (1–5) tras resolución → campo ya existe en BD.
- Autenticación JWT para `/admin/*` (fuera de alcance actual): validar que sin token sean 401.
- Concurrencia: dos solicitudes simultáneas del mismo email nuevo no deben duplicar cliente.
- Carga: reporte con miles de tickets (paginación y tiempos de exporte).

## Publicar en internet (GitHub + Render, gratis)

El proyecto se despliega **todo en uno** (frontend + backend) como servicio Docker
gratuito en [Render](https://render.com), conectado a tu repositorio de GitHub:

1. **Sube el proyecto a GitHub**:
   - Crea una cuenta en https://github.com y un repositorio nuevo (ej. `portal-atencion`, público)
   - Desde la carpeta del proyecto:
     ```bash
     git init
     git add .
     git commit -m "portal de atencion con IA"
     git branch -M main
     git remote add origin https://github.com/TU_USUARIO/portal-atencion.git
     git push -u origin main
     ```
   (No se suben `node_modules`, `backend/.venv`, `dev.db` ni `.env`: están en `.gitignore`)

2. **Despliega en Render** (cuenta gratis, sin tarjeta):
   - Entra a https://render.com con "Sign up with GitHub"
   - *New + → Web Service* → autoriza y selecciona tu repositorio
   - Runtime: **Docker** (detecta el Dockerfile automáticamente)
   - Instance type: **Free**
   - Antes de crear: *Advanced → Add environment variable*
     - Name: `GEMINI_API_KEY` → Value: tu clave de AI Studio

3. Espera el build (~5 min). Tu portal quedará en una URL tipo:
   `https://portal-atencion-xxxx.onrender.com`

Notas del plan gratuito de Render:
- El servicio se **duerme tras 15 minutos** sin visitas; la siguiente visita tarda
  30–60 segundos en despertar (Render muestra una pantalla de carga).
- La base SQLite vive dentro del contenedor: los tickets guardados **se pierden**
  cuando el servicio se duerme o redespliega. Para demo/portafolio está bien;
  para datos reales habría que migrar a PostgreSQL (fuera de alcance por ahora).
- Cada `git push` a GitHub redespliega automáticamente.

Para desarrollo local nada cambia: sigue funcionando con los dos servidores.

## Fuera de alcance (por ahora)

Autenticación JWT/OAuth2 y contenedores Docker/Docker Compose, según lo acordado.
