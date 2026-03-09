# Unit 3 Assignment Results

## Question 1

Variable used for randomization check: meal_type

Chi-square statistic = 1.577

p-value = 0.209187

Contingency table:

| promotion | Dinner | Lunch |
| --- | --- | --- |
| A | 8706 | 16257 |
| B | 8889 | 16213 |

## Question 2

Click-through rates by promotion:

| promotion | impressions | clicks | ctr |
| --- | --- | --- | --- |
| A | 24963 | 554 | 2.22% |
| B | 25102 | 759 | 3.02% |

Equality of CTR test statistic = 31.7105

p-value = 1.78949e-08

## Question 3A

CTR by promotion and meal type:

| promotion_label | meal_type | ctr |
| --- | --- | --- |
| A | Dinner | 0.90% |
| A | Lunch | 2.93% |
| B | Dinner | 4.15% |
| B | Lunch | 2.41% |

## Question 3B

Average order amount among clickers by promotion and meal type:

| promotion_label | meal_type | avg_order_amount |
| --- | --- | --- |
| A | Dinner | $24.37 |
| A | Lunch | $24.68 |
| B | Dinner | $23.59 |
| B | Lunch | $23.62 |

## Question 4

ROC% analysis by promotion and meal type:

| promotion | meal_type | ad_cost | promo_cost | contribution_before_promo | net_contribution | roc_pct |
| --- | --- | --- | --- | --- | --- | --- |
| A | Dinner | $261.18 | $18.72 | $729.83 | $449.93 | 160.75% |
| A | Lunch | $487.71 | $114.24 | $4511.17 | $3909.22 | 649.43% |
| B | Dinner | $266.67 | $417.85 | $3342.79 | $2658.27 | 388.34% |
| B | Lunch | $486.39 | $442.24 | $3537.88 | $2609.26 | 280.98% |

## Question 5A

Promotion A delivers the stronger average ROC% across lunch and dinner in this one-week test. Based on immediate campaign profitability, it is the better rollout candidate.

## Question 5B

Assumption #4 is unlikely to be fully true because some observed orders would probably have happened even without the ads or promotions. If that is the case, the profitability calculated here is overstated, because we treated all observed promotional revenue as incremental.

