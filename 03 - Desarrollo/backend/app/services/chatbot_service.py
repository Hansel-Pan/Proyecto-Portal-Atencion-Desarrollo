import json
import logging
from dataclasses import dataclass

from app.ai.base import ProveedorIAError, extraer_json
from app.ai.factory import obtener_proveedor
from app.ai.prompts import MENSAJE_ESCALADO, MENSAJE_FALLO_TECNICO, SISTEMA_PROMPT_CHATBOT
from app.core.config import get_settings
from app.models.enums import PrioridadTicket, TipoTicket

logger = logging.getLogger(__name__)

PRIORIDADES_VALIDAS = {p.value for p in PrioridadTicket}


@dataclass
class ResultadoIA:
    resuelto: bool
    respuesta: str
    confianza: float
    modelo: str
    prioridad: PrioridadTicket | None = None
    tokens_entrada: int = 0
    tokens_salida: int = 0


def clasificar_prioridad(tipo: TipoTicket) -> PrioridadTicket:
    return {
        TipoTicket.QUEJA: PrioridadTicket.ALTA,
        TipoTicket.SOLICITUD: PrioridadTicket.MEDIA,
        TipoTicket.CONSULTA: PrioridadTicket.BAJA,
    }[tipo]


def procesar_solicitud(tipo: TipoTicket, asunto: str, descripcion: str) -> ResultadoIA:
    settings = get_settings()
    proveedor = obtener_proveedor()
    prompt_usuario = f"Tipo: {tipo.value}\nAsunto: {asunto}\nDescripción: {descripcion}"

    try:
        respuesta_llm = proveedor.generar(SISTEMA_PROMPT_CHATBOT, prompt_usuario, json_mode=True)
        datos = extraer_json(respuesta_llm.texto)
    except (ProveedorIAError, ValueError, json.JSONDecodeError, KeyError) as exc:
        logger.warning("IA no disponible o respuesta inválida (%s): ticket escalado por seguridad", exc)
        return ResultadoIA(
            resuelto=False,
            respuesta=MENSAJE_FALLO_TECNICO,
            confianza=0.0,
            modelo=proveedor.nombre,
        )

    puede_resolver = bool(datos.get("puede_resolver"))
    try:
        confianza = min(1.0, max(0.0, float(datos.get("confianza", 0.0))))
    except (TypeError, ValueError):
        confianza = 0.0
    respuesta_texto = str(datos.get("respuesta") or "").strip()
    prioridad_raw = datos.get("prioridad")

    resuelto = puede_resolver and confianza >= settings.umbral_confianza and bool(respuesta_texto)

    return ResultadoIA(
        resuelto=resuelto,
        respuesta=respuesta_texto if resuelto else MENSAJE_ESCALADO,
        confianza=confianza,
        modelo=respuesta_llm.modelo,
        prioridad=(
            PrioridadTicket(prioridad_raw)
            if prioridad_raw in PRIORIDADES_VALIDAS
            else None
        ),
        tokens_entrada=respuesta_llm.tokens_entrada,
        tokens_salida=respuesta_llm.tokens_salida,
    )
