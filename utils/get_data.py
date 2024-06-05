"""
This script fetches and processes stock market data for energy sector companies,
as well as armed conflict data from the UCDP API. The data is saved in CSV format for further analysis.
"""

import json  # Importing JSON module for working with JSON data
import yfinance as yf  # Importing yfinance for fetching stock market data
import plotly.graph_objects as go  # Importing Plotly for interactive plotting
import pandas as pd  # Importing pandas for data manipulation
import requests  # Importing requests for making HTTP requests
from datetime import datetime  # Importing datetime module for working with dates and times
import os  # Importing os module for interacting with the operating system

# Define the energy sector companies and their details
energy_sector = [
    {"sector": "Oil&Gas",
     "companies": [
         {"name": "Repsol", "country": "Spain", "symbol": "REP.MC", "data": []},
         {"name": "Exxon Mobil Corporation", "country": "USA", "symbol": "XOM", "data": []},
         {"name": "Saudi Arabian Oil Company (Aramco)", "country": "Saudi Arabia", "symbol": "2222.SR", "data": []},
         {"name": "Gazprom", "country": "Russia", "symbol": "GAZP.ME", "data": []},
         {"name": "BP plc", "country": "UK", "symbol": "BP", "data": []}
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
         {"name": "Honeywell International Inc.", "country": "USA", "symbol": "HON", "data": []},
         {"name": "Schlumberger Limited", "country": "USA", "symbol": "SLB", "data": []}
     ]},
    {"sector": "Infrastructure",
     "companies": [
         {"name": "Enagas", "country": "Spain", "symbol": "ENG.MC", "data": []},
         {"name": "Kinder Morgan, Inc.", "country": "USA", "symbol": "KMI", "data": []}
     ]}
]

# Get current date and time
now_date = datetime.now()
# Start date for fetching data
start_date = datetime(2000, 1, 1)
# URL for fetching events data
get_events_url = "https://ucdpapi.pcr.uu.se/api/gedevents/23.1"
# URL for fetching conflict data
armed_conflict_url = "https://ucdpapi.pcr.uu.se/api/ucdpprioconflict/23.1"
# End date for fetching data
end_date = datetime(now_date.year, now_date.month, now_date.day)

# Parameters for API requests
parameters = {
    "pagesize": 10000,
    "format": "json",
    "StartDate": start_date.strftime('%Y-%m-%d'),
    "EndDate": end_date.strftime('%Y-%m-%d')
}

def main():
    """
    Main function to fetch UCDP events and conflict data,
    and to get market actions history values for energy companies.
    """
    # Get events data
    get_data_ucdp([], start_date, get_events_url, '../data/ucdp_data_events_2000_2024.csv')
    # Get conflict data
    get_data_ucdp([], start_date, armed_conflict_url, '../data/ucdp_data_conflicts_2000_2024.csv')

    # Get market actions history values for energy companies
    get_market_actions_history_values()

def get_market_actions_history_values():
    """
    Fetches historical market data for each company in the energy sector
    and saves the data to CSV files in the 'docs' directory.
    """
    if not os.path.exists('../docs'):
        os.makedirs('../docs')
    for sector in energy_sector:
        for company in sector['companies']:
            # Download market data for each company
            company_data = yf.download(company['symbol'], start='2000-01-01', end=now_date)
            file_name = f"{company['name']}_data.csv"
            # Save market data to CSV file
            company_data.to_csv(os.path.join('../docs', file_name))
            company['data'] = company_data

def get_data_ucdp(all_data, current_date, url, csv_name, page=1):
    """
    Fetches data from the UCDP API and saves it to a CSV file.

    Args:
    - all_data (list): List to store the data fetched from the API.
    - current_date (datetime): The start date for fetching data.
    - url (str): The API endpoint URL.
    - csv_name (str): The name of the CSV file to save the data.
    - page (int): The page number for pagination.
    """
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
    # Save UCDP data to CSV file
    df.to_csv(csv_name, index=False)

if __name__ == "__main__":
    main()
