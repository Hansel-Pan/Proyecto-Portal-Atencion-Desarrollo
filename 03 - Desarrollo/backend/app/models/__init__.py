from app.models.cliente import Cliente
from app.models.enums import AutorInteraccion, EstadoTicket, PrioridadTicket, TipoTicket
from app.models.insight_mensual import InsightMensual
from app.models.interaccion import Interaccion
from app.models.ticket import Ticket

__all__ = [
    "Cliente",
    "Ticket",
    "Interaccion",
    "InsightMensual",
    "TipoTicket",
    "EstadoTicket",
    "PrioridadTicket",
    "AutorInteraccion",
]
