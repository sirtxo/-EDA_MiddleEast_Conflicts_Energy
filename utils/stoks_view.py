"""
This script creates a Dash web application for visualizing stock data and technical indicators.
The application allows users to select a stock, a date range, and a technical indicator to visualize.
"""

import os
import pandas as pd
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

def read_stock_data(file_name):
    """
    Reads a CSV file containing stock data from the 'docs' directory.

    Args:
    - file_name (str): The name of the CSV file to read.

    Returns:
    - pd.DataFrame: A DataFrame containing the stock data.
    """
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Remove the 'utils' part from the path to get the root directory
    ROOT_DIR = current_dir.replace('utils', '')
    # Construct the full path to the file in the 'docs' directory
    file_path = os.path.join(ROOT_DIR, 'docs', file_name)
    # Read the CSV file, parsing the 'Date' column as dates
    return pd.read_csv(file_path, parse_dates=['Date'])

# List of CSV file names to be read
csv_files = [
    'Acciona_data.csv', 'BP plc_data.csv', 'Enagas_data.csv',  'Exxon Mobil Corporation_data.csv', 'Gazprom_data.csv', 'Honeywell International Inc._data.csv',
    'Iberdrola_data.csv', 'Kinder Morgan, Inc._data.csv',
    'NextEra Energy, Inc._data.csv', 'Repsol_data.csv', 'Saudi Arabian Oil Company (Aramco)_data.csv',
    'Schlumberger Limited_data.csv', 'Solaredge Technologies Inc._data.csv' ,'Solaria_data.csv', 'Técnicas Reunidas_data.csv'
]

# Read and concatenate all CSV files into a dictionary of DataFrames
dfs = {file_name: read_stock_data(file_name) for file_name in csv_files}

# Default start and end dates for the date picker
start_date = '2011-08-01'
end_date = '2014-12-31'

# Create a Dash application
app = Dash(__name__)

# Layout of the Dash application
app.layout = html.Div([
    # Dropdown for selecting the stock
    dcc.Dropdown(
        id='stock-dropdown',
        options=[{'label': name.split('_data.csv')[0], 'value': name} for name in csv_files],
        value=csv_files[0]
    ),
    # Date picker for selecting the date range
    dcc.DatePickerRange(
        id='date-picker',
        start_date=start_date,
        end_date=end_date,
        display_format='YYYY-MM-DD',
        initial_visible_month=start_date
    ),
    # Graph for displaying the stock's closing price
    dcc.Graph(id='close-graph'),
    # Dropdown for selecting the indicator
    dcc.Dropdown(
        id='indicator-dropdown',
        options=[
            {'label': 'RSI', 'value': 'RSI'},
            {'label': 'SMA_10', 'value': 'SMA_10'},
            {'label': 'SMA_20', 'value': 'SMA_20'},
            {'label': 'EMA_10', 'value': 'EMA_10'},
            {'label': 'EMA_20', 'value': 'EMA_20'},
            {'label': 'MACD', 'value': 'MACD'},
            {'label': 'Signal Line', 'value': 'Signal Line'},
            {'label': 'Upper Band', 'value': 'Upper Band'},
            {'label': 'Lower Band', 'value': 'Lower Band'},
            {'label': '%K', 'value': '%K'},
            {'label': '%D', 'value': '%D'}
        ],
        value='RSI'
    ),
    # Graph for displaying the selected indicator
    dcc.Graph(id='indicator-graph')
])

@app.callback(
    [Output('close-graph', 'figure'),
     Output('indicator-graph', 'figure')],
    [Input('stock-dropdown', 'value'),
     Input('indicator-dropdown', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_graphs(selected_stock, selected_indicator, start_date, end_date):
    """
    Updates the graphs based on the selected stock, indicator, and date range.

    Args:
    - selected_stock (str): The filename of the selected stock.
    - selected_indicator (str): The selected technical indicator.
    - start_date (str): The start date of the selected date range.
    - end_date (str): The end date of the selected date range.

    Returns:
    - tuple: A tuple containing the updated figures for the closing price and indicator graphs.
    """
    # Get the data for the selected stock
    df = dfs[selected_stock]
    # Filter the data based on the selected date range
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    # Create a candlestick chart for the stock's closing price
    close_trace = go.Candlestick(
        x=filtered_df['Date'],
        open=filtered_df['Open'],
        high=filtered_df['High'],
        low=filtered_df['Low'],
        close=filtered_df['Close'],
        name='Candlesticks'
    )

    # Create a line chart for the selected indicator
    indicator_trace = go.Scatter(
        x=filtered_df['Date'], y=filtered_df[selected_indicator], mode='lines', name=selected_indicator)

    # Layout for the closing price chart
    close_layout = go.Layout(
        title=f'Precio de Cierre de {selected_stock.split("_data.csv")[0]}',
        xaxis_title='Fecha',
        yaxis_title='Precio de Cierre'
    )
    # Layout for the indicator chart
    indicator_layout = go.Layout(
        title=f'{selected_indicator} de {selected_stock.split("_data.csv")[0]}',
        xaxis_title='Fecha',
        yaxis_title=selected_indicator
    )

    # Create the figures
    close_fig = go.Figure(data=[close_trace], layout=close_layout)
    indicator_fig = go.Figure(data=[indicator_trace], layout=indicator_layout)

    return close_fig, indicator_fig

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)
