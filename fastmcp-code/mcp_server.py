from fastmcp import FastMCP
import backend

mcp = FastMCP("support-assistant")

@mcp.tool
def get_ticket(ticket_id: str) -> dict:
    """Fetch a support ticket by ID"""
    return backend.get_ticket(ticket_id)

@mcp.tool
def update_ticket(ticket_id: str, status: str = None, assignee: str = None) -> dict:
    """Update a ticket's status or assignee"""
    return backend.update_ticket(ticket_id, status, assignee)

if __name__ == "__main__":
    mcp.run()
