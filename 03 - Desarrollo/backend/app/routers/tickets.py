from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.ticket import MensajeCreate, TicketCreate, TicketDetalle
from app.services import ticket_service

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("", response_model=TicketDetalle, status_code=status.HTTP_201_CREATED)
def crear_ticket(datos: TicketCreate, db: Session = Depends(get_db)):
    return ticket_service.crear_ticket(db, datos)


@router.get("/{ticket_ref}", response_model=TicketDetalle)
def consultar_ticket(ticket_ref: str, db: Session = Depends(get_db)):
    ticket = ticket_service.obtener_ticket(db, ticket_ref)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket


@router.post("/{ticket_ref}/mensajes", response_model=TicketDetalle)
def enviar_mensaje(ticket_ref: str, datos: MensajeCreate, db: Session = Depends(get_db)):
    ticket = ticket_service.responder_mensaje(db, ticket_ref, datos.mensaje)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket no encontrado o cerrado")
    return ticket
