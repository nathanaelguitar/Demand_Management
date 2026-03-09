# Project Conclusions and Notes

This document collects the high‑level takeaways from the demand management
assignment and links to the detailed question responses that are stored in
separate markdown files.

## Key Topics Covered

- **Data ingestion and processing**: the `data_ingestion.py` and
  `process_data.py` modules read the original Excel file, clean the data, and
  compute unit‑level metrics such as margins, market shares, and profits.

- **Descriptive statistics**: the cleaned dataset reveals that Brand 1 sells
  fewer units than the private label, carries a higher retail price, and yields
  lower retailer profitability on average.

- **Demand model (semi‑log)**: estimated in question 2, the log‑linear model
  relates Brand 1 unit sales to its own retail price and to the private label
  price.

- **Optimization (question 4)**: the manufacturer chooses a wholesale price to
  maximize its weekly profit. Two competitive scenarios are considered:
  1. Private‑label price fixed at the historical average.
  2. Private‑label price set at a constant 35¢ gap below Brand 1.

  The analysis shows that the manufacturer is better off lowering its price
  slightly in both cases, with larger gains when the private label is
  unresponsive.

- **Implied values (question 5)**: plugging the optimal prices back into the
  demand model yields predicted volumes, market shares, and profits for both
  brands and the retailer. The table in `q5_answer.md` summarizes these
  comparisons with the current situation, and discusses potential limitations
  of the pricing assumptions.

## File Summary

| File | Description |
|------|-------------|
| `q4_answer.md` | Detailed explanation of the optimal manufacturer prices and
  profit calculations under scenarios 4(a) and 4(b). |
| `q5_answer.md` | Computation of implied values at the optimal prices and a discussion of
  the reasonableness of the retailer–price assumptions. |
| `README.md` | Overview of the codebase, data structure, and usage instructions. |

## Final Remarks

The models and scripts in this repository can be adapted to other product
categories or datasets by changing the input Excel file and adjusting cost
assumptions.  Further extensions might incorporate more sophisticated demand
functions, dynamic pricing, or game‑theoretic considerations between the
manufacturer and retailer.
