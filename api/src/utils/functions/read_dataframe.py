import pandas as pd


def format_numeric_value(value):
    try:
        float_value = float(value)
        if float_value.is_integer():
            return str(int(float_value))  
        else:
            return str(float_value).replace('.', ',')
    except ValueError:
        return value  

def read_dataframe(path: str):
    try:
        df = pd.read_excel(path, dtype=str) 
        
        for col in df.columns:
            if df[col].str.replace('.', '', 1).str.isdigit().any():
                df[col] = df[col].apply(format_numeric_value)
        
        return df.where(pd.notnull(df), "")
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None