from mcp.server.fastmcp import FastMCP
from MCP_stock_tools import StockTools as tools
import os

mcp = FastMCP("StockApp")
AV_STOCK_API_KEY = os.environ.get('AV_STOCK_API_KEY')


def get_income_statement_info(stock_symbol: str) -> dict:
    """
       Retrieves the last year net income for a given stock.

       Args:
           stock_symbol: The stock symbol, e.g., "IBM".

       Returns:
           A dictionary containing the last income with fiscal date ending.
       """
    print(f"Getting last year net income for {stock_symbol}")
    return tools.call_stock_service_info(stock_symbol)


if __name__ == "__main__":
    mcp.run(transport='stdio')
