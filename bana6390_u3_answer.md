# Unit 3 Assignment Answers

## 1. Random Assignment Check

I used meal type (Lunch vs. Dinner) to test whether the random assignment worked, since it is not the treatment itself and should be independent of promotion if assignment was done correctly. The chi-square statistic is 1.5770 with a p-value of 0.2092. Because the p-value is greater than 0.05, I do not reject the null hypothesis of independence. This suggests the lunch/dinner mix is similar across Promotions A and B, so the randomization appears successful and the later comparisons are more credible.

## 2A. Click-Through Rate of Each Promotion

The click-through rate is clicks divided by impressions. Promotion A received 554 clicks on 24,963 impressions, so its CTR is 2.22%. Promotion B received 759 clicks on 25,102 impressions, so its CTR is 3.02%. Based on CTR alone, Promotion B performed better because it generated more engagement at the ad stage and moved more consumers into the purchase funnel.

## 2B. Test Whether the CTRs Are Equal

I used a two-proportion test to compare the click-through rates of the two promotions. The test statistic is 31.7105 and the p-value is 1.78949e-08, which is far below 0.05. Therefore, I reject the null hypothesis that the CTRs are equal. Promotion B generated a statistically significantly higher click-through rate than Promotion A, which suggests the 5% discount was more effective at getting consumers to click. However, CTR only captures ad response, not final profitability.

## 3A. CTR by Promotion and Meal Type

Breaking CTR out by meal type shows a more mixed result. Promotion A had a CTR of 0.90% for dinner and 2.93% for lunch, while Promotion B had a CTR of 4.15% for dinner and 2.41% for lunch. So Promotion B was much stronger at dinner, but Promotion A was stronger at lunch. This suggests the effectiveness of the promotion depends on context, and the overall CTR hides that difference.

## 3B. Average Order Size for Clickers by Promotion and Meal Type

For consumers who clicked, Promotion A produced slightly larger average orders in both meal periods. Promotion A averaged $24.37 at dinner and $24.68 at lunch, while Promotion B averaged $23.59 at dinner and $23.62 at lunch. The differences are not large, but they are consistent. This matters because Promotion B was better at driving clicks, while Promotion A appears to generate slightly more value per order.

## 4. Return on the Campaign (ROC%) for Lunch and Dinner

Using the assignment assumptions, including a $0.25 cost for Promotion A, 40% contribution margin, $0.03 advertising cost per exposure, and a 4% cart abandonment rate, the final ROC% values are:

|  | Lunch | Dinner |
| --- | ---: | ---: |
| Promotion A | 649.43% | 160.75% |
| Promotion B | 280.98% | 388.34% |

Both promotions are profitable, but they perform differently by meal type. Promotion A is much stronger at lunch, while Promotion B is better at dinner. The main reason is cost structure: Promotion A has a fixed giveaway cost, while Promotion B’s 5% discount becomes more expensive as order size rises. So even though Promotion B generated more clicks overall, Promotion A delivered the stronger profitability result when costs were included. If Quick Dosa wants one promotion overall, I would recommend Promotion A. If the company can target by daypart, a mixed strategy could make sense: Promotion A at lunch and Promotion B at dinner.

## 5A. Note to Chef Chad

Promotion B was better at generating clicks, but Promotion A performed better on profitability because it produced slightly larger orders and did so at a lower promotional cost, especially at lunch. Based on ROC% as the decision metric, I would recommend Promotion A if Quick Dosa wants to choose one promotion overall.

## 5B. Comment on Assumption #4

The assumption that all revenue from the promotions is incremental is probably too strong. Some customers likely would have ordered even without the ad or promotion, so the campaign should not get full credit for all observed revenue. If that is true, then the ROC% figures above overstate true profitability because some baseline demand is being counted as campaign-driven demand.
