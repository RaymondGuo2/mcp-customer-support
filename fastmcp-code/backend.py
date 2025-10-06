"""
FastMCP allows you to write tools directly without the need for FastAPI if REST endpoints aren't needed
"""

tickets_db = {
    "T123": {"id":"T123","subject":"Login issue","body":"I can't log in","status":"open","priority":"low","customer_id":"C42"}
}

def get_ticket(ticket_id: str):
    return tickets_db.get(ticket_id, {"error": "Not found"})

def update_ticket(ticket_id: str, status: str = None, assignee: str = None):
    ticket = tickets_db.get(ticket_id)
    if not ticket:
        return {"success": False, "message": "Ticket not found"}
    if status:
        ticket["status"] = status
    if assignee:
        ticket["assignee"] = assignee
    return {"success": True, "message": "Updated successfully"}
