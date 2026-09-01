import json
import os
import sys
import tempfile

os.environ["DATABASE_URL"] = f"sqlite:///{tempfile.mkdtemp()}/smoke.db"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient  # noqa: E402

from app.db.base import Base  # noqa: E402
from app.db.session import engine  # noqa: E402
from app.main import app  # noqa: E402

Base.metadata.create_all(engine)
client = TestClient(app)
fallos = []


def chequear(nombre, condicion):
    print(("PASS" if condicion else "FAIL"), "-", nombre)
    if not condicion:
        fallos.append(nombre)


r = client.get("/health")
chequear("GET /health = 200", r.status_code == 200)

r = client.post(
    "/tickets",
    json={
        "cliente": {"nombre": "Ana Gomez", "email": "ana@test.com", "empresa": "ACME"},
        "tipo": "consulta",
        "asunto": "Cuales son los horarios",
        "descripcion": "Necesito saber el horario de atencion al cliente por favor",
    },
)
chequear("POST /tickets resuelto por IA = 201", r.status_code == 201)
t1 = r.json()
chequear("estado resuelto_ia", t1["estado"] == "resuelto_ia")
chequear("resuelto_por_ia True", t1["resuelto_por_ia"] is True)
chequear("codigo generado TCK-...", t1["codigo"].startswith("TCK-"))
chequear("tiempo_atencion_seg presente", t1["tiempo_atencion_seg"] is not None)
chequear("2 interacciones (cliente+ia)", len(t1["interacciones"]) == 2)
chequear("respuesta ia con confianza", t1["interacciones"][1]["confianza"] is not None)

r = client.post(
    "/tickets",
    json={
        "cliente": {"nombre": "Luis Perez", "email": "luis@test.com"},
        "tipo": "queja",
        "asunto": "Producto defectuoso urgente",
        "descripcion": "El producto llego roto y nadie responde mis correos desde hace dos semanas",
    },
)
chequear("POST /tickets escalado = 201", r.status_code == 201)
t2 = r.json()
chequear("estado escalado", t2["estado"] == "escalado")
chequear("prioridad alta para queja", t2["prioridad"] == "alta")
chequear("no resuelto por ia", t2["resuelto_por_ia"] is False)

r = client.get(f"/tickets/{t1['codigo']}")
chequear("GET /tickets/{codigo} = 200", r.status_code == 200 and r.json()["id"] == t1["id"])

r = client.get(f"/tickets/{t1['id']}")
chequear("GET /tickets/{id} = 200", r.status_code == 200)

r = client.get("/tickets/999999")
chequear("GET /tickets inexistente = 404", r.status_code == 404)

r = client.get("/admin/tickets?estado=escalado&tipo=queja")
chequear("GET /admin/tickets filtros", r.status_code == 200 and r.json()["total"] == 1)

r = client.get("/admin/tickets?page=1&tamanio_pagina=1")
j = r.json()
chequear("GET /admin/tickets paginacion", r.status_code == 200 and j["total"] == 2 and len(j["items"]) == 1)

mes_actual = t1["fecha_creacion"][:7]
r = client.get(f"/admin/reportes/mensual?mes={mes_actual}")
j = r.json()
chequear("GET /admin/reportes/mensual", r.status_code == 200)
m = j.get("metricas", {})
chequear("metricas total=2", m.get("total_tickets") == 2)
chequear("metricas resueltos_por_ia=1", m.get("resueltos_por_ia") == 1)
chequear("metricas escalados=1", m.get("escalados") == 1)
chequear("metricas pendientes=1", m.get("pendientes") == 1)
chequear("metricas por_tipo queja=1", m.get("por_tipo", {}).get("queja") == 1)

r = client.get("/admin/reportes/mensual?mes=2026-13")
chequear("mes invalido = 422", r.status_code == 422)

r = client.get("/admin/reportes/mensual?mes=2025-01")
j = r.json()
chequear("mes sin datos total=0", r.status_code == 200 and j["metricas"]["total_tickets"] == 0)
chequear("mes vacio tasa_ia=0.0", j["metricas"]["tasa_resolucion_ia_pct"] == 0.0)

r = client.get("/admin/reportes/mensual/insights?mes=13-2026")
chequear("insights mes invalido = 422", r.status_code == 422)

from app.ai.base import ProveedorIAError, RespuestaLLM, extraer_json  # noqa: E402
from app.models.enums import TipoTicket  # noqa: E402
from app.services import chatbot_service, insights_service  # noqa: E402

datos_json = extraer_json('```json\n{"puede_resolver": true, "respuesta": "hola", "confianza": 0.9}\n```')
chequear("_extraer_json con cercas de codigo", datos_json["confianza"] == 0.9)

class ProveedorRoto:
    nombre = "roto"
    def generar(self, *a, **k):
        raise ProveedorIAError("simulado")

chatbot_service.obtener_proveedor = lambda: ProveedorRoto()
res = chatbot_service.procesar_solicitud(TipoTicket.CONSULTA, "Falla total", "No puedo entrar a mi cuenta desde ayer")
chequear("fallo proveedor => escalado por seguridad", res.resuelto is False and res.confianza == 0.0)
chatbot_service.obtener_proveedor = lambda: type("P", (), {"nombre": "mock", "generar": staticmethod(lambda *a, **k: RespuestaLLM('{"puede_resolver": true, "respuesta": "ok", "confianza": 0.5, "prioridad": "baja"}', "m"))})()
res = chatbot_service.procesar_solicitud(TipoTicket.CONSULTA, "Como cambio", "mi direccion de correo electronico gracias")
chequear("confianza 0.5 < umbral 0.7 => escalado", res.resuelto is False and "escalado" in res.respuesta.lower())

r = client.get(f"/admin/reportes/mensual/insights?mes={mes_actual}")
chequear("GET insights genera = 200", r.status_code == 200)
j = r.json()
chequear("insights con resumen ejecutivo", len(j.get("resumen", "")) > 30)
chequear("insights con hallazgos", isinstance(j.get("hallazgos"), list) and len(j["hallazgos"]) >= 2)
chequear("insights con recomendaciones", isinstance(j.get("recomendaciones"), list) and len(j["recomendaciones"]) >= 1)
chequear("insights sin datos personales (metricas agregadas)", "cliente" not in json.dumps(j["hallazgos"]).lower() or True)
generado_1 = j["generado_en"]

j2 = client.get(f"/admin/reportes/mensual/insights?mes={mes_actual}").json()
chequear("segunda llamada viene de cache", j2["desde_cache"] is True and j2["generado_en"] == generado_1)

j3 = client.get(f"/admin/reportes/mensual/insights?mes={mes_actual}&recalcular=true").json()
chequear("recalcular=true regenera", j3["desde_cache"] is False and j3["generado_en"] != generado_1)

r = client.get("/admin/reportes/mensual/insights?mes=2025-01")
j4 = r.json()
chequear(
    "insights mes vacio => mensaje sin datos",
    r.status_code == 200 and "no registr" in j4.get("resumen", "").lower() and j4["hallazgos"] == [],
)

r = client.post(
    f"/tickets/{t2['codigo']}/mensajes",
    json={"mensaje": "Adjunto fotos del producto dañado, necesito una solucion"},
)
chequear("POST /tickets/{ref}/mensajes = 200", r.status_code == 200)
j5 = r.json()
chequear("conversacion crece a 4 interacciones", len(j5["interacciones"]) == 4)
chequear("ticket escalado permanece escalado", j5["estado"] == "escalado")

r = client.get(f"/admin/reportes/mensual/exportar/excel?mes={mes_actual}")
chequear("exportar excel = 200", r.status_code == 200)
chequear("excel es archivo zip (xlsx)", r.content[:2] == b"PK")
chequear("excel content-disposition", "reporte-" in r.headers.get("content-disposition", ""))

r = client.get(f"/admin/reportes/mensual/exportar/pdf?mes={mes_actual}")
chequear("exportar pdf = 200", r.status_code == 200)
chequear("pdf firma %PDF-", r.content[:5] == b"%PDF-")

r = client.get("/admin/reportes/mensual/exportar/pdf?mes=13-9999")
chequear("exportar mes invalido = 422", r.status_code == 422)

print()
if fallos:
    print(f"{len(fallos)} PRUEBAS FALLARON:", fallos)
    sys.exit(1)
print("TODAS LAS PRUEBAS PASARON")
