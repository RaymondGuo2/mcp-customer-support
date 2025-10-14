import httpx
from fastmcp import FastMCP


# Final bit that needs to be run
client = httpx.AsyncClient(
    base_url="http://127.0.0.1:8000",
    headers={"Accept": "text/event-stream"}
    )

openapi_spec = httpx.get("http://127.0.0.1:8000/openapi.json").json()
print(openapi_spec)

mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name="Customer Support Assistant"
    )

if __name__ == "__main__":
    mcp.run(transport="http", port=8001, stateless_http=True)

# import asyncio
# import httpx
# from fastmcp import FastMCP
# import logging
# logging.basicConfig(level=logging.DEBUG)


# async def main():
#     async with httpx.AsyncClient(
#         base_url="http://127.0.0.1:8000",
#         headers={"Accept": "text/event-stream"},
#     ) as client:
#         # Load the OpenAPI spec properly within async context
#         response = await client.get("/openapi.json", headers={"Accept": "application/json"})
#         response.raise_for_status()
#         openapi_spec = response.json()
#         print("✅ OpenAPI spec loaded successfully")

#         # Initialize FastMCP
#         mcp = FastMCP.from_openapi(
#             openapi_spec=openapi_spec,
#             client=client,
#             name="support-assistant",
#             stateless_http=True,
#         )

#         # Run the MCP server
#         await mcp.run_async(transport="http", port=8001)


# if __name__ == "__main__":
#     asyncio.run(main())
