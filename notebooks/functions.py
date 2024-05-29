import warnings  # Importing warnings module to suppress warnings

import mpld3  # Importing mpld3 for converting matplotlib plots to HTML
import pandas as pd  # Importing pandas for data manipulation
from folium import folium, plugins  # Importing folium for creating interactive maps

# Suppressing warnings to avoid cluttering the output
warnings.filterwarnings("ignore")

# Function to create a heatmap of conflicts over time
def create_heatmap_full(data_filtered):
    # Convert 'date_start' column to datetime format
    data_filtered['date_start'] = pd.to_datetime(data_filtered['date_start'])

    heatmap_time_datee_n = []  # List to store dates for heatmap
    heatmap_time_dataa_n = []  # List to store heatmap data

    # Group data by date
    grouped_data = data_filtered.groupby(data_filtered['date_start'].dt.strftime('%Y-%m-%d'))

    # Iterate over grouped data
    for (date), group_data in grouped_data:
        try:
            # Extract date and append to list
            date_start_list = group_data['date_start'].tolist()
            date = date_start_list[1].strftime('%Y-%m-%d')
            heatmap_time_datee_n.append(date)

            # Access daily positions for the current conflict
            positions = data_filtered[(data_filtered['date_start'].dt.strftime('%Y-%m-%d') == date)].head(100)
            positions_list = []
            # Extract latitude and longitude for each conflict and append to list
            for index, row in positions.iterrows():
                lat_lon = [row['latitude'], row['longitude']]
                positions_list.append(lat_lon)
            heatmap_time_dataa_n.append(positions_list)
        except Exception as ex:
            print(ex)

    # Create a Folium map
    map_heatmap_time = folium.Map([0, 0], tiles='CartoDB Dark_Matter', zoom_start=3)

    # Create HeatMapWithTime plugin for Folium
    heatmap_time_plugin = plugins.HeatMapWithTime(heatmap_time_dataa_n, index=heatmap_time_datee_n)

    # Add heatmap plugin to the map
    heatmap_time_plugin.add_to(map_heatmap_time)

    # Save the map as HTML file
    map_heatmap_time.save(f"html/03_heatmap_conflicts-2011-2013.html")

    # Return the map
    return map_heatmap_time

# Function to plot stock data

import matplotlib.pyplot as plt


import matplotlib.pyplot as plt
import seaborn as sns

def plot_all_data(name, data):
    # Calculate PriceChange (difference of closing price between consecutive days)
    data['PriceChange'] = data['Close'] - data['Open']

    # Set Seaborn style
    plt.style.use('seaborn-dark')

    # Create subplots
    figi, (ax1, ax2) = plt.subplots(2, 1, figsize=(13.5, 9), sharex=True)

    # Set background color of the figure to black
    figi.patch.set_facecolor('black')

    # Line plot for Close Value
    color = 'lightblue'
    ax1.set_ylabel('Close Value ($)', color=color)
    ax1.plot(data.index, data['Close'], color=color, label=' Close Value ')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend(loc='upper left', facecolor='black', edgecolor='white', fontsize='small', framealpha=0.8)

    # Bar plot for PriceChange
    ax2.set_ylabel('Lost Win (Shares)', color='lightblue')
    bars = ax2.bar(data.index, data['PriceChange'], color=data['PriceChange'].apply(lambda x: 'red' if x < 0 else 'green'))
    ax2.set_xlabel('Date')

    # Add date labels for negative PriceChange bars
    for bar in bars:
        index = bars.index(bar)
        price_change = data['PriceChange'].iloc[index]
        date = data.index[index].strftime('%Y-%m-%d')
        if price_change < 0:
            bar.set_label(date)

    # Add title
    plt.suptitle(f'{name} Close Value and Lost-Win', fontsize=16, color='lightblue')

    # Set background color of the subplots to black
    ax1.set_facecolor('black')
    ax2.set_facecolor('black')

    # Set color of ticks and labels to white
    ax1.tick_params(colors='white')
    ax2.tick_params(colors='white')

    # Set color of spine edges to white
    for spine in ax1.spines.values():
        spine.set_edgecolor('white')
    for spine in ax2.spines.values():
        spine.set_edgecolor('white')

    # Adjust layout
    plt.tight_layout()

    # Show plot
    plt.show()

    # Convert plot to HTML
    html_output = mpld3.fig_to_html(figi)

    # Save HTML output to file
    with open(f'html/04_plot_all_data_{name}.html', 'w') as file:
        file.write(html_output)




# Function to create heatmap for a specific year
def create_heatmap(year, datos):
    # Filter data for the specified year
    data_for_year = datos[datos['year'] == year]
    data_for_year['date_start'] = pd.to_datetime(data_for_year['date_start'])
    heatmap_data_n = []

    heatmap_time_datee_n = []
    heatmap_time_dataa_n = []

    # Group data by date
    grouped_data = data_for_year.groupby(data_for_year['date_start'].dt.strftime('%Y-%m-%d'))

    # Iterate over grouped data
    for (date), group_data in grouped_data:
        try:
            # Calculate intensity (sum of 'deaths_civilians')
            intensity = group_data['deaths_civilians'].sum()
            date_start_list = group_data['date_start'].tolist()
            date = date_start_list[1].strftime('%Y-%m-%d')
            heatmap_time_datee_n.append(date)

            # Access daily positions for the current conflict
            positions = data_for_year[(data_for_year['date_start'].dt.strftime('%Y-%m-%d') == date)].head(100)
            positions_list = []
            # Extract latitude and longitude for each conflict and append to list
            for index, row in positions.iterrows():
                lat_lon = [row['latitude'], row['longitude']]
                positions_list.append(lat_lon)
            heatmap_time_dataa_n.append(positions_list)
        except Exception as ex:
            print(ex)

    # Create a Folium map
    map_heatmap_time = folium.Map([0, 0], tiles='CartoDB Dark_Matter', zoom_start=3)

    # Create HeatMapWithTime plugin for Folium
    heatmap_time_plugin = plugins.HeatMapWithTime(heatmap_time_dataa_n, index=heatmap_time_datee_n)

    # Add heatmap plugin to the map
    heatmap_time_plugin.add_to(map_heatmap_time)

    # Save the map as HTML file
    map_heatmap_time.save(f"heatmap_conflicts-{year}.html")

    # Return the map
    return map_heatmap_time

# Function to filter intervals based on correlation threshold
def filtrar_intervalos(intervalos_fechas, data_full, data, umbral):
    intervalos_filtrados = []

    for index, intervalo in intervalos_fechas.iterrows():
        fecha_inicio = intervalo['date_start'] - pd.Timedelta(days=2)
        fecha_fin = intervalo['date_start'] + pd.Timedelta(days=2)

        # Filter data within the interval
        data_filtered = data_full[(pd.to_datetime(data_full['date_start']) >= fecha_inicio) & (pd.to_datetime(data_full['date_start']) < fecha_fin)]
        stock_data = data[(data['Date'] >= fecha_inicio) & (data['Date'] < fecha_fin)]

        # Group conflicts and stock data by date
        conflicts_by_day = data_filtered.groupby('date_start').size().reset_index(name='conflict_count')
        conflicts_by_day['date_start'] = pd.to_datetime(conflicts_by_day['date_start'])

        volume_by_day = stock_data.groupby('Date').agg({'Close': 'sum', 'Open': 'sum'})
        volume_by_day['Volume'] = volume_by_day['Close'] - volume_by_day['Open']

        # Merge conflicts and stock data
        combined_data = pd.merge(volume_by_day, conflicts_by_day, left_on='Date', right_on='date_start', how='inner')

        # Calculate correlation between stock volume and conflict count
        correlation = combined_data['Volume'].corr(combined_data['conflict_count'])

        if correlation < umbral:
            intervalos_filtrados.append((fecha_inicio, fecha_fin, data_filtered, stock_data, correlation))

    return intervalos_filtrados

# Función para calcular los indicadores técnicos y guardar el archivo modificado
def process_stock_data(file_name):
    # Importar el archivo CSV como DataFrame y parsear las fechas
    df = pd.read_csv('../docs/' + file_name, parse_dates=['Date'])

    # Calcular los cambios diarios en el precio de cierre
    df['Daily Return'] = df['Close'].pct_change()

    # Definir el período de tiempo para el cálculo del RSI
    period = 14

    # Calcular los cambios positivos y negativos
    df['Positive Change'] = df['Daily Return'].apply(lambda x: x if x > 0 else 0)
    df['Negative Change'] = df['Daily Return'].apply(lambda x: -x if x < 0 else 0)

    # Calcular el promedio de los cambios positivos y negativos
    df['Avg Gain'] = df['Positive Change'].rolling(window=period).mean()
    df['Avg Loss'] = df['Negative Change'].rolling(window=period).mean()

    # Calcular el RSI
    df['RS'] = df['Avg Gain'] / df['Avg Loss']
    df['RSI'] = 100 - (100 / (1 + df['RS']))

    # Eliminar columnas auxiliares utilizadas en el cálculo del RSI
    df.drop(['Daily Return', 'Positive Change', 'Negative Change', 'Avg Gain', 'Avg Loss', 'RS'], axis=1, inplace=True)

    # Calcular la media móvil simple (SMA) para diferentes períodos
    for period in [10, 20, 50, 100, 200]:
        df[f'SMA_{period}'] = df['Close'].rolling(window=period).mean()

    # Calcular la media móvil exponencial (EMA) para diferentes períodos
    for period in [10, 20, 50, 100, 200]:
        df[f'EMA_{period}'] = df['Close'].ewm(span=period, adjust=False).mean()

    # Calcular el MACD (Moving Average Convergence Divergence)
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # Calcular las bandas de Bollinger
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['20dSTD'] = df['Close'].rolling(window=20).std()
    df['Upper Band'] = df['MA20'] + (df['20dSTD'] * 2)
    df['Lower Band'] = df['MA20'] - (df['20dSTD'] * 2)

    # Calcular el estocástico
    high14 = df['High'].rolling(window=14).max()
    low14 = df['Low'].rolling(window=14).min()
    df['%K'] = ((df['Close'] - low14) / (high14 - low14)) * 100
    df['%D'] = df['%K'].rolling(window=3).mean()

    # Eliminar filas con valores NaN (debido a los cálculos)
    df.dropna(inplace=True)

    # Guardar el DataFrame resultante en el mismo archivo CSV
    df.to_csv('../docs/' + file_name, index=False)

def filtrar_intervalos_end(intervalos_fechas, data_full, data, umbral):
    intervalos_filtrados = []

    for index, intervalo in intervalos_fechas.iterrows():
        fecha_inicio = intervalo['date_start'] + pd.Timedelta(days=(intervalo['date_diff'].days-2))

        fecha_fin = intervalo['date_start']+ pd.Timedelta(days=(intervalo['date_diff'].days+2))

        data_filtered = data_full[(data_full['date_start'] >= fecha_inicio) & (data_full['date_start'] < fecha_fin)]
        stock_data = data[(data['Date'] >= fecha_inicio) & (data['Date'] < fecha_fin)]

        conflicts_by_day = data_filtered.groupby('date_start').size().reset_index(name='conflict_count')
        conflicts_by_day['date_start'] = pd.to_datetime(conflicts_by_day['date_start'])

        volume_by_day = stock_data.groupby('Date').agg({'Close': 'sum', 'Open': 'sum'})
        volume_by_day['Volume'] = volume_by_day['Close'] - volume_by_day['Open']

        combined_data = pd.merge(volume_by_day, conflicts_by_day, left_on='Date', right_on='date_start', how='inner')

        correlation = combined_data['Volume'].corr(combined_data['conflict_count'])

        if correlation < umbral:
            #print(f"Correlation between stock volume and conflict count: {correlation} Interval: {fecha_inicio} - {fecha_fin}")
            intervalos_filtrados.append((fecha_inicio, fecha_fin, data_filtered, stock_data, correlation))

    return intervalos_filtrados


def fill_nan_data(data_original, date_start, date_end, date_name ='Date', value_name ='Volume'):
    # Ordenar los datos por fecha
    data_original.sort_values(by=date_name, inplace=True)

    # Crear un rango de fechas
    rango_fechas = pd.date_range(start=date_start, end=date_end)

    # Crear un DataFrame con todas las fechas del rango y valores nulos
    fechas_faltantes_df = pd.DataFrame({date_name: rango_fechas})

    # Fusionar el DataFrame original con el DataFrame de fechas faltantes
    data_completa = pd.merge(fechas_faltantes_df, data_original, on=date_name, how='left')

    # Iterar sobre los índices faltantes y rellenar los valores
    for idx, row in data_completa.iterrows():
        if pd.isnull(row[value_name]):
            idx_siguiente = data_completa.iloc[idx:].index.min()
            if pd.notnull(idx_siguiente):
                data_completa.at[idx, value_name] = data_completa.at[idx_siguiente, value_name]

    return data_completa
