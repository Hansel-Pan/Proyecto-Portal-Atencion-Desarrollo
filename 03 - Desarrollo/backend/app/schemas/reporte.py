from pydantic import BaseModel


class MetricasMensuales(BaseModel):
    periodo: str
    total_tickets: int
    por_tipo: dict[str, int]
    por_estado: dict[str, int]
    por_prioridad: dict[str, int]
    resueltos_por_ia: int
    resueltos_manual: int
    escalados: int
    pendientes: int
    tasa_resolucion_ia_pct: float
    tiempo_promedio_atencion_seg: float | None = None
    satisfaccion_promedio: float | None = None


class ReporteMensualOut(BaseModel):
    metricas: MetricasMensuales
