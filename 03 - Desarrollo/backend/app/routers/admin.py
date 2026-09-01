from datetime import date, datetime, time, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.ai.base import ProveedorIAError
from app.db.session import get_db
from app.models.enums import EstadoTicket, PrioridadTicket, TipoTicket
from app.schemas.reporte import ReporteMensualOut
from app.schemas.ticket import PaginaTickets
from app.services import exporte_service, insights_service, reporte_service, ticket_service

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/tickets", response_model=PaginaTickets)
def listar_tickets(
    tipo: TipoTicket | None = None,
    estado: EstadoTicket | None = None,
    prioridad: PrioridadTicket | None = None,
    fecha_desde: date | None = None,
    fecha_hasta: date | None = None,
    pagina: int = Query(1, ge=1),
    tamanio_pagina: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    desde = datetime.combine(fecha_desde, time.min, tzinfo=timezone.utc) if fecha_desde else None
    hasta = (
        datetime.combine(fecha_hasta, time.min, tzinfo=timezone.utc) + timedelta(days=1)
        if fecha_hasta
        else None
    )
    items, total = ticket_service.listar_tickets(
        db,
        tipo=tipo,
        estado=estado,
        prioridad=prioridad,
        fecha_desde=desde,
        fecha_hasta=hasta,
        pagina=pagina,
        tamanio=tamanio_pagina,
    )
    return PaginaTickets(total=total, pagina=pagina, tamanio_pagina=tamanio_pagina, items=items)


@router.get("/reportes/mensual", response_model=ReporteMensualOut)
def reporte_mensual(mes: str = Query(..., description="Periodo en formato YYYY-MM"), db: Session = Depends(get_db)):
    try:
        metricas = reporte_service.calcular_metricas(db, mes)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return ReporteMensualOut(metricas=metricas)


@router.get("/reportes/mensual/insights")
def insights_mensuales(
    mes: str = Query(..., description="Periodo en formato YYYY-MM"),
    recalcular: bool = Query(False, description="Fuerza regenerar aunque exista caché"),
    db: Session = Depends(get_db),
):
    try:
        resultado = insights_service.generar_insight(db, mes, forzar=recalcular)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except ProveedorIAError as exc:
        raise HTTPException(status_code=503, detail=f"Proveedor de IA no disponible: {exc}") from exc
    return resultado


@router.get("/reportes/mensual/exportar/excel")
def exportar_excel(mes: str = Query(...), db: Session = Depends(get_db)):
    try:
        contenido, nombre = exporte_service.generar_excel(db, mes)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return Response(
        content=contenido,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{nombre}"'},
    )


@router.get("/reportes/mensual/exportar/pdf")
def exportar_pdf(mes: str = Query(...), db: Session = Depends(get_db)):
    try:
        contenido, nombre = exporte_service.generar_pdf(db, mes)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return Response(
        content=contenido,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{nombre}"'},
    )
