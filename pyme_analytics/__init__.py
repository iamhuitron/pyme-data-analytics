"""
PyME Data Analytics: Retail Data Science & Inventory Intelligence for Mexican SMEs.
"""

__version__ = "1.0.0"
__author__ = "Miguel Delgado Huitron (@iamhuitron)"

from .models import TransactionRecord, CustomerSegment, ABCItemClassification, AssociationRule
from .rfm import RFMAnalyzer
from .abc import ABCAnalyzer
from .basket import MarketBasketAnalyzer
from .inventory import InventoryOptimizer
from .samples import get_sample_retail_transactions, get_sample_inventory_stocks

__all__ = [
    "TransactionRecord",
    "CustomerSegment",
    "ABCItemClassification",
    "AssociationRule",
    "RFMAnalyzer",
    "ABCAnalyzer",
    "MarketBasketAnalyzer",
    "InventoryOptimizer",
    "get_sample_retail_transactions",
    "get_sample_inventory_stocks",
]
