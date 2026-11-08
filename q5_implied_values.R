# ============================================================================
# Question 5: Implied Values at Optimal Prices (R Version)
# ============================================================================
# Compute the "implied" values of different variables at the optimal prices
# in each of scenarios 4(a) and 4(b), and compare them with the current situation.
#
# R implementation, a companion to the Python version in this repo.
# ============================================================================

library(readxl)
library(broom)

# ============================================================================
# Constants
# ============================================================================
UNITS_PER_CASE <- 24
SELLING_COST_PER_CASE <- 10.00
SELLING_COST_PER_UNIT <- SELLING_COST_PER_CASE / UNITS_PER_CASE

# ============================================================================
# Data Loading and Processing
# ============================================================================

load_data <- function(file_path = "bana6390_u2_assignment.xlsx") {
  # Read the raw data
  df_raw <- read_excel(file_path, sheet = "Original Data", skip = 3)
  
  # Assign column names
  colnames(df_raw) <- c(
    "Week",
    "PrivateLabel_Retail_Price",
    "PrivateLabel_Cases_Sold",
    "PrivateLabel_Units_Sold_Ignore",
    "PrivateLabel_Retailer_Cost",
    "Brand1_Retail_Price",
    "Brand1_Cases_Sold",
    "Brand1_Units_Sold_Ignore",
    "Brand1_Retailer_Cost",
    "Brand1_Manufacturing_Cost"
  )
  
  # Keep relevant columns
  df <- df_raw[, c("Week", "PrivateLabel_Retail_Price", "PrivateLabel_Cases_Sold",
                   "PrivateLabel_Retailer_Cost", "Brand1_Retail_Price", "Brand1_Cases_Sold",
                   "Brand1_Retailer_Cost", "Brand1_Manufacturing_Cost")]
  
  # Convert to numeric
  for (col in names(df)) {
    df[[col]] <- as.numeric(df[[col]])
  }
  
  # Remove NAs in Week
  df <- df[!is.na(df$Week), ]
  df$Week <- as.integer(df$Week)
  
  # Convert cases to units
  df$Brand1_Units_Sold <- df$Brand1_Cases_Sold * UNITS_PER_CASE
  df$PrivateLabel_Units_Sold <- df$PrivateLabel_Cases_Sold * UNITS_PER_CASE
  df$Brand1_Unit_Cost <- df$Brand1_Retailer_Cost / UNITS_PER_CASE
  df$PrivateLabel_Unit_Cost <- df$PrivateLabel_Retailer_Cost / UNITS_PER_CASE
  df$Brand1_Mfg_Cost_Per_Unit <- df$Brand1_Manufacturing_Cost / UNITS_PER_CASE
  
  # Calculate margins
  df$Brand1_Retail_Margin <- df$Brand1_Retail_Price - df$Brand1_Unit_Cost
  df$PrivateLabel_Retail_Margin <- df$PrivateLabel_Retail_Price - df$PrivateLabel_Unit_Cost
  df$Brand1_Margin_Pct <- (df$Brand1_Retail_Margin / df$Brand1_Retail_Price) * 100
  df$PrivateLabel_Margin_Pct <- (df$PrivateLabel_Retail_Margin / df$PrivateLabel_Retail_Price) * 100
  
  # Calculate totals and shares
  df$Total_Units_Sold <- df$Brand1_Units_Sold + df$PrivateLabel_Units_Sold
  df$Brand1_Share <- (df$Brand1_Units_Sold / df$Total_Units_Sold) * 100
  df$PrivateLabel_Share <- (df$PrivateLabel_Units_Sold / df$Total_Units_Sold) * 100
  df$Price_Gap <- df$Brand1_Retail_Price - df$PrivateLabel_Retail_Price
  
  # Calculate profits
  df$Retailer_Profit_Brand1 <- df$Brand1_Retail_Margin * df$Brand1_Units_Sold
  df$Retailer_Profit_PL <- df$PrivateLabel_Retail_Margin * df$PrivateLabel_Units_Sold
  df$Retailer_Total_Profit <- df$Retailer_Profit_Brand1 + df$Retailer_Profit_PL
  df$Brand1_Mfg_Profit <- (df$Brand1_Unit_Cost - df$Brand1_Mfg_Cost_Per_Unit - SELLING_COST_PER_UNIT) * df$Brand1_Units_Sold
  
  return(df)
}

# ============================================================================
# Current Situation (Q1)
# ============================================================================

compute_current_situation <- function(df) {
  current <- list(
    brand1_units = mean(df$Brand1_Units_Sold, na.rm = TRUE),
    pl_units = mean(df$PrivateLabel_Units_Sold, na.rm = TRUE),
    brand1_share = mean(df$Brand1_Share, na.rm = TRUE),
    pl_share = mean(df$PrivateLabel_Share, na.rm = TRUE),
    retailer_profit = mean(df$Retailer_Total_Profit, na.rm = TRUE),
    manufacturer_profit = mean(df$Brand1_Mfg_Profit, na.rm = TRUE)
  )
  return(current)
}

# ============================================================================
# Demand Models (Q2)
# ============================================================================

estimate_demand_models <- function(df) {
  # Create log of sales for semi-log model
  df$ln_Brand1_Sales <- log(df$Brand1_Units_Sold)
  df$ln_PL_Sales <- log(df$PrivateLabel_Units_Sold)
  
  # Brand 1 demand model
  model_brand1 <- lm(ln_Brand1_Sales ~ Brand1_Retail_Price + PrivateLabel_Retail_Price, data = df)
  
  # Private Label demand model
  model_pl <- lm(ln_PL_Sales ~ Brand1_Retail_Price + PrivateLabel_Retail_Price, data = df)
  
  cat("\n")
  cat(strrep("=", 80), "\n")
  cat("BRAND 1 DEMAND MODEL\n")
  cat(strrep("=", 80), "\n")
  print(summary(model_brand1))
  
  cat("\n")
  cat(strrep("=", 80), "\n")
  cat("PRIVATE LABEL DEMAND MODEL\n")
  cat(strrep("=", 80), "\n")
  print(summary(model_pl))
  
  return(list(brand1 = model_brand1, pl = model_pl))
}

# ============================================================================
# Helper Functions
# ============================================================================

predict_units <- function(model, brand1_price, pl_price) {
  # Create data frame with new values
  new_data <- data.frame(
    Brand1_Retail_Price = brand1_price,
    PrivateLabel_Retail_Price = pl_price
  )
  
  # Predict log(units)
  ln_units <- predict(model, newdata = new_data)
  
  # Exponentiate to get units
  return(exp(ln_units))
}

compute_retailer_margin_goal <- function(df) {
  return(mean(df$Brand1_Margin_Pct, na.rm = TRUE) / 100)
}

compute_avg_pl_cost <- function(df) {
  return(mean(df$PrivateLabel_Unit_Cost, na.rm = TRUE))
}

compute_avg_pl_retail_price <- function(df) {
  return(mean(df$PrivateLabel_Retail_Price, na.rm = TRUE))
}

compute_avg_brand1_mfg_cost_per_unit <- function(df) {
  return(mean(df$Brand1_Mfg_Cost_Per_Unit, na.rm = TRUE))
}

# ============================================================================
# Optimization Functions (Q4)
# ============================================================================

manufacturer_profit_scenario_a <- function(mfg_price, model_brand1, avg_pl_price, 
                                           margin_pct, mfg_cost_per_unit) {
  # Retailer sets retail price based on margin goal
  brand1_retail_price <- mfg_price / (1 - margin_pct)
  
  # Predicted Brand 1 unit sales
  brand1_units <- predict_units(model_brand1, brand1_retail_price, avg_pl_price)
  
  # Manufacturer profit
  profit_per_unit <- mfg_price - mfg_cost_per_unit - SELLING_COST_PER_UNIT
  total_profit <- profit_per_unit * brand1_units
  
  return(total_profit)
}

manufacturer_profit_scenario_b <- function(mfg_price, model_brand1, model_pl,
                                           margin_pct, mfg_cost_per_unit) {
  # Retailer sets retail price based on margin goal
  brand1_retail_price <- mfg_price / (1 - margin_pct)
  pl_retail_price <- brand1_retail_price - 0.35
  
  # Predicted Brand 1 unit sales
  brand1_units <- predict_units(model_brand1, brand1_retail_price, pl_retail_price)
  
  # Manufacturer profit
  profit_per_unit <- mfg_price - mfg_cost_per_unit - SELLING_COST_PER_UNIT
  total_profit <- profit_per_unit * brand1_units
  
  return(total_profit)
}

find_optimal_price_scenario_a <- function(model_brand1, avg_pl_price, margin_pct, mfg_cost_per_unit) {
  # Negative profit function for minimization
  neg_profit_fn <- function(price) {
    -manufacturer_profit_scenario_a(price, model_brand1, avg_pl_price, margin_pct, mfg_cost_per_unit)
  }
  
  # Optimize
  result <- optim(c(1.5), neg_profit_fn, method = "Brent", 
                  lower = 0.5, upper = 5.0)
  
  optimal_price <- result$par[1]
  optimal_profit <- -result$value
  
  return(list(price = optimal_price, profit = optimal_profit))
}

find_optimal_price_scenario_b <- function(model_brand1, model_pl, margin_pct, mfg_cost_per_unit) {
  # Negative profit function for minimization
  neg_profit_fn <- function(price) {
    -manufacturer_profit_scenario_b(price, model_brand1, model_pl, margin_pct, mfg_cost_per_unit)
  }
  
  # Optimize
  result <- optim(c(1.5), neg_profit_fn, method = "Brent",
                  lower = 0.5, upper = 5.0)
  
  optimal_price <- result$par[1]
  optimal_profit <- -result$value
  
  return(list(price = optimal_price, profit = optimal_profit))
}

# ============================================================================
# Q5: Compute Implied Values
# ============================================================================

compute_implied_values <- function(scenario_label, optimal_mfg_price, brand1_retail_price, 
                                   pl_retail_price, model_brand1, model_pl, 
                                   avg_pl_cost, mfg_cost_per_unit) {
  # Predicted unit sales
  brand1_units <- predict_units(model_brand1, brand1_retail_price, pl_retail_price)
  pl_units <- predict_units(model_pl, brand1_retail_price, pl_retail_price)
  total_units <- brand1_units + pl_units
  
  # Market shares
  brand1_share <- (brand1_units / total_units) * 100
  pl_share <- (pl_units / total_units) * 100
  
  # Retailer profit
  retailer_profit_brand1 <- (brand1_retail_price - optimal_mfg_price) * brand1_units
  retailer_profit_pl <- (pl_retail_price - avg_pl_cost) * pl_units
  retailer_total_profit <- retailer_profit_brand1 + retailer_profit_pl
  
  # Manufacturer profit
  mfg_profit_per_unit <- optimal_mfg_price - mfg_cost_per_unit - SELLING_COST_PER_UNIT
  manufacturer_profit <- mfg_profit_per_unit * brand1_units
  
  return(list(
    scenario = scenario_label,
    optimal_mfg_price = optimal_mfg_price,
    brand1_retail_price = brand1_retail_price,
    pl_retail_price = pl_retail_price,
    brand1_units = brand1_units,
    pl_units = pl_units,
    brand1_share = brand1_share,
    pl_share = pl_share,
    retailer_profit = retailer_total_profit,
    manufacturer_profit = manufacturer_profit
  ))
}

# ============================================================================
# Printing Functions
# ============================================================================

print_comparison_table <- function(implied_a, implied_b, current) {
  cat("\n")
  cat(strrep("=", 90), "\n")
  cat("QUESTION 5: COMPARISON TABLE — TYPICAL WEEK\n")
  cat(strrep("=", 90), "\n")
  
  # Create data for the table
  metrics <- c(
    "Optimal Mfg Price (per unit)",
    "Brand 1 Retail Price",
    "PL Retail Price",
    "",
    "Units sold — Brand 1",
    "Units sold — Private Label",
    "",
    "Market share — Brand 1",
    "Market share — Private Label",
    "",
    "Weekly Retailer Profit",
    "Weekly Manufacturer Profit"
  )
  
  scenario_a_vals <- c(
    sprintf("$%.2f", implied_a$optimal_mfg_price),
    sprintf("$%.2f", implied_a$brand1_retail_price),
    sprintf("$%.2f", implied_a$pl_retail_price),
    "",
    sprintf("%.0f", implied_a$brand1_units),
    sprintf("%.0f", implied_a$pl_units),
    "",
    sprintf("%.2f%%", implied_a$brand1_share),
    sprintf("%.2f%%", implied_a$pl_share),
    "",
    sprintf("$%.2f", implied_a$retailer_profit),
    sprintf("$%.2f", implied_a$manufacturer_profit)
  )
  
  scenario_b_vals <- c(
    sprintf("$%.2f", implied_b$optimal_mfg_price),
    sprintf("$%.2f", implied_b$brand1_retail_price),
    sprintf("$%.2f", implied_b$pl_retail_price),
    "",
    sprintf("%.0f", implied_b$brand1_units),
    sprintf("%.0f", implied_b$pl_units),
    "",
    sprintf("%.2f%%", implied_b$brand1_share),
    sprintf("%.2f%%", implied_b$pl_share),
    "",
    sprintf("$%.2f", implied_b$retailer_profit),
    sprintf("$%.2f", implied_b$manufacturer_profit)
  )
  
  current_vals <- c(
    "N/A",
    "N/A",
    "N/A",
    "",
    sprintf("%.0f", current$brand1_units),
    sprintf("%.0f", current$pl_units),
    "",
    sprintf("%.2f%%", current$brand1_share),
    sprintf("%.2f%%", current$pl_share),
    "",
    sprintf("$%.2f", current$retailer_profit),
    sprintf("$%.2f", current$manufacturer_profit)
  )
  
  # Print header
  cat(sprintf("%-50s | %14s | %14s | %14s\n", 
              "", "Scenario 4(a)", "Scenario 4(b)", "Current (Q1)"))
  cat(strrep("-", 50), "-+-", strrep("-", 14), "-+-", strrep("-", 14), "-+-", strrep("-", 14), "\n", sep = "")
  
  # Print rows
  for (i in seq_along(metrics)) {
    cat(sprintf("%-50s | %14s | %14s | %14s\n",
                metrics[i], scenario_a_vals[i], scenario_b_vals[i], current_vals[i]))
  }
  
  cat(strrep("-", 50), "-+-", strrep("-", 14), "-+-", strrep("-", 14), "-+-", strrep("-", 14), "\n", sep = "")
}

print_concerns <- function() {
  cat("\n")
  cat(strrep("=", 90), "\n")
  cat("CONCERNS ABOUT SCENARIO ASSUMPTIONS\n")
  cat(strrep("=", 90), "\n")
  
  cat("
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
")
}

# ============================================================================
# Main Execution
# ============================================================================

main <- function() {
  cat("\n")
  cat(strrep("=", 80), "\n")
  cat("QUESTION 5: IMPLIED VALUES AT OPTIMAL PRICES (R VERSION)\n")
  cat(strrep("=", 80), "\n")
  
  # Load data
  df <- load_data()
  cat("\nData loaded: ", nrow(df), " observations\n")
  
  # Compute current situation
  current <- compute_current_situation(df)
  
  # Estimate demand models
  models <- estimate_demand_models(df)
  
  # Compute inputs
  margin_pct <- compute_retailer_margin_goal(df)
  avg_pl_price <- compute_avg_pl_retail_price(df)
  avg_pl_cost <- compute_avg_pl_cost(df)
  mfg_cost_per_unit <- compute_avg_brand1_mfg_cost_per_unit(df)
  
  cat("\nRetailer margin goal (Brand 1 avg):", sprintf("%.2f%%", margin_pct * 100), "\n")
  cat("Average PL retail price:           ", sprintf("$%.2f", avg_pl_price), "\n")
  cat("Average PL cost to retailer (unit):", sprintf("$%.4f", avg_pl_cost), "\n")
  cat("Brand 1 mfg cost per unit:         ", sprintf("$%.4f", mfg_cost_per_unit), "\n")
  cat("Selling cost per unit:             ", sprintf("$%.4f", SELLING_COST_PER_UNIT), "\n")
  
  # Scenario 4(a)
  cat("\n")
  cat(strrep("=", 80), "\n")
  cat("SCENARIO 4(a): PL price fixed at average\n")
  cat(strrep("=", 80), "\n")
  
  result_a <- find_optimal_price_scenario_a(models$brand1, avg_pl_price, margin_pct, mfg_cost_per_unit)
  brand1_retail_a <- result_a$price / (1 - margin_pct)
  
  cat("Optimal mfg price per unit:   ", sprintf("$%.4f", result_a$price), "\n")
  cat("Implied Brand 1 retail price: ", sprintf("$%.4f", brand1_retail_a), "\n")
  cat("PL retail price (fixed):      ", sprintf("$%.4f", avg_pl_price), "\n")
  cat("Max manufacturer profit:      ", sprintf("$%.2f", result_a$profit), "\n")
  
  # Scenario 4(b)
  cat("\n")
  cat(strrep("=", 80), "\n")
  cat("SCENARIO 4(b): PL price = Brand 1 price - $0.35\n")
  cat(strrep("=", 80), "\n")
  
  result_b <- find_optimal_price_scenario_b(models$brand1, models$pl, margin_pct, mfg_cost_per_unit)
  brand1_retail_b <- result_b$price / (1 - margin_pct)
  pl_retail_b <- brand1_retail_b - 0.35
  
  cat("Optimal mfg price per unit:   ", sprintf("$%.4f", result_b$price), "\n")
  cat("Implied Brand 1 retail price: ", sprintf("$%.4f", brand1_retail_b), "\n")
  cat("Implied PL retail price:      ", sprintf("$%.4f", pl_retail_b), "\n")
  cat("Max manufacturer profit:      ", sprintf("$%.2f", result_b$profit), "\n")
  
  # Compute implied values
  implied_a <- compute_implied_values(
    "Scenario 4(a)", result_a$price, brand1_retail_a, avg_pl_price,
    models$brand1, models$pl, avg_pl_cost, mfg_cost_per_unit
  )
  
  implied_b <- compute_implied_values(
    "Scenario 4(b)", result_b$price, brand1_retail_b, pl_retail_b,
    models$brand1, models$pl, avg_pl_cost, mfg_cost_per_unit
  )
  
  # Print comparison table and concerns
  print_comparison_table(implied_a, implied_b, current)
  print_concerns()
  
  cat("\n")
  cat("(R version completed successfully!)\n")
  cat("\n")
  
  return(list(implied_a = implied_a, implied_b = implied_b, current = current))
}

# Run the analysis
if (!interactive()) {
  results <- main()
}
