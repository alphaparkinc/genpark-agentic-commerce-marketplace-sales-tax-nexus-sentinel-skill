# -*- coding: utf-8 -*-
"""Marketplace Sales Tax Economic Nexus Sentinel for GenPark Agentic Commerce."""
import json
from typing import Dict, Any, List

class MarketplaceSalesTaxEconomicNexusSentinel:
    @staticmethod
    def evaluate_state_economic_nexus_exposure(state_code: str, gross_sales_usd: float, transaction_count: int, marketplace_facilitator_sales_usd: float = 0.0) -> Dict[str, Any]:
        state = state_code.strip().upper()
        # Direct non-facilitator sales that seller is obligated to collect tax for
        direct_sales_usd = max(0.0, gross_sales_usd - marketplace_facilitator_sales_usd)
        
        # General Wayfair threshold: $100,000 OR 200 transactions
        threshold_usd = 100000.0
        threshold_tx = 200
        if state in ["CA", "TX", "NY"]:
            threshold_usd = 500000.0  # Higher threshold for large states
            threshold_tx = 999999
            
        dollar_nexus = gross_sales_usd >= threshold_usd
        tx_nexus = transaction_count >= threshold_tx
        nexus_established = dollar_nexus or tx_nexus
        
        return {
            "state": state,
            "gross_sales_usd": gross_sales_usd,
            "direct_seller_obligation_sales_usd": direct_sales_usd,
            "transaction_count": transaction_count,
            "economic_nexus_established": nexus_established,
            "threshold_breach_reason": "DOLLAR_THRESHOLD_EXCEEDED" if dollar_nexus else ("TRANSACTION_COUNT_EXCEEDED" if tx_nexus else "BELOW_NEXUS_THRESHOLD"),
            "action_required": "REGISTER_AND_COLLECT_SALES_TAX" if (nexus_established and direct_sales_usd > 0) else ("MARKETPLACE_FACILITATOR_RELIEF" if nexus_established else "NO_FILING_REQUIRED")
        }

    @staticmethod
    def generate_state_by_state_nexus_registration_roadmap(breached_states: List[str]) -> Dict[str, Any]:
        steps = []
        for st in breached_states:
            steps.append({
                "state": st,
                "portal": f"Department of Revenue / Taxation ({st})",
                "form": "SST (Streamlined Sales Tax) Registration",
                "recommended_effective_date": "Immediate next calendar month 1st"
            })
        return {
            "total_breached_states": len(breached_states),
            "registration_roadmap": steps,
            "compliance_notice": "Avoid back taxes and 10% late-filing statutory penalties by registering prior to subsequent nexus quarter."
        }
