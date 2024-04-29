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
         {"name": "Técnicas Reunidas", "country": "Spain", "symbol": "TRE.MC", "data": []},
         {"name": "Honeywell International Inc.", "country": "USA", "symbol": "HON", "data": []}
     ]},
    {"sector": "Infrastructure",
     "companies": [
         {"name": "Enagas", "country": "Spain", "symbol": "ENG.MC", "data": []},
         {"name": "Kinder Morgan, Inc.", "country": "USA", "symbol": "KMI", "data": []}
     ]}
]

now_date = datetime.now()

start_date = datetime(2000, 1, 1)

get_events_url = "https://ucdpapi.pcr.uu.se/api/gedevents/23.1"
armed_conflict_url = "https://ucdpapi.pcr.uu.se/api/ucdpprioconflict/23.1"
end_date = datetime(now_date.year, now_date.month, now_date.day)
parameters = {
    "pagesize": 10000,
    "format": "json",
    "StartDate": start_date.strftime('%Y-%m-%d'),
    "EndDate": end_date.strftime('%Y-%m-%d')
}


def main():
    #get events
    get_data_ucdp([], start_date, get_events_url, 'ucdp_data_events_2000_2024.csv')
    #get conflict
    get_data_ucdp([], start_date, armed_conflict_url, 'ucdp_data_conflicts_2000_2024.csv')

    get_market_actions_history_values()


def get_market_actions_history_values():
    if not os.path.exists('docs'):
        os.makedirs('docs')
    for sector in energy_sector:
        for company in sector['companies']:
            company_data = yf.download(company['symbol'], start='2000-01-01', end=now_date)
            file_name = f"{company['name']}_data.csv"
            company_data.to_csv(os.path.join('docs', file_name))
            company['data'] = company_data


def get_data_ucdp(all_data, current_date, url, csv_name, page=1):
    response = requests.get(url, params=parameters)
    data = json.loads(response.text)
    total_pages = data['TotalPages']
    print(f"total_pages: {total_pages} ")
    print(f"actual page: {page} ")
    next_page = data['NextPageUrl']
    if response.status_code == 200:
        all_data.extend(data['Result'])
    df = pd.DataFrame(all_data)
    while page < total_pages:
        try:
            if next_page != "":
                response = requests.get(next_page)
                data = json.loads(response.text)
                next_page = data['NextPageUrl']
                if response.status_code == 200:
                    all_data.extend(data['Result'])
                    df = pd.DataFrame(all_data)
                else:
                    print(f"Error al obtener los datos del UCDP para la fecha {current_date}.")

                page = page + 1
                print(f"actual page: {page} ")
            else:
                break

        except:
            print("Error")
    df.to_csv(csv_name, index=False)


if __name__ == "__main__":
    main()
