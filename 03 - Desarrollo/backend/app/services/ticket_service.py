import re
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.models import AutorInteraccion, Cliente, EstadoTicket, Interaccion, PrioridadTicket, Ticket, TipoTicket
from app.schemas.ticket import TicketCreate
from app.services.chatbot_service import clasificar_prioridad, procesar_solicitud

CODIGO_RE = re.compile(r"^TCK-\d{4}-\d{6}$")


def obtener_o_crear_cliente(db: Session, datos: TicketCreate) -> Cliente:
    cliente = db.scalar(select(Cliente).where(Cliente.email == datos.cliente.email))
    if cliente is None:
        cliente = Cliente(**datos.cliente.model_dump())
        db.add(cliente)
        db.flush()
    return cliente


def crear_ticket(db: Session, datos: TicketCreate) -> Ticket:
    cliente = obtener_o_crear_cliente(db, datos)
    resultado = procesar_solicitud(datos.tipo, datos.asunto, datos.descripcion)

    ticket = Ticket(
        codigo="",
        cliente_id=cliente.id,
        tipo=datos.tipo,
        asunto=datos.asunto,
        descripcion=datos.descripcion,
        prioridad=resultado.prioridad or clasificar_prioridad(datos.tipo),
        estado=EstadoTicket.ABIERTO,
    )
    db.add(ticket)
    db.flush()

    ahora = datetime.now(timezone.utc)
    ticket.codigo = f"TCK-{ahora.year}-{ticket.id:06d}"

    db.add(
        Interaccion(
            ticket_id=ticket.id,
            autor=AutorInteraccion.CLIENTE,
            mensaje=datos.descripcion,
        )
    )
    db.add(
        Interaccion(
            ticket_id=ticket.id,
            autor=AutorInteraccion.IA,
            mensaje=resultado.respuesta,
            modelo=resultado.modelo,
            confianza=resultado.confianza,
            escalado=not resultado.resuelto,
            tokens_entrada=resultado.tokens_entrada,
            tokens_salida=resultado.tokens_salida,
        )
    )

    if resultado.resuelto:
        ticket.estado = EstadoTicket.RESUELTO_IA
        ticket.resuelto_por_ia = True
        ticket.fecha_resolucion = ahora
        ticket.tiempo_atencion_seg = int((ahora - ticket.fecha_creacion.replace(tzinfo=timezone.utc)).total_seconds())
    else:
        ticket.estado = EstadoTicket.ESCALADO

    db.commit()
    db.refresh(ticket)
    return ticket


def obtener_ticket(db: Session, ref: str | int) -> Ticket | None:
    stmt = select(Ticket).options(
        joinedload(Ticket.cliente),
        joinedload(Ticket.interacciones),
    )
    if isinstance(ref, str) and CODIGO_RE.match(ref):
        stmt = stmt.where(Ticket.codigo == ref)
    elif isinstance(ref, int) or (isinstance(ref, str) and ref.isdigit()):
        stmt = stmt.where(Ticket.id == int(ref))
    else:
        return None
    return db.scalar(stmt)


def responder_mensaje(db: Session, ref: str | int, mensaje: str) -> Ticket | None:
    ticket = obtener_ticket(db, ref)
    if ticket is None or ticket.estado == EstadoTicket.CERRADO:
        return None

    contexto = "\n".join(
        f"{i.autor.value}: {i.mensaje}" for i in (ticket.interacciones or [])[-6:]
    )
    descripcion_ia = (
        f"Descripción original: {ticket.descripcion}\n\n"
        f"Conversación previa:\n{contexto}\n\nMensaje nuevo del cliente: {mensaje}"
    )
    resultado = procesar_solicitud(ticket.tipo, ticket.asunto, descripcion_ia)

    ahora = datetime.now(timezone.utc)
    db.add(
        Interaccion(ticket_id=ticket.id, autor=AutorInteraccion.CLIENTE, mensaje=mensaje)
    )
    db.add(
        Interaccion(
            ticket_id=ticket.id,
            autor=AutorInteraccion.IA,
            mensaje=resultado.respuesta,
            modelo=resultado.modelo,
            confianza=resultado.confianza,
            escalado=not resultado.resuelto,
            tokens_entrada=resultado.tokens_entrada,
            tokens_salida=resultado.tokens_salida,
        )
    )

    if resultado.resuelto and ticket.estado == EstadoTicket.ABIERTO:
        ticket.estado = EstadoTicket.RESUELTO_IA
        ticket.resuelto_por_ia = True
        ticket.fecha_resolucion = ahora
        if ticket.fecha_creacion.tzinfo is None:
            ticket.fecha_creacion = ticket.fecha_creacion.replace(tzinfo=timezone.utc)
        ticket.tiempo_atencion_seg = int((ahora - ticket.fecha_creacion).total_seconds())

    db.commit()
    db.expire(ticket)
    return obtener_ticket(db, ticket.id)


def listar_tickets(
    db: Session,
    tipo: TipoTicket | None = None,
    estado: EstadoTicket | None = None,
    prioridad: PrioridadTicket | None = None,
    fecha_desde: datetime | None = None,
    fecha_hasta: datetime | None = None,
    pagina: int = 1,
    tamanio: int = 20,
) -> tuple[list[Ticket], int]:
    filtros = []
    if tipo:
        filtros.append(Ticket.tipo == tipo)
    if estado:
        filtros.append(Ticket.estado == estado)
    if prioridad:
        filtros.append(Ticket.prioridad == prioridad)
    if fecha_desde:
        filtros.append(Ticket.fecha_creacion >= fecha_desde)
    if fecha_hasta:
        filtros.append(Ticket.fecha_creacion < fecha_hasta)

    base = select(Ticket).where(*filtros) if filtros else select(Ticket)

    total = db.scalar(
        select(func.count())
        .select_from(Ticket)
        .where(*filtros)
        if filtros
        else select(func.count()).select_from(Ticket)
    )
    items = db.scalars(
        base.order_by(Ticket.fecha_creacion.desc()).offset((pagina - 1) * tamanio).limit(tamanio)
    ).all()
    return list(items), total or 0
