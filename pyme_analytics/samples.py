"""
Sample transaction dataset generator for retail and automotive parts PyMEs.
"""

from typing import List, Dict
from datetime import datetime, timedelta
from .models import TransactionRecord


def get_sample_retail_transactions() -> List[TransactionRecord]:
    """Generates 120 realistic transaction lines representing a Mexican refaccionaria / retail shop."""
    skus = [
        ("SKU-ACEITE-5W30", "Aceite Sintetico 5W-30 (Garrafa 5L)", 680.0),
        ("SKU-FILTRO-ACEITE", "Filtro de Aceite Blindado PH-3614", 125.0),
        ("SKU-BUJIAS-IRIDIUM", "Juego de 4 Bujias de Iridio NGK", 520.0),
        ("SKU-BALATAS-DEL", "Juego Balatas Delanteras Ceramicas", 780.0),
        ("SKU-ANTICONGELANTE", "Anticongelante Organico 50/50 4L", 210.0),
        ("SKU-LIMPIADOR-CARB", "Spray Limpiador de Carburador", 95.0),
        ("SKU-BATERIA-L47", "Bateria Automotriz 12V 550A", 1850.0),
        ("SKU-FOCO-H4", "Foco Halogeno H4 12V", 85.0),
    ]

    customers = [
        "CLI-TALLER-PEREZ",
        "CLI-FLOTILLA-RAPIDA",
        "CLI-MECANICA-LOPEZ",
        "CLI-AUTO-ZONE-LOCAL",
        "CLI-TAXIS-UNIDOS",
        "CLI-MOSTRADOR-01",
        "CLI-MOSTRADOR-02",
        "CLI-MOSTRADOR-03"
    ]

    base_date = datetime(2026, 3, 1)
    transactions = []

    # Ticket 1 to 35
    for t_idx in range(1, 36):
        ticket_id = f"TCK-2026-{t_idx:04d}"
        t_date = (base_date + timedelta(days=(t_idx % 25))).strftime("%Y-%m-%d")
        cust = customers[t_idx % len(customers)]

        # Always bundle oil + oil filter for mechanics
        if t_idx % 2 == 0:
            transactions.append(TransactionRecord(
                ticket_id=ticket_id, fecha=t_date, cliente_id=cust,
                sku=skus[0][0], descripcion=skus[0][1], cantidad=2.0,
                precio_unitario=skus[0][2], importe_total=2.0 * skus[0][2]
            ))
            transactions.append(TransactionRecord(
                ticket_id=ticket_id, fecha=t_date, cliente_id=cust,
                sku=skus[1][0], descripcion=skus[1][1], cantidad=2.0,
                precio_unitario=skus[1][2], importe_total=2.0 * skus[1][2]
            ))
        else:
            item = skus[(t_idx * 3) % len(skus)]
            qty = 1.0 + (t_idx % 3)
            transactions.append(TransactionRecord(
                ticket_id=ticket_id, fecha=t_date, cliente_id=cust,
                sku=item[0], descripcion=item[1], cantidad=qty,
                precio_unitario=item[2], importe_total=qty * item[2]
            ))

    return transactions


def get_sample_inventory_stocks() -> Dict[str, float]:
    return {
        "SKU-ACEITE-5W30": 8.0,
        "SKU-FILTRO-ACEITE": 6.0,
        "SKU-BUJIAS-IRIDIUM": 24.0,
        "SKU-BALATAS-DEL": 12.0,
        "SKU-ANTICONGELANTE": 35.0,
        "SKU-LIMPIADOR-CARB": 50.0,
        "SKU-BATERIA-L47": 3.0,
        "SKU-FOCO-H4": 40.0,
    }
