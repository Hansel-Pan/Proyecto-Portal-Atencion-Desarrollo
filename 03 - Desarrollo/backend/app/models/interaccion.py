from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, BigIntPK
from app.models.enums import ENUM_KWARGS, AutorInteraccion


class Interaccion(Base):
    __tablename__ = "interacciones"

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id", ondelete="CASCADE"), index=True)
    autor: Mapped[AutorInteraccion] = mapped_column(Enum(AutorInteraccion, name="autor_interaccion", **ENUM_KWARGS))
    mensaje: Mapped[str] = mapped_column(Text)
    modelo: Mapped[str | None] = mapped_column(String(100))
    confianza: Mapped[float | None] = mapped_column(Numeric(4, 3))
    escalado: Mapped[bool] = mapped_column(Boolean, default=False)
    tokens_entrada: Mapped[int | None] = mapped_column(Integer)
    tokens_salida: Mapped[int | None] = mapped_column(Integer)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    ticket: Mapped["Ticket"] = relationship(back_populates="interacciones")
