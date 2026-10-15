"""
Command Line Interface for PyME Data Analytics.
"""

import sys
import argparse
from .samples import get_sample_retail_transactions, get_sample_inventory_stocks
from .rfm import RFMAnalyzer
from .abc import ABCAnalyzer
from .basket import MarketBasketAnalyzer
from .inventory import InventoryOptimizer


def main():
    parser = argparse.ArgumentParser(
        description="PyME Data Analytics: Retail & Inventory Intelligence Engine"
    )
    subparsers = parser.add_subparsers(dest="command", help="Comandos de análisis")

    # Command: rfm
    subparsers.add_parser("rfm", help="Ejecuta segmentación de clientes RFM")

    # Command: abc
    subparsers.add_parser("abc", help="Calcula distribución Pareto ABC del catálogo")

    # Command: basket
    subparsers.add_parser("basket", help="Minería de reglas de asociación (Market Basket)")

    # Command: rop
    subparsers.add_parser("rop", help="Calcula Puntos de Reorden y Días de Inventario")

    # Command: report
    subparsers.add_parser("report", help="Genera reporte gerencial consolidado")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    transactions = get_sample_retail_transactions()
    stocks = get_sample_inventory_stocks()

    if args.command == "rfm":
        segments = RFMAnalyzer.analyze_customers(transactions)
        print("\n================== SEGMENTACIÓN RFM DE CLIENTES ==================")
        print(f"{'Cliente ID':<22} | {'R':<2} {'F':<2} {'M':<2} | {'Gasto Total':<12} | {'Segmento'}")
        print("-" * 65)
        for s in segments:
            print(f"{s.cliente_id:<22} | {s.r_score}  {s.f_score}  {s.m_score}  | ${s.monetary_total:>9,.2f} | {s.segment_label}")
        print("==================================================================\n")

    elif args.command == "abc":
        abc_items = ABCAnalyzer.classify_inventory(transactions)
        print("\n================= CLASIFICACIÓN DE INVENTARIO ABC =================")
        print(f"{'Categoría':<10} | {'SKU':<18} | {'Ventas ($)':<12} | {'% Acumulado'}")
        print("-" * 65)
        for item in abc_items:
            print(f"[{item.categoria_abc}]        | {item.sku:<18} | ${item.ingresos_totales:>9,.2f} | {item.pct_acumulado:>5.1f}%")
        print("==================================================================\n")

    elif args.command == "basket":
        rules = MarketBasketAnalyzer.find_rules(transactions, min_support=0.10, min_confidence=0.30)
        print("\n================= REGLAS DE ASOCIACIÓN (CROSS-SELL) =================")
        print(f"{'Si compra (Antecedente)':<20} -> {'También compra':<20} | {'Confianza':<9} | {'Lift'}")
        print("-" * 75)
        for r in rules[:8]:
            print(f"{r.antecedente:<20} -> {r.consecuente:<20} | {r.confidence * 100:>7.1f}% | {r.lift:>5.2f}x")
        print("=====================================================================\n")

    elif args.command == "rop":
        reorder = InventoryOptimizer.calculate_reorder_points(transactions, stocks)
        print("\n================ PREVENCIÓN DE DESABASTO & REORDEN ================")
        print(f"{'SKU':<18} | {'Stock':<6} | {'ROP':<6} | {'Días Inv':<8} | {'Estado Alerta'}")
        print("-" * 75)
        for r in reorder:
            print(f"{r['sku']:<18} | {r['stock_actual']:>5.0f}  | {r['punto_reorden_rop']:>5.1f}  | {r['dias_inventario_doi']:>6.1f} d | {r['estado_alerta']}")
        print("====================================================================\n")

    elif args.command == "report":
        print("=== REPORTE EJECUTIVO INTEGRAL DE PYME DATA ANALYTICS ===")
        print(f"Transacciones analizadas: {len(transactions)} registros de venta.")
        abc = ABCAnalyzer.classify_inventory(transactions)
        top_rev = sum(i.ingresos_totales for i in abc if i.categoria_abc == "A")
        total_rev = sum(i.ingresos_totales for i in abc)
        print(f"Ingresos Totales: ${total_rev:,.2f} MXN (Categoría A concentra el {(top_rev/total_rev)*100:.1f}%)")
        print("Ejecuta 'pyme-analytics rfm', 'abc', 'basket' o 'rop' para detalles de cada módulo.")


if __name__ == "__main__":
    main()
