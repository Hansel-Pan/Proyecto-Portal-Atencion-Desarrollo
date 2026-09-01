import enum


class TipoTicket(str, enum.Enum):
    CONSULTA = "consulta"
    SOLICITUD = "solicitud"
    QUEJA = "queja"


class EstadoTicket(str, enum.Enum):
    ABIERTO = "abierto"
    ESCALADO = "escalado"
    RESUELTO_IA = "resuelto_ia"
    RESUELTO_MANUAL = "resuelto_manual"
    CERRADO = "cerrado"


class PrioridadTicket(str, enum.Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


class AutorInteraccion(str, enum.Enum):
    CLIENTE = "cliente"
    IA = "ia"
    AGENTE = "agente"


ENUM_KWARGS = {
    "values_callable": lambda e: [m.value for m in e],
    "native_enum": True,
}
