from mcp.server.fastmcp import FastMCP
from MCP_stock_tools import StockTools as tools
from MCP_stock_prompt import get_report_prompt, get_analyse_prompt
from typing import List, Dict

mcp = FastMCP("StockApp")


@mcp.tool()
def get_income_statement_info(stock_symbol: str) -> List[Dict]:
    """
       Retrieves the income statements info for a given stock for the last 3 years'

       Args:
           stock_symbol: The stock symbol, e.g., "IBM".

       Returns:
           A set of dictionary containing the income statements info for a given stock for the last 3 years
       """
    print(f"Getting last year net income for {stock_symbol}")
    return tools.call_income_statement_info_service(stock_symbol)


@mcp.tool()
def get_balance_sheet_info(stock_symbol: str) -> List[Dict]:
    """
       Retrieves the balance sheet info for a given stock for the last 3 years'

       Args:
           stock_symbol: The stock symbol, e.g., "IBM".

       Returns:
           A set of dictionary containing the balance sheet info for a given stock for the last 3 years
       """

    return tools.call_balance_sheet_info_service(stock_symbol)


@mcp.tool()
def get_cash_flow_info(stock_symbol: str) -> List[Dict]:
    """
     Retrieves the cash flow info for a given stock for the last 3 years'

     Args:
         stock_symbol: The stock symbol, e.g., "IBM".

     Returns:
         A set of dictionary containing the cash flow info for a given stock for the last 3 years
     """

    return tools.call_cash_flow_info_service(stock_symbol)


@mcp.tool()
def get_earnings_info(stock_symbol: str) -> List[Dict]:
    """
       Retrieves the earnings info for a given stock for the last 3 years'

       Args:
           stock_symbol: The stock symbol, e.g., "IBM".

       Returns:
           A set of dictionary containing the earnings info for a given stock for the last 3 years
       """

    return tools.call_earnings_info_service(stock_symbol)


@mcp.tool()
def get_insiders_tx_info(stock_symbol: str) -> List[Dict]:
    """
       Retrieves the insiders transaction info for a given stock for the last 3 years'

       Args:
           stock_symbol: The stock symbol, e.g., "IBM".

       Returns:
           A set of dictionary containing the insiders transaction info for a given stock for the last 3 years
       """

    return tools.call_insider_tx_info_service(stock_symbol)


@mcp.tool()
def get_weekly_adjusted_info(stock_symbol: str) -> List[Dict]:
    """
         Retrieves the daily stock data info for a given stock for the last 3 years'

         Args:
             stock_symbol: The stock symbol, e.g., "IBM".

         Returns:
             A set of dictionary containing the daily stock data info for a given stock for the last 3 years
         """

    return tools.call_weekly_adjusted_info_service(stock_symbol)

@mcp.tool()
def generate_pdf_doc(analyze_doc: str) -> None:
    """
    Generate a PDF from the provided markdown content.

    :param analyze_doc: The markdown content to convert into a PDF
    """

    return tools.generate_pdf(analyze_doc)


@mcp.prompt()
def get_report_system_prompt() -> str:
    """ Returns the system report prompt """
    return get_report_prompt()

@mcp.prompt()
def get_analyse_system_prompt() -> str:
    """ Returns the system analyse prompt """
    return get_analyse_prompt()


if __name__ == "__main__":
    mcp.run(transport='stdio')
