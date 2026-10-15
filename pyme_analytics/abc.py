"""
Inventory Pareto Analysis: ABC Classification Engine.
"""

from typing import List, Dict, Any
from .models import TransactionRecord, ABCItemClassification


class ABCAnalyzer:
    @staticmethod
    def classify_inventory(transactions: List[TransactionRecord]) -> List[ABCItemClassification]:
        """
        Calculates Pareto 80/20 distribution across catalog SKUs.
        """
        if not transactions:
            return []

        item_map: Dict[str, Dict[str, Any]] = {}
        for t in transactions:
            if t.sku not in item_map:
                item_map[t.sku] = {
                    "sku": t.sku,
                    "descripcion": t.descripcion,
                    "qty": 0.0,
                    "revenue": 0.0
                }
            item_map[t.sku]["qty"] += t.cantidad
            item_map[t.sku]["revenue"] += t.importe_total

        total_revenue = sum(item["revenue"] for item in item_map.values())
        if total_revenue <= 0:
            return []

        # Sort descending by revenue
        sorted_items = sorted(item_map.values(), key=lambda x: x["revenue"], reverse=True)

        classifications: List[ABCItemClassification] = []
        cum_pct = 0.0

        for item in sorted_items:
            pct = (item["revenue"] / total_revenue) * 100.0
            cum_pct += pct

            # Categorize based on standard Pareto thresholds
            if cum_pct <= 80.0:
                cat = "A"
            elif cum_pct <= 95.0:
                cat = "B"
            else:
                cat = "C"

            classifications.append(ABCItemClassification(
                sku=item["sku"],
                descripcion=item["descripcion"],
                unidades_vendidas=round(item["qty"], 2),
                ingresos_totales=round(item["revenue"], 2),
                pct_ingresos=round(pct, 2),
                pct_acumulado=round(cum_pct, 2),
                categoria_abc=cat
            ))

        return classifications
