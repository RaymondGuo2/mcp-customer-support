from typing import Optional
from pydantic import BaseModel
# -----------------------------
# Mock databases
# -----------------------------

tickets_db = {
    "T123": {
        "id": "T123",
        "subject": "Login issue",
        "body": "I can't login",
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