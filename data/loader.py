import pandas as pd

def load_file(filepath):
    if filepath.endswith('csv'):
        df = pd.read_csv(filepath)
    elif filepath.endswith('xlsx'):
        df = pd.read_excel(filepath)
    else:
        return None
    
    return df

def get_columns(df):
    return list(df.columns)