from openai import AzureOpenAI, OpenAI
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

allowed_tools = [
    "tool_get_ticket",
    "tool_update_ticket",
    "tool_suggest_response",
    "tool_get_customer",
    "tool_search_faq"
]

ngrok_url = "https://uncombinative-unprotesting-anders.ngrok-free.dev"
server_url = f"{ngrok_url}/mcp"

class MCPClient:
    def __init__(self, model:str="gpt-4o-mini"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.allowed_tools = allowed_tools

    def ask(self, user_input:str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_input})

        response = self.client.responses.create(
            model = self.model,
            input = messages,
            tools=[
                {
                    "type": "web_search"
                },
                {
                    "type": "mcp",
                    "server_url": server_url,
                    "server_label": "support-assistant",
                    "allowed_tools": allowed_tools,
                    "require_approval": "never",
                }

            ]
        )
        return response.output

# async def run_agent(user_input: str):
#     # Get the OpenAI-style tool definitions
#     tools = await mcp_server.mcp._tool_manager.list_tools()
#     openai_tools = convert_to_openai_tools(tools)
#     for t in openai_tools:
#         print(f"⚒️: {t['name']} and {t['parameters']}")

    

if __name__ == "__main__":
    client = MCPClient()
    while True:
        customer_query = input()
        client.ask(customer_query)