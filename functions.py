import matplotlib.pyplot as plt
import pandas as pd
import ipywidgets as widgets
from folium import folium, plugins
from ipywidgets import interact

def plot_all_data(name, data, year):
    # Calcular la diferencia de precio de cierre entre días consecutivos
    data['PriceChange'] = data['Adj Close'].diff()

    # Crear la figura y los ejes
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13.5, 9), sharex=True)

    # Gráfico de líneas para el valor de cierre ajustado (Adj Close)
    color = 'blue'
    ax1.set_ylabel('Adj Close Value ($)', color=color)
    ax1.plot(data.index, data['Adj Close'], color=color, label='Adj Close')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend(loc='upper left')

    # Gráfico de barras para el volumen (positivo y negativo)
    color = 'red'
    ax2.set_ylabel('Volume (Shares)', color=color)
    bars = ax2.bar(data.index, data['Volume'],
                   color=data['PriceChange'].apply(lambda x: 'red' if x < 0 else 'green'))
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_xlabel('Date')

    # Añadir texto como etiqueta en la leyenda para volúmenes negativos
    for bar in bars:
        index = bars.index(bar)
        volume = data['Volume'].iloc[index]
        date = data.index[index].strftime('%Y-%m-%d')
        if volume < 0:  # Solo para volúmenes negativos
            bar.set_label(date)  # Utiliza la fecha como etiqueta

    # Añadir título
    plt.title(f'{name} Close Value and Volume')

    # Ajustar espacios entre subgráficos
    plt.tight_layout()

    # Mostrar la gráfica
    plt.show()

def plot_by_year(name, data, year):
    # Filtrar los datos por año seleccionado
    data_year = data[data.index.year == year]

    # Calcular la diferencia de precio de cierre entre días consecutivos
    data_year['PriceChange'] = data_year['Adj Close'].diff()

    # Crear la figura y los ejes
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13.5, 9), sharex=True)

    # Gráfico de líneas para el valor de cierre ajustado (Adj Close)
    color = 'blue'
    ax1.set_ylabel('Adj Close Value ($)', color=color)
    ax1.plot(data_year.index, data_year['Adj Close'], color=color, label=f'Adj Close - Year {year}')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend(loc='upper left')

    # Gráfico de barras para el volumen (positivo y negativo)
    color = 'red'
    ax2.set_ylabel('Volume (Shares)', color=color)
    bars = ax2.bar(data_year.index, data_year['Volume'],
                   color=data_year['PriceChange'].apply(lambda x: 'red' if x < 0 else 'green'))
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_xlabel('Date')

    # Añadir texto como etiqueta en la leyenda para volúmenes negativos
    for bar in bars:
        index = bars.index(bar)
        volume = data_year['Volume'].iloc[index]
        date = data_year.index[index].strftime('%Y-%m-%d')
        if volume < 0:  # Solo para volúmenes negativos
            bar.set_label(date)  # Utiliza la fecha como etiqueta

    # Añadir título
    plt.title(f'{name} Close Value and Volume - Year {year}')

    # Ajustar espacios entre subgráficos
    plt.tight_layout()

    # Mostrar la gráfica
    plt.show()


def create_heatmap(year, datos):
    data_for_year = datos[datos['year'] == year]
    data_for_year['date_start'] = pd.to_datetime(data_for_year['date_start'])
    heatmap_data_n = []

    heatmap_time_datee_n = []
    heatmap_time_dataa_n = []
    grouped_data = data_for_year.groupby(data_for_year['date_start'].dt.strftime('%Y-%m-%d'))

    for (date), group_data in grouped_data:
        try:
            # Extract intensity value for the current conflict and date (consider aggregation)
            intensity = group_data['deaths_civilians'].sum()  # Assuming deaths_civilians is the intensity value
            date_start_list = group_data['date_start'].tolist()
            date = date_start_list[1].strftime('%Y-%m-%d')
            heatmap_time_datee_n.append(date)

            # Access daily positions for the current conflict
            positions = data_for_year[(data_for_year['date_start'].dt.strftime('%Y-%m-%d') == date)].head(100)
            num_rows = positions.shape[0]
            positions_list = []
            for index, row in positions.iterrows():
                lat_lon = [row['latitude'], row['longitude']]
                positions_list.append(lat_lon)
            heatmap_time_dataa_n.append(positions_list)
        except Exception as ex:
            print(ex)

    # take note of data format needed for heat map with time (using plugins.HeatMapWithTime?)

    # map
    map_heatmap_time = folium.Map([0, 0], tiles='CartoDB Dark_Matter', zoom_start=3)

    # heatmap plugin
    heatmap_time_plugin = plugins.HeatMapWithTime(heatmap_time_dataa_n, index=heatmap_time_datee_n)

    # add heatmap plugin to map
    heatmap_time_plugin.add_to(map_heatmap_time)

    map_heatmap_time.save(f"heatmap_conflicts-{year}.html")
    # display map
    return map_heatmap_time


def filtrar_intervalos(intervalos_fechas, data_full, data, umbral):

    intervalos_filtrados = []

    for index, intervalo in intervalos_fechas.iterrows():
        fecha_inicio = intervalo['date_start'] - pd.Timedelta(days=2)
        fecha_fin = intervalo['date_start'] + pd.Timedelta(days=2)

        data_filtered = data_full[(data_full['date_start'] >= fecha_inicio) & (data_full['date_start'] < fecha_fin)]
        stock_data = data[(data['Date'] >= fecha_inicio) & (data['Date'] < fecha_fin)]

        conflicts_by_day = data_filtered.groupby('date_start').size().reset_index(name='conflict_count')
        conflicts_by_day['date_start'] = pd.to_datetime(conflicts_by_day['date_start'])

        volume_by_day = stock_data.groupby('Date')['Volume'].sum().reset_index()

        combined_data = pd.merge(volume_by_day, conflicts_by_day, left_on='Date', right_on='date_start', how='inner')

        correlation = combined_data['Volume'].corr(combined_data['conflict_count'])

        if correlation < umbral:
            print(f"Correlation between stock volume and conflict count: {correlation} Interval: {fecha_inicio} - {fecha_fin}")
            intervalos_filtrados.append((fecha_inicio, fecha_fin, data_filtered, stock_data, correlation))

    return intervalos_filtrados
