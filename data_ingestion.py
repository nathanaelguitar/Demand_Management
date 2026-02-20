"""
Data Ingestion Layer for BANA6390 Unit 2 Assignment
Handles reading and initial processing of Excel data
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Optional


class DataIngestion:
    """
    Ingestion layer for pricing optimization data from Excel file.
    Handles reading multiple sheets and initial data validation.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the data ingestion layer.
        
        Args:
            file_path: Path to the Excel file
        """
        self.file_path = Path(file_path)
        self.excel_file = None
        self.raw_data = {}
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"Excel file not found: {file_path}")
    
    def load_excel(self) -> pd.ExcelFile:
        """
        Load the Excel file.
        
        Returns:
            ExcelFile object
        """
        self.excel_file = pd.ExcelFile(self.file_path)
        print(f"Loaded Excel file with sheets: {self.excel_file.sheet_names}")
        return self.excel_file
    
    def get_sheet_names(self) -> list:
        """
        Get list of available sheet names.
        
        Returns:
            List of sheet names
        """
        if self.excel_file is None:
            self.load_excel()
        return self.excel_file.sheet_names
    
    def read_original_data(self, skip_rows: int = 3) -> pd.DataFrame:
        """
        Read the 'Original Data' sheet with proper header handling.
        
        Args:
            skip_rows: Number of rows to skip before header
            
        Returns:
            DataFrame with cleaned column names
        """
        df = pd.read_excel(
            self.file_path,
            sheet_name='Original Data',
            skiprows=skip_rows
        )
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Store raw data
        self.raw_data['original'] = df.copy()
        
        print(f"Loaded Original Data: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        
        return df
    
    def read_sheet(self, sheet_name: str, **kwargs) -> pd.DataFrame:
        """
        Read any specific sheet from the Excel file.
        
        Args:
            sheet_name: Name of the sheet to read
            **kwargs: Additional arguments to pass to pd.read_excel
            
        Returns:
            DataFrame with the sheet data
        """
        df = pd.read_excel(self.file_path, sheet_name=sheet_name, **kwargs)
        self.raw_data[sheet_name] = df.copy()
        
        print(f"Loaded sheet '{sheet_name}': {df.shape}")
        return df
    
    def read_all_sheets(self) -> Dict[str, pd.DataFrame]:
        """
        Read all sheets from the Excel file.
        
        Returns:
            Dictionary of DataFrames, keyed by sheet name
        """
        if self.excel_file is None:
            self.load_excel()
        
        all_data = {}
        for sheet_name in self.excel_file.sheet_names:
            try:
                df = pd.read_excel(self.file_path, sheet_name=sheet_name)
                all_data[sheet_name] = df
                print(f"  {sheet_name}: {df.shape}")
            except Exception as e:
                print(f"  Error reading {sheet_name}: {e}")
        
        self.raw_data = all_data
        return all_data
    
    def validate_data(self, df: pd.DataFrame) -> dict:
        """
        Validate the loaded data and return statistics.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Dictionary with validation results
        """
        validation = {
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.to_dict(),
            'null_counts': df.isnull().sum().to_dict(),
            'null_percentage': (df.isnull().sum() / len(df) * 100).to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum() / 1024**2  # MB
        }
        
        return validation
    
    def preview_data(self, df: pd.DataFrame, n: int = 5) -> None:
        """
        Print a preview of the DataFrame.
        
        Args:
            df: DataFrame to preview
            n: Number of rows to display
        """
        print("\n" + "="*80)
        print(f"Data Preview (first {n} rows):")
        print("="*80)
        print(df.head(n))
        print("\n" + "="*80)
        print("Data Info:")
        print("="*80)
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print("\nData Types:")
        print(df.dtypes)
        print("\nMissing Values:")
        print(df.isnull().sum())
        print("="*80)


def main():
    """
    Main function to demonstrate data ingestion.
    """
    # Initialize ingestion layer
    ingestion = DataIngestion('bana6390_u2_assignment.xlsx')
    
    # Load Excel file
    ingestion.load_excel()
    
    # Get sheet names
    print("\nAvailable sheets:")
    for sheet in ingestion.get_sheet_names():
        print(f"  - {sheet}")
    
    # Read original data
    print("\n" + "="*80)
    print("Reading Original Data sheet...")
    print("="*80)
    df = ingestion.read_original_data()
    
    # Preview data
    ingestion.preview_data(df)
    
    # Validate data
    print("\n" + "="*80)
    print("Data Validation Results:")
    print("="*80)
    validation = ingestion.validate_data(df)
    for key, value in validation.items():
        if key not in ['dtypes', 'null_counts', 'null_percentage']:
            print(f"{key}: {value}")
    
    return df


if __name__ == "__main__":
    df = main()
