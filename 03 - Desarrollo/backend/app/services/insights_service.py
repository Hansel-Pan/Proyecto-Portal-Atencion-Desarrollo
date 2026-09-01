import json
import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.ai.base import ProveedorIAError, extraer_json
from app.ai.factory import obtener_proveedor
from app.ai.prompts import SISTEMA_PROMPT_INSIGHTS
from app.models import InsightMensual
from app.services.reporte_service import calcular_metricas, validar_periodo

logger = logging.getLogger(__name__)

MAX_ITEMS_LISTA = 8


def obtener_insight(db: Session, periodo: str) -> InsightMensual | None:
    validar_periodo(periodo)
    return db.query(InsightMensual).filter(InsightMensual.periodo == periodo).first()


def _fila_a_dict(fila: InsightMensual) -> dict:
    return {
        "periodo": fila.periodo,
        "metricas": fila.metricas,
        "resumen": fila.resumen,
        "hallazgos": fila.hallazgos,
        "recomendaciones": fila.recomendaciones,
        "modelo": fila.modelo,
        "generado_en": fila.generado_en.isoformat() if fila.generado_en else None,
        "desde_cache": True,
    }


def generar_insight(db: Session, periodo: str, forzar: bool = False) -> dict:
    validar_periodo(periodo)

    if not forzar:
        existente = obtener_insight(db, periodo)
        if existente is not None:
            return _fila_a_dict(existente)

    metricas = calcular_metricas(db, periodo)

    if metricas["total_tickets"] == 0:
        return {
            "periodo": periodo,
            "metricas": metricas,
            "resumen": (
                f"El período {periodo} no registró solicitudes de clientes. "
                "No hay datos suficientes para generar hallazgos ni recomendaciones."
            ),
            "hallazgos": [],
            "recomendaciones": [],
            "modelo": "sin-datos",
            "generado_en": datetime.now(timezone.utc).isoformat(),
            "desde_cache": False,
        }

    proveedor = obtener_proveedor()
    try:
        respuesta_llm = proveedor.generar(
            SISTEMA_PROMPT_INSIGHTS,
            json.dumps(metricas, ensure_ascii=False),
            json_mode=True,
        )
        datos = extraer_json(respuesta_llm.texto)
        resumen = str(datos["resumen"]).strip()
        hallazgos = _normalizar_lista(datos.get("hallazgos"))
        recomendaciones = _normalizar_lista(datos.get("recomendaciones"))
        if not resumen or not hallazgos or not recomendaciones:
            raise ValueError("La IA devolvió un informe incompleto")
    except (ProveedorIAError, ValueError, KeyError, json.JSONDecodeError, TypeError) as exc:
        logger.warning("No se pudieron generar insights para %s: %s", periodo, exc)
        raise ProveedorIAError(f"Generación de insights falló para {periodo}: {exc}") from exc

    ahora = datetime.now(timezone.utc)
    fila = obtener_insight(db, periodo)
    if fila is None:
        fila = InsightMensual(periodo=periodo)
        db.add(fila)

    fila.metricas = metricas
    fila.resumen = resumen
    fila.hallazgos = hallazgos
    fila.recomendaciones = recomendaciones
    fila.modelo = respuesta_llm.modelo
    fila.tokens_entrada = respuesta_llm.tokens_entrada
    fila.tokens_salida = respuesta_llm.tokens_salida
    fila.generado_en = ahora

    db.commit()
    db.refresh(fila)
    resultado = _fila_a_dict(fila)
    resultado["desde_cache"] = False
    return resultado


def _normalizar_lista(items) -> list[dict]:
    if not isinstance(items, list):
        return []
    normalizados = []
    for item in items[:MAX_ITEMS_LISTA]:
        if isinstance(item, dict):
            titulo = str(item.get("titulo") or "").strip()
            detalle = str(item.get("detalle") or "").strip()
            if titulo and detalle:
                normalizados.append({"titulo": titulo, "detalle": detalle})
        elif isinstance(item, str) and item.strip():
            normalizados.append({"titulo": item.strip(), "detalle": ""})
    return normalizados
