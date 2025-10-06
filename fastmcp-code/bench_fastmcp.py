import asyncio, time
from fastmcp.client import Client

async def bench_mcp(n=1000):
    client = Client("mcp_server.py")
    async with client:
        start = time.perf_counter()
        for _ in range(n):
            res = await client.call_tool("get_ticket", {"ticket_id": "T123"})
        elapsed = time.perf_counter() - start
        print(f"MCP {n} calls in {elapsed:.2f}s → {n/elapsed:.1f} req/s")

asyncio.run(bench_mcp())
