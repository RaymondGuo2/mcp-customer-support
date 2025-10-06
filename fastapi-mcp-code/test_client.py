import asyncio
from fastapi_mcp.client import MCPClient

async def main():
    client = MCPClient("http://127.0.0.1:8000/mcp")
    async with client:
        ticket = await client.call_tool("get_ticket", {"ticket_id": "T123"})
        print("Ticket:", ticket)

        result = await client.call_tool(
            "update_ticket", {"ticket_id": "T123", "status": "resolved"}
        )
        print("Update:", result)

if __name__ == "__main__":
    asyncio.run(main())
