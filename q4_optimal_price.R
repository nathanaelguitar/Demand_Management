# ============================================================================
# Question 4: Optimal Manufacturer Selling Price (R Version)
# ============================================================================
# Determine the optimal selling price of the manufacturer for an average week.
#
# Uses the semi-log demand models estimated in Q2 (re-estimated from the raw
# data) and finds the manufacturer unit price that maximises weekly profit
# under two scenarios:
#
#   4(a) Private label retail price is fixed at the historical average.
#   4(b) Private label retail price is always $0.35 below Brand 1 retail price.
#
# Assumptions:
#   - The retailer maintains its historical average margin % on Brand 1.
#   - Manufacturing cost per case is the average from the data.
#   - Selling cost is $10.00 per case ($0.4167 per unit).
#   - 24 units per case.
#
# R implementation, a companion to the Python version in this repo.
# ============================================================================

library(readxl)
library(broom)

# ============================================================================
# Constants
# ============================================================================
UNITS_PER_CASE        <- 24
SELLING_COST_PER_CASE <- 10.00
SELLING_COST_PER_UNIT <- SELLING_COST_PER_CASE / UNITS_PER_CASE

# ============================================================================
# Data Loading and Processing
# ============================================================================

load_data <- function(file_path = "bana6390_u2_assignment.xlsx") {
  df_raw <- read_excel(file_path, sheet = "Original Data", skip = 3)

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

  df <- df_raw[, c("Week", "PrivateLabel_Retail_Price", "PrivateLabel_Cases_Sold",
                   "PrivateLabel_Retailer_Cost", "Brand1_Retail_Price", "Brand1_Cases_Sold",
                   "Brand1_Retailer_Cost", "Brand1_Manufacturing_Cost")]

  for (col in names(df)) df[[col]] <- as.numeric(df[[col]])
  df <- df[!is.na(df$Week), ]
  df$Week <- as.integer(df$Week)

  # Unit conversions
  df$Brand1_Units_Sold       <- df$Brand1_Cases_Sold     * UNITS_PER_CASE
  df$PrivateLabel_Units_Sold <- df$PrivateLabel_Cases_Sold * UNITS_PER_CASE
  df$Brand1_Unit_Cost        <- df$Brand1_Retailer_Cost   / UNITS_PER_CASE
  df$PrivateLabel_Unit_Cost  <- df$PrivateLabel_Retailer_Cost / UNITS_PER_CASE
  df$Brand1_Mfg_Cost_Per_Unit <- df$Brand1_Manufacturing_Cost / UNITS_PER_CASE

  # Margins
  df$Brand1_Margin_Pct <- ((df$Brand1_Retail_Price - df$Brand1_Unit_Cost) /
                             df$Brand1_Retail_Price) * 100

  return(df)
}

# ============================================================================
# Demand Models — semi-log (Q2)
# ============================================================================

estimate_demand_models <- function(df) {
  df$ln_Brand1_Units <- log(df$Brand1_Units_Sold)
  df$ln_PL_Units     <- log(df$PrivateLabel_Units_Sold)

  model_b1 <- lm(ln_Brand1_Units ~ Brand1_Retail_Price + PrivateLabel_Retail_Price, data = df)
  model_pl <- lm(ln_PL_Units     ~ Brand1_Retail_Price + PrivateLabel_Retail_Price, data = df)

  return(list(brand1 = model_b1, pl = model_pl))
}

predict_units <- function(model, brand1_price, pl_price) {
  new_data <- data.frame(
    Brand1_Retail_Price       = brand1_price,
    PrivateLabel_Retail_Price = pl_price
  )
  exp(predict(model, newdata = new_data))
}

# ============================================================================
# Manufacturer Profit Functions
# ============================================================================

mfg_profit <- function(mfg_price, brand1_retail, pl_retail, model_b1, mfg_cost) {
  units <- predict_units(model_b1, brand1_retail, pl_retail)
  (mfg_price - mfg_cost - SELLING_COST_PER_UNIT) * units
}

# ============================================================================
# Optimisation — Scenario 4(a): PL price fixed at historical average
# ============================================================================

optimize_scenario_a <- function(model_b1, avg_pl_price, margin_pct, mfg_cost) {
  neg_profit_a <- function(mfg_price) {
    b1_retail <- mfg_price / (1 - margin_pct)
    -mfg_profit(mfg_price, b1_retail, avg_pl_price, model_b1, mfg_cost)
  }

  result <- optimize(neg_profit_a, interval = c(0.50, 5.00))
  list(
    mfg_price    = result$minimum,
    retail_price = result$minimum / (1 - margin_pct),
    profit       = -result$objective
  )
}

# ============================================================================
# Optimisation — Scenario 4(b): PL price = Brand 1 retail − $0.35
# ============================================================================

optimize_scenario_b <- function(model_b1, margin_pct, mfg_cost) {
  neg_profit_b <- function(mfg_price) {
    b1_retail <- mfg_price / (1 - margin_pct)
    pl_retail <- b1_retail - 0.35
    -mfg_profit(mfg_price, b1_retail, pl_retail, model_b1, mfg_cost)
  }

  result <- optimize(neg_profit_b, interval = c(0.50, 5.00))
  b1_retail <- result$minimum / (1 - margin_pct)
  list(
    mfg_price    = result$minimum,
    retail_price = b1_retail,
    pl_retail    = b1_retail - 0.35,
    profit       = -result$objective
  )
}

# ============================================================================
# Main
# ============================================================================

main <- function() {
  df     <- load_data()
  models <- estimate_demand_models(df)

  margin_pct   <- mean(df$Brand1_Margin_Pct, na.rm = TRUE) / 100
  avg_pl_price <- mean(df$PrivateLabel_Retail_Price, na.rm = TRUE)
  avg_pl_cost  <- mean(df$PrivateLabel_Unit_Cost, na.rm = TRUE)
  mfg_cost     <- mean(df$Brand1_Mfg_Cost_Per_Unit, na.rm = TRUE)

  # Current situation baseline
  current_mfg_price  <- mean(df$Brand1_Retail_Price, na.rm = TRUE) * (1 - margin_pct)
  current_b1_retail  <- mean(df$Brand1_Retail_Price, na.rm = TRUE)
  current_profit     <- mfg_profit(current_mfg_price, current_b1_retail,
                                   avg_pl_price, models$brand1, mfg_cost)

  opt_a <- optimize_scenario_a(models$brand1, avg_pl_price, margin_pct, mfg_cost)
  opt_b <- optimize_scenario_b(models$brand1, margin_pct, mfg_cost)

  # ---- Print Results -------------------------------------------------------
  cat(strrep("=", 80), "\n")
  cat("QUESTION 4: OPTIMAL MANUFACTURER SELLING PRICE\n")
  cat(strrep("=", 80), "\n")

  cat("\n--- Assumptions ---\n")
  cat(sprintf("  Retailer margin goal (Brand 1 avg):  %.2f%%\n", margin_pct * 100))
  cat(sprintf("  Average PL retail price:             $%.4f\n", avg_pl_price))
  cat(sprintf("  Average PL cost to retailer (unit):  $%.4f\n", avg_pl_cost))
  cat(sprintf("  Brand 1 mfg cost per unit:           $%.4f\n", mfg_cost))
  cat(sprintf("  Selling cost per unit:               $%.4f\n", SELLING_COST_PER_UNIT))

  b1_coefs <- coef(models$brand1)
  pl_coefs <- coef(models$pl)
  cat("\n--- Demand Model Coefficients (re-estimated from raw data) ---\n")
  cat(sprintf("  Brand 1: ln(Units) = %.4f + (%.4f) x B1_Price + (%.4f) x PL_Price\n",
              b1_coefs[1], b1_coefs["Brand1_Retail_Price"],
              b1_coefs["PrivateLabel_Retail_Price"]))
  cat(sprintf("  PL:      ln(Units) = %.4f + (%.4f) x PL_Price + (%.4f) x B1_Price\n",
              pl_coefs[1], pl_coefs["PrivateLabel_Retail_Price"],
              pl_coefs["Brand1_Retail_Price"]))

  cat("\n", strrep("=", 80), "\n", sep = "")
  cat("SCENARIO 4(a): PL retail price fixed at historical average\n")
  cat(strrep("=", 80), "\n")
  cat(sprintf("  Optimal mfg price per unit:      $%.4f\n", opt_a$mfg_price))
  cat(sprintf("  Implied Brand 1 retail price:    $%.4f\n", opt_a$retail_price))
  cat(sprintf("  PL retail price (fixed):         $%.4f\n", avg_pl_price))
  cat(sprintf("  Max manufacturer weekly profit:  $%.2f\n", opt_a$profit))

  cat("\n", strrep("=", 80), "\n", sep = "")
  cat("SCENARIO 4(b): PL retail price = Brand 1 retail price - $0.35\n")
  cat(strrep("=", 80), "\n")
  cat(sprintf("  Optimal mfg price per unit:      $%.4f\n", opt_b$mfg_price))
  cat(sprintf("  Implied Brand 1 retail price:    $%.4f\n", opt_b$retail_price))
  cat(sprintf("  Implied PL retail price:         $%.4f\n", opt_b$pl_retail))
  cat(sprintf("  Max manufacturer weekly profit:  $%.2f\n", opt_b$profit))

  cat("\n", strrep("=", 80), "\n", sep = "")
  cat("COMPARISON WITH CURRENT SITUATION\n")
  cat(strrep("=", 80), "\n")
  cat(sprintf("  Current avg mfg price per unit:  $%.4f\n", current_mfg_price))
  cat(sprintf("  Current avg mfg weekly profit:   $%.2f\n", current_profit))
  cat(sprintf("  Scenario 4(a) improvement:       $%+.2f (%+.1f%%)\n",
              opt_a$profit - current_profit,
              (opt_a$profit / current_profit - 1) * 100))
  cat(sprintf("  Scenario 4(b) improvement:       $%+.2f (%+.1f%%)\n",
              opt_b$profit - current_profit,
              (opt_b$profit / current_profit - 1) * 100))
  cat(strrep("=", 80), "\n")

  invisible(list(scenario_a = opt_a, scenario_b = opt_b))
}

main()
