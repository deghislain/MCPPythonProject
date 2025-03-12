import os
import requests

MISTRAL_API_KEY = os.environ.get('MISTRAL_API_KEY')


class StockTools:
    def call_stock_service_info(stock_symbol: str) -> dict:
        """
                  Retrieves the last year net income for a given stock.

                  Args:
                      stock_symbol: The stock symbol, e.g., "IBM".

                  Returns:
                      A dictionary containing the last income with fiscal date ending.
                  """
        print(f"Getting last year net income for {stock_symbol}")
        try:
            stock_url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={stock_symbol}&apikey={MISTRAL_API_KEY}"
            stock_data = requests.get(stock_url)
            fiscal_date_ending = stock_data.json()["annualReports"][0]["fiscalDateEnding"]
            net_income = stock_data.json()["annualReports"][0]["netIncome"]
            return {
                "fiscalDateEnding": fiscal_date_ending,
                "netIncome": net_income
            }
        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return {
                "fiscalDateEnding": "none",
                "netIncome": "none"
            }
