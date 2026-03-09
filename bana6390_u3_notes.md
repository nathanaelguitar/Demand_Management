# BANA 6390 Unit 3 Notes

## Unit 3: Digital Advertising Analytics

These notes were cleaned and condensed from `BANA6390_U3_course-transcript.pdf`.

## What Unit 3 Covers

Unit 3 focuses on how to evaluate digital advertising performance using:

- Sponsored search and display advertising concepts
- Advertising effectiveness and efficiency metrics
- Multi-touch attribution models
- Randomized field experiments for causal measurement

## Learning Objectives

By the end of Unit 3, you should be able to:

- Compute sponsored search performance metrics
- Evaluate return on advertising spend using contribution margin
- Assign conversion credit across multiple digital touchpoints
- Understand when to use rules-based versus data-driven attribution
- Design and interpret randomized field experiments for advertising

## Core Concepts

### Two-Sided Markets

Many digital platforms are two-sided markets. They serve consumers on one side and advertisers on the other.

- Consumers often receive content or services for free
- Advertisers pay to access consumer attention
- Examples: Google, Facebook, Instagram, LinkedIn, newspapers

### Sponsored Search Advertising

Sponsored search ads appear on search engine results pages (SERPs) above or alongside organic results.

- Advertisers bid on keywords
- Ads are shown when users search those terms
- Advertisers usually pay when a user clicks
- This allows firms to target consumer intent at the moment of search

### SEO vs. Sponsored Search

**SEO**

- Improves rank in organic search results
- Slower, less controllable, longer-term

**Sponsored Search**

- Uses paid placement on the SERP
- Faster, more controllable, auction-driven

### Google Ad Auction

Sponsored search uses a generalized second-price sealed-bid auction.

- `Generalized`: multiple ad slots are auctioned
- `Second-price`: winners pay roughly enough to beat the next bidder
- `Sealed-bid`: advertisers know their own bid, not competitors' bids

Higher placement usually costs more but tends to produce more clicks.

## Advertising Funnel

Professor Gupta frames digital ad response in three stages:

1. `Exposure / Attention`: an impression is created
2. `Engagement`: the user clicks the ad
3. `Behavior`: the user converts

This process is not always linear. A user may convert without clicking if they were influenced earlier.

## Key Metrics

### Effectiveness Metrics

- `CTR (Click-Through Rate)` = clicks / impressions
- `TCR (Transaction Conversion Rate)` = transactions / clicks
- `TPI (Transactions Per Impression)` = transactions / impressions

How to interpret them:

- Low `CTR` can signal weak targeting or weak ad creative
- Low `TCR` can signal a landing page or offer problem
- `TPI` summarizes total funnel performance

### Efficiency Metrics

- `CPM` = campaign cost / impressions * 1000
- `CPC` = campaign cost / clicks
- `Cost per transaction` = campaign cost / transactions

Cost per transaction can also function like customer acquisition cost when the goal is acquiring new customers.

### Return on Ad Dollars Spent

`ROA = (A - B) / B`

Where:

- `A` = contribution margin dollars attributed to the campaign
- `B` = advertising cost

Example from the transcript:

- Campaign cost = `$100`
- Revenue attributed to campaign = `$1,000`
- Contribution margin = `25%`
- Contribution margin dollars = `$250`
- `ROA = (250 - 100) / 100 = 150%`

Interpretation: each `$1` spent generated `$1.50` in incremental contribution after ad cost.

## Air World Case

The Air World case uses sponsored search campaign data with these variables:

- Search engine
- Keyword
- Impressions
- Clicks
- Transactions
- Click charges
- Revenue

Case setup from the activity document:

- Air World is trying to increase travelers from North America to Europe
- The campaign ran for one month
- Ads were purchased on Google and MSN Bing in both the U.S. and Europe
- Pricing is `cost per click`, so clicks generate cost but impressions alone do not
- The data are hypothetical but modeled after real campaign data

The case is mainly used to practice pivot tables and metric computation.

Typical analyses include:

- Summarizing performance by search engine
- Calculating aggregate-first metrics such as `CPC`, `CPI`, `CPT`, `CTR`, `TCR`, and `TPI`
- Sorting keywords or engines by clicks, cost, or revenue
- Ranking the top 10 keywords by clicks across search engines
- Computing `ROA` for keywords; in the case activity, assume contribution margin is `100%`

## Display Advertising Ecosystem

Unit 3 also introduces display advertising as another major digital ad format. Compared with search, display ads are more focused on exposure and audience targeting, while search is tightly linked to active consumer intent.

## Multi-Touch Attribution (MTA)

Many customers see several ads before converting. Multi-touch attribution determines how much credit each touchpoint should receive.

### Rules-Based Attribution

Rules-based attribution assigns credit using a predefined rule tied to the advertiser's objective.

Common rules:

- `Last touch`: all credit goes to the final touchpoint
- `First touch`: all credit goes to the first touchpoint
- `Linear`: equal credit across touchpoints
- `Time decay`: more recent touchpoints get more credit

Example sequence before a `$100` purchase:

1. Search ad
2. Display ad
3. Social media ad
4. Display ad

Credit outcomes:

- `First touch`: search gets 100%
- `Last touch`: final display gets 100%
- `Linear`: each touch gets `$25`

Why last-touch is common:

- It is simple
- Firms often observe the final click more easily than the full path

### Data-Driven Attribution

Data-driven MTA uses statistical models to estimate how ad exposures change purchase probability.

It has two steps:

1. `Response modeling`: estimate how advertising affects conversion probability
2. `Credit allocation`: assign incremental conversion credit to ad exposures

Important features the model should capture:

- Carryover effects
- Intensity of exposures
- Timing of exposures
- Competitive ads
- User heterogeneity

#### JD.com Example

The transcript uses a JD.com case on cell phone purchases.

- Tens of millions of users were observed
- Billions of ad impressions were available
- Researchers modeled purchase probability using a recurrent neural network (`RNN`)
- Credit allocation used `Shapley values`

Key takeaway:

- Data-driven attribution can produce very different credit allocation than last-touch attribution
- It is richer and more realistic, but requires large datasets and more computation

## Randomized Field Experiments

Field experiments are presented as the gold standard for estimating causal advertising effects.

### Why Experiments Matter

Observational data can show correlation, but not necessarily causation. Experiments help isolate the true impact of advertising by comparing treatment and control groups.

### Facebook Example

The course discusses large-scale Facebook field experiments to estimate incremental advertising effects. The central idea is to compare exposed and unexposed groups so the analyst can measure incremental outcomes attributable to the campaign.

### eBay Example

eBay tested whether branded paid search keywords were actually useful.

Design:

- Pause branded keyword ads on one search engine
- Keep them active on another
- Compare click traffic outcomes

Finding:

- When branded paid search was paused, organic traffic increased sharply
- This indicated high substitution between paid and organic traffic
- Conclusion: branded keyword search ads created little measurable incremental sales

Managerial implication:

- eBay cut branded paid search spending significantly

## Challenges With Field Experiments

Field experiments are powerful, but they come with practical issues:

- `Large samples required`: ad effects per impression are usually small
- `Foregone revenue`: control groups may miss incremental sales
- `Platform control issues`: advertisers often do not fully control delivery algorithms

This means experiments can be expensive and operationally difficult even when they are analytically strong.

## Chi-Square Demonstration

The unit also includes an Excel demo on cross-tabulation and the chi-square test for categorical variables.

Main lesson:

- Use pivot tables to build contingency tables
- Compare observed counts with expected counts under independence
- Use `CHISQ.TEST` in Excel to test dependence

This is relevant when evaluating relationships between categorical variables in marketing data.

## Unit 3 Assignment

The final assignment asks students to analyze an A/B test for a restaurant chain and compare two advertising campaigns.

You are expected to:

- Read the assignment document
- Analyze the provided dataset
- Interpret the A/B test results
- Submit answers in a document format such as `.doc`, `.docx`, or `.pdf`

## Main Takeaways

- Digital advertising produces rich behavioral data
- Search ads are powerful because they target consumer intent
- Metrics should separate effectiveness from efficiency
- `ROA` links ad performance to business value
- Attribution is necessary when multiple touchpoints influence conversion
- Rules-based attribution is simpler; data-driven attribution is more realistic
- Randomized field experiments are the strongest method for causal measurement
