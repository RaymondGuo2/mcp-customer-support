from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel
from typing import Optional, Dict

# --- Mock Database (to be replaced) ---
tickets_db = {
    "T123": {
        "id": "T123",
        "subject": "Login issue",
        "body": "I can't log in",
        "status": "open",
        "priority": "low",
    }
}

# --- Define models for requests and responses ---
class Ticket(BaseModel):
    id: str
    subject: str
    body: str
    status: str
    priority: str
    assignee: Optional[str] = None

class UpdateTicketRequest(BaseModel):
    status: Optional[str] = None
    assignee: Optional[str] = None

class UpdateTicketResponse(BaseModel):
    success: bool
    message: str
    ticket: Optional[Ticket] = None


app = FastAPI("Support Assistant API")
mcp = FastApiMCP(app, name="support-assistant-fastapi")
mcp.mount()

@app.get("/tickets/{ticket_id}", response_model=Ticket)
async def get_ticket(ticket_id: str):
    """
    Fetch a support ticket by ID.
    """
    ticket = tickets_db.get(ticket_id)
    if not ticket:
        # return a default object to preserve schema consistency
        return Ticket(id=ticket_id, subject="", body="Not found", status="missing", priority="low")
    return ticket

@app.post("/tickets/{ticket_id}/update", response_model=UpdateTicketResponse)
async def update_ticket(ticket_id: str, update: UpdateTicketRequest):
    """
    Update the status or assignee of a ticket.
    """
    ticket = tickets_db.get(ticket_id)
    if not ticket:
        return UpdateTicketResponse(success=False, message="Ticket not found")

    if update.status:
        ticket["status"] = update.status
    if update.assignee:
        ticket["assignee"] = update.assignee

    return UpdateTicketResponse(success=True, message="Updated successfully", ticket=ticket)
