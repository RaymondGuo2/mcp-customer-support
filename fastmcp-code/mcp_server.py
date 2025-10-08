# -----------------------------
# MCP Tool Assignment
# -----------------------------

from fastmcp import FastMCP
import backend

mcp = FastMCP("support-assistant", stateless_http=True)

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

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)

