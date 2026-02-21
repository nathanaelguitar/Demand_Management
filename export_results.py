"""
Export Q4 & Q5 Results to Excel
================================
Generates a formatted Excel workbook with:
  - Sheet 1: Q4 Assumptions & Optimal Prices
  - Sheet 2: Q5 Comparison Table (Scenario 4a vs 4b vs Current)
"""

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill, numbers
from openpyxl.utils import get_column_letter

from process_data import DataProcessor
from q4_optimal_price import (
    UNITS_PER_CASE, SELLING_COST_PER_UNIT,
    B1_INTERCEPT, B1_COEF_B1_PRICE, B1_COEF_PL_PRICE,
    PL_INTERCEPT, PL_COEF_PL_PRICE, PL_COEF_B1_PRICE,
    predict_brand1_units, predict_pl_units,
    load_averages, optimize_scenario_a, optimize_scenario_b,
)
from q5_implied_values import compute_implied_values, compute_current_situation

# =============================================================================
# Styles
# =============================================================================
HEADER_FONT = Font(bold=True, size=12)
TITLE_FONT = Font(bold=True, size=14)
BOLD_FONT = Font(bold=True)
MONEY_FMT = '$#,##0.00'
MONEY4_FMT = '$#,##0.0000'
PCT_FMT = '0.00%'
NUM_FMT = '#,##0'
HEADER_FILL = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
HEADER_FONT_WHITE = Font(bold=True, color='FFFFFF', size=11)
LIGHT_FILL = PatternFill(start_color='D9E2F3', end_color='D9E2F3', fill_type='solid')
THIN_BORDER = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin'),
)


def apply_header_row(ws, row, cols):
    """Style a header row with blue background and white bold text."""
    for col in range(1, cols + 1):
        cell = ws.cell(row=row, column=col)
        cell.font = HEADER_FONT_WHITE
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal='center', wrap_text=True)
        cell.border = THIN_BORDER


def apply_border_range(ws, min_row, max_row, min_col, max_col):
    """Apply thin borders to a rectangular range."""
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            ws.cell(row=r, column=c).border = THIN_BORDER


def stripe_rows(ws, min_row, max_row, min_col, max_col):
    """Apply light-blue striping to alternating rows."""
    for r in range(min_row, max_row + 1):
        if (r - min_row) % 2 == 0:
            for c in range(min_col, max_col + 1):
                ws.cell(row=r, column=c).fill = LIGHT_FILL


# =============================================================================
# Sheet 1: Q4 — Assumptions & Optimal Prices
# =============================================================================

def build_q4_sheet(wb, avg, opt_a, b1_retail_a, opt_b, b1_retail_b, pl_retail_b,
                   current_mfg_price, current_profit, opt_profit_a, opt_profit_b):
    ws = wb.active
    ws.title = 'Q4 - Optimal Price'

    # Title
    ws.merge_cells('A1:D1')
    ws['A1'] = 'Question 4: Optimal Manufacturer Selling Price'
    ws['A1'].font = TITLE_FONT

    # ----- Assumptions -----
    ws['A3'] = 'Assumptions'
    ws['A3'].font = HEADER_FONT

    assumptions = [
        ('Retailer margin goal (Brand 1 avg)', avg['b1_margin_pct'], PCT_FMT),
        ('Average PL retail price', avg['pl_retail_price'], MONEY4_FMT),
        ('Average PL cost to retailer (unit)', avg['pl_unit_cost'], MONEY4_FMT),
        ('Brand 1 mfg cost per unit', avg['b1_mfg_cost_per_unit'], MONEY4_FMT),
        ('Selling cost per unit', SELLING_COST_PER_UNIT, MONEY4_FMT),
    ]
    for i, (label, val, fmt) in enumerate(assumptions, start=4):
        ws.cell(row=i, column=1, value=label).font = BOLD_FONT
        cell = ws.cell(row=i, column=2, value=val)
        cell.number_format = fmt
        cell.alignment = Alignment(horizontal='right')

    # ----- Demand model coefficients -----
    r = 10
    ws.cell(row=r, column=1, value='Demand Model Coefficients (from Q2)').font = HEADER_FONT
    r += 1
    headers = ['Model', 'Intercept', 'B1 Price Coef', 'PL Price Coef']
    for c, h in enumerate(headers, 1):
        ws.cell(row=r, column=c, value=h)
    apply_header_row(ws, r, len(headers))
    r += 1
    for label, b0, b1, b2 in [
        ('Brand 1', B1_INTERCEPT, B1_COEF_B1_PRICE, B1_COEF_PL_PRICE),
        ('Private Label', PL_INTERCEPT, PL_COEF_B1_PRICE, PL_COEF_PL_PRICE),
    ]:
        ws.cell(row=r, column=1, value=label)
        for c, v in enumerate([b0, b1, b2], 2):
            cell = ws.cell(row=r, column=c, value=v)
            cell.number_format = '0.0000'
            cell.alignment = Alignment(horizontal='right')
        r += 1
    apply_border_range(ws, 11, r - 1, 1, 4)

    # ----- Optimal price results -----
    r += 1
    ws.cell(row=r, column=1, value='Optimal Price Results').font = HEADER_FONT
    r += 1
    result_headers = ['Metric', 'Scenario 4(a)', 'Scenario 4(b)', 'Current']
    for c, h in enumerate(result_headers, 1):
        ws.cell(row=r, column=c, value=h)
    apply_header_row(ws, r, len(result_headers))
    r += 1

    rows_data = [
        ('Mfg price per unit', opt_a, opt_b, current_mfg_price, MONEY4_FMT),
        ('Brand 1 retail price', b1_retail_a, b1_retail_b,
         avg['b1_retail_price'], MONEY4_FMT),
        ('PL retail price', avg['pl_retail_price'], pl_retail_b,
         avg['pl_retail_price'], MONEY4_FMT),
        ('Max weekly mfg profit', opt_profit_a, opt_profit_b,
         current_profit, MONEY_FMT),
    ]
    start_r = r
    for label, va, vb, vc, fmt in rows_data:
        ws.cell(row=r, column=1, value=label).font = BOLD_FONT
        for c, v in enumerate([va, vb, vc], 2):
            cell = ws.cell(row=r, column=c, value=v)
            cell.number_format = fmt
            cell.alignment = Alignment(horizontal='right')
        r += 1

    apply_border_range(ws, start_r - 1, r - 1, 1, 4)
    stripe_rows(ws, start_r, r - 1, 1, 4)

    # Improvement row
    r += 1
    ws.cell(row=r, column=1, value='Profit improvement vs. current').font = BOLD_FONT
    for c, diff in enumerate([opt_profit_a - current_profit, opt_profit_b - current_profit], 2):
        cell = ws.cell(row=r, column=c, value=diff)
        cell.number_format = '+$#,##0.00;-$#,##0.00'
        cell.alignment = Alignment(horizontal='right')

    r += 1
    ws.cell(row=r, column=1, value='% improvement').font = BOLD_FONT
    for c, pct in enumerate([(opt_profit_a / current_profit - 1),
                              (opt_profit_b / current_profit - 1)], 2):
        cell = ws.cell(row=r, column=c, value=pct)
        cell.number_format = '+0.0%;-0.0%'
        cell.alignment = Alignment(horizontal='right')

    # Column widths
    ws.column_dimensions['A'].width = 38
    ws.column_dimensions['B'].width = 18
    ws.column_dimensions['C'].width = 18
    ws.column_dimensions['D'].width = 18


# =============================================================================
# Sheet 2: Q5 — Implied Values Comparison Table
# =============================================================================

def build_q5_sheet(wb, implied_a, implied_b, current):
    ws = wb.create_sheet('Q5 - Implied Values')

    # Title
    ws.merge_cells('A1:D1')
    ws['A1'] = 'Question 5: Implied Values at Optimal Prices'
    ws['A1'].font = TITLE_FONT

    # Header row
    r = 3
    headers = ['Metric', 'Scenario 4(a)', 'Scenario 4(b)', 'Current (Q1)']
    for c, h in enumerate(headers, 1):
        ws.cell(row=r, column=c, value=h)
    apply_header_row(ws, r, len(headers))
    r += 1

    # Table rows: (label, key_implied, key_current_or_None, format)
    table = [
        ('Mfg price per unit', 'mfg_price', None, MONEY4_FMT),
        ('Brand 1 retail price', 'b1_retail', None, MONEY4_FMT),
        ('PL retail price', 'pl_retail', None, MONEY4_FMT),
        None,  # spacer
        ('Brand 1 weekly units', 'b1_units', 'b1_units', NUM_FMT),
        ('Private Label weekly units', 'pl_units', 'pl_units', NUM_FMT),
        None,
        ('Brand 1 market share', 'b1_share', 'b1_share', '0.00"%"'),
        ('Private Label market share', 'pl_share', 'pl_share', '0.00"%"'),
        None,
        ('Retailer weekly profit', 'retailer_profit', 'retailer_profit', MONEY_FMT),
        ('Manufacturer weekly profit', 'manufacturer_profit', 'manufacturer_profit', MONEY_FMT),
    ]

    start_r = r
    for item in table:
        if item is None:
            r += 1
            continue
        label, key_imp, key_cur, fmt = item
        ws.cell(row=r, column=1, value=label).font = BOLD_FONT
        # Scenario 4(a)
        cell_a = ws.cell(row=r, column=2, value=implied_a[key_imp])
        cell_a.number_format = fmt
        cell_a.alignment = Alignment(horizontal='right')
        # Scenario 4(b)
        cell_b = ws.cell(row=r, column=3, value=implied_b[key_imp])
        cell_b.number_format = fmt
        cell_b.alignment = Alignment(horizontal='right')
        # Current
        if key_cur is not None:
            cell_c = ws.cell(row=r, column=4, value=current[key_cur])
            cell_c.number_format = fmt
            cell_c.alignment = Alignment(horizontal='right')
        else:
            ws.cell(row=r, column=4, value='—').alignment = Alignment(horizontal='center')
        r += 1

    apply_border_range(ws, 3, r - 1, 1, 4)
    stripe_rows(ws, start_r, r - 1, 1, 4)

    # ----- Concerns -----
    r += 2
    ws.cell(row=r, column=1, value='Concerns About Scenario Assumptions').font = HEADER_FONT
    r += 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    ws.cell(row=r, column=1, value=(
        'Scenario 4(a): The assumption that PL price stays fixed is unrealistic. '
        'If Brand 1 becomes more competitive, the retailer would likely lower the PL price '
        'to defend volume, meaning we overestimate the demand shift toward Brand 1.'
    )).alignment = Alignment(wrap_text=True)
    ws.row_dimensions[r].height = 45

    r += 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    ws.cell(row=r, column=1, value=(
        'Scenario 4(b): A rigid $0.35 gap breaks down at extremes — if the manufacturer '
        'cuts price aggressively, the implied PL retail price could fall below the retailer\'s '
        'PL cost, making PL unprofitable. The retailer would not allow this.'
    )).alignment = Alignment(wrap_text=True)
    ws.row_dimensions[r].height = 45

    # Column widths
    ws.column_dimensions['A'].width = 34
    ws.column_dimensions['B'].width = 18
    ws.column_dimensions['C'].width = 18
    ws.column_dimensions['D'].width = 18


# =============================================================================
# Main
# =============================================================================

def main():
    # Load data
    avg = load_averages()

    # Run Q4 optimization
    opt_price_a, opt_profit_a = optimize_scenario_a(avg)
    opt_price_b, opt_profit_b = optimize_scenario_b(avg)

    margin_pct = avg['b1_margin_pct']
    b1_retail_a = opt_price_a / (1.0 - margin_pct)
    b1_retail_b = opt_price_b / (1.0 - margin_pct)
    pl_retail_b = b1_retail_b - 0.35

    current_mfg_price = avg['b1_retail_price'] * (1.0 - margin_pct)
    from q4_optimal_price import manufacturer_weekly_profit
    current_profit = manufacturer_weekly_profit(
        current_mfg_price, avg['b1_retail_price'],
        avg['pl_retail_price'], avg['b1_mfg_cost_per_unit'],
    )

    # Compute Q5 implied values
    implied_a = compute_implied_values(
        opt_price_a, b1_retail_a, avg['pl_retail_price'],
        avg['pl_unit_cost'], avg['b1_mfg_cost_per_unit'],
    )
    implied_b = compute_implied_values(
        opt_price_b, b1_retail_b, pl_retail_b,
        avg['pl_unit_cost'], avg['b1_mfg_cost_per_unit'],
    )
    current = compute_current_situation()

    # Build workbook
    wb = Workbook()
    build_q4_sheet(wb, avg, opt_price_a, b1_retail_a,
                   opt_price_b, b1_retail_b, pl_retail_b,
                   current_mfg_price, current_profit,
                   opt_profit_a, opt_profit_b)
    build_q5_sheet(wb, implied_a, implied_b, current)

    out_path = 'q4_q5_results.xlsx'
    wb.save(out_path)
    print(f"Exported to {out_path}")


if __name__ == '__main__':
    main()
