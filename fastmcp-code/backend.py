from pydantic import BaseModel
from typing import Optional, List
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data import datamodel

# -----------------------------
# Functions
# -----------------------------

def get_ticket(ticket_id: str):
    ticket = datamodel.tickets_db.get(ticket_id)
    if not ticket:
        return datamodel.Ticket(id=ticket_id, subject="", body="Not found", status="missing", priority="low")
    return ticket


def update_ticket(ticket_id: str, update: datamodel.UpdateTicketRequest):
    """Update a ticket’s status or assignee."""
    ticket = datamodel.tickets_db.get(ticket_id)
    if not ticket:
        return datamodel.UpdateTicketResponse(success=False, message="Ticket not found")

    if update.status:
        ticket["status"] = update.status
    if update.assignee:
        ticket["assignee"] = update.assignee

    return datamodel.UpdateTicketResponse(success=True, message="Updated successfully", ticket=ticket)

def suggest_response(ticket_id: str):
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

def get_customer(customer_id: str):
    """Retrieve customer information."""
    customer = datamodel.customers_db.get(customer_id)
    if not customer:
        return datamodel.Customer(id=customer_id, name="Unknown", email="unknown@example.com", plan="Free")
    return customer

def search_faq(q: str) -> List[datamodel.FAQItem]:
    """Search FAQs for a given query string."""
    results = [
        datamodel.FAQItem(**f)
        for f in datamodel.faq_db
        if q.lower() in f["question"].lower() or q.lower() in f["answer"].lower()
    ]
    return results