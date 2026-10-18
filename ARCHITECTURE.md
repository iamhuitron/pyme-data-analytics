# 🏛️ PyME Data Analytics Architecture & Topology

Algorithmic business intelligence and decision-support library for Mexican small and medium enterprises (PyMEs). Delivers ABC inventory classification, RFM customer segmentation, market basket cross-selling analysis, and safety stock reorder forecasting. Built with Python 3.12, Pandas, Numpy, and Pydantic.

---

## 1. Technology Stack

| Layer | Technology | Details |
| :--- | :--- | :--- |
| **Runtime** | Python 3.12+ | Vectorized numerical computing and strict type contracts |
| **Data Engine** | `pandas` & `numpy` | High-performance tabular transformation and matrix operations |
| **Validation** | `pydantic` v2 | Transaction and product ledger schema validation |
| **Algorithms** | Scikit-learn / Custom | Apriori association rules, Pareto distribution, quantile scoring |
| **CLI & Export** | `rich` / `argparse` | Formatted terminal dashboards, markdown tables, and CSV exports |

---

## 2. System Topology & Component Graph

```mermaid
flowchart TD
    subgraph DataInputs["Input Transactions"]
        POS["POS / ERP Sales Logs (CSV / JSON)"]
        Catalog["Product & Inventory Catalog"]
    end

    subgraph AnalyticsEngine["pyme_analytics Core"]
        CLI["CLI Driver (pyme_analytics/cli.py)"]
        Models["Transaction Models (pyme_analytics/models.py)"]
        ABC["ABC Inventory Classifier (pyme_analytics/abc.py)"]
        RFM["RFM Customer Segmentation (pyme_analytics/rfm.py)"]
        Basket["Market Basket Analysis (pyme_analytics/basket.py)"]
        Inventory["Reorder Point & Safety Stock (pyme_analytics/inventory.py)"]
    end

    subgraph Outputs["Business Insights"]
        SegmentMatrix["Customer Cohorts & Churn Risk"]
        ParetoChart["High-Value SKU Strategy (Pareto 80/20)"]
        Bundles["Cross-Selling Bundles (Support / Confidence / Lift)"]
        PurchasePlan["Supplier Reorder Schedules"]
    end

    DataInputs --> CLI
    CLI --> Models
    Models --> ABC
    Models --> RFM
    Models --> Basket
    Models --> Inventory
    ABC --> ParetoChart
    RFM --> SegmentMatrix
    Basket --> Bundles
    Inventory --> PurchasePlan
```

---

## 3. Analytical Pipeline Lifecycle

```mermaid
sequenceDiagram
    autonumber
    actor Owner as Business Owner / Operator
    participant CLI as pyme-analytics CLI
    participant Engine as Analytics Module
    participant RFM as RFM Segmenter
    participant ABC as ABC Classifier
    participant Out as Formatted Dashboard

    Owner->>CLI: pyme-analytics run-all --sales-file data/sales.csv
    CLI->>Engine: Ingest transaction records
    Engine->>RFM: Compute Recency, Frequency, Monetary values per customer
    RFM->>RFM: Quantile quintiles (1-5), assign cohorts (Champions, At Risk, Lost)
    Engine->>ABC: Calculate cumulative revenue contribution per SKU
    ABC->>ABC: Partition into Class A (80%), B (15%), C (5%)
    Engine->>Out: Compile executive decision report
    Out-->>Owner: Render action items (reorder list, target campaigns)
```

---

## 4. Directory Structure & Module Breakdown

```
pyme-data-analytics/
├── pyme_analytics/           # Core analytics library
│   ├── abc.py                # Pareto 80/20 inventory analysis by volume & revenue
│   ├── rfm.py                # Recency, Frequency, Monetary segmentation engine
│   ├── basket.py             # Market basket cross-selling association rules (Apriori)
│   ├── inventory.py          # Safety stock, lead-time variance & reorder calculation
│   ├── models.py             # Pydantic data schemas for sales, items, customers
│   ├── samples.py            # Synthetic business data generator for simulations
│   └── cli.py                # Terminal command-line interface & summary reports
├── tests/                    # Algorithmic test suite
│   └── test_analytics.py     # Deterministic checks on ABC, RFM, and reorder points
├── pyproject.toml            # Packaging metadata
└── requirements.txt          # Python dependencies
```
