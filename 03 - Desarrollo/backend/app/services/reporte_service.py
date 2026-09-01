import re
from calendar import monthrange
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import EstadoTicket, PrioridadTicket, Ticket, TipoTicket

PERIODO_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


def validar_periodo(mes: str) -> str:
    if not PERIODO_RE.match(mes):
        raise ValueError(f"Formato de mes inválido: '{mes}'. Use YYYY-MM, ej: 2026-08")
    return mes


def rango_periodo(periodo: str) -> tuple[datetime, datetime]:
    anio, mes = int(periodo[:4]), int(periodo[5:7])
    inicio = datetime(anio, mes, 1, tzinfo=timezone.utc)
    fin_exclusivo = datetime(anio + (mes == 12), (mes % 12) + 1, 1, tzinfo=timezone.utc)
    return inicio, fin_exclusivo


def calcular_metricas(db: Session, periodo: str) -> dict:
    validar_periodo(periodo)
    inicio, fin = rango_periodo(periodo)
    filtro_fecha = Ticket.fecha_creacion >= inicio, Ticket.fecha_creacion < fin

    total = db.scalar(select(func.count()).select_from(Ticket).where(*filtro_fecha)) or 0

    def conteos(columna) -> dict[str, int]:
        filas = db.execute(
            select(columna, func.count()).select_from(Ticket).where(*filtro_fecha).group_by(columna)
        ).all()
        return {clave.value if hasattr(clave, "value") else str(clave): cantidad for clave, cantidad in filas}

    por_tipo = conteos(Ticket.tipo)
    por_estado = conteos(Ticket.estado)
    por_prioridad = conteos(Ticket.prioridad)

    resueltos_ia = por_estado.get(EstadoTicket.RESUELTO_IA.value, 0)
    escalados = por_estado.get(EstadoTicket.ESCALADO.value, 0)
    pendientes = por_estado.get(EstadoTicket.ABIERTO.value, 0) + escalados

    tiempo_promedio = db.scalar(
        select(func.avg(Ticket.tiempo_atencion_seg))
        .select_from(Ticket)
        .where(*filtro_fecha, Ticket.tiempo_atencion_seg.isnot(None))
    )
    satisfaccion_promedio = db.scalar(
        select(func.avg(Ticket.satisfaccion))
        .select_from(Ticket)
        .where(*filtro_fecha, Ticket.satisfaccion.isnot(None))
    )

    return {
        "periodo": periodo,
        "total_tickets": total,
        "por_tipo": {t.value: por_tipo.get(t.value, 0) for t in TipoTicket},
        "por_estado": {e.value: por_estado.get(e.value, 0) for e in EstadoTicket},
        "por_prioridad": {p.value: por_prioridad.get(p.value, 0) for p in PrioridadTicket},
        "resueltos_por_ia": resueltos_ia,
        "resueltos_manual": por_estado.get(EstadoTicket.RESUELTO_MANUAL.value, 0),
        "escalados": escalados,
        "pendientes": pendientes,
        "tasa_resolucion_ia_pct": round(resueltos_ia / total * 100, 1) if total else 0.0,
        "tiempo_promedio_atencion_seg": round(float(tiempo_promedio), 1) if tiempo_promedio is not None else None,
        "satisfaccion_promedio": round(float(satisfaccion_promedio), 2) if satisfaccion_promedio is not None else None,
    }
