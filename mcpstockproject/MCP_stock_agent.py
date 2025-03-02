import anthropic
from utils import load_config
config = load_config()
dep_config = config["deployment"]


class StockAgent:
    def __init__(self, session):
        self.session = session
        self.result = ""

    async def fetch_data(self, prompt):
        tools = await self.session.list_tools()
        available_tools = [
            {"name": tool.name, "description": tool.description, "input_schema": tool.inputSchema}
            for tool in tools.tools
        ]
        client = anthropic.Anthropic(api_key=dep_config["ANTHROPIC_API_KEY"])

        messages = [
            {"role": "user", "content": prompt}
        ]
        response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=messages,
                tools=available_tools
        )
        if response.content:
            return available_tools, messages, response.content, client
        else:
            return None

    async def parse_data(self, messages, available_tools, response, client):
        final_text = []
        if response:
            tool_results = []
            assistant_message_content = []
            for content in response:
                if content.type == 'text':
                    final_text.append(content.text)
                    assistant_message_content.append(content)
                elif content.type == 'tool_use':
                    tool_name = content.name
                    tool_args = content.input
                    result = await self.session.call_tool(tool_name, tool_args)
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

        return final_text[2]

    async def run(self, prompt):
        """
        Execute the prompt.

        Args:
            prompt that contains the user query

        Returns:
            the answer to the user query
        """
        if not prompt:
            print("No prompt provided.")
            return
        else:
            available_tools, messages, response, client = await self.fetch_data(prompt)
            return await self.parse_data(messages,available_tools, response, client)