from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import AutorInteraccion, EstadoTicket, PrioridadTicket, TipoTicket


class ClienteCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=150)
    email: EmailStr
    telefono: str | None = Field(default=None, max_length=30)
    empresa: str | None = Field(default=None, max_length=150)


class ClienteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    email: EmailStr
    empresa: str | None = None


class TicketCreate(BaseModel):
    cliente: ClienteCreate
    tipo: TipoTicket
    asunto: str = Field(min_length=5, max_length=200)
    descripcion: str = Field(min_length=10)


class MensajeCreate(BaseModel):
    mensaje: str = Field(min_length=1, max_length=4000)


class InteraccionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    autor: AutorInteraccion
    mensaje: str
    modelo: str | None = None
    confianza: float | None = None
    escalado: bool
    tokens_entrada: int | None = None
    tokens_salida: int | None = None
    fecha: datetime


class TicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    tipo: TipoTicket
    asunto: str
    estado: EstadoTicket
    prioridad: PrioridadTicket
    resuelto_por_ia: bool
    tiempo_atencion_seg: int | None = None
    fecha_creacion: datetime
    fecha_resolucion: datetime | None = None
    cliente: ClienteOut


class TicketDetalle(TicketOut):
    descripcion: str
    satisfaccion: int | None = None
    interacciones: list[InteraccionOut] = []


class PaginaTickets(BaseModel):
    total: int
    pagina: int
    tamanio_pagina: int
    items: list[TicketOut]
