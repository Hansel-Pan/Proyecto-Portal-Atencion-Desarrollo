from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, BigIntPK
from app.models.enums import ENUM_KWARGS, EstadoTicket, PrioridadTicket, TipoTicket


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(24), unique=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), index=True)
    tipo: Mapped[TipoTicket] = mapped_column(Enum(TipoTicket, name="tipo_ticket", **ENUM_KWARGS))
    asunto: Mapped[str] = mapped_column(String(200))
    descripcion: Mapped[str] = mapped_column()
    estado: Mapped[EstadoTicket] = mapped_column(
        Enum(EstadoTicket, name="estado_ticket", **ENUM_KWARGS), default=EstadoTicket.ABIERTO
    )
    prioridad: Mapped[PrioridadTicket] = mapped_column(
        Enum(PrioridadTicket, name="prioridad_ticket", **ENUM_KWARGS), default=PrioridadTicket.MEDIA
    )
    resuelto_por_ia: Mapped[bool] = mapped_column(Boolean, default=False)
    tiempo_atencion_seg: Mapped[int | None] = mapped_column(Integer)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_resolucion: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    satisfaccion: Mapped[int | None] = mapped_column()

    cliente: Mapped["Cliente"] = relationship(back_populates="tickets")
    interacciones: Mapped[list["Interaccion"]] = relationship(
        back_populates="ticket", cascade="all, delete-orphan", order_by="Interaccion.fecha"
    )
