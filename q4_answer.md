# Question 4: Optimal Manufacturer Selling Price

## Prompt

> **(7 points)** Next, you will determine the optimal selling price of the manufacturer using Excel (or calculus) for an average week. Make reasonable assumptions about manufacturer costs and be sure to state them in your response. Remember that the retailer sets the retail price. Assume that the retailer has margin goals that serve as norms. Please state your assumptions about the retailer clearly.
>
> With regard to the competitor's price, consider the following two scenarios and provide the optimal selling price of the manufacturer under each scenario separately:
>
> - **(a)** Assume that the private label's retail price is fixed at the average level in the data.
> - **(b)** Assume that the private label's retail price is always 35 cents below the retail price of Brand 1.

---

## Assumptions

We begin by stating the assumptions that underlie the optimization.

**Manufacturer costs.** The manufacturer incurs two variable costs per unit of Brand 1 sold:

1. **Manufacturing cost:** We use the historical average from the data, which is **$1.18 per unit** ($28.44 per case ÷ 24 units).
2. **Selling cost:** Given as **$0.4167 per unit** ($10.00 per case ÷ 24 units).

There are no other variable costs specified; we treat these as the only costs relevant to the manufacturer's profit calculation.

**Retailer pricing behavior.** The manufacturer does not set the retail price — the retailer does. We assume the retailer applies a **constant percentage margin** on Brand 1 equal to its historical average of **17.12%**. This means the retailer marks up the manufacturer's unit price according to:

$$\text{Retail Price} = \frac{\text{Manufacturer Price}}{1 - 0.1712}$$

This is a reasonable assumption because retailers typically have internal margin targets (sometimes called "margin norms") that they apply consistently across similar products.

---

## Approach

The manufacturer's weekly profit on Brand 1 is:

$$\pi = (\text{Mfg Price} - \text{Mfg Cost} - \text{Selling Cost}) \times \text{Predicted Units Sold}$$

We predict Brand 1 unit sales using the semi-log demand model estimated in Q2:

$$\ln(\text{Brand 1 Units}) = 12.2993 - 2.1551 \times P_{B1} + 0.6426 \times P_{PL}$$

where $P_{B1}$ and $P_{PL}$ are the retail prices of Brand 1 and the private label, respectively.

The manufacturer chooses its unit price to the retailer. The retailer then sets the retail price via the margin relationship above. As the manufacturer raises its price, two things happen simultaneously:

- **Profit per unit increases** (since selling price rises while costs stay fixed).
- **Units sold decrease** (since the higher retail price drives consumers away).

The optimal price balances these two effects. We use numerical optimization (bounded search over the interval $0.50 to $5.00) to find the manufacturer price that maximizes weekly profit.

---

## Scenario 4(a): Private Label Retail Price Fixed at Its Historical Average

In this scenario, the private label's retail price stays at the historical average of **$2.15 per unit** regardless of what happens to the Brand 1 price. This represents a situation where the retailer does not adjust private label pricing in response to changes in Brand 1.

### Result

| Variable | Value |
|---|---|
| **Optimal manufacturer price per unit** | **$1.99** |
| Implied Brand 1 retail price | $2.40 |
| Private label retail price (fixed) | $2.15 |
| **Maximum weekly manufacturer profit** | **$1,925.89** |

Compared to the current average manufacturer price of $2.16/unit and current weekly profit of $1,773, this represents an **8.6% increase in profit** ($153 per week).

The optimal strategy here is to **lower** the manufacturer's price by about $0.17/unit. Although profit per unit falls, the lower retail price generates enough additional volume to more than offset the margin reduction. The implied retail price of $2.40 is roughly $0.21 below the current average of $2.61, narrowing the price gap with the private label from $0.46 to $0.25.

---

## Scenario 4(b): Private Label Retail Price Always $0.35 Below Brand 1

In this scenario, the retailer maintains a fixed $0.35 price gap, always pricing the private label 35 cents below Brand 1:

$$P_{PL} = P_{B1} - 0.35$$

This is a more realistic pricing rule in many retail environments where the category manager maintains a consistent price ladder between national brands and store brands.

### Result

| Variable | Value |
|---|---|
| **Optimal manufacturer price per unit** | **$2.15** |
| Implied Brand 1 retail price | $2.59 |
| Implied PL retail price | $2.24 |
| **Maximum weekly manufacturer profit** | **$1,901.03** |

Compared to the current situation, this represents a **7.2% increase in profit** ($128 per week).

Under this scenario, the optimal manufacturer price is very close to the current price ($2.15 vs. $2.16), meaning the manufacturer is already near its optimum. The key difference from Scenario 4(a) is that lowering the Brand 1 price now also lowers the private label price, which partially offsets the demand gains for Brand 1 — the private label becomes cheaper too, so it continues to compete aggressively.

---

## Comparison and Discussion

| Metric | Scenario 4(a) | Scenario 4(b) | Current |
|---|---|---|---|
| Mfg price per unit | $1.99 | $2.15 | $2.16 |
| Brand 1 retail price | $2.40 | $2.59 | $2.61 |
| PL retail price | $2.15 | $2.24 | $2.15 |
| Mfg weekly profit | $1,925.89 | $1,901.03 | $1,773 |
| Profit improvement | +8.6% | +7.2% | — |

**Scenario 4(a) yields the higher profit** because the manufacturer can lower its price (and thus the Brand 1 retail price) without triggering a competitive response from the private label. The price gap narrows, consumers switch to Brand 1, and volume increases enough to boost total profit.

**Scenario 4(b) yields less improvement** because any price reduction by the manufacturer is partially neutralized: the retailer also lowers the private label price by the same amount, maintaining the $0.35 gap. This limits the competitive advantage of cutting the Brand 1 price.

In both scenarios, the manufacturer benefits from lowering its price relative to the current average — the current pricing is slightly above the profit-maximizing level. The analysis suggests that a modest price decrease is the profit-maximizing move for the manufacturer.
