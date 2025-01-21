#%% 
#----- Liberias  -----
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os 
from sklearn.cluster import KMeans
import plotly.express as px

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
    "NVIDIA": "NVDA",
    'Alibaba': 'BABA',
    'ASML': 'ASML',
    'Berkshire Hathaway': 'BRK-B',
    'Citi Group': 'C',
    'Everest': 'EG',
    'Nu': 'NU',
    'Ecopetrol': 'EC',
    'JP Morgan': 'JPM',
    'LVMH': 'LVMUY',
    'Moderna': ' MRNA',
    'SLB': 'SLB',
    'UBER': 'UBER'
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



#%%

#--- Función para generar gráficas ---
def graficar_precios(dataframes, output_path="./plots/"):
    """
    Genera una gráfica del precio de cierre y precio ajustado para cada acción.

    Args:
        dataframes (dict): Diccionario con nombres como llave y DataFrames como valores.
        output_path (str): Ruta donde se guardarán las gráficas en formato PNG.
    """
    # Crear el directorio para guardar las gráficas
    os.makedirs(output_path, exist_ok=True)

    for name, df in dataframes.items():
        plt.figure(figsize=(12, 6))
        plt.plot(df['Close'], label=f'{name}_Close', color='blue')
        plt.plot(df['Adj Close'], label=f'{name}_Adj', color='green')
        plt.title(f'Precio de compra: {name}')
        plt.xlabel('Fecha')
        plt.ylabel('Precio USD')
        plt.legend()
        plt.grid(True)

        # Guardar la gráfica como archivo PNG
        filename = f"{output_path}{name.replace(' ', '_')}_precios.png"
        plt.savefig(filename)
        print(f"Gráfica guardada para {name} en {filename}")

        plt.close()

#--- Llamada a la función ---
graficar_precios(dataframes, output_path="./plots/")

#%%
#--- Función para calcular retornos y volatilidad ---
def calcular_metricas_anuales(dataframes):
    """
    Calcula retornos y volatilidad anualizados para cada acción.

    Args:
        dataframes (dict): Diccionario con nombres como llave y DataFrames como valores.

    Returns:
        pd.DataFrame: DataFrame con las métricas anualizadas (retorno y volatilidad).
    """
    metricas = []

    for name, df in dataframes.items():
        daily_log_returns = np.log(df['Adj Close'] / df['Adj Close'].shift(1))
        annualized_returns = daily_log_returns.mean() * 252
        annualized_volatility = daily_log_returns.std() * np.sqrt(252)
        metricas.append([name, annualized_returns, annualized_volatility])

    # Convertir a DataFrame
    metricas_df = pd.DataFrame(metricas, columns=['Empresa', 'Retorno Anualizado', 'Volatilidad Anualizada'])
    return metricas_df

#--- Función para clustering y gráfico de dispersión ---
def clustering_interactivo(metricas_df, n_clusters=3, output_path=None):
    """
    Realiza clustering en las métricas anualizadas y genera un gráfico interactivo.

    Args:
        metricas_df (pd.DataFrame): DataFrame con métricas anualizadas.
        n_clusters (int): Número de clusters a usar en el modelo de clustering.
        output_path (str): Ruta donde se guardará la gráfica interactiva (opcional).

    Returns:
        pd.DataFrame: DataFrame con las asignaciones de cluster.
    """
    # Preparar datos para clustering
    X = metricas_df[['Volatilidad Anualizada', 'Retorno Anualizado']].values

    # Modelo de clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    metricas_df['Cluster'] = kmeans.fit_predict(X)

    # Crear gráfico interactivo con Plotly
    fig = px.scatter(
        metricas_df,
        x='Volatilidad Anualizada',
        y='Retorno Anualizado',
        color='Cluster',
        text='Empresa',
        color_continuous_scale=px.colors.sequential.Viridis,  # Cambia aquí la paleta de colores
        title='Clustering: Volatilidad vs. Retorno Anualizado'
    )

    # Mejorar visualización
    fig.update_traces(textposition='top center')  # Ubicación de etiquetas
    fig.update_layout(
        xaxis_title='Volatilidad Anualizada',
        yaxis_title='Retorno Anualizado',
        template='plotly_white',  # Cambiar estilo general
        title_font=dict(size=20),
        legend_title=dict(text='Cluster'),
        font=dict(size=12),
    )

    # Guardar la gráfica si se especifica una ruta
    if output_path:
        fig.write_html(output_path)
        print(f"Gráfica interactiva guardada en {output_path}")

    fig.show()
    return metricas_df

# Ejecutar el clustering con visualización mejorada
resultado_interactivo = clustering_interactivo(
    metricas_df=calcular_metricas_anuales(dataframes), 
    n_clusters=5)