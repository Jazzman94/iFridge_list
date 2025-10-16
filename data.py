"""
Data operations module (loading, saving, DataFrame operations)
"""
import pandas as pd
import os
from datetime import datetime
from config import DATE_FORMAT

def load_dataframe(path: str) -> pd.DataFrame:
    """
    Load DataFrame from CSV or create empty one if file doesn't exist
    
    Returns:
        DataFrame with data from CSV or empty DataFrame
    """
    if os.path.exists(path):
        df = pd.read_csv(path)
        print(f"✓ Loaded {len(df)} rows from {path}")
        print(f"✓ Columns: {df.columns.tolist()}")
        if not df.empty:
            print(f"✓ First row: {df.iloc[0].to_dict()}")
        return df
    else:
        print(f"✗ File {path} not found, creating empty DataFrame")
        return pd.DataFrame(columns=['id', 'Item', 'Quantity', 'Expiry date'])

def save_dataframe(df: pd.DataFrame, path: str) -> bool:
    """
    Save DataFrame to CSV
    
    Args:
        df: DataFrame to save
        
    Returns:
        True if save successful, False otherwise
    """
    try:
        df.to_csv(path, index=False, date_format=DATE_FORMAT)
        print(f"✓ Saved {len(df)} rows to {path}")
        return True
    except Exception as e:
        print(f"✗ Error saving DataFrame: {e}")
        return False

def create_new_row(df: pd.DataFrame) -> dict:
    """
    Create new empty row with next ID
    
    Args:
        df: Current DataFrame
        
    Returns:
        Dictionary with new row data
    """
    new_id = df["id"].max() + 1 if "id" in df.columns and not df.empty else 1
    return {
        "id": int(new_id),
        "Item": "",
        "Quantity": 1,
        "Expiry date": datetime.now().strftime(DATE_FORMAT),
    }

def delete_rows_by_ids(df: pd.DataFrame, ids: list) -> pd.DataFrame:
    """
    Delete rows by ID and reset index
    
    Args:
        df: Current DataFrame
        ids: List of row IDs to delete
        
    Returns:
        DataFrame without deleted rows
    """
    df = df[~df['id'].isin(ids)]
    df = df.reset_index(drop=True)
    return df