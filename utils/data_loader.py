import pandas as pd
import streamlit as st
from datetime import datetime
import os

@st.cache_data(ttl=300)
def load_car_data():
    try:
        # Get the absolute path to the CSV file
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(current_dir, 'car_exported.csv')
        
        # Load data from CSV with error handling for malformed lines
        # Use on_bad_lines='skip' for pandas >= 1.3.0 or error_bad_lines=False for older versions
        try:
            # Try with newer pandas version parameter
            df = pd.read_csv(csv_path, on_bad_lines='skip', quotechar='"', escapechar='\\')
        except TypeError:
            # Fall back to older pandas version parameter
            df = pd.read_csv(csv_path, error_bad_lines=False, warn_bad_lines=True, quotechar='"', escapechar='\\')
        
        # Convert price and year to numeric, handling non-numeric values
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        
        # Filter data similar to the original SQL query
        df = df[
            (df['price'] > 0) & 
            (df['price'] < 1000000) & 
            (~df['year'].isna()) & 
            (df['year'] >= 1900) & 
            (df['year'] <= datetime.now().year)
        ]

        df['year'] = df['year'].astype(int)
        
        # Process the data
        process_vehicle_data(df)
        return df
    except Exception as e:
        st.error(f"Failed to load car data: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_motorcycle_data():
    try:
        # Get the absolute path to the CSV file
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(current_dir, 'motor_exported.csv')
        
        # Load data from CSV with error handling for malformed lines
        # Use on_bad_lines='skip' for pandas >= 1.3.0 or error_bad_lines=False for older versions
        try:
            # Try with newer pandas version parameter
            df = pd.read_csv(csv_path, on_bad_lines='skip', quotechar='"', escapechar='\\')
        except TypeError:
            # Fall back to older pandas version parameter
            df = pd.read_csv(csv_path, error_bad_lines=False, warn_bad_lines=True, quotechar='"', escapechar='\\')
        
        # Convert price and year to numeric, handling non-numeric values
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        
        # Filter data similar to the original SQL query
        df = df[
            (df['price'] > 0) & 
            (df['price'] < 100000) & 
            (~df['year'].isna()) & 
            (df['year'] >= 1900) & 
            (df['year'] <= datetime.now().year)
        ]
        
        # Process the data
        process_vehicle_data(df)
        return df
    except Exception as e:
        st.error(f"Failed to load motorcycle data: {str(e)}")
        return pd.DataFrame()

def process_vehicle_data(df):
    """Common data processing for both vehicles"""
    # Year is already converted to numeric above
    df['age'] = datetime.now().year - df['year']
    
    if 'mileage_min' in df.columns and 'mileage_max' in df.columns:
        df['mileage_min'] = pd.to_numeric(df['mileage_min'], errors='coerce')
        df['mileage_max'] = pd.to_numeric(df['mileage_max'], errors='coerce')
        df['mileage_avg'] = (df['mileage_min'] + df['mileage_max']) / 2