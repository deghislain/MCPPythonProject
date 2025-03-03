from langchain_mcp_tools import convert_mcp_to_langchain_tools
import asyncio
import logging
import sys
from utils import load_config
import streamlit as st

config = load_config()
dep_config = config["deployment"]

try:
    from langchain.chat_models import init_chat_model
    from langchain.schema import HumanMessage
    from langgraph.prebuilt import create_react_agent
except ImportError as e:
    print(f'\nError: Required package not found: {e}')
    print('Please ensure all required packages are installed\n')
    sys.exit(1)

def init_logger() -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,  # logging.DEBUG,
        format='\x1b[90m[%(levelname)s]\x1b[0m %(message)s'
    )
    return logging.getLogger()


async def get_income_statement_info(prompt: str) -> str:
    try:
        mcp_configs = {
            'stock_tools': {
                'command': 'python',
                'args': [
                    '-m',
                    'MCP_stock_app_server'
                ]
            }
        }

        tools, cleanup = await convert_mcp_to_langchain_tools(
            mcp_configs,
            init_logger()
        )

        llm = init_chat_model(
            model="claude-3-5-sonnet-20241022",
            model_provider='anthropic',
            api_key=dep_config["ANTHROPIC_API_KEY"],
            temperature=0,
            max_tokens=1000
        )

        agent = create_react_agent(
            llm,
            tools
        )

        messages = [HumanMessage(content=prompt)]

        result = await agent.ainvoke({'messages': messages})

        result_messages = result['messages']
        # the last message should be an AIMessage
        response = result_messages[-1].content

    finally:
        if cleanup is not None:
            await cleanup()
    return response



if __name__ == "__main__":
    symbol = st.text_input(':blue[Enter a stock symbol:]')
    st.button("Submit")
    if symbol:
        prompt = "Retrieve the last year net income for this stock: " + symbol
        result = asyncio.run(get_income_statement_info(prompt))
        st.write(result)
