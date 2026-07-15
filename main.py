import sys

# Force standard I/O streams to use UTF-8 on Windows environments
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from pathlib import Path
import typer
from rich.console import Console

from config import Config
from assistant import AIAssistant
from cli import DeveloperAssistantCLI

app = typer.Typer(
    name="ai-developer-assistant",
    help="AI Developer Assistant: A modular, professional AI Developer Assistant CLI",
    add_completion=False,
)
console = Console()


def get_project_root() -> Path:
    """Helper to locate the project's base directory."""
    return Path(__file__).resolve().parent


@app.command(name="chat")
def chat(
    model: str = typer.Option(
        None,
        "--model",
        "-m",
        help="Override the LLM model configured in .env",
    ),
    api_base: str = typer.Option(
        None,
        "--api-base",
        "-b",
        help="Override the API base URL configured in .env",
    ),
) -> None:
    """Start an interactive chat session with the AI assistant (Default)."""
    # 1. Load Configurations
    config = Config()
    
    # Apply command line overrides if provided
    if model:
        config.model = model
    if api_base:
        config.api_base = api_base

    # 2. Instantiate core services
    assistant = AIAssistant(config)
    
    # 3. Create and start CLI controller
    project_dir = get_project_root()
    cli = DeveloperAssistantCLI(config, assistant, project_dir)
    cli.run()


@app.command(name="explain", help="[Roadmap] Explain a target source code file.")
def explain(
    file_path: str = typer.Argument(..., help="Path to the file to explain"),
) -> None:
    """Stub command for source code explanation."""
    console.print(
        "[bold yellow]Roadmap Feature:[/bold yellow] Code explanation is scheduled for Day 2.\n"
        f"Target file: [cyan]{file_path}[/cyan]"
    )


@app.command(name="debug", help="[Roadmap] Debug code syntax or traceback logs.")
def debug(
    file_path: str = typer.Argument(..., help="Path to the buggy file"),
    error_log: str = typer.Option(None, "--error", "-e", help="Optional compiler error message or logs"),
) -> None:
    """Stub command for code debugging."""
    console.print(
        "[bold yellow]Roadmap Feature:[/bold yellow] Code debugging is scheduled for Day 2.\n"
        f"Target file: [cyan]{file_path}[/cyan]"
    )


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Callback function when running the base command."""
    # If no subcommand is specified, default to launching the interactive chat
    if ctx.invoked_subcommand is None:
        chat(model=None, api_base=None)


if __name__ == "__main__":
    app()
