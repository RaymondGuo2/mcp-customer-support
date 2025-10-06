from fastapi import FastAPI, Query
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel
from typing import Optional, List

# -----------------------------
# Mock databases
# -----------------------------

tickets_db = {
    "T123": {
        "id": "T123",
        "subject": "Login issue",
        "body": "I can't log in",
        "status": "open",
        "priority": "low",
        "assignee": "support_agent_1",
        "customer_id": "C001"
    }
}

customers_db = {
    "C001": {
        "id": "C001",
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "plan": "Premium"
    }
}

faq_db = [
    {"question": "How do I reset my password?", "answer": "Click 'Forgot Password' on the login page."},
    {"question": "Why can't I log in?", "answer": "Check if your password is correct or reset it."},
    {"question": "How to contact support?", "answer": "You can email us at support@example.com."}
]

# -----------------------------
# Models
# -----------------------------

class Ticket(BaseModel):
    id: str
    subject: str
    body: str
    status: str
    priority: str
    assignee: Optional[str] = None
    customer_id: Optional[str] = None


class UpdateTicketRequest(BaseModel):
    status: Optional[str] = None
    assignee: Optional[str] = None


class UpdateTicketResponse(BaseModel):
    success: bool
    message: str
    ticket: Optional[Ticket] = None


class Customer(BaseModel):
    id: str
    name: str
    email: str
    plan: str


class FAQItem(BaseModel):
    question: str
    answer: str


class SuggestedResponse(BaseModel):
    ticket_id: str
    suggested_text: str

# -----------------------------
# FastAPI + MCP Setup
# -----------------------------

app = FastAPI()
mcp = FastApiMCP(app, name="support-assistant-fastapi")
mcp.mount()

# -----------------------------
# Endpoints
# -----------------------------

@app.get("/tickets/{ticket_id}", response_model=Ticket)
async def get_ticket(ticket_id: str):
    """Fetch a ticket by ID."""
    ticket = tickets_db.get(ticket_id)
    if not ticket:
        return Ticket(id=ticket_id, subject="", body="Not found", status="missing", priority="low")
    return ticket


@app.post("/tickets/{ticket_id}/actions/update", response_model=UpdateTicketResponse)
async def update_ticket(ticket_id: str, update: UpdateTicketRequest):
    """Update a ticket’s status or assignee."""
    ticket = tickets_db.get(ticket_id)
    if not ticket:
        return UpdateTicketResponse(success=False, message="Ticket not found")

    if update.status:
        ticket["status"] = update.status
    if update.assignee:
        ticket["assignee"] = update.assignee

    return UpdateTicketResponse(success=True, message="Updated successfully", ticket=ticket)


@app.post("/tickets/{ticket_id}/actions/suggest_response", response_model=SuggestedResponse)
async def suggest_response(ticket_id: str):
    """Suggest an automated response for a ticket."""
    ticket = tickets_db.get(ticket_id)
    if not ticket:
        return SuggestedResponse(ticket_id=ticket_id, suggested_text="Ticket not found.")

    # Naive suggestion logic (replace with LLM in production)
    body = ticket["body"].lower()
    if "login" in body:
        suggestion = "Please try resetting your password or confirm your email address is correct."
    elif "refund" in body:
        suggestion = "Our team will review your request and issue a refund if applicable."
    else:
        suggestion = "Thank you for reaching out! Our support team will respond shortly."

    return SuggestedResponse(ticket_id=ticket_id, suggested_text=suggestion)


@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: str):
    """Retrieve customer information."""
    customer = customers_db.get(customer_id)
    if not customer:
        return Customer(id=customer_id, name="Unknown", email="unknown@example.com", plan="Free")
    return customer


@app.get("/faq/search", response_model=List[FAQItem])
async def search_faq(q: str = Query(..., description="Search query for FAQ")):
    """Search FAQs for a given query string."""
    results = [f for f in faq_db if q.lower() in f["question"].lower() or q.lower() in f["answer"].lower()]
    return results