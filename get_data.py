import json
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import requests
from datetime import datetime
import os

energy_sector = [
    {"sector": "Oil&Gas",
     "companies": [
         {"name": "Repsol", "country": "Spain", "symbol": "REP.MC", "data": []},
         {"name": "Exxon Mobil Corporation", "country": "USA", "symbol": "XOM", "data": []}
     ]},
    {"sector": "ElectricPower",
     "companies": [
         {"name": "Iberdrola", "country": "Spain", "symbol": "IBE.MC", "data": []},
         {"name": "NextEra Energy, Inc.", "country": "USA", "symbol": "NEE", "data": []}
     ]},
    {"sector": "RenewableEnergy",
     "companies": [
         {"name": "Acciona", "country": "Spain", "symbol": "ANA.MC", "data": []},
         {"name": "Solaria", "country": "Spain", "symbol": "SOL", "data": []},
         {"name": "Solaredge Technologies Inc.", "country": "USA", "symbol": "SEDG", "data": []}
     ]},
    {"sector": "EnergyServices",
     "companies": [
         {"name": "Siemens Gamesa Renewable Energy", "country": "Spain", "symbol": "SGRE.MC", "data": []},
         {"name": "Honeywell International Inc.", "country": "USA", "symbol": "HON", "data": []}
     ]},
    {"sector": "Infrastructure",
     "companies": [
         {"name": "Enagas", "country": "Spain", "symbol": "ENG.MC", "data": []},
         {"name": "Kinder Morgan, Inc.", "country": "USA", "symbol": "KMI", "data": []}
     ]}
]


def main():
    now_date = datetime.now()

    events_url = "https://ucdpapi.pcr.uu.se/api/gedevents/23.1"

    start_date = datetime(2001, 1, 1)
    end_date = datetime(now_date.year, now_date.month, now_date.day)

    all_data = []

    current_date = start_date
    parameters = {
        "pagesize": 1000,
        "format": "json",
        "date_start": start_date.strftime('%Y-%m-%d'),
        "date_end": end_date.strftime('%Y-%m-%d')
    }

    response = requests.get(events_url, params=parameters)
    data = json.loads(response.text)
    page = 1
    total_pages = data['TotalPages']

    print(total_pages)
    print(page)
    next_page = data['NextPageUrl']
    if response.status_code == 200:
        all_data.extend(data['Result'])

    while page <= total_pages:
        response = requests.get(next_page)
        data = json.loads(response.text)
        next_page = data['NextPageUrl']
        if response.status_code == 200:

            all_data.extend(data['Result'])
            df = pd.DataFrame(all_data)

        else:
            print(f"Error al obtener los datos del UCDP para la fecha {current_date}.")
        print(total_pages)
        print(page)
        page = page + 1

    # Guardar los datos en un archivo CSV
    df.to_csv('ucdp_data_events_2000_2024.csv', index=False)
    events_url = "https://ucdpapi.pcr.uu.se/api/ucdpprioconflict/23.1"

    start_date = datetime(2001, 1, 1)
    end_date = datetime(now_date.year, now_date.month, now_date.day)

    all_data = []

    current_date = start_date
    parameters = {
        "pagesize": 10000,
        "format": "json",
        "date_start": start_date.strftime('%Y-%m-%d'),
        "date_end": end_date.strftime('%Y-%m-%d')
    }

    response = requests.get(events_url, params=parameters)
    data = json.loads(response.text)
    page = 1
    total_pages = data['TotalPages']

    print(total_pages)
    print(page)
    next_page = data['NextPageUrl']
    if response.status_code == 200:
        all_data.extend(data['Result'])

    while page < total_pages:
        response = requests.get(next_page)
        data = json.loads(response.text)
        next_page = data['NextPageUrl']
        if response.status_code == 200:

            all_data.extend(data['Result'])
            df = pd.DataFrame(all_data)

            # Guardar los datos en un archivo CSV
        else:
            print(f"Error al obtener los datos del UCDP para la fecha {current_date}.")
        print(total_pages)
        page = page + 1
        print(page)

    df.to_csv('ucdp_data_conflicts_2000_2024.csv', index=False)

    if not os.path.exists('docs'):
        os.makedirs('docs')

    for sector in energy_sector:
        for company in sector['companies']:
            company_data = yf.download(company['symbol'], start='2000-01-01', end=now_date)
            file_name = f"{company['name']}_data.csv"
            company_data.to_csv(os.path.join('docs', file_name))
            company['data'] = company_data


if __name__ == "__main__":
    main()
