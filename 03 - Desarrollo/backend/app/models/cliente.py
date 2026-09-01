from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, BigIntPK


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(200), unique=True)
    telefono: Mapped[str | None] = mapped_column(String(30))
    empresa: Mapped[str | None] = mapped_column(String(150))
    fecha_registro: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="cliente")
