import matplotlib.pyplot as plt  # Importing matplotlib for plotting
import mpld3  # Importing mpld3 for converting matplotlib plots to HTML
import pandas as pd  # Importing pandas for data manipulation
from folium import folium, plugins  # Importing folium for creating interactive maps
import warnings  # Importing warnings module to suppress warnings

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
def plot_all_data(name, data):
    # Calculate PriceChange (difference of closing price between consecutive days)
    data['PriceChange'] = data['Close'] - data['Open']

    # Create subplots
    figi, (ax1, ax2) = plt.subplots(2, 1, figsize=(13.5, 9), sharex=True)

    # Line plot for Close Value
    color = 'blue'
    ax1.set_ylabel('Close Value ($)', color=color)
    ax1.plot(data.index, data['Close'], color=color, label=' Close Value ')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend(loc='upper left')

    # Bar plot for PriceChange
    color = 'red'
    ax2.set_ylabel('Lost Win (Shares)', color=color)
    bars = ax2.bar(data.index, data['PriceChange'], color=data['PriceChange'].apply(lambda x: 'red' if x < 0 else 'green'))
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_xlabel('Date')

    # Add date labels for negative PriceChange bars
    for bar in bars:
        index = bars.index(bar)
        price_change = data['PriceChange'].iloc[index]
        date = data.index[index].strftime('%Y-%m-%d')
        if price_change < 0:
            bar.set_label(date)

    # Add title
    plt.title(f'{name} Close Value and Lost-Win')

    # Adjust layout
    plt.tight_layout()

    # Show plot
    plt.show()

    # Convert plot to HTML
    html_output = mpld3.fig_to_html(plt.gcf())

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
