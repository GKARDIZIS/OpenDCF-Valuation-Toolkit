import pandas as pd
import numpy as np

class OpenDCF:
    def __init__(self, ticker, risk_free_rate, market_return, beta, tax_rate):
        """
        Initialize the DCF model with market parameters.
        Designed for quick Transaction Services screening.
        """
        self.ticker = ticker
        self.risk_free_rate = risk_free_rate
        self.market_return = market_return
        self.beta = beta
        self.tax_rate = tax_rate
        
    def calculate_wacc(self, cost_of_debt, equity_weight, debt_weight):
        """Calculate Weighted Average Cost of Capital (WACC)"""
        cost_of_equity = self.risk_free_rate + self.beta * (self.market_return - self.risk_free_rate)
        after_tax_cost_of_debt = cost_of_debt * (1 - self.tax_rate)
        
        wacc = (equity_weight * cost_of_equity) + (debt_weight * after_tax_cost_of_debt)
        return wacc

    def calculate_enterprise_value(self, fcf_projections, wacc, terminal_growth_rate):
        """Calculate Present Value of FCFs and Terminal Value"""
        discount_factors = [(1 + wacc) ** i for i in range(1, len(fcf_projections) + 1)]
        pv_fcf = sum([fcf / df for fcf, df in zip(fcf_projections, discount_factors)])
        
        # Terminal Value calculation using Gordon Growth Model
        terminal_value = (fcf_projections[-1] * (1 + terminal_growth_rate)) / (wacc - terminal_growth_rate)
        pv_terminal_value = terminal_value / ((1 + wacc) ** len(fcf_projections))
        
        enterprise_value = pv_fcf + pv_terminal_value
        return enterprise_value, pv_fcf, pv_terminal_value

if __name__ == "__main__":
    # Example Valuation Run
    print("--- OpenDCF Valuation Initialized ---")
    
    # Market Inputs
    model = OpenDCF(ticker="DEMO", risk_free_rate=0.04, market_return=0.10, beta=1.2, tax_rate=0.22)
    
    # Capital Structure & Debt Cost
    wacc = model.calculate_wacc(cost_of_debt=0.05, equity_weight=0.7, debt_weight=0.3)
    
    # Projected Unlevered Free Cash Flows for next 5 years (in millions)
    projected_fcf = [150, 165, 182, 195, 210]
    
    ev, pv_fcf, pv_tv = model.calculate_enterprise_value(fcf_projections=projected_fcf, wacc=wacc, terminal_growth_rate=0.02)
    
    print(f"Calculated WACC: {wacc:.2%}")
    print(f"PV of Free Cash Flows: ${pv_fcf:.2f}M")
    print(f"PV of Terminal Value: ${pv_tv:.2f}M")
    print(f"Implied Enterprise Value: ${ev:.2f}M")
