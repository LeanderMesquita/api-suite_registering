import pandas as pd

def read_dataframe(path: str):
    try:
        df = pd.read_excel(path)
        return df
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None