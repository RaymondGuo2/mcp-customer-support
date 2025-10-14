from openai import OpenAI
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

# --- Setup ---
load_dotenv()
console = Console()

SERVER_URL = os.getenv("NGROK_URL")
MODEL = "gpt-4o-mini"

TOOLS = [
    {
        "type": "mcp",
        "server_url": SERVER_URL,
        "server_label": "support-assistant",
        "require_approval": "never"
    },
]

# --- Client Class ---
class MCPClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        console.print(Panel.fit(f"[bold green]MCPClient Ready[/bold green]\nModel: {MODEL}", title="✅ Initialized"))

    def _display_response(self, response):
        console.rule("[bold blue]Model Response[/bold blue]")
        text = getattr(response, "output_text", None)
        console.print(Panel(text or "[red]No textual output[/red]", title="💬 Assistant", style="bold green"))
        if getattr(response, "tool_calls", None):
            table = Table(title="🔧 Tool Calls", show_lines=True)
            table.add_column("Tool", style="cyan")
            table.add_column("Arguments", style="magenta")
            for t in response.tool_calls:
                table.add_row(t.get("name", "unknown"), str(t.get("arguments", {})))
            console.print(table)

    def ask(self, user_input, system_prompt=None):
        console.print(f"\n[bold yellow]🧠 User:[/bold yellow] {user_input}")
        messages = [{"role": "system", "content": system_prompt}] if system_prompt else []
        messages.append({"role": "user", "content": user_input})

        try:
            response = self.client.responses.create(model=MODEL, input=messages, tools=TOOLS)
            self._display_response(response)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

# --- Interactive Loop ---
if __name__ == "__main__":
    client = MCPClient()
    console.rule("[bold blue]MCP Interactive Session[/bold blue]")

    while True:
        query = Prompt.ask("[bold cyan]Enter your message[/bold cyan]").strip()
        if query.lower() in ("exit", "quit"):
            console.print("[bold red]Exiting MCP Client...[/bold red]")
            break
        client.ask(query)

