"""
Question 4: Optimal Manufacturer Selling Price
===============================================
Determine the optimal selling price of the manufacturer for an average week.

Uses the semi-log demand models estimated in Q2 (from the Excel workbook)
and finds the manufacturer unit price that maximizes weekly profit under
two scenarios:

  4(a) Private label retail price is fixed at the historical average.
  4(b) Private label retail price is always $0.35 below Brand 1 retail price.

Assumptions:
  - The retailer maintains its historical average margin % on Brand 1.
  - Manufacturing cost per case is the average from the data.
  - Selling cost is $10.00 per case ($0.4167 per unit).
  - 24 units per case.
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
from process_data import DataProcessor

# =============================================================================
# Constants
# =============================================================================
UNITS_PER_CASE = 24
SELLING_COST_PER_CASE = 10.00
SELLING_COST_PER_UNIT = SELLING_COST_PER_CASE / UNITS_PER_CASE

# ---------------------------------------------------------------------------
# Regression coefficients from the Excel workbook (Sheet "2")
# These match the semi-log models estimated in Q2.
#
# Private Label model:  ln(PL Units) = 8.6907 - 0.7472*PL_Price + 0.5098*B1_Price
# Brand 1 model:        ln(B1 Units) = 12.2993 + 0.6426*PL_Price - 2.1551*B1_Price
# ---------------------------------------------------------------------------
PL_INTERCEPT = 8.690723702745355
PL_COEF_PL_PRICE = -0.7472414515333461
PL_COEF_B1_PRICE = 0.5098153554308285

B1_INTERCEPT = 12.29929203058571
B1_COEF_PL_PRICE = 0.6425820392535629
B1_COEF_B1_PRICE = -2.155144775871096


# =============================================================================
# Data Loading — pull averages from the dataset
# =============================================================================

def load_averages():
    """Load data and compute the averages needed for the optimization."""
    processor = DataProcessor('bana6390_u2_assignment.xlsx')
    df = processor.get_dataframe()

    avg = {
        'pl_retail_price': df['PrivateLabel_Retail_Price'].mean(),
        'b1_retail_price': df['Brand1_Retail_Price'].mean(),
        'pl_unit_cost': df['PrivateLabel_Unit_Cost'].mean(),     # retailer's PL cost
        'b1_margin_pct': df['Brand1_Margin_Pct'].mean() / 100,  # retailer's Brand 1 margin goal
        'b1_mfg_cost_per_unit': df['Brand1_Mfg_Cost_Per_Unit'].mean(),
    }

    return avg


# =============================================================================
# Demand prediction from the semi-log model
# =============================================================================

def predict_brand1_units(b1_retail_price, pl_retail_price):
    """Predict Brand 1 weekly unit sales."""
    ln_units = B1_INTERCEPT + B1_COEF_B1_PRICE * b1_retail_price + B1_COEF_PL_PRICE * pl_retail_price
    return np.exp(ln_units)


def predict_pl_units(b1_retail_price, pl_retail_price):
    """Predict Private Label weekly unit sales."""
    ln_units = PL_INTERCEPT + PL_COEF_B1_PRICE * b1_retail_price + PL_COEF_PL_PRICE * pl_retail_price
    return np.exp(ln_units)


# =============================================================================
# Manufacturer profit function
# =============================================================================

def manufacturer_weekly_profit(mfg_price_per_unit, b1_retail_price, pl_retail_price, mfg_cost_per_unit):
    """
    Calculate manufacturer weekly profit.

    Profit per unit = mfg_price - mfg_cost - selling_cost
    Total profit    = profit_per_unit × predicted Brand 1 units
    """
    profit_per_unit = mfg_price_per_unit - mfg_cost_per_unit - SELLING_COST_PER_UNIT
    units = predict_brand1_units(b1_retail_price, pl_retail_price)
    return profit_per_unit * units


# =============================================================================
# Scenario 4(a): PL retail price fixed at historical average
# =============================================================================

def optimize_scenario_a(avg):
    """
    Find the optimal manufacturer unit price when the private label
    retail price is fixed at its historical average.

    The retailer sets Brand 1 retail price to maintain its margin goal:
        retail_price = mfg_price / (1 - margin_pct)
    """
    margin_pct = avg['b1_margin_pct']
    avg_pl_price = avg['pl_retail_price']
    mfg_cost = avg['b1_mfg_cost_per_unit']

    def neg_profit(mfg_price):
        b1_retail = mfg_price / (1.0 - margin_pct)
        return -manufacturer_weekly_profit(mfg_price, b1_retail, avg_pl_price, mfg_cost)

    result = minimize_scalar(neg_profit, bounds=(0.50, 5.00), method='bounded')
    return result.x, -result.fun


# =============================================================================
# Scenario 4(b): PL price = Brand 1 retail price − $0.35
# =============================================================================

def optimize_scenario_b(avg):
    """
    Find the optimal manufacturer unit price when the private label
    retail price is always $0.35 below the Brand 1 retail price.

    retail_price  = mfg_price / (1 - margin_pct)
    pl_retail     = retail_price - 0.35
    """
    margin_pct = avg['b1_margin_pct']
    mfg_cost = avg['b1_mfg_cost_per_unit']

    def neg_profit(mfg_price):
        b1_retail = mfg_price / (1.0 - margin_pct)
        pl_retail = b1_retail - 0.35
        return -manufacturer_weekly_profit(mfg_price, b1_retail, pl_retail, mfg_cost)

    result = minimize_scalar(neg_profit, bounds=(0.50, 5.00), method='bounded')
    return result.x, -result.fun


# =============================================================================
# Main
# =============================================================================

def main():
    # Load historical averages
    avg = load_averages()

    print("=" * 80)
    print("QUESTION 4: OPTIMAL MANUFACTURER SELLING PRICE")
    print("=" * 80)

    print("\n--- Assumptions ---")
    print(f"  Retailer margin goal (Brand 1 avg):  {avg['b1_margin_pct']*100:.2f}%")
    print(f"  Average PL retail price:             ${avg['pl_retail_price']:.4f}")
    print(f"  Average PL cost to retailer (unit):  ${avg['pl_unit_cost']:.4f}")
    print(f"  Brand 1 mfg cost per unit:           ${avg['b1_mfg_cost_per_unit']:.4f}")
    print(f"  Selling cost per unit:               ${SELLING_COST_PER_UNIT:.4f}")

    print("\n--- Demand Model Coefficients (from Q2 Excel) ---")
    print(f"  Brand 1:  ln(Units) = {B1_INTERCEPT:.4f}"
          f" + ({B1_COEF_B1_PRICE:.4f}) × B1_Price"
          f" + ({B1_COEF_PL_PRICE:.4f}) × PL_Price")
    print(f"  PL:       ln(Units) = {PL_INTERCEPT:.4f}"
          f" + ({PL_COEF_PL_PRICE:.4f}) × PL_Price"
          f" + ({PL_COEF_B1_PRICE:.4f}) × B1_Price")

    # --- Scenario 4(a) -------------------------------------------------------
    opt_price_a, opt_profit_a = optimize_scenario_a(avg)
    b1_retail_a = opt_price_a / (1.0 - avg['b1_margin_pct'])

    print("\n" + "=" * 80)
    print("SCENARIO 4(a): PL retail price fixed at historical average")
    print("=" * 80)
    print(f"  Optimal mfg price per unit:      ${opt_price_a:.4f}")
    print(f"  Implied Brand 1 retail price:    ${b1_retail_a:.4f}")
    print(f"  PL retail price (fixed):         ${avg['pl_retail_price']:.4f}")
    print(f"  Max manufacturer weekly profit:  ${opt_profit_a:,.2f}")

    # --- Scenario 4(b) -------------------------------------------------------
    opt_price_b, opt_profit_b = optimize_scenario_b(avg)
    b1_retail_b = opt_price_b / (1.0 - avg['b1_margin_pct'])
    pl_retail_b = b1_retail_b - 0.35

    print("\n" + "=" * 80)
    print("SCENARIO 4(b): PL retail price = Brand 1 retail price − $0.35")
    print("=" * 80)
    print(f"  Optimal mfg price per unit:      ${opt_price_b:.4f}")
    print(f"  Implied Brand 1 retail price:    ${b1_retail_b:.4f}")
    print(f"  Implied PL retail price:         ${pl_retail_b:.4f}")
    print(f"  Max manufacturer weekly profit:  ${opt_profit_b:,.2f}")

    # --- Comparison -----------------------------------------------------------
    current_mfg_price = avg['b1_retail_price'] * (1.0 - avg['b1_margin_pct'])
    current_profit = manufacturer_weekly_profit(
        current_mfg_price, avg['b1_retail_price'], avg['pl_retail_price'],
        avg['b1_mfg_cost_per_unit']
    )

    print("\n" + "=" * 80)
    print("COMPARISON WITH CURRENT SITUATION")
    print("=" * 80)
    print(f"  Current avg mfg price per unit:  ${current_mfg_price:.4f}")
    print(f"  Current avg mfg weekly profit:   ${current_profit:,.2f}")
    print(f"  Scenario 4(a) improvement:       ${opt_profit_a - current_profit:+,.2f} "
          f"({(opt_profit_a/current_profit - 1)*100:+.1f}%)")
    print(f"  Scenario 4(b) improvement:       ${opt_profit_b - current_profit:+,.2f} "
          f"({(opt_profit_b/current_profit - 1)*100:+.1f}%)")
    print("=" * 80)

    return {
        'scenario_a': {'mfg_price': opt_price_a, 'retail_price': b1_retail_a, 'profit': opt_profit_a},
        'scenario_b': {'mfg_price': opt_price_b, 'retail_price': b1_retail_b, 'profit': opt_profit_b},
    }


if __name__ == "__main__":
    results = main()
