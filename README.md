# 📊 PyME Data Analytics: Transactional Data Science & Inventory Optimization

<p align="left">
  <strong>Data Science Engine for Mexican SMEs: RFM Segmentation, ABC Pareto Inventory & Market Basket Analysis</strong><br>
  Designed and engineered by <a href="https://github.com/iamhuitron"><strong>Miguel Delgado Huitrón</strong></a> (<code>@iamhuitron</code>) · Informatics, UNAM
</p>

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Data_Science-RFM_%2F_Pareto_%2F_Apriori-0284C7?style=flat-square" alt="Data Science" />
  <img src="https://img.shields.io/badge/Tests-Pytest_Passing-success?style=flat-square&logo=pytest&logoColor=white" alt="Pytest" />
  <img src="https://img.shields.io/badge/Domain-Retail_%2F_PyME_FinTech-059669?style=flat-square" alt="Domain" />
  <img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" alt="MIT" />
</p>

---

## 📌 Problem & Business Value

In Mexico, traditional small and medium enterprises (PyMEs, auto-part refaccionarias, hardware stores, retail counters) record hundreds of daily sales tickets but fail to extract actionable business intelligence:
1. **Capital Trapped in Dead Stock:** Stores frequently stock out of high-velocity revenue drivers while tying up operating cash flow in slow-moving items (the long tail).
2. **Generic Customer Treatment:** High-volume repeat wholesale mechanics and fleet owners receive the exact same treatment and communications as infrequent, single-ticket buyers.
3. **Missed Cross-Selling Revenue:** Cashiers miss cross-selling complementary products (e.g., selling synthetic engine oil without pairing the matching oil filter).

**PyME Data Analytics** serves as the analytical intelligence layer complementing [`pyme-manager-core`](https://github.com/Xaol-Studio/pyme-manager-core). It ingests transactional sales logs and applies deterministic statistical models to optimize working capital and customer retention.

---

## 🏗️ Analytics Architecture & Modules

```
┌────────────────────────────────────────────────────────┐
│               POS Sales & Transaction Logs             │
│        (Tickets, SKUs, Customer IDs, Quantities)       │
└───────────────────────────┬────────────────────────────┘
                            │
               Data Normalization & Cleaning
                            │
┌───────────────────────────▼────────────────────────────┐
│                  Core Analytics Engine                 │
│                                                        │
│  ├── 1. RFM Customer Segmentation                      │
│  │      Quintile scoring & Cohort identification       │
│  │                                                     │
│  ├── 2. ABC Inventory Pareto Classification            │
│  │      80/20 Revenue concentration curve              │
│  │                                                     │
│  ├── 3. Market Basket Association Mining               │
│  │      Support, Confidence & Lift calculation         │
│  │                                                     │
│  └── 4. Stock-out Risk & Reorder Point (ROP)           │
│         Daily sales velocity & Days of Inventory (DOI) │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│           Actionable Decision Dashboards & CLI         │
│  ├── Procurement purchase orders                       │
│  ├── Automated cross-sell bundle recommendations       │
│  └── Retention campaigns for 'At Risk' clients         │
└────────────────────────────────────────────────────────┘
```

---

## 🧮 Mathematical Formulations

### 1. Market Basket Association Rules
- **Support:**
$$\text{Support}(A \cap B) = \frac{\text{Total Tickets containing both } A \text{ and } B}{\text{Total Tickets}}$$

- **Confidence:**
$$\text{Confidence}(A \to B) = \frac{\text{Support}(A \cap B)}{\text{Support}(A)}$$

- **Lift (Strength of Association):**
$$\text{Lift}(A \to B) = \frac{\text{Confidence}(A \to B)}{\text{Support}(B)}$$
*A $\text{Lift} > 1.0$ indicates that purchasing item $A$ significantly increases the likelihood of purchasing item $B$.*

### 2. Reorder Point (ROP) & Safety Stock
$$\text{ROP} = (\bar{d} \times L) + SS$$
$$\text{DOI} = \frac{\text{Current Stock}}{\bar{d}}$$
Where $\bar{d}$ is average daily sales demand, $L$ is vendor lead time in days, and $SS$ is safety stock.

---

## 🚀 Quick Start & CLI Usage

### 1. Installation

```bash
git clone https://github.com/iamhuitron/pyme-data-analytics.git
cd pyme-data-analytics

python3 -m venv .venv
source .venv/bin/activate

pip install -e .[dev]
```

### 2. Customer RFM Segmentation

```bash
python3 -m pyme_analytics.cli rfm
```

Output:
```text
================== SEGMENTACIÓN RFM DE CLIENTES ==================
Cliente ID             | R  F  M  | Gasto Total  | Segmento
-----------------------------------------------------------------
CLI-FLOTILLA-RAPIDA    | 1  4  4  | $ 7,020.00 | En Riesgo
CLI-MECANICA-LOPEZ     | 2  4  5  | $ 8,050.00 | En Riesgo
CLI-TAXIS-UNIDOS       | 3  1  2  | $ 6,440.00 | Potenciales a Fidelizar
CLI-MOSTRADOR-01       | 4  1  1  | $   765.00 | Nuevos Prometedores
CLI-TALLER-PEREZ       | 5  1  2  | $ 6,440.00 | Nuevos Prometedores
==================================================================
```

### 3. ABC Pareto Inventory Classification

```bash
python3 -m pyme_analytics.cli abc
```

Output:
```text
================= CLASIFICACIÓN DE INVENTARIO ABC =================
Categoría  | SKU                | Ventas ($)   | % Acumulado
-----------------------------------------------------------------
[A]        | SKU-ACEITE-5W30    | $23,120.00 |  62.2%
[B]        | SKU-BALATAS-DEL    | $ 7,020.00 |  81.1%
[C]        | SKU-FILTRO-ACEITE  | $ 5,500.00 |  95.9%
[C]        | SKU-FOCO-H4        | $   765.00 |  98.0%
[C]        | SKU-LIMPIADOR-CARB | $   760.00 | 100.0%
==================================================================
```

### 4. Cross-Selling Association Rules (Market Basket)

```bash
python3 -m pyme_analytics.cli basket
```

Output:
```text
================= REGLAS DE ASOCIACIÓN (CROSS-SELL) =================
Si compra (Antecedente) -> También compra       | Confianza | Lift
---------------------------------------------------------------------------
SKU-ACEITE-5W30      -> SKU-FILTRO-ACEITE    |   100.0% |  1.59x
SKU-FILTRO-ACEITE    -> SKU-ACEITE-5W30      |    77.3% |  1.59x
=====================================================================
```

### 5. Stock-out Risk & Reorder Point (ROP)

```bash
python3 -m pyme_analytics.cli rop
```

---

## 🐍 Python SDK Integration

```python
from pyme_analytics import RFMAnalyzer, ABCAnalyzer, MarketBasketAnalyzer
from pyme_analytics.samples import get_sample_retail_transactions

transactions = get_sample_retail_transactions()

# 1. Segment customers
segments = RFMAnalyzer.analyze_customers(transactions)
for s in segments[:3]:
    print(f"Cliente {s.cliente_id}: {s.segment_label}")

# 2. Classify inventory
abc_items = ABCAnalyzer.classify_inventory(transactions)
category_a = [i.sku for i in abc_items if i.categoria_abc == "A"]
print("Top Revenue SKUs (A):", category_a)

# 3. Discover cross-selling bundles
rules = MarketBasketAnalyzer.find_rules(transactions, min_confidence=0.5)
for r in rules:
    print(f"Bundle: {r.antecedente} + {r.consecuente} (Lift: {r.lift}x)")
```

---

## 🧪 Automated Testing

Execute automated unit tests across all 4 modules:

```bash
pytest --verbose
```

```text
tests/test_analytics.py::test_rfm_segmentation PASSED
tests/test_analytics.py::test_abc_pareto PASSED
tests/test_analytics.py::test_market_basket_association PASSED
tests/test_analytics.py::test_inventory_rop_and_doi PASSED

============================== 4 passed in 0.24s ===============================
```

---

## 📄 License

This project is licensed under the **MIT License**. Created by [Miguel Delgado Huitrón](https://github.com/iamhuitron).
