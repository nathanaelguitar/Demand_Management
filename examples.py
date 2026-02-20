"""
Quick reference guide for working with the pricing data
"""

import pandas as pd
from process_data import DataProcessor

# =============================================================================
# EXAMPLE 1: Load and process data directly from Excel
# =============================================================================

def load_data():
    """Load and process the pricing data directly from the Excel file."""
    processor = DataProcessor('bana6390_u2_assignment.xlsx')
    df_units = processor.get_dataframe()
    return df_units

# =============================================================================
# EXAMPLE 2: Access specific data
# =============================================================================

def example_data_access():
    """Examples of accessing specific data."""
    df = load_data()
    
    # Get Brand 1 prices and sales
    brand1_prices = df['Brand1_Retail_Price']
    brand1_sales = df['Brand1_Units_Sold']
    
    # Get Private Label prices and sales
    pl_prices = df['PrivateLabel_Retail_Price']
    pl_sales = df['PrivateLabel_Units_Sold']
    
    # Get profits
    retailer_profit = df['Retailer_Total_Profit']
    manufacturer_profit = df['Brand1_Mfg_Profit']
    
    return brand1_prices, brand1_sales, pl_prices, pl_sales

# =============================================================================
# EXAMPLE 3: Calculate custom metrics
# =============================================================================

def calculate_custom_metrics():
    """Calculate additional metrics."""
    df = load_data()
    
    # Calculate revenue
    df['Brand1_Revenue'] = df['Brand1_Retail_Price'] * df['Brand1_Units_Sold']
    df['PL_Revenue'] = df['PrivateLabel_Retail_Price'] * df['PrivateLabel_Units_Sold']
    df['Total_Revenue'] = df['Brand1_Revenue'] + df['PL_Revenue']
    
    # Calculate price ratio
    df['Price_Ratio'] = df['Brand1_Retail_Price'] / df['PrivateLabel_Retail_Price']
    
    return df

# =============================================================================
# EXAMPLE 4: Filter data
# =============================================================================

def filter_examples():
    """Examples of filtering data."""
    df = load_data()
    
    # Filter by week range
    early_weeks = df[df['Week'] <= 26]
    late_weeks = df[df['Week'] > 78]
    
    # Filter by price conditions
    low_pl_price = df[df['PrivateLabel_Retail_Price'] < 2.10]
    high_brand1_sales = df[df['Brand1_Units_Sold'] > 3000]
    
    # Combined conditions
    profitable_weeks = df[
        (df['Brand1_Mfg_Profit'] > 2000) & 
        (df['Brand1_Share'] > 45)
    ]
    
    return early_weeks, late_weeks, profitable_weeks

# =============================================================================
# EXAMPLE 5: Prepare data for regression
# =============================================================================

def prepare_for_regression():
    """Prepare data for demand modeling (semi-log regression)."""
    df = load_data()
    
    import numpy as np
    
    # Create log of sales for semi-log model
    df['ln_Brand1_Sales'] = np.log(df['Brand1_Units_Sold'])
    df['ln_PL_Sales'] = np.log(df['PrivateLabel_Units_Sold'])
    
    # Regression variables for Brand 1 demand
    y_brand1 = df['ln_Brand1_Sales']
    X_brand1 = df[['Brand1_Retail_Price', 'PrivateLabel_Retail_Price']]
    
    # Regression variables for Private Label demand
    y_pl = df['ln_PL_Sales']
    X_pl = df[['PrivateLabel_Retail_Price', 'Brand1_Retail_Price']]
    
    return X_brand1, y_brand1, X_pl, y_pl

# =============================================================================
# EXAMPLE 6: Summary statistics
# =============================================================================

def get_summary_stats():
    """Get summary statistics."""
    df = load_data()
    
    print("="*80)
    print("DESCRIPTIVE STATISTICS")
    print("="*80)
    
    # Overall summary
    print("\nOverall Data Summary:")
    print(df.describe())
    
    # Specific metrics
    print("\n" + "="*80)
    print("KEY METRICS")
    print("="*80)
    
    metrics = {
        'Average Brand 1 Price': df['Brand1_Retail_Price'].mean(),
        'Average PL Price': df['PrivateLabel_Retail_Price'].mean(),
        'Average Brand 1 Sales': df['Brand1_Units_Sold'].mean(),
        'Average PL Sales': df['PrivateLabel_Units_Sold'].mean(),
        'Average Brand 1 Share': df['Brand1_Share'].mean(),
        'Average PL Share': df['PrivateLabel_Share'].mean(),
        'Average Retailer Profit': df['Retailer_Total_Profit'].mean(),
        'Average Manufacturer Profit': df['Brand1_Mfg_Profit'].mean(),
    }
    
    for key, value in metrics.items():
        print(f"{key:.<40} {value:>10.2f}")
    
    return metrics

# =============================================================================
# EXAMPLE 7: Plotting data
# =============================================================================

def plot_sales_over_time():
    """Plot sales over time (requires matplotlib)."""
    try:
        import matplotlib.pyplot as plt
        
        df = load_data()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Plot 1: Unit sales over time
        ax1.plot(df['Week'], df['Brand1_Units_Sold'], label='Brand 1', marker='o', markersize=3)
        ax1.plot(df['Week'], df['PrivateLabel_Units_Sold'], label='Private Label', marker='s', markersize=3)
        ax1.set_xlabel('Week')
        ax1.set_ylabel('Unit Sales')
        ax1.set_title('Unit Sales Over Time')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Prices over time
        ax2.plot(df['Week'], df['Brand1_Retail_Price'], label='Brand 1', marker='o', markersize=3)
        ax2.plot(df['Week'], df['PrivateLabel_Retail_Price'], label='Private Label', marker='s', markersize=3)
        ax2.set_xlabel('Week')
        ax2.set_ylabel('Retail Price ($)')
        ax2.set_title('Retail Prices Over Time')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('sales_and_prices_over_time.png', dpi=300, bbox_inches='tight')
        print("\nPlot saved as 'sales_and_prices_over_time.png'")
        plt.show()
        
    except ImportError:
        print("Matplotlib not installed. Install with: pip install matplotlib")

# =============================================================================
# Main function
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("PRICING DATA - QUICK EXAMPLES")
    print("="*80)
    
    # Load data
    print("\n1. Loading data from CSV...")
    df = load_data()
    print(f"   Loaded {len(df)} rows and {len(df.columns)} columns")
    
    # Show summary stats
    print("\n2. Summary Statistics:")
    stats = get_summary_stats()
    
    # Show regression prep
    print("\n3. Preparing data for regression...")
    X_b1, y_b1, X_pl, y_pl = prepare_for_regression()
    print(f"   Brand 1 regression: {X_b1.shape} predictors, {len(y_b1)} observations")
    print(f"   Private Label regression: {X_pl.shape} predictors, {len(y_pl)} observations")
    
    print("\n" + "="*80)
    print("Examples complete! See code comments for more usage examples.")
    print("="*80)
