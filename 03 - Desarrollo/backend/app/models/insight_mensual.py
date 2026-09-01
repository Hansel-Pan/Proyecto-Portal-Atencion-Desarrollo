from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base

JSONCompat = JSON().with_variant(JSONB(), "postgresql")


class InsightMensual(Base):
    __tablename__ = "insights_mensuales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    periodo: Mapped[str] = mapped_column(String(7), unique=True)
    metricas: Mapped[dict] = mapped_column(JSONCompat)
    resumen: Mapped[str] = mapped_column(Text)
    hallazgos: Mapped[list] = mapped_column(JSONCompat)
    recomendaciones: Mapped[list] = mapped_column(JSONCompat)
    modelo: Mapped[str] = mapped_column(String(100))
    tokens_entrada: Mapped[int | None] = mapped_column(Integer)
    tokens_salida: Mapped[int | None] = mapped_column(Integer)
    generado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
