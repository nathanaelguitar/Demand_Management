"""
Question 5: Implied Values at Optimal Prices
=============================================
Compute the "implied" values of different variables at the optimal prices
in each of scenarios 4(a) and 4(b), and compare them with the current situation.

Fills in the comparison table and identifies concerns about each scenario's
assumptions regarding the retailer's pricing behavior.
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.optimize import minimize_scalar
from process_data import DataProcessor

# =============================================================================
# Constants
# =============================================================================
UNITS_PER_CASE = 24
SELLING_COST_PER_CASE = 10.00
SELLING_COST_PER_UNIT = SELLING_COST_PER_CASE / UNITS_PER_CASE


def load_data():
    """Load and process the pricing data."""
    processor = DataProcessor('bana6390_u2_assignment.xlsx')
    df = processor.get_dataframe()
    return df


def compute_current_situation(df):
    """
    Compute the current (historical average) situation from Q1 answers.
    Returns a dict with the values for the 'From Qs 1' column.
    """
    current = {
        'brand1_units': df['Brand1_Units_Sold'].mean(),
        'pl_units': df['PrivateLabel_Units_Sold'].mean(),
        'brand1_share': df['Brand1_Share'].mean(),
        'pl_share': df['PrivateLabel_Share'].mean(),
        'retailer_profit': df['Retailer_Total_Profit'].mean(),
        'manufacturer_profit': df['Brand1_Mfg_Profit'].mean(),
    }
    return current


def estimate_demand_models(df):
    """
    Estimate semi-log (exponential) demand models for Brand 1 and Private Label.
    
    Model form:  ln(Units) = b0 + b1 * Brand1_Price + b2 * PL_Price
    
    Returns:
        results_brand1: OLS results for Brand 1
        results_pl:     OLS results for Private Label
    """
    # Dependent variables (log of unit sales)
    ln_brand1 = np.log(df['Brand1_Units_Sold'])
    ln_pl = np.log(df['PrivateLabel_Units_Sold'])

    # Independent variables (both retail prices)
    X = df[['Brand1_Retail_Price', 'PrivateLabel_Retail_Price']].copy()
    X = sm.add_constant(X)

    # Brand 1 demand model
    model_brand1 = sm.OLS(ln_brand1, X).fit()

    # Private Label demand model
    model_pl = sm.OLS(ln_pl, X).fit()

    print("=" * 80)
    print("BRAND 1 DEMAND MODEL")
    print("=" * 80)
    print(model_brand1.summary())

    print("\n" + "=" * 80)
    print("PRIVATE LABEL DEMAND MODEL")
    print("=" * 80)
    print(model_pl.summary())

    return model_brand1, model_pl


def predict_units(model, brand1_price, pl_price):
    """Predict unit sales from a semi-log model given retail prices."""
    X = np.array([1.0, brand1_price, pl_price])
    ln_units = model.predict(X)[0]
    return np.exp(ln_units)


def compute_retailer_margin_goal(df):
    """
    Compute the retailer's average margin percentage for Brand 1.
    This serves as the retailer's margin-goal 'norm'.
    """
    avg_margin_pct_brand1 = df['Brand1_Margin_Pct'].mean() / 100.0
    return avg_margin_pct_brand1


def compute_avg_pl_cost(df):
    """Compute the average retailer cost per unit for the Private Label."""
    return df['PrivateLabel_Unit_Cost'].mean()


def compute_avg_pl_retail_price(df):
    """Compute the average Private Label retail price."""
    return df['PrivateLabel_Retail_Price'].mean()


def compute_avg_brand1_mfg_cost_per_unit(df):
    """Compute the average Brand 1 manufacturing cost per unit."""
    return df['Brand1_Mfg_Cost_Per_Unit'].mean()


# =============================================================================
# Optimal price functions
# =============================================================================

def manufacturer_profit_scenario_a(
    mfg_price_per_unit, model_brand1, avg_pl_price, margin_pct, mfg_cost_per_unit
):
    """
    Compute manufacturer weekly profit given a manufacturer price per unit.
    
    Scenario 4(a): PL retail price is fixed at the historical average.
    
    The retailer sets the Brand 1 retail price to maintain its margin goal:
        retail_price = mfg_price_per_unit / (1 - margin_pct)
    
    Manufacturer profit per unit = mfg_price - mfg_cost - selling_cost
    """
    # Retailer sets retail price based on margin goal
    brand1_retail_price = mfg_price_per_unit / (1.0 - margin_pct)

    # Predicted Brand 1 unit sales
    brand1_units = predict_units(model_brand1, brand1_retail_price, avg_pl_price)

    # Manufacturer profit
    profit_per_unit = mfg_price_per_unit - mfg_cost_per_unit - SELLING_COST_PER_UNIT
    total_profit = profit_per_unit * brand1_units

    return total_profit


def manufacturer_profit_scenario_b(
    mfg_price_per_unit, model_brand1, model_pl, margin_pct, mfg_cost_per_unit
):
    """
    Compute manufacturer weekly profit given a manufacturer price per unit.
    
    Scenario 4(b): PL retail price is always $0.35 below Brand 1 retail price.
    
    The retailer sets the Brand 1 retail price to maintain its margin goal:
        retail_price = mfg_price_per_unit / (1 - margin_pct)
        pl_retail_price = brand1_retail_price - 0.35
    """
    brand1_retail_price = mfg_price_per_unit / (1.0 - margin_pct)
    pl_retail_price = brand1_retail_price - 0.35

    brand1_units = predict_units(model_brand1, brand1_retail_price, pl_retail_price)

    profit_per_unit = mfg_price_per_unit - mfg_cost_per_unit - SELLING_COST_PER_UNIT
    total_profit = profit_per_unit * brand1_units

    return total_profit


def find_optimal_price_scenario_a(model_brand1, avg_pl_price, margin_pct, mfg_cost_per_unit):
    """Find the manufacturer unit price that maximizes profit under scenario 4(a)."""
    def neg_profit(price):
        return -manufacturer_profit_scenario_a(
            price, model_brand1, avg_pl_price, margin_pct, mfg_cost_per_unit
        )

    result = minimize_scalar(neg_profit, bounds=(0.50, 5.00), method='bounded')
    optimal_price = result.x
    optimal_profit = -result.fun
    return optimal_price, optimal_profit


def find_optimal_price_scenario_b(model_brand1, model_pl, margin_pct, mfg_cost_per_unit):
    """Find the manufacturer unit price that maximizes profit under scenario 4(b)."""
    def neg_profit(price):
        return -manufacturer_profit_scenario_b(
            price, model_brand1, model_pl, margin_pct, mfg_cost_per_unit
        )

    result = minimize_scalar(neg_profit, bounds=(0.50, 5.00), method='bounded')
    optimal_price = result.x
    optimal_profit = -result.fun
    return optimal_price, optimal_profit


# =============================================================================
# Q5: Compute implied values at optimal prices
# =============================================================================

def compute_implied_values(
    scenario_label,
    optimal_mfg_price,
    brand1_retail_price,
    pl_retail_price,
    model_brand1,
    model_pl,
    avg_pl_cost,
    mfg_cost_per_unit,
):
    """
    Compute the implied values (unit sales, shares, profits) at the optimal
    prices for a given scenario.
    """
    # Predicted unit sales
    brand1_units = predict_units(model_brand1, brand1_retail_price, pl_retail_price)
    pl_units = predict_units(model_pl, brand1_retail_price, pl_retail_price)
    total_units = brand1_units + pl_units

    # Market shares
    brand1_share = (brand1_units / total_units) * 100.0
    pl_share = (pl_units / total_units) * 100.0

    # Retailer profit
    brand1_unit_cost = optimal_mfg_price  # cost to retailer = manufacturer's selling price
    retailer_profit_brand1 = (brand1_retail_price - brand1_unit_cost) * brand1_units
    retailer_profit_pl = (pl_retail_price - avg_pl_cost) * pl_units
    retailer_total_profit = retailer_profit_brand1 + retailer_profit_pl

    # Manufacturer profit
    mfg_profit_per_unit = optimal_mfg_price - mfg_cost_per_unit - SELLING_COST_PER_UNIT
    manufacturer_profit = mfg_profit_per_unit * brand1_units

    implied = {
        'scenario': scenario_label,
        'optimal_mfg_price': optimal_mfg_price,
        'brand1_retail_price': brand1_retail_price,
        'pl_retail_price': pl_retail_price,
        'brand1_units': brand1_units,
        'pl_units': pl_units,
        'brand1_share': brand1_share,
        'pl_share': pl_share,
        'retailer_profit': retailer_total_profit,
        'manufacturer_profit': manufacturer_profit,
    }
    return implied


def print_comparison_table(scenario_a, scenario_b, current):
    """Print the side-by-side comparison table."""
    print("\n" + "=" * 90)
    print("QUESTION 5: COMPARISON TABLE — TYPICAL WEEK")
    print("=" * 90)

    header = f"{'':50s} | {'Scenario 4(a)':>14s} | {'Scenario 4(b)':>14s} | {'Current (Q1)':>14s}"
    sep = "-" * 50 + "-+-" + "-" * 14 + "-+-" + "-" * 14 + "-+-" + "-" * 14

    print(header)
    print(sep)

    rows = [
        ("Optimal Mfg Price (per unit)",
         f"${scenario_a['optimal_mfg_price']:.2f}",
         f"${scenario_b['optimal_mfg_price']:.2f}",
         "N/A"),
        ("Brand 1 Retail Price",
         f"${scenario_a['brand1_retail_price']:.2f}",
         f"${scenario_b['brand1_retail_price']:.2f}",
         "N/A (avg)"),
        ("PL Retail Price",
         f"${scenario_a['pl_retail_price']:.2f}",
         f"${scenario_b['pl_retail_price']:.2f}",
         "N/A (avg)"),
        ("", "", "", ""),
        ("Units sold — Brand 1",
         f"{scenario_a['brand1_units']:,.0f}",
         f"{scenario_b['brand1_units']:,.0f}",
         f"{current['brand1_units']:,.0f}"),
        ("Units sold — Private Label",
         f"{scenario_a['pl_units']:,.0f}",
         f"{scenario_b['pl_units']:,.0f}",
         f"{current['pl_units']:,.0f}"),
        ("", "", "", ""),
        ("Market share — Brand 1",
         f"{scenario_a['brand1_share']:.2f}%",
         f"{scenario_b['brand1_share']:.2f}%",
         f"{current['brand1_share']:.2f}%"),
        ("Market share — Private Label",
         f"{scenario_a['pl_share']:.2f}%",
         f"{scenario_b['pl_share']:.2f}%",
         f"{current['pl_share']:.2f}%"),
        ("", "", "", ""),
        ("Weekly Retailer Profit",
         f"${scenario_a['retailer_profit']:,.2f}",
         f"${scenario_b['retailer_profit']:,.2f}",
         f"${current['retailer_profit']:,.2f}"),
        ("Weekly Manufacturer Profit",
         f"${scenario_a['manufacturer_profit']:,.2f}",
         f"${scenario_b['manufacturer_profit']:,.2f}",
         f"${current['manufacturer_profit']:,.2f}"),
    ]

    for label, val_a, val_b, val_c in rows:
        print(f"{label:50s} | {val_a:>14s} | {val_b:>14s} | {val_c:>14s}")

    print(sep)


def print_concerns():
    """Print concerns about the reasonableness of each scenario's assumptions."""
    print("\n" + "=" * 90)
    print("CONCERNS ABOUT SCENARIO ASSUMPTIONS")
    print("=" * 90)

    print("""
Scenario 4(a) — PL retail price fixed at historical average:
  Concern: In reality, the retailer's category manager adjusts the private
  label price in response to competitive changes. If Brand 1's price moves
  significantly (up or down), the retailer is likely to re-price the private
  label to maintain a target price gap or to protect private label volume.
  Holding PL price fixed ignores this competitive response, which could lead
  to overestimation of the benefit of lowering Brand 1's price (since PL
  would not be repriced downward to match).

Scenario 4(b) — PL retail price always $0.35 below Brand 1:
  Concern: This assumes a perfectly rigid price gap, which constrains the
  retailer's pricing flexibility. If the manufacturer lowers Brand 1's price
  substantially, the PL retail price would also drop, potentially below the
  retailer's cost for the private label, making the private label unprofitable
  for the retailer. The retailer would likely not allow this to happen, so
  the fixed-gap rule would break down at extreme price points. This could
  lead the model to suggest prices where the PL retail price is unrealistically
  low or even below the retailer's PL cost.
""")


# =============================================================================
# Main
# =============================================================================

def main():
    # ------------------------------------------------------------------
    # 1. Load data & compute current situation
    # ------------------------------------------------------------------
    df = load_data()
    current = compute_current_situation(df)

    # ------------------------------------------------------------------
    # 2. Estimate semi-log demand models (Q2)
    # ------------------------------------------------------------------
    model_brand1, model_pl = estimate_demand_models(df)

    # ------------------------------------------------------------------
    # 3. Compute inputs needed for optimization
    # ------------------------------------------------------------------
    margin_pct = compute_retailer_margin_goal(df)          # Brand 1 avg margin %
    avg_pl_price = compute_avg_pl_retail_price(df)         # PL avg retail price
    avg_pl_cost = compute_avg_pl_cost(df)                  # PL avg retailer cost/unit
    mfg_cost_per_unit = compute_avg_brand1_mfg_cost_per_unit(df)

    print(f"\nRetailer margin goal (Brand 1 avg): {margin_pct*100:.2f}%")
    print(f"Average PL retail price:            ${avg_pl_price:.2f}")
    print(f"Average PL cost to retailer (unit): ${avg_pl_cost:.4f}")
    print(f"Brand 1 mfg cost per unit:          ${mfg_cost_per_unit:.4f}")
    print(f"Selling cost per unit:              ${SELLING_COST_PER_UNIT:.4f}")

    # ------------------------------------------------------------------
    # 4. Find optimal manufacturer prices (Q4)
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("SCENARIO 4(a): PL price fixed at average")
    print("=" * 80)
    opt_price_a, opt_profit_a = find_optimal_price_scenario_a(
        model_brand1, avg_pl_price, margin_pct, mfg_cost_per_unit
    )
    brand1_retail_a = opt_price_a / (1.0 - margin_pct)
    print(f"Optimal mfg price per unit:   ${opt_price_a:.4f}")
    print(f"Implied Brand 1 retail price: ${brand1_retail_a:.4f}")
    print(f"PL retail price (fixed):      ${avg_pl_price:.4f}")
    print(f"Max manufacturer profit:      ${opt_profit_a:,.2f}")

    print("\n" + "=" * 80)
    print("SCENARIO 4(b): PL price = Brand 1 price - $0.35")
    print("=" * 80)
    opt_price_b, opt_profit_b = find_optimal_price_scenario_b(
        model_brand1, model_pl, margin_pct, mfg_cost_per_unit
    )
    brand1_retail_b = opt_price_b / (1.0 - margin_pct)
    pl_retail_b = brand1_retail_b - 0.35
    print(f"Optimal mfg price per unit:   ${opt_price_b:.4f}")
    print(f"Implied Brand 1 retail price: ${brand1_retail_b:.4f}")
    print(f"Implied PL retail price:      ${pl_retail_b:.4f}")
    print(f"Max manufacturer profit:      ${opt_profit_b:,.2f}")

    # ------------------------------------------------------------------
    # 5. Compute implied values at optimal prices (Q5)
    # ------------------------------------------------------------------
    implied_a = compute_implied_values(
        scenario_label="Scenario 4(a)",
        optimal_mfg_price=opt_price_a,
        brand1_retail_price=brand1_retail_a,
        pl_retail_price=avg_pl_price,
        model_brand1=model_brand1,
        model_pl=model_pl,
        avg_pl_cost=avg_pl_cost,
        mfg_cost_per_unit=mfg_cost_per_unit,
    )

    implied_b = compute_implied_values(
        scenario_label="Scenario 4(b)",
        optimal_mfg_price=opt_price_b,
        brand1_retail_price=brand1_retail_b,
        pl_retail_price=pl_retail_b,
        model_brand1=model_brand1,
        model_pl=model_pl,
        avg_pl_cost=avg_pl_cost,
        mfg_cost_per_unit=mfg_cost_per_unit,
    )

    # ------------------------------------------------------------------
    # 6. Print comparison table & concerns
    # ------------------------------------------------------------------
    print_comparison_table(implied_a, implied_b, current)
    print_concerns()

    return implied_a, implied_b, current


if __name__ == "__main__":
    implied_a, implied_b, current = main()
