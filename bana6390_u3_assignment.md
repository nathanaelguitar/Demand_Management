## Overview

The goal of this course is to give you the knowledge and tools that you need to successfully design and offer products and services to customers. To put your skills from Unit Three into practice, you will examine the data provided along with this assignment, read through the scenario described in this document and then follow the prompts to compute and analyze the effectiveness of a promotional campaign.

The dataset is available for download on the assignment page.

**Completion of this project is a course requirement.**

**Please submit a Word or PDF NOT EXCEEDING FIVE PAGES. NO Excel files please. Completion of this assignment is a course requirement.**

Except as indicated, use this document to record all your Unit Three assignment work and responses to any questions. At a minimum, you will need to turn in a digital copy of this document to your facilitator as part of your project completion. You may also have additional supporting documents that you will need to submit.

**Note:** Though your work will only be seen by those grading the course and will not be used or shared outside the course, you should take care to obscure any information you feel might be of a sensitive or confidential nature.

*Grading details and directions to submit your Unit Three assignment can be found on the assignment page in Canvas. Do not hesitate to contact your facilitator if you have any questions about the Unit Three assignment.*

## The Scenario

Quick Dosa (QD) is one of the world’s first fast-food restaurant chains serving vegetarian South Indian food. It is the brainchild of the well-known chef Chad Rao, who successfully operated six high-end Indian restaurants in North America and Europe. Based on extensive market research, Chad had learned that a segment of U.S. urban consumers was seeking nutritious, vegetarian fast-food, and was familiar with (and liked) Indian cuisine.

Chad spent twelve months developing and perfecting a menu of South Indian dishes for the fast-food restaurant format. Within two years of launch, the QD chain had 163 franchised restaurants in New York, NY; Philadelphia, PA; Boston, MA; and Buffalo, NY. The largest selling dishes on QD’s menu were classic South Indian snacks — idlis, vadas, upma, and mango lassi (yogurt drink). Dine-in customers accounted for 80% of the business and this number was increasing rapidly. Soon, QD restaurants were starting to experience significant crowding that resulted in increased wait times for tables. Although there was capacity in the kitchen, the seating space constraint in restaurants began to affect growth negatively.

\
Promotions to Grow the Takeout Business
---------------------------------------

As a strategic initiative to maintain growth, Chad thought about expanding the takeout business. As a first step, he invested in developing an attractive website for QD where customers could place takeout orders efficiently. The next step was to drive customer traffic to the website. QD’s marketing team developed a promotional campaign to be advertised via digital display ads. They considered two alternative promotional offers: Promotion A was a free small mango lassi or soft drink with every takeout order worth \$7.50 or more. Promotion B was 5% off with every takeout order worth \$7.50 or more.\
\
There was considerable disagreement amongst marketing team members about which of the two promotions would be better for the takeout business. They decided to run an A-B test for one week to help them make the decision. The design of the experiment was as follows.

**Test Week Setup**

QD bought display advertising at many food-themed websites based on specific targeting criteria. During the test week, each targeted individual in Buffalo, NY would be randomly assigned to group A or group B. Individuals in group A were shown a banner ad for promotion A; individuals in group B were shown a banner ad for promotion B. An individual who clicked on the ad would be taken to a specific landing page on QD’s website that reinforced the promotional message and invited the individual to place a takeout order. The promotion was automatically applied to the order. In the test data, all clicks converted to orders. However, there was a 4% cart abandonment rate after the order was registered by the server (this usually happened because of difficulties in approving credit cards). For this assignment, assume that the rate of conversion from clicks to orders is 100%, and there is a 4% cart abandonment rate after the order being recorded.

Chad Rao and his marketing team were anxious to find out what the one-week test revealed about the effectiveness of the promotions, and how to roll out promotions into his larger markets.

**Test Week Results**

At the end of the test week, ads for promotions A and B had been served up 24,963 and 25,102 times. The Excel file accompanying this case contains 50,065 rows of data corresponding to the ad impressions. The variables in the file are as follows:

- **Column A:** Anonymized Individual ID

- **Column B:** Promotion (A or B)

- **Column C:** Clicked (1) or not (0)

- **Column D:** Takeout order amount (\$). This was only available for those who clicked. The order amount is before promotional discount, and before cart abandonment.

- **Column E:** An indicator for whether the order was for lunch (1) or dinner (0). A cutoff time of 3 pm based on the time the ad was shown to the consumer was used to classify orders.

\
Instructions
------------

To receive full credit for this unit assignment, follow the instructions and provide your\
observations below.

1.  (5 points) Test whether the random assignment of individuals to the two promotional conditions was successful. Choose one variable for this purpose (other than “Promotion”, which is the random assignment itself!) and conduct a chi-square test. Hint: Remember that random assignment is performed BEFORE the ad is shown.

|              |
|--------------|
| Answer here… |

2.  **A.** (2 points) What was the click-through rate of each promotion? Click-through rate is defined as the number of times an ad was clicked on as a fraction of the number of times the ad was served up.

|              |
|--------------|
| Answer here… |

> **B.** (4 points) Test statistically whether the click-through rate of the two promotions is equal. Provide your finding below.

|              |
|--------------|
| Answer here… |

3.  **A.** (3 points) Compute and report the click-through rate of the two promotions by type of meal (lunch and dinner).

|              |
|--------------|
| Answer here… |

> **\
> B.** (3 points) Compute and report the average order size in \$ (for consumers who clicked) of each of the two types of promotions by type of meal (lunch and dinner).

|              |
|--------------|
| Answer here… |

4.  (6 points) Compute the profitability of each of the two promotions as Return on the Campaign (ROC%) as a percentage, separately for lunch and dinner. ROC% is defined as the net contribution on incremental revenue after cost of advertising and promotion, divided by the cost of advertising and promotion, multiplied by 100 to express as a percentage. Your final answer should be provided in the table below for evaluation but show your calculations in as much detail as you consider necessary.

> Make the following assumptions in Q4:

1.  The cost to QD of a small mango lassi or soft drink that is given away with Promotion A\
    is \$0.25.

2.  The average contribution margin on both lunch and dinner orders is 40% of before- promotion revenue.

3.  The cost per exposure for display advertising is \$0.03.

4.  Assume that all revenue derived from the promotions is incremental.

5.  Ignore the long-term positive impact of the promotion on customer traffic and revenue. That is, consider only the immediate impact. This means that we are understating the positive effects of both promotions.

|             |           |            |
|:-----------:|:---------:|:----------:|
|             | **Lunch** | **Dinner** |
| Promotion A |           |            |
| Promotion B |           |            |

5.  **A.** (1 point) Write a note to Chef Chad summarizing in no more than two sentences the key finding about the profitability of the two campaigns (use ROC% as the measure of profitability), and therefore your recommendation.

|              |
|--------------|
| Answer here… |

> **B.** (1 point) Comment on assumption \#4 we made in Question 4 (“Assume that all revenue derived from the promotions is incremental”) in no more than four sentences. Specifically note whether this assumption is likely to be true or not and why; if not true, whether the profitability you computed in Question 4 above is likely to be an over-estimation or under-estimation of true profitability of the promotions, and why.

|              |
|--------------|
| Answer here… |
