"""
Question 5: Implied Values at Optimal Prices
==============================================
Compute the "implied" values of different variables at the optimal prices
from each of scenarios 4(a) and 4(b), and compare them with the current
situation (from Q1).

The assignment asks us to fill in a table for a typical week showing:
  - Brand 1 and PL unit sales
  - Market shares of both brands
  - Weekly retailer profit (on both brands combined)
  - Weekly manufacturer profit (Brand 1 only)

We also identify one concern about the reasonableness of each scenario's
assumption regarding the retailer's private label pricing behavior.

This script reuses the demand model coefficients and data pipeline from
q4_optimal_price.py, re-running the optimization to get the exact
optimal prices, then computing all implied downstream metrics.
"""

import numpy as np
from process_data import DataProcessor

# =============================================================================
# Import shared constants and model coefficients from Q4
# =============================================================================
from q4_optimal_price import (
    UNITS_PER_CASE,
    SELLING_COST_PER_UNIT,
    # Model coefficients (from Q2 Excel regression)
    B1_INTERCEPT, B1_COEF_B1_PRICE, B1_COEF_PL_PRICE,
    PL_INTERCEPT, PL_COEF_PL_PRICE, PL_COEF_B1_PRICE,
    # Functions
    predict_brand1_units,
    predict_pl_units,
    load_averages,
    optimize_scenario_a,
    optimize_scenario_b,
)


# =============================================================================
# Compute implied values for a given scenario
# =============================================================================

def compute_implied_values(mfg_price, b1_retail, pl_retail, avg_pl_cost, mfg_cost):
    """
    Given the optimal manufacturer price and the resulting retail prices,
    compute all the downstream "implied" values for a typical week.

    Parameters
    ----------
    mfg_price : float
        Manufacturer's selling price per unit to the retailer.
    b1_retail : float
        Brand 1 retail price per unit (set by retailer via margin norm).
    pl_retail : float
        Private label retail price per unit (depends on scenario).
    avg_pl_cost : float
        Retailer's average cost per unit for the private label.
    mfg_cost : float
        Manufacturer's average production cost per unit for Brand 1.

    Returns
    -------
    dict
        Dictionary with all implied metrics.
    """
    # --- Predicted unit sales from semi-log demand models ---
    b1_units = predict_brand1_units(b1_retail, pl_retail)
    pl_units = predict_pl_units(b1_retail, pl_retail)
    total_units = b1_units + pl_units

    # --- Market shares ---
    b1_share = (b1_units / total_units) * 100
    pl_share = (pl_units / total_units) * 100

    # --- Retailer profit ---
    # Brand 1: retailer buys at mfg_price, sells at b1_retail
    retailer_profit_b1 = (b1_retail - mfg_price) * b1_units
    # Private label: retailer buys at avg_pl_cost, sells at pl_retail
    retailer_profit_pl = (pl_retail - avg_pl_cost) * pl_units
    retailer_total_profit = retailer_profit_b1 + retailer_profit_pl

    # --- Manufacturer profit (Brand 1 only) ---
    mfg_profit_per_unit = mfg_price - mfg_cost - SELLING_COST_PER_UNIT
    manufacturer_profit = mfg_profit_per_unit * b1_units

    return {
        'mfg_price': mfg_price,
        'b1_retail': b1_retail,
        'pl_retail': pl_retail,
        'b1_units': b1_units,
        'pl_units': pl_units,
        'b1_share': b1_share,
        'pl_share': pl_share,
        'retailer_profit': retailer_total_profit,
        'manufacturer_profit': manufacturer_profit,
    }


# =============================================================================
# Compute current-situation values (reproduces Q1 answers)
# =============================================================================

def compute_current_situation():
    """
    Compute the "current" column of the comparison table by averaging
    across all 104 weeks of historical data.  These reproduce the Q1
    answers for parts (d), (e), and (f).
    """
    processor = DataProcessor('bana6390_u2_assignment.xlsx')
    df = processor.get_dataframe()

    # Average weekly unit sales
    b1_units = df['Brand1_Units_Sold'].mean()
    pl_units = df['PrivateLabel_Units_Sold'].mean()

    # Average weekly market shares
    b1_share = df['Brand1_Share'].mean()
    pl_share = df['PrivateLabel_Share'].mean()

    # Average weekly retailer profit (both brands combined)
    retailer_profit = df['Retailer_Total_Profit'].mean()

    # Average weekly manufacturer profit (Brand 1 only)
    manufacturer_profit = df['Brand1_Mfg_Profit'].mean()

    return {
        'b1_units': b1_units,
        'pl_units': pl_units,
        'b1_share': b1_share,
        'pl_share': pl_share,
        'retailer_profit': retailer_profit,
        'manufacturer_profit': manufacturer_profit,
    }


# =============================================================================
# Formatted comparison table
# =============================================================================

def print_comparison_table(implied_a, implied_b, current):
    """
    Print the Q5 comparison table matching the assignment format:
    columns for Scenario 4(a), Scenario 4(b), and the Current situation.
    """
    # Column widths
    W_LABEL = 40
    W_COL = 16

    header = (f"{'':>{W_LABEL}} | {'Scenario 4(a)':>{W_COL}} | "
              f"{'Scenario 4(b)':>{W_COL}} | {'Current (Q1)':>{W_COL}}")
    separator = "-" * W_LABEL + "-+-" + "-" * W_COL + "-+-" + "-" * W_COL + "-+-" + "-" * W_COL

    print(header)
    print(separator)

    # --- Prices ---
    print(f"{'Mfg price per unit':>{W_LABEL}} | "
          f"{'${:.4f}'.format(implied_a['mfg_price']):>{W_COL}} | "
          f"{'${:.4f}'.format(implied_b['mfg_price']):>{W_COL}} | "
          f"{'N/A':>{W_COL}}")
    print(f"{'Brand 1 retail price':>{W_LABEL}} | "
          f"{'${:.4f}'.format(implied_a['b1_retail']):>{W_COL}} | "
          f"{'${:.4f}'.format(implied_b['b1_retail']):>{W_COL}} | "
          f"{'N/A':>{W_COL}}")
    print(f"{'PL retail price':>{W_LABEL}} | "
          f"{'${:.4f}'.format(implied_a['pl_retail']):>{W_COL}} | "
          f"{'${:.4f}'.format(implied_b['pl_retail']):>{W_COL}} | "
          f"{'N/A':>{W_COL}}")

    print(separator)

    # --- Unit sales ---
    print(f"{'Brand 1 weekly units':>{W_LABEL}} | "
          f"{implied_a['b1_units']:>{W_COL},.0f} | "
          f"{implied_b['b1_units']:>{W_COL},.0f} | "
          f"{current['b1_units']:>{W_COL},.0f}")
    print(f"{'Private Label weekly units':>{W_LABEL}} | "
          f"{implied_a['pl_units']:>{W_COL},.0f} | "
          f"{implied_b['pl_units']:>{W_COL},.0f} | "
          f"{current['pl_units']:>{W_COL},.0f}")

    print(separator)

    # --- Market shares ---
    print(f"{'Brand 1 share':>{W_LABEL}} | "
          f"{implied_a['b1_share']:>{W_COL}.2f}% | "
          f"{implied_b['b1_share']:>{W_COL}.2f}% | "
          f"{current['b1_share']:>{W_COL}.2f}%")
    print(f"{'Private Label share':>{W_LABEL}} | "
          f"{implied_a['pl_share']:>{W_COL}.2f}% | "
          f"{implied_b['pl_share']:>{W_COL}.2f}% | "
          f"{current['pl_share']:>{W_COL}.2f}%")

    print(separator)

    # --- Profits ---
    print(f"{'Retailer weekly profit':>{W_LABEL}} | "
          f"{'${:,.2f}'.format(implied_a['retailer_profit']):>{W_COL}} | "
          f"{'${:,.2f}'.format(implied_b['retailer_profit']):>{W_COL}} | "
          f"{'${:,.2f}'.format(current['retailer_profit']):>{W_COL}}")
    print(f"{'Manufacturer weekly profit':>{W_LABEL}} | "
          f"{'${:,.2f}'.format(implied_a['manufacturer_profit']):>{W_COL}} | "
          f"{'${:,.2f}'.format(implied_b['manufacturer_profit']):>{W_COL}} | "
          f"{'${:,.2f}'.format(current['manufacturer_profit']):>{W_COL}}")

    print(separator)


# =============================================================================
# Concerns about scenario assumptions
# =============================================================================

def print_concerns():
    """
    Identify one concern for each scenario about the reasonableness of
    the assumption regarding the retailer's private label pricing.
    """
    print("""
CONCERN — Scenario 4(a): PL price fixed at historical average
  The assumption that the private label price remains unchanged is unrealistic
  if Brand 1's retail price moves significantly. In practice, the retailer's
  category manager would likely adjust the PL price in response — for example,
  lowering it to protect PL volume if Brand 1 becomes more competitively
  priced.  Holding PL price fixed therefore overstates the demand shift
  toward Brand 1 and may overestimate the manufacturer's profit gain.

CONCERN — Scenario 4(b): PL price always $0.35 below Brand 1
  A rigid price gap constrains the retailer's flexibility. If the
  manufacturer lowers its price substantially, the implied PL retail price
  could fall below the retailer's cost for the private label, making the PL
  unprofitable.  The retailer would not allow this, so the fixed-gap rule
  breaks down at extreme prices.  The model could therefore recommend a
  manufacturer price that is infeasible in practice.""")


# =============================================================================
# Main
# =============================================================================

def main():
    # ------------------------------------------------------------------
    # Step 1: Load data averages (shared with Q4)
    # ------------------------------------------------------------------
    avg = load_averages()

    # ------------------------------------------------------------------
    # Step 2: Re-run Q4 optimization to get optimal prices
    # ------------------------------------------------------------------
    opt_price_a, opt_profit_a = optimize_scenario_a(avg)
    opt_price_b, opt_profit_b = optimize_scenario_b(avg)

    # Implied retail prices from the margin relationship
    margin_pct = avg['b1_margin_pct']
    b1_retail_a = opt_price_a / (1.0 - margin_pct)
    b1_retail_b = opt_price_b / (1.0 - margin_pct)
    pl_retail_a = avg['pl_retail_price']           # fixed in scenario (a)
    pl_retail_b = b1_retail_b - 0.35               # linked in scenario (b)

    # ------------------------------------------------------------------
    # Step 3: Compute implied values at the optimal prices
    # ------------------------------------------------------------------
    implied_a = compute_implied_values(
        opt_price_a, b1_retail_a, pl_retail_a,
        avg['pl_unit_cost'], avg['b1_mfg_cost_per_unit'],
    )
    implied_b = compute_implied_values(
        opt_price_b, b1_retail_b, pl_retail_b,
        avg['pl_unit_cost'], avg['b1_mfg_cost_per_unit'],
    )

    # ------------------------------------------------------------------
    # Step 4: Compute current-situation values (Q1 d, e, f)
    # ------------------------------------------------------------------
    current = compute_current_situation()

    # ------------------------------------------------------------------
    # Step 5: Print the comparison table
    # ------------------------------------------------------------------
    print("=" * 90)
    print("QUESTION 5: IMPLIED VALUES AT OPTIMAL PRICES")
    print("=" * 90)
    print()
    print_comparison_table(implied_a, implied_b, current)

    # ------------------------------------------------------------------
    # Step 6: Print concerns about scenario assumptions
    # ------------------------------------------------------------------
    print()
    print("=" * 90)
    print("CONCERNS ABOUT SCENARIO ASSUMPTIONS")
    print("=" * 90)
    print_concerns()
    print()
    print("=" * 90)

    return {
        'scenario_a': implied_a,
        'scenario_b': implied_b,
        'current': current,
    }


if __name__ == "__main__":
    results = main()
