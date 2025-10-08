from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

load_dotenv()
console = Console()

# ----------------------------------------
# Configuration
# ----------------------------------------

allowed_tools = [
    "get_ticket",
    "update_ticket",
    "suggest_response",
    "get_customer",
    "search_faq"
]

# Replace with your running FastAPI MCP ngrok or local URL
ngrok_url = "https://uncombinative-unprotesting-anders.ngrok-free.dev"
server_url = f"{ngrok_url}/mcp"  # The MCP entrypoint created by FastApiMCP.mount()

# ----------------------------------------
# MCP Client for FastAPI-MCP
# ----------------------------------------

class MCPClientFastAPI:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.allowed_tools = allowed_tools

        console.print(
            Panel.fit(
                f"[bold green]Initialized MCPClientFastAPI[/bold green]\nModel: {model}",
                title="✅ Ready"
            )
        )

    def _log_tools(self, tool_calls: List[Dict[str, Any]]):
        """Pretty-print any tool calls."""
        if not tool_calls:
            return

        table = Table(title="🔧 Tool Invocations", show_lines=True)
        table.add_column("Tool Name", style="cyan")
        table.add_column("Arguments", style="magenta")

        for call in tool_calls:
            name = call.get("name", "Unknown Tool")
            args = str(call.get("arguments", {}))
            table.add_row(name, args)

        console.print(table)

    def _log_response(self, response: Any):
        """Display model output and any associated tool logs."""
        console.rule("[bold blue]Model Response[/bold blue]")
        try:
            output_text = response.output_text
            console.print(Panel(output_text, style="bold green", title="💬 Assistant"))
        except AttributeError:
            console.print("[red]No textual output available from model.[/red]")

        if hasattr(response, "tool_calls") and response.tool_calls:
            self._log_tools(response.tool_calls)

    def ask(self, user_input: str, system_prompt: Optional[str] = None):
        """Send a user message to the model with MCP tool access."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_input})

        console.print(f"\n[bold yellow]🧠 User:[/bold yellow] {user_input}")

        try:
            response = self.client.responses.create(
                model=self.model,
                input=messages,
                tools=[
                    {"type": "web_search"},
                    {
                        "type": "mcp",
                        "server_url": server_url,
                        "server_label": "support-assistant-fastapi",
                        "allowed_tools": self.allowed_tools,
                        "require_approval": "never",
                    }
                ]
            )

            self._log_response(response)
            return response
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

# ----------------------------------------
# Interactive session
# ----------------------------------------

if __name__ == "__main__":
    client = MCPClientFastAPI()

    console.rule("[bold blue]MCP Interactive Session (FastAPI MCP)[/bold blue]")
    while True:
        customer_query = Prompt.ask("[bold cyan]Enter your message[/bold cyan]")
        if customer_query.lower() in ["exit", "quit"]:
            console.print("[bold red]Exiting MCP Client...[/bold red]")
            break
        client.ask(customer_query)
