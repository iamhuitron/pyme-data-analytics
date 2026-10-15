"""
Inventory Optimization and Stock-out Forecasting Engine.
"""

from typing import List, Dict, Any
from .models import TransactionRecord


class InventoryOptimizer:
    @staticmethod
    def calculate_reorder_points(
        transactions: List[TransactionRecord],
        current_stocks: Dict[str, float],
        lead_time_days: int = 7,
        safety_stock_days: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Calculates daily sales velocity, Reorder Point (ROP), and Days of Inventory (DOI).
        """
        if not transactions:
            return []

        # Calculate sales per SKU
        sku_sales: Dict[str, float] = {}
        sku_names: Dict[str, str] = {}
        dates = set()

        for t in transactions:
            sku_sales[t.sku] = sku_sales.get(t.sku, 0.0) + t.cantidad
            sku_names[t.sku] = t.descripcion
            dates.add(t.fecha)

        num_days = max(len(dates), 1)

        recommendations = []
        for sku, total_qty in sku_sales.items():
            daily_velocity = total_qty / num_days
            curr_stock = current_stocks.get(sku, 0.0)
            
            # Reorder Point (ROP) = (Daily Sales * Lead Time) + Safety Stock
            safety_stock = daily_velocity * safety_stock_days
            rop = (daily_velocity * lead_time_days) + safety_stock

            # Days of Inventory (DOI)
            doi = (curr_stock / daily_velocity) if daily_velocity > 0 else 999.0

            if curr_stock <= safety_stock:
                status = "CRÍTICO (Riesgo de Desabasto)"
            elif curr_stock <= rop:
                status = "REORDENAR AHORA"
            elif doi > 60:
                status = "SOBRE-INVENTARIO"
            else:
                status = "NIVEL SALUDABLE"

            recommendations.append({
                "sku": sku,
                "descripcion": sku_names[sku],
                "velocidad_diaria": round(daily_velocity, 2),
                "stock_actual": curr_stock,
                "punto_reorden_rop": round(rop, 1),
                "dias_inventario_doi": round(doi, 1),
                "estado_alerta": status
            })

        recommendations.sort(key=lambda x: x["dias_inventario_doi"])
        return recommendations
