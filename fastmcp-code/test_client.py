from fastmcp.client import Client

async def main():
    async with Client("mcp_server.py") as client:
        result = await client.call_tool("get_ticket", {"ticket_id": "T123"})
        print("Ticket:", result)

        result = await client.call_tool("update_ticket", {"ticket_id": "T123", "status": "resolved"})
        print("Update:", result)

import asyncio
asyncio.run(main())
