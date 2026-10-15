"""
Market Basket Analysis & Association Rules Mining Engine (Apriori-style).
Calculates Support, Confidence, and Lift for cross-selling opportunities.
"""

from typing import List, Dict, Set, Tuple
from collections import defaultdict
from itertools import combinations
from .models import TransactionRecord, AssociationRule


class MarketBasketAnalyzer:
    @staticmethod
    def find_rules(
        transactions: List[TransactionRecord],
        min_support: float = 0.05,
        min_confidence: float = 0.20
    ) -> List[AssociationRule]:
        if not transactions:
            return []

        # Group items by ticket
        baskets: Dict[str, Set[str]] = defaultdict(set)
        for t in transactions:
            baskets[t.ticket_id].add(t.sku)

        total_baskets = len(baskets)
        if total_baskets == 0:
            return []

        # Single item frequencies
        item_counts: Dict[str, int] = defaultdict(int)
        # Pairwise frequencies
        pair_counts: Dict[Tuple[str, str], int] = defaultdict(int)

        for basket in baskets.values():
            for item in basket:
                item_counts[item] += 1
            for a, b in combinations(sorted(basket), 2):
                pair_counts[(a, b)] += 1

        rules: List[AssociationRule] = []

        for (a, b), count in pair_counts.items():
            support_ab = count / total_baskets
            if support_ab < min_support:
                continue

            support_a = item_counts[a] / total_baskets
            support_b = item_counts[b] / total_baskets

            # Rule A -> B
            conf_a_b = support_ab / support_a if support_a > 0 else 0
            lift_a_b = conf_a_b / support_b if support_b > 0 else 0
            if conf_a_b >= min_confidence:
                rules.append(AssociationRule(
                    antecedente=a,
                    consecuente=b,
                    support=round(support_ab, 4),
                    confidence=round(conf_a_b, 4),
                    lift=round(lift_a_b, 4)
                ))

            # Rule B -> A
            conf_b_a = support_ab / support_b if support_b > 0 else 0
            lift_b_a = conf_b_a / support_a if support_a > 0 else 0
            if conf_b_a >= min_confidence:
                rules.append(AssociationRule(
                    antecedente=b,
                    consecuente=a,
                    support=round(support_ab, 4),
                    confidence=round(conf_b_a, 4),
                    lift=round(lift_b_a, 4)
                ))

        # Sort by Lift descending
        rules.sort(key=lambda r: r.lift, reverse=True)
        return rules
