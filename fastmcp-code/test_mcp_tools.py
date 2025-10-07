from . import backend
from data import datamodel

# Direct calls to your backend functions (same logic as your MCP tools)
print("=== get_ticket ===")
print(backend.get_ticket("T123"))

print("\n=== update_ticket ===")
req = datamodel.UpdateTicketRequest(status="closed", assignee="support_agent_2")
print(backend.update_ticket("T123", req))

print("\n=== suggest_response ===")
print(backend.suggest_response("T123"))

print("\n=== get_customer ===")
print(backend.get_customer("C001"))

print("\n=== search_faq ===")
print(backend.search_faq("login"))
