from typing import List, Dict
import stock_service_utils as stock_dict_keys
import os
import requests

AV_STOCK_API_KEY = os.environ.get('AV_STOCK_API_KEY')


def get_dictionary_keys(key_type):
    if key_type == 'income_statement':
        return stock_dict_keys.get_income_statement_keys()
    elif key_type == 'balance_sheet':
        return stock_dict_keys.get_balance_sheet_keys()
    elif key_type == 'cash_flow':
        return stock_dict_keys.get_cash_flow_keys()
    elif key_type == 'earnings':
        return stock_dict_keys.get_earnings_keys()
    elif key_type == 'insiders_tx':
        return stock_dict_keys.get_insider_tx_keys()


def retrieve_stock_last_3years_info(stock_data, key_type, info_type) -> List[Dict]:
    """
    Retrieves stock information for the last consecutive 3 years from a JSON object
    and returns a list of dictionaries representing each year.

    Args:
        stock_data (object): Object containing JSON data with annual reports.
        key_type: The type of key representing a specific type of stock data e.g income statement
        info_type: the type of information being retrieved e.g annualReports

    Returns:
        list: List of dictionaries, each representing a specific type of stock data for a year.
    """

    info_list = stock_data.json()[info_type]

    last_3year_info = []
    for report in info_list[:3]:  # Get the last 3 annual reports
        info = {key: report[key] for key in get_dictionary_keys(key_type)}
        last_3year_info.append(info)

    return last_3year_info


class StockTools:
    def call_income_statement_info_service(stock_symbol: str) -> List[Dict]:
        """
           Retrieves the income statements info for a given stock for the last 3 years'

           Args:
               stock_symbol: The stock symbol, e.g., "IBM".

           Returns:
               A set of dictionary containing the income statements info for a given stock for the last 3 years
           """
        print(f"Getting last year net income for {stock_symbol}")
        try:
            stock_url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={stock_symbol}&apikey={AV_STOCK_API_KEY}"
            stock_data = requests.get(stock_url)
            return retrieve_stock_last_3years_info(stock_data, 'income_statement', 'annualReports')

        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return []

    def call_balance_sheet_info_service(stock_symbol: str) -> List[Dict]:
        """
           Retrieves the balance sheet info for a given stock for the last 3 years'

           Args:
               stock_symbol: The stock symbol, e.g., "IBM".

           Returns:
               A set of dictionary containing the balance sheet info for a given stock for the last 3 years
           """
        print(f"Getting last year balance sheet for {stock_symbol}")
        try:
            stock_url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={stock_symbol}&apikey={AV_STOCK_API_KEY}"
            stock_data = requests.get(stock_url)
            return retrieve_stock_last_3years_info(stock_data, 'balance_sheet', 'annualReports')

        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return []

    def call_cash_flow_info_service(stock_symbol: str) -> List[Dict]:
        """
           Retrieves the cash flow info for a given stock for the last 3 years'

           Args:
               stock_symbol: The stock symbol, e.g., "IBM".

           Returns:
               A set of dictionary containing the cash flow info for a given stock for the last 3 years
           """
        print(f"Getting last year cash flow for {stock_symbol}")
        try:
            stock_url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={stock_symbol}&apikey={AV_STOCK_API_KEY}"
            stock_data = requests.get(stock_url)
            return retrieve_stock_last_3years_info(stock_data, 'cash_flow', 'annualReports')

        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return []

    def call_earnings_info_service(stock_symbol: str) -> List[Dict]:
        """
           Retrieves the earnings info for a given stock for the last 3 years'

           Args:
               stock_symbol: The stock symbol, e.g., "IBM".

           Returns:
               A set of dictionary containing the earnings info for a given stock for the last 3 years
           """
        print(f"Getting last year cash flow for {stock_symbol}")
        try:
            stock_url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={stock_symbol}&apikey={AV_STOCK_API_KEY}"
            stock_data = requests.get(stock_url)
            return retrieve_stock_last_3years_info(stock_data, 'earnings', 'annualEarnings')

        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return []

    def call_insider_tx_info_service(stock_symbol: str) -> List[Dict]:
        """
           Retrieves the insiders transaction info for a given stock for the last 3 years'

           Args:
               stock_symbol: The stock symbol, e.g., "IBM".

           Returns:
               A set of dictionary containing the insiders transaction info for a given stock for the last 3 years
           """
        print(f"Getting last year insider transaction for {stock_symbol}")
        try:
            stock_url = f"https://www.alphavantage.co/query?function=INSIDER_TRANSACTIONS&symbol={stock_symbol}&apikey={AV_STOCK_API_KEY}"
            stock_data = requests.get(stock_url)
            return retrieve_stock_last_3years_info(stock_data, 'insiders_tx', 'data')

        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return []

    def call_weekly_adjusted_info_service(stock_symbol: str) -> List[Dict]:
        """
           Retrieves the daily stock data info for a given stock for the last 3 years'

           Args:
               stock_symbol: The stock symbol, e.g., "IBM".

           Returns:
               A set of dictionary containing the daily stock data info for a given stock for the last 3 years
           """
        print(f"Getting daily adjusted stock data for {stock_symbol}")
        try:
            stock_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={stock_symbol}&apikey={AV_STOCK_API_KEY}"
            stock_data = requests.get(stock_url)
            previous_refresh = stock_data.json()['Meta Data']['3. Last Refreshed']
            weekly_adjusted_data = stock_data.json()['Weekly Adjusted Time Series']
            last_quarter = []

            for count in range(12):
                try:
                    week_dict ={previous_refresh: {key: weekly_adjusted_data[previous_refresh][key] for key in stock_dict_keys.get_weekly_adjusted_keys()}}
                    last_quarter.append(week_dict)
                    previous_refresh = stock_dict_keys.get_date_one_week_ago(previous_refresh)
                except Exception as e:
                    print(f"Error while parsing weekly adjusted data: {e}")

            return last_quarter
        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return []

