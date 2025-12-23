import pandas as pd
import re

def clean_price(price_str):
    """Converts price string to integer"""
    if not isinstance(price_str, str):
        return None
    
    price_str = price_str.lower().strip()
    
    if "call for price" in price_str:
        return None
    
    # Removing "pkr" and commas
    price_str = price_str.replace("pkr", "").replace(",", "").strip()
    
    try:
        if "crore" in price_str:
            number = float(price_str.replace("crore", "").strip())
            return int(number * 10000000)
        elif "lacs" in price_str or "lac" in price_str:
            number = float(price_str.replace("lacs", "").replace("lac", "").strip())
            return int(number * 100000)
        else:
            return int(float(price_str))
    except ValueError:
        return None

def clean_mileage(mileage_str):
    """Converts mileage string to integer"""
    if not isinstance(mileage_str, str):
        return None
    
    mileage_str = mileage_str.lower().replace("km", "").replace(",", "").strip()
    try:
        return int(mileage_str)
    except ValueError:
        return None

def clean_engine(engine_str):
    """Converts engine string to integer"""
    if not isinstance(engine_str, str):
        return None
    
    engine_str = engine_str.lower().replace("cc", "").replace(",", "").strip()
    try:
        return int(engine_str)
    except ValueError:
        return None

def clean_dataset(df):
    """Applies cleaning functions"""
    df = df.copy()
    
  
    if 'price' in df.columns:
        df['price'] = df['price'].apply(clean_price)
    
    if 'mileage' in df.columns:
        df['mileage'] = df['mileage'].apply(clean_mileage)
        
    if 'engine' in df.columns:
        df['engine'] = df['engine'].apply(clean_engine)

    string_cols = ['name', 'city', 'fuel', 'transmission']
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
            
    if 'url' in df.columns:
        df = df.drop_duplicates(subset=['url'])
        
    return df
