from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import streamlit as st
from MCP_stock_agent import StockAgent

server_params = StdioServerParameters(
    command="python",  # Executable
    args=["MCP_stock_app_server.py"],  # Optional command line arguments
    env=None  # Optional environment variables
)


async def get_income_statement_info(prompt: str) -> str:
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            stock_agent = StockAgent(session)
            return await stock_agent.run(prompt)


if __name__ == "__main__":
    symbol = st.text_input(':blue[Enter a stock symbol:]')
    st.button("Submit")
    if symbol:
        prompt = "Retrieve the last year net income for this stock: " + symbol
        result = asyncio.run(get_income_statement_info(prompt))
        st.write(result)
