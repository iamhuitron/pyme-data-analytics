"""
Customer Segmentation Engine: RFM (Recency, Frequency, Monetary) Modeling.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from .models import TransactionRecord, CustomerSegment


def _assign_quintile(val: float, thresholds: List[float], reverse: bool = False) -> int:
    """Assigns score 1 to 5 based on quantile thresholds."""
    score = 1
    for t in thresholds:
        if val > t:
            score += 1
    return 6 - score if reverse else score


class RFMAnalyzer:
    @staticmethod
    def analyze_customers(
        transactions: List[TransactionRecord],
        reference_date: Optional[str] = None
    ) -> List[CustomerSegment]:
        if not transactions:
            return []

        if reference_date:
            ref_dt = datetime.strptime(reference_date, "%Y-%m-%d")
        else:
            dates = [datetime.strptime(t.fecha, "%Y-%m-%d") for t in transactions]
            ref_dt = max(dates)

        # Aggregate by customer
        cust_map: Dict[str, Dict[str, Any]] = {}
        for t in transactions:
            c_id = t.cliente_id
            if c_id not in cust_map:
                cust_map[c_id] = {
                    "last_date": datetime.strptime(t.fecha, "%Y-%m-%d"),
                    "tickets": set(),
                    "monetary": 0.0
                }
            t_dt = datetime.strptime(t.fecha, "%Y-%m-%d")
            if t_dt > cust_map[c_id]["last_date"]:
                cust_map[c_id]["last_date"] = t_dt
            cust_map[c_id]["tickets"].add(t.ticket_id)
            cust_map[c_id]["monetary"] += t.importe_total

        records = []
        for c_id, data in cust_map.items():
            recency = (ref_dt - data["last_date"]).days
            frequency = len(data["tickets"])
            monetary = round(data["monetary"], 2)
            records.append({
                "cliente_id": c_id,
                "recency": max(recency, 0),
                "frequency": frequency,
                "monetary": monetary
            })

        # Calculate scores
        recencies = sorted(r["recency"] for r in records)
        frequencies = sorted(r["frequency"] for r in records)
        monetaries = sorted(r["monetary"] for r in records)
        n = len(records)

        def get_thresholds(arr):
            return [
                arr[int(n * 0.20)],
                arr[int(n * 0.40)],
                arr[int(n * 0.60)],
                arr[int(n * 0.80)]
            ]

        r_thresh = get_thresholds(recencies)
        f_thresh = get_thresholds(frequencies)
        m_thresh = get_thresholds(monetaries)

        segments = []
        for r in records:
            # Lower recency is better (reverse = True)
            r_score = _assign_quintile(r["recency"], r_thresh, reverse=True)
            f_score = _assign_quintile(r["frequency"], f_thresh, reverse=False)
            m_score = _assign_quintile(r["monetary"], m_thresh, reverse=False)

            # Assign business segment
            if r_score >= 4 and f_score >= 4:
                label = "Champions"
            elif r_score >= 3 and f_score >= 3:
                label = "Clientes Leales"
            elif r_score >= 4 and f_score <= 2:
                label = "Nuevos Prometedores"
            elif r_score <= 2 and f_score >= 3:
                label = "En Riesgo"
            elif r_score <= 2 and f_score <= 2:
                label = "Inactivos / Perdidos"
            else:
                label = "Potenciales a Fidelizar"

            segments.append(CustomerSegment(
                cliente_id=r["cliente_id"],
                recency_days=r["recency"],
                frequency_count=r["frequency"],
                monetary_total=r["monetary"],
                r_score=r_score,
                f_score=f_score,
                m_score=m_score,
                segment_label=label
            ))

        return segments
