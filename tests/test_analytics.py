import pytest
from pyme_analytics.samples import get_sample_retail_transactions, get_sample_inventory_stocks
from pyme_analytics.rfm import RFMAnalyzer
from pyme_analytics.abc import ABCAnalyzer
from pyme_analytics.basket import MarketBasketAnalyzer
from pyme_analytics.inventory import InventoryOptimizer

@pytest.fixture
def sample_data():
    transactions = get_sample_retail_transactions()
    stocks = get_sample_inventory_stocks()
    return transactions, stocks

def test_rfm_segmentation(sample_data):
    transactions, _ = sample_data
    segments = RFMAnalyzer.analyze_customers(transactions)
    
    assert len(segments) > 0
    first = segments[0]
    assert first.cliente_id.startswith("CLI-")
    assert 1 <= first.r_score <= 5
    assert 1 <= first.f_score <= 5
    assert 1 <= first.m_score <= 5
    assert len(first.segment_label) > 0

def test_abc_pareto(sample_data):
    transactions, _ = sample_data
    abc = ABCAnalyzer.classify_inventory(transactions)
    
    assert len(abc) > 0
    # Must be sorted descending by revenue
    assert abc[0].ingresos_totales >= abc[-1].ingresos_totales
    # Must contain category A
    categories = {i.categoria_abc for i in abc}
    assert "A" in categories

def test_market_basket_association(sample_data):
    transactions, _ = sample_data
    rules = MarketBasketAnalyzer.find_rules(transactions, min_support=0.05, min_confidence=0.10)
    
    assert len(rules) > 0
    top_rule = rules[0]
    assert top_rule.antecedente != top_rule.consecuente
    assert 0 < top_rule.confidence <= 1.0
    assert top_rule.lift > 0

def test_inventory_rop_and_doi(sample_data):
    transactions, stocks = sample_data
    reorder = InventoryOptimizer.calculate_reorder_points(transactions, stocks)
    
    assert len(reorder) > 0
    for r in reorder:
        assert r["velocidad_diaria"] >= 0
        assert r["punto_reorden_rop"] >= 0
        assert r["dias_inventario_doi"] >= 0
        assert r["estado_alerta"] in [
            "CRÍTICO (Riesgo de Desabasto)",
            "REORDENAR AHORA",
            "NIVEL SALUDABLE",
            "SOBRE-INVENTARIO"
        ]
