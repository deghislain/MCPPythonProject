from langchain_mcp_tools import convert_mcp_to_langchain_tools
from langchain.chat_models import init_chat_model
from langchain.schema import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from MCP_stock_app_server import mcp
import asyncio
import logging
from utils import load_config, read_yaml_file
import streamlit as st

config = load_config()
dep_config = config["deployment"]


def init_logger() -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,  # logging.DEBUG,
        format='\x1b[90m[%(levelname)s]\x1b[0m %(message)s'
    )
    return logging.getLogger()


async def write_financial_report(tools, stock_symbol) -> str:
    llm = init_chat_model(
        model="claude-3-5-sonnet-20241022",
        model_provider='anthropic',
        api_key=load_config()["deployment"]["ANTHROPIC_API_KEY"],
        temperature=0,
        max_tokens=8000
    )

    agent = create_react_agent(
        llm,
        tools
    )

    # Define the system prompt and messages
    system_prompt = await mcp.get_prompt('get_report_system_prompt')
    messages = [
        SystemMessage(
            content=system_prompt.messages[0].content.text
        ),
        HumanMessage(
            content=stock_symbol
        )
    ]

    result = await agent.ainvoke({'messages': messages})

    result_messages = result['messages']
    # the last message should be an AIMessage
    return result_messages[-1].content


async def perform_financial_analyze(financial_report, tools, stock_symbol) -> str:
    prompt = f"""Perform a comprehensive financial analysis for this stock: {stock_symbol}.
    Your analyse must be based on the provided financial report. Ensure you highlighting key trends,
     strengths, weaknesses, and areas for improvement. Here is the financial report{financial_report}"""

    llm = init_chat_model(
        model="claude-3-5-sonnet-20241022",
        model_provider='anthropic',
        api_key=load_config()["deployment"]["ANTHROPIC_API_KEY"],
        temperature=0,
        max_tokens=8000
    )

    agent = create_react_agent(
        llm,
        tools
    )

    # Define the system prompt and messages
    system_prompt = await mcp.get_prompt('get_analyse_system_prompt')
    messages = [
        SystemMessage(
            content=system_prompt.messages[0].content.text
        ),
        HumanMessage(
            content=prompt
        )
    ]

    result = await agent.ainvoke({'messages': messages})

    result_messages = result['messages']
    # the last message should be an AIMessage
    return result_messages[-1].content


async def get_stock_info(stock_symbol: str) -> str:
    mcp_configs = read_yaml_file("mcp_configs.yaml")['mcp_configs']

    tools, cleanup = await convert_mcp_to_langchain_tools(
        mcp_configs,
        init_logger()
    )
    response = None
    try:
        financial_report = await write_financial_report(tools, stock_symbol)
        response = await perform_financial_analyze(financial_report, tools, stock_symbol)
    except (FileNotFoundError, ValueError) as e:
        print(e)
    finally:
        if cleanup is not None:
            await cleanup()
    return response


if __name__ == "__main__":
    symbol = st.text_input(':blue[Enter a stock symbol:]')
    submit_btn = st.button("Submit")
    if symbol and submit_btn:
        result = asyncio.run(get_stock_info(symbol))
        st.write(result)
