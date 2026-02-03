
import pandas as pd

def split_by_date(df, date_col, split_date):
    """
    Splits the DataFrame into two windows based on a split date.
    
    Args:
        df (pd.DataFrame): The dataset.
        date_col (str): Name of the datetime column.
        split_date (str): Date string (YYYY-MM-DD) to split on.
        
    Returns:
        tuple: (reference_df, current_df)
    """
    df[date_col] = pd.to_datetime(df[date_col])
    mask = df[date_col] < split_date
    reference = df[mask].copy()
    current = df[~mask].copy()
    
    return reference, current

def split_half(df, date_col):
    """
    Splits the DataFrame into two equal halves based on time.
    
    Args:
        df (pd.DataFrame): The dataset.
        date_col (str): Name of the datetime column.
        
    Returns:
        tuple: (reference_df, current_df)
    """
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(by=date_col)
    
    mid_idx = len(df) // 2
    reference = df.iloc[:mid_idx].copy()
    current = df.iloc[mid_idx:].copy()
    
    return reference, current
