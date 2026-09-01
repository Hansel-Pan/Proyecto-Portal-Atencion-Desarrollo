import json

from app.ai.base import ProveedorLLM, RespuestaLLM
from app.ai.prompts import MENSAJE_ESCALADO

REGLAS_CONOCIDAS = {
    "horario": (
        "Nuestro horario de atención es de lunes a viernes de 8:00 a 18:00. "
        "El portal y el chatbot están disponibles 24/7.",
        0.95,
    ),
    "contraseña": (
        "Para restablecer su contraseña, vaya a 'Olvidé mi contraseña' en la pantalla de inicio "
        "y siga las instrucciones enviadas a su correo.",
        0.90,
    ),
    "factura": (
        "Puede descargar sus facturas desde la sección 'Mi cuenta > Facturación'. "
        "Las facturas se emiten dentro de las 24 horas posteriores al pago.",
        0.88,
    ),
    "garantía": (
        "Todos los productos cuentan con 12 meses de garantía. Para hacerla efectiva, "
        "conserv su número de pedido y cree una solicitud con el detalle.",
        0.85,
    ),
}

PRIORIDAD_POR_TIPO = {"queja": "alta", "solicitud": "media", "consulta": "baja"}


class MockProveedor(ProveedorLLM):
    """Proveedor gratuito sin API key: reglas por palabras clave.

    Imita el contrato JSON del resto de proveedores para que todo el
    pipeline (parseo, decisión, guardado) se pruebe sin costo.
    """

    nombre = "mock-reglas"

    def generar(self, prompt_sistema: str, prompt_usuario: str, json_mode: bool = False) -> RespuestaLLM:
        if "hallazgos" in prompt_sistema:
            return self._generar_insights(prompt_usuario)
        return self._generar_chatbot(prompt_usuario)

    def _generar_chatbot(self, prompt_usuario: str) -> RespuestaLLM:
        texto = prompt_usuario.lower()
        tipo = next((t for t in PRIORIDAD_POR_TIPO if f"tipo: {t}" in texto), "consulta")
        tokens_entrada = len(texto.split())

        for clave, (respuesta, confianza) in REGLAS_CONOCIDAS.items():
            if clave in texto:
                datos = {
                    "puede_resolver": True,
                    "respuesta": respuesta,
                    "confianza": confianza,
                    "prioridad": PRIORIDAD_POR_TIPO[tipo],
                }
                break
        else:
            datos = {
                "puede_resolver": False,
                "respuesta": MENSAJE_ESCALADO,
                "confianza": 0.2,
                "prioridad": PRIORIDAD_POR_TIPO[tipo],
            }

        return RespuestaLLM(
            texto=json.dumps(datos, ensure_ascii=False),
            modelo=self.nombre,
            tokens_entrada=tokens_entrada,
            tokens_salida=len(json.dumps(datos).split()),
        )

    def _generar_insights(self, metricas_json: str) -> RespuestaLLM:
        try:
            m = json.loads(metricas_json)
        except json.JSONDecodeError:
            m = {}
        periodo = m.get("periodo", "?")
        total = m.get("total_tickets", 0)
        tasa_ia = m.get("tasa_resolucion_ia_pct", 0.0)
        pendientes = m.get("pendientes", 0)
        por_tipo = {k: v for k, v in m.get("por_tipo", {}).items() if isinstance(v, int)}
        tipo_dominante = max(por_tipo, key=lambda k: por_tipo[k]) if any(por_tipo.values()) else None

        if total:
            resumen = (
                f"Durante el período {periodo} se registraron {total} solicitudes de clientes. "
                f"El chatbot con IA resolvió automáticamente el {tasa_ia}% de los casos. "
                + (
                    f"Quedan {pendientes} casos pendientes que requieren gestión manual por parte del equipo."
                    if pendientes
                    else "No hay casos pendientes de revisión manual."
                )
            )
            hallazgos = [
                {
                    "titulo": "Volumen del período",
                    "detalle": f"Se recibieron {total} solicitudes en total.",
                },
                {
                    "titulo": f"Tipo dominante: {tipo_dominante}",
                    "detalle": f"{por_tipo.get(tipo_dominante, 0)} de {total} solicitudes fueron de tipo '{tipo_dominante}'.",
                },
                {
                    "titulo": "Nivel de automatización",
                    "detalle": f"La IA resolvió el {tasa_ia}% de las solicitudes sin intervención humana.",
                },
            ]
        else:
            resumen = f"El período {periodo} no registró solicitudes de clientes; no hay variaciones que analizar."
            hallazgos = [{"titulo": "Sin actividad", "detalle": "No se registraron tickets en el período."}]

        recomendaciones = []
        if pendientes:
            recomendaciones.append(
                {
                    "titulo": "Reducir la cola de pendientes",
                    "detalle": f"Asignar a un agente los {pendientes} tickets pendientes para evitar demoras.",
                }
            )
        if total and tasa_ia < 60:
            recomendaciones.append(
                {
                    "titulo": "Ampliar la base de conocimiento del chatbot",
                    "detalle": f"Con una tasa de resolución automática de {tasa_ia}%, ampliarla reduciría la carga manual.",
                }
            )
        recomendaciones.append(
            {
                "titulo": "Monitorear satisfacción",
                "detalle": "Medir la satisfacción del cliente mensualmente para detectar deterioros temprano.",
            }
        )

        datos = {
            "resumen": resumen,
            "hallazgos": hallazgos[:5],
            "recomendaciones": recomendaciones[:5],
        }
        return RespuestaLLM(texto=json.dumps(datos, ensure_ascii=False), modelo=self.nombre)
