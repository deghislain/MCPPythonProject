from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import streamlit as st
import json
# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["MCP_stock_app_server.py"],  # Optional command line arguments
    env=None  # Optional environment variables
)


async def get_income_statement_info(symbol: str) -> dict:
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()

            # Call a tool
            return await session.call_tool(tools.tools[0].name, arguments={'stock_symbol': symbol})


if __name__ == "__main__":
    symbol = st.text_input(':blue[Enter a stock symbol:]')
    st.button("Submit")
    if symbol:
        result = asyncio.run(get_income_statement_info(symbol))
        stock_info = json.loads(result.content[0].text)
        st.write(f"Net Income: {stock_info['netIncome']}")
        st.write(f"Fiscal Date Ending: {stock_info['fiscalDateEnding']}")
