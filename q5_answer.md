# Question 5: Implied Values at Optimal Prices

## Prompt

> **(4 points)** Compute the "implied" values of different variables at the optimal prices in each of scenarios 4(a) and 4(b), and compare them with the current situation. Fill in the table below to represent a typical week. Take the retailer's cost of the private label to be the average cost in the historical data. The last column can be filled in by reproducing your answers to question 1 (d), (e), and (f).
>
> For scenarios 4(a) and 4(b), identify one concern about the reasonableness of the assumption about the retailer's pricing behavior with respect to the private label.

---

## Comparison Table

Using the optimal manufacturer prices from Q4 and plugging them into our demand models, here's what a typical week would look like under each scenario compared to the status quo:

| | **Scenario 4(a)** | **Scenario 4(b)** | **From Q1** |
|---|---|---|---|
| **How many units will the retailer sell of each brand?** | | | |
| 1. Brand 1 | 5,008 | 3,469 | 3,221 |
| 2. Private Label | 4,037 | 4,174 | 4,545 |
| **What will be the market shares of the two brands?** | | | |
| 1. Brand 1 | 55.37% | 45.39% | 41.31% |
| 2. Private Label | 44.63% | 54.61% | 58.69% |
| **What will be the total weekly profits of the** | | | |
| 1. Retailer | $4,055 | $3,984 | $3,689 |
| 2. Manufacturer | $1,926 | $1,901 | $1,802 |

---

## What's Going On Here

Both scenarios tell a similar story — the manufacturer should lower its price a bit to boost Brand 1 volume — but the details play out differently depending on what happens to the private label.

**Scenario 4(a)** is the more dramatic shift. Since the PL price stays put at $2.15, dropping Brand 1's retail price to $2.40 narrows the gap between the two products significantly (from $0.46 down to $0.25). Consumers respond by switching to Brand 1 in a big way — weekly Brand 1 sales jump from about 3,221 units to over 5,000, and Brand 1 actually flips from a minority player (41%) to the majority share holder (55%). Even though the manufacturer is charging less per unit, the volume bump more than makes up for it, pushing weekly profit up by about $124. The retailer wins too — total store profit goes up by roughly $367/week because they're moving way more Brand 1 units at a decent margin.

**Scenario 4(b)** is a lot more muted. Here, when Brand 1's price drops, the PL price drops right along with it (staying $0.35 below). So the competitive advantage of cutting Brand 1's price gets partially cancelled out — you're cheaper, but so is the PL. Brand 1 still picks up a few share points (41% → 45%), but nothing like the swing in 4(a). The manufacturer's optimal price here ($2.15) is basically where it already is, so not much changes. Profit still goes up, but only by about $99/week.

Interestingly, the retailer benefits under both scenarios. That makes sense — more total units are moving through the store, and the margins on both products are healthy.

---

## Concerns About the Assumptions

**Scenario 4(a):** The idea that the PL price just stays frozen while Brand 1 gets way more competitive isn't super realistic. If Brand 1 suddenly grabbed 55% share, the retailer's category manager would almost certainly react — maybe by dropping the PL price to defend its volume, or adjusting the shelf positioning. Holding PL price fixed means we're probably overestimating how much demand actually shifts to Brand 1.

**Scenario 4(b):** A rigid $0.35 gap sounds clean on paper, but it breaks down at the extremes. If the manufacturer dropped its price aggressively enough, the PL retail price could end up below what the retailer actually pays for the private label product, which would mean the retailer is losing money on every PL unit sold. No retailer would let that happen, so this pricing rule has a built-in floor that the model doesn't account for.
