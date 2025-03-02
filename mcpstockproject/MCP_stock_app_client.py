from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import streamlit as st
import anthropic
from utils import load_config

config = load_config()
dep_config = config["deployment"]
# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["MCP_stock_app_server.py"],  # Optional command line arguments
    env=None  # Optional environment variables
)


async def get_income_statement_info(symbol: str) -> str:
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            final_answer = ""
            # List available tools
            tools = await session.list_tools()
            available_tools = [{
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            } for tool in tools.tools]
            client = anthropic.Anthropic(
                api_key=dep_config["ANTHROPIC_API_KEY"],
            )
            query = "Retrieve the last year net income for this stock: " + symbol
            messages = [
                {
                    "role": "user",
                    "content": query
                }
            ]
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=messages,
                tools=available_tools
            )
            tool_results = []
            final_text = []
            assistant_message_content = []
            for content in response.content:
                if content.type == 'text':
                    final_text.append(content.text)
                    assistant_message_content.append(content)
                elif content.type == 'tool_use':
                    tool_name = content.name
                    tool_args = content.input
                    result = await session.call_tool(tool_name, tool_args)
                    tool_results.append({"call": tool_name, "result": result})
                    final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")
                    assistant_message_content.append(content)
                    messages.append({
                        "role": "assistant",
                        "content": assistant_message_content
                    })
                    messages.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": content.id,
                                "content": result.content
                            }
                        ]
                    })

                    # Get next response from Claude
                    response = client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=1000,
                        messages=messages,
                        tools=available_tools
                    )

                    final_text.append(response.content[0].text)

                    final_answer = final_text[2]

    return final_answer



if __name__ == "__main__":
    symbol = st.text_input(':blue[Enter a stock symbol:]')
    st.button("Submit")
    if symbol:
        result = asyncio.run(get_income_statement_info(symbol))
        st.write(result)
