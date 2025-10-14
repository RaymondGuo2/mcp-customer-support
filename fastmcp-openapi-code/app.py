from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from typing import List
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data import datamodel

# -----------------------------
# FastAPI + MCP Setup
# -----------------------------

app = FastAPI(title="support-assistant")

# -----------------------------
# Endpoints
# -----------------------------

@app.get("/tickets/{ticket_id}", operation_id="get_ticket", response_model=datamodel.Ticket)
async def get_ticket(ticket_id: str):
    """Fetch a ticket by ID."""
    ticket = datamodel.tickets_db.get(ticket_id)
    if not ticket:
        return datamodel.Ticket(id=ticket_id, subject="", body="Not found", status="missing", priority="low")
    return ticket


@app.post("/tickets/{ticket_id}/actions/update",operation_id="update_ticket", response_model=datamodel.UpdateTicketResponse)
async def update_ticket(ticket_id: str, update: datamodel.UpdateTicketRequest):
    """Update a ticket’s status or assignee."""
    ticket = datamodel.tickets_db.get(ticket_id)
    if not ticket:
        return datamodel.UpdateTicketResponse(success=False, message="Ticket not found")

    if update.status:
        ticket["status"] = update.status
    if update.assignee:
        ticket["assignee"] = update.assignee

    return datamodel.UpdateTicketResponse(success=True, message="Updated successfully", ticket=ticket)


@app.post("/tickets/{ticket_id}/actions/suggest_response", operation_id="suggest_response", response_model=datamodel.SuggestedResponse)
async def suggest_response(ticket_id: str):
    """Suggest an automated response for a ticket."""
    ticket = datamodel.tickets_db.get(ticket_id)
    if not ticket:
        return datamodel.SuggestedResponse(ticket_id=ticket_id, suggested_text="Ticket not found.")

    # Naive suggestion logic (replace with LLM in production)
    body = ticket["body"].lower()
    if "login" in body:
        suggestion = "Please try resetting your password or confirm your email address is correct."
    elif "refund" in body:
        suggestion = "Our team will review your request and issue a refund if applicable."
    else:
        suggestion = "Thank you for reaching out! Our support team will respond shortly."

    return datamodel.SuggestedResponse(ticket_id=ticket_id, suggested_text=suggestion)


@app.get("/customers/{customer_id}", operation_id="get_customer",response_model=datamodel.Customer)
async def get_customer(customer_id: str):
    """Retrieve customer information."""
    customer = datamodel.customers_db.get(customer_id)
    if not customer:
        return datamodel.Customer(id=customer_id, name="Unknown", email="unknown@example.com", plan="Free")
    return customer


@app.get("/faq/search", operation_id="search_faq", response_model=List[datamodel.FAQItem])
async def search_faq(q: str = Query(..., description="Search query for FAQ")):
    """Search FAQs for a given query string."""
    results = [f for f in datamodel.faq_db if q.lower() in f["question"].lower() or q.lower() in f["answer"].lower()]
    return results


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
