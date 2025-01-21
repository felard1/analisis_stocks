#%% 
#----- Liberias  -----
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
from datetime import datetime
from dateutil.relativedelta import relativedelta

#%%
#--- Empresas a investigar  ---
big_tech_symbols = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Alphabet (Google) - Clase A": "GOOGL",
    "Alphabet (Google) - Clase C": "GOOG",
    "Meta": "META",
    "Tesla": "TSLA",
    "NVIDIA": "NVDA"
}



#%%
#--- Función para generar DataFrames ---
def generar_dataframes(symbols_dict, start, end):
    """
    Genera un diccionario de DataFrames con datos históricos para cada símbolo.

    Args:
        symbols_dict (dict): Diccionario con nombres como llave y símbolos como valores.
        start (str): Fecha de inicio en formato 'YYYY-MM-DD'.
        end (str): Fecha de fin en formato 'YYYY-MM-DD'.

    Returns:
        dict: Diccionario con nombres como llave y DataFrames como valores.
    """
    dataframes = {}
    for name, symbol in symbols_dict.items():
        df = yf.download(symbol, start=start, end=end)
        dataframes[name] = df
        print(f"Datos descargados para: {name}")
    return dataframes

#--- Función para guardar DataFrames como .txt ---
def guardar_dataframes(dataframes, output_path="./data/"):
    """
    Guarda DataFrames en archivos .txt.

    Args:
        dataframes (dict): Diccionario con nombres como llave y DataFrames como valores.
        output_path (str): Ruta donde se guardarán los archivos .txt.
    """
    os.makedirs(output_path, exist_ok=True)
    for name, df in dataframes.items():
        filename = f"{output_path}{name.replace(' ', '_')}.txt"
        df.to_csv(filename, sep="\t", index=True)
        print(f"Datos de {name} guardados en {filename}")

#%% 
#--- Fechas de consulta ---
current_date = datetime.now()
end = current_date.strftime("%Y-%m-%d")
date_minus_3_years = current_date - relativedelta(years=3)
start = date_minus_3_years.strftime("%Y-%m-%d")

#--- Llamar a las funciones ---
# 1. Generar los DataFrames
dataframes = generar_dataframes(big_tech_symbols, start, end)


#%%
# 2. Guardar los DataFrames como .txt
guardar_dataframes(dataframes, output_path="./data/")