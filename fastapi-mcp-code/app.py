from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

tickets_db = {
    "T123": {"id": "T123", "subject": "Login issue", "body": "I can't log in", "status": "open", "priority": "low"}
}

app = FastAPI()
mcp = FastApiMCP(app, name="support-assistant-fastapi")
mcp.mount()

@app.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: str):
    """Fetch a ticket by ID"""
    return tickets_db.get(ticket_id, {"error": "Not found"})

@app.post("/tickets/{ticket_id}/update")
async def update_ticket(ticket_id: str, status: str | None = None, assignee: str | None = None):
    """Update a ticket’s status or assignee"""
    ticket = tickets_db.get(ticket_id)
    if not ticket:
        return {"success": False, "message": "Ticket not found"}
    if status:
        ticket["status"] = status
    if assignee:
        ticket["assignee"] = assignee
    return {"success": True, "message": "Updated successfully"}