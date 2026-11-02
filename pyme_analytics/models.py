"""
Data models for retail transactions, inventory items, and analytics outputs.
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional


@dataclass
class TransactionRecord:
    ticket_id: str
    fecha: str
    cliente_id: str
    sku: str
    descripcion: str
    cantidad: float
    precio_unitario: float
    importe_total: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CustomerSegment:
    cliente_id: str
    recency_days: int
    frequency_count: int
    monetary_total: float
    r_score: int
    f_score: int
    m_score: int
    segment_label: str

    @property
    def rfm_combined_score(self) -> str:
        """Returns the concatenated RFM score string, e.g. '555' or '341'."""
        return f"{self.r_score}{self.f_score}{self.m_score}"


@dataclass
class ABCItemClassification:
    sku: str
    descripcion: str
    unidades_vendidas: float
    ingresos_totales: float
    pct_ingresos: float
    pct_acumulado: float
    categoria_abc: str  # 'A', 'B', 'C'

    @property
    def is_top_performer(self) -> bool:
        """Returns True if the item belongs to Class A (Pareto top 80% revenue)."""
        return self.categoria_abc == "A"


@dataclass
class AssociationRule:
    antecedente: str
    consecuente: str
    support: float
    confidence: float
    lift: float
