import dash
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from jupyter_dash import JupyterDash

# Leer los archivos CSV y concatenar los datos
def read_stock_data(file_name):
    return pd.read_csv(f'../docs/{file_name}', parse_dates=['Date'])

# Lista de nombres de archivos CSV
csv_files = [
    'Acciona_data.csv', 'BP plc_data.csv', 'Enagas_data.csv',  'Exxon Mobil Corporation_data.csv', 'Gazprom_data.csv', 'Honeywell International Inc._data.csv',
    'Iberdrola_data.csv', 'Kinder Morgan, Inc._data.csv',
    'NextEra Energy, Inc._data.csv', 'Repsol_data.csv', 'Saudi Arabian Oil Company (Aramco)_data.csv',
    'Schlumberger Limited_data.csv', 'Solaredge Technologies Inc._data.csv' ,'Solaria_data.csv', 'Técnicas Reunidas_data.csv'
]

# Leer y concatenar todos los datos
dfs = {file_name: read_stock_data(file_name) for file_name in csv_files}

# Fechas de inicio y fin predeterminadas
start_date = '2011-08-01'
end_date = '2014-12-31'

# Crear una aplicación Dash
app = Dash(__name__)

# Layout de la aplicación
app.layout = html.Div([
    dcc.Dropdown(
        id='stock-dropdown',
        options=[{'label': name.split('_data.csv')[0], 'value': name} for name in csv_files],
        value=csv_files[0]
    ),
    dcc.DatePickerRange(
        id='date-picker',
        start_date=start_date,
        end_date=end_date,
        display_format='YYYY-MM-DD',
        initial_visible_month=start_date
    ),
    dcc.Graph(id='close-graph'),
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
    df = dfs[selected_stock]
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    close_trace = go.Candlestick(
        x=filtered_df['Date'],
        open=filtered_df['Open'],
        high=filtered_df['High'],
        low=filtered_df['Low'],
        close=filtered_df['Close'],
        name='Candlesticks'
    )

    indicator_trace = go.Scatter(
        x=filtered_df['Date'], y=filtered_df[selected_indicator], mode='lines', name=selected_indicator)

    close_layout = go.Layout(
        title=f'Precio de Cierre de {selected_stock.split("_data.csv")[0]}',
        xaxis_title='Fecha',
        yaxis_title='Precio de Cierre'
    )
    indicator_layout = go.Layout(
        title=f'{selected_indicator} de {selected_stock.split("_data.csv")[0]}',
        xaxis_title='Fecha',
        yaxis_title=selected_indicator
    )

    close_fig = go.Figure(data=[close_trace], layout=close_layout)
    indicator_fig = go.Figure(data=[indicator_trace], layout=indicator_layout)

    return close_fig, indicator_fig

# Ejecutar la aplicación
app.run_server(mode='inline', debug=True)
