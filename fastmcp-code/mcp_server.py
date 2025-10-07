# -----------------------------
# MCP Tool Assignment
# -----------------------------

from fastmcp import FastMCP
from . import backend
from data import datamodel
from pydantic import BaseModel
from typing import Optional

mcp = FastMCP("support-assistant")

@mcp.tool()
def tool_get_ticket(ticket_id: str):
    """Fetch a support ticket by ID."""
    return backend.get_ticket(ticket_id)

@mcp.tool()
def tool_update_ticket(ticket_id: str, status: str | None = None, assignee: str | None = None):
    """Update a ticket’s status or assignee."""
    req = backend.UpdateTicketRequest(status=status, assignee=assignee)
    return backend.update_ticket(ticket_id, req)

@mcp.tool()
def tool_suggest_response(ticket_id: str):
    """Suggest an automated response for a ticket."""
    return backend.suggest_response(ticket_id)

@mcp.tool()
def tool_get_customer(customer_id: str):
    """Retrieve customer information."""
    return backend.get_customer(customer_id)

@mcp.tool()
def tool_search_faq(q: str):
    """Search the FAQ database for a given query."""
    return backend.search_faq(q)

# -----------------------------
# LLM Integration
# -----------------------------
from openai import AzureOpenAI, OpenAI
import json
import os
import asyncio
from .util import convert_to_openai_tools
from dotenv import load_dotenv

load_dotenv()


"""
Optionally choose between AzureOpenAI and OpenAI directly
"""

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")


client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_API_KEY
)

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=OPENAI_API_KEY)

async def run_agent(user_input: str):
    tools = await mcp._tool_manager.list_tools()
    print(tools)
    openai_tools = convert_to_openai_tools(tools)
    print(openai_tools)
    # double-check nothing unserializable remains
    json.dumps(openai_tools)  # should not raise any errors

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a support assistant."},
            {"role": "user", "content": user_input},
        ],
        tools=openai_tools,  # ✅ now guaranteed serializable
    )

    message = response.choices[0].message
    if getattr(message, "tool_calls", None):
        for call in message.tool_calls:
            tool_name = call.function.name
            tool_args = await parse_tool_args(tool_name, call.function.arguments)
            result = await mcp._tool_manager.call_tool(tool_name, tool_args)
            print(f"🛠️ Tool call: {tool_name}({tool_args}) → {result}")

    else:
        print("💬 LLM:", message.content)

async def parse_tool_args(tool_name, args_raw):
    """Convert LLM-provided arguments into a dict for FastMCP."""
    if isinstance(args_raw, dict):
        return args_raw  # already good

    # try to parse JSON if it’s a string
    try:
        parsed = json.loads(args_raw)
        if isinstance(parsed, dict):
            return parsed
    except (json.JSONDecodeError, TypeError):
        parsed = args_raw

    # fallback for single-argument tools
    tools = await mcp._tool_manager.list_tools()
    tool_def = next(t for t in tools if t.key == tool_name)
    param_names = list(tool_def.args_schema.model_fields.keys())
    if len(param_names) == 1:
        return {param_names[0]: parsed}

    raise ValueError(f"Cannot parse arguments for tool {tool_name}: {args_raw}")

if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        asyncio.run(run_agent(user_input))
