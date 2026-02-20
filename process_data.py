"""
Data Processing Layer for BANA6390 Unit 2 Assignment
Converts raw Excel data into clean DataFrames for analysis
"""

import pandas as pd
import numpy as np
from data_ingestion import DataIngestion
from typing import Tuple, Dict


class DataProcessor:
    """
    Processes raw data from the ingestion layer into clean DataFrames
    ready for pricing optimization analysis.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the data processor.
        
        Args:
            file_path: Path to the Excel file
        """
        self.ingestion = DataIngestion(file_path)
        self.clean_data = {}
    
    def load_and_clean_original_data(self) -> pd.DataFrame:
        """
        Load the original data and clean it for analysis.
        
        Returns:
            Clean DataFrame with properly named columns
        """
        # Read the raw data - structure is:
        # Row 0-2: Headers/titles
        # Row 3: Column headers
        # Row 4+: Data
        df_raw = pd.read_excel(
            self.ingestion.file_path,
            sheet_name='Original Data',
            skiprows=3  # Skip the title rows
        )
        
        # The data has this structure:
        # Col 0: Week
        # Col 1: PL Price per unit
        # Col 2: PL Sales (Cases)
        # Col 3: PL Sales (Units) - we'll ignore this as we can calculate it
        # Col 4: PL Cost per case to retailer
        # Col 5: Brand 1 Price per unit
        # Col 6: Brand 1 Sales (Cases)
        # Col 7: Brand 1 Sales (Units) - we'll ignore this
        # Col 8: Brand 1 Cost per case to retailer
        # Col 9: Brand 1 Manufacturing cost per case
        
        column_names = [
            'Week',
            'PrivateLabel_Retail_Price',
            'PrivateLabel_Cases_Sold',
            'PrivateLabel_Units_Sold_Ignore',
            'PrivateLabel_Retailer_Cost',
            'Brand1_Retail_Price',
            'Brand1_Cases_Sold',
            'Brand1_Units_Sold_Ignore',
            'Brand1_Retailer_Cost',
            'Brand1_Manufacturing_Cost'
        ]
        
        df_raw.columns = column_names
        
        # Keep only relevant columns (drop the pre-calculated units)
        relevant_cols = [
            'Week',
            'PrivateLabel_Retail_Price',
            'PrivateLabel_Cases_Sold',
            'PrivateLabel_Retailer_Cost',
            'Brand1_Retail_Price',
            'Brand1_Cases_Sold',
            'Brand1_Retailer_Cost',
            'Brand1_Manufacturing_Cost'
        ]
        
        df = df_raw[relevant_cols].copy()
        
        # Convert all columns to numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove any rows with all NaN values
        df = df.dropna(how='all')
        
        # Remove rows where Week is NaN
        df = df[df['Week'].notna()].copy()
        
        # Convert Week to integer
        df['Week'] = df['Week'].astype(int)
        
        # Reset index
        df = df.reset_index(drop=True)
        
        self.clean_data['original'] = df
        
        print(f"\nCleaned data shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print(f"Week range: {df['Week'].min()} to {df['Week'].max()}")
        
        return df
    
    def calculate_unit_level_data(self, df: pd.DataFrame, units_per_case: int = 24) -> pd.DataFrame:
        """
        Convert case-level data to unit-level data and add calculated fields.
        
        Args:
            df: DataFrame with case-level data
            units_per_case: Number of units per case (default: 24)
            
        Returns:
            DataFrame with unit-level calculations
        """
        df_units = df.copy()
        
        # Convert cases to units
        df_units['Brand1_Units_Sold'] = df_units['Brand1_Cases_Sold'] * units_per_case
        df_units['PrivateLabel_Units_Sold'] = df_units['PrivateLabel_Cases_Sold'] * units_per_case
        
        # Calculate per-unit costs
        df_units['Brand1_Unit_Cost'] = df_units['Brand1_Retailer_Cost'] / units_per_case
        df_units['PrivateLabel_Unit_Cost'] = df_units['PrivateLabel_Retailer_Cost'] / units_per_case
        df_units['Brand1_Mfg_Cost_Per_Unit'] = df_units['Brand1_Manufacturing_Cost'] / units_per_case
        
        # Calculate retail margins (per unit)
        df_units['Brand1_Retail_Margin'] = df_units['Brand1_Retail_Price'] - df_units['Brand1_Unit_Cost']
        df_units['PrivateLabel_Retail_Margin'] = df_units['PrivateLabel_Retail_Price'] - df_units['PrivateLabel_Unit_Cost']
        
        # Calculate percentage margins
        df_units['Brand1_Margin_Pct'] = (df_units['Brand1_Retail_Margin'] / df_units['Brand1_Retail_Price']) * 100
        df_units['PrivateLabel_Margin_Pct'] = (df_units['PrivateLabel_Retail_Margin'] / df_units['PrivateLabel_Retail_Price']) * 100
        
        # Calculate total category sales
        df_units['Total_Units_Sold'] = df_units['Brand1_Units_Sold'] + df_units['PrivateLabel_Units_Sold']
        
        # Calculate market shares
        df_units['Brand1_Share'] = (df_units['Brand1_Units_Sold'] / df_units['Total_Units_Sold']) * 100
        df_units['PrivateLabel_Share'] = (df_units['PrivateLabel_Units_Sold'] / df_units['Total_Units_Sold']) * 100
        
        # Calculate price gap
        df_units['Price_Gap'] = df_units['Brand1_Retail_Price'] - df_units['PrivateLabel_Retail_Price']
        
        # Calculate weekly profits
        # Retailer profit = (retail price - cost) * units sold for both brands
        df_units['Retailer_Profit_Brand1'] = df_units['Brand1_Retail_Margin'] * df_units['Brand1_Units_Sold']
        df_units['Retailer_Profit_PL'] = df_units['PrivateLabel_Retail_Margin'] * df_units['PrivateLabel_Units_Sold']
        df_units['Retailer_Total_Profit'] = df_units['Retailer_Profit_Brand1'] + df_units['Retailer_Profit_PL']
        
        # Manufacturer profit = (selling price to retailer - mfg cost - selling cost) * units sold
        # Selling cost is $10 per case = $10/24 per unit
        selling_cost_per_unit = 10.0 / units_per_case
        df_units['Brand1_Mfg_Profit'] = (
            df_units['Brand1_Unit_Cost'] - 
            df_units['Brand1_Mfg_Cost_Per_Unit'] - 
            selling_cost_per_unit
        ) * df_units['Brand1_Units_Sold']
        
        self.clean_data['unit_level'] = df_units
        
        return df_units
    
    def get_summary_statistics(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate summary statistics for the assignment.
        
        Args:
            df: DataFrame with unit-level data
            
        Returns:
            Dictionary with summary statistics
        """
        stats = {
            # Average retail prices
            'avg_brand1_price': df['Brand1_Retail_Price'].mean(),
            'avg_pl_price': df['PrivateLabel_Retail_Price'].mean(),
            'avg_price_gap': df['Price_Gap'].mean(),
            
            # Average margins
            'avg_brand1_margin_pct': df['Brand1_Margin_Pct'].mean(),
            'avg_pl_margin_pct': df['PrivateLabel_Margin_Pct'].mean(),
            
            # Average weekly unit sales
            'avg_brand1_units': df['Brand1_Units_Sold'].mean(),
            'avg_pl_units': df['PrivateLabel_Units_Sold'].mean(),
            
            # Average market shares
            'avg_brand1_share': df['Brand1_Share'].mean(),
            'avg_pl_share': df['PrivateLabel_Share'].mean(),
            
            # Average weekly profits
            'avg_retailer_profit': df['Retailer_Total_Profit'].mean(),
            'avg_manufacturer_profit': df['Brand1_Mfg_Profit'].mean(),
        }
        
        return stats
    
    def print_summary_statistics(self, stats: Dict[str, float]) -> None:
        """
        Print formatted summary statistics.
        
        Args:
            stats: Dictionary with summary statistics
        """
        print("\n" + "="*80)
        print("SUMMARY STATISTICS")
        print("="*80)
        
        print("\n1. Average Retail Prices (per unit):")
        print(f"   Brand 1:       ${stats['avg_brand1_price']:.2f}")
        print(f"   Private Label: ${stats['avg_pl_price']:.2f}")
        print(f"   Price Gap:     ${stats['avg_price_gap']:.2f}")
        
        print("\n2. Average Retail Margins:")
        print(f"   Brand 1:       {stats['avg_brand1_margin_pct']:.2f}%")
        print(f"   Private Label: {stats['avg_pl_margin_pct']:.2f}%")
        
        print("\n3. Average Weekly Unit Sales:")
        print(f"   Brand 1:       {stats['avg_brand1_units']:.0f} units")
        print(f"   Private Label: {stats['avg_pl_units']:.0f} units")
        
        print("\n4. Average Market Share:")
        print(f"   Brand 1:       {stats['avg_brand1_share']:.2f}%")
        print(f"   Private Label: {stats['avg_pl_share']:.2f}%")
        
        print("\n5. Average Weekly Profits:")
        print(f"   Retailer:      ${stats['avg_retailer_profit']:.2f}")
        print(f"   Manufacturer:  ${stats['avg_manufacturer_profit']:.2f}")
        
        print("="*80)
    
    def get_dataframe(self) -> pd.DataFrame:
        """
        Full pipeline: load, clean, and return the unit-level DataFrame.
        
        Returns:
            Fully processed DataFrame ready for analysis
        """
        df_clean = self.load_and_clean_original_data()
        df_units = self.calculate_unit_level_data(df_clean)
        return df_units


def main():
    """
    Main function to demonstrate data processing.
    """
    # Initialize processor
    processor = DataProcessor('bana6390_u2_assignment.xlsx')
    
    # Load and clean original data
    print("\n" + "="*80)
    print("LOADING AND CLEANING DATA")
    print("="*80)
    df_clean = processor.load_and_clean_original_data()
    
    # Display first few rows
    print("\nFirst 10 rows of cleaned data:")
    print(df_clean.head(10))
    
    # Calculate unit-level data
    print("\n" + "="*80)
    print("CALCULATING UNIT-LEVEL METRICS")
    print("="*80)
    df_units = processor.calculate_unit_level_data(df_clean)
    
    # Get and print summary statistics
    stats = processor.get_summary_statistics(df_units)
    processor.print_summary_statistics(stats)
    
    return df_units, stats


if __name__ == "__main__":
    df, stats = main()
