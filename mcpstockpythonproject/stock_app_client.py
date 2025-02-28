from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["stock_app.py"],  # Optional command line arguments
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
            result = await session.call_tool(tools.tools[0].name, arguments={'stock_symbol': symbol})
            print("result---------------------------", result)


if __name__ == "__main__":
    asyncio.run(get_income_statement_info('IBM'))
