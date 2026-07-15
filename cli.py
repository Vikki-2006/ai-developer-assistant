"""CLI presentation module.

Handles terminal formatting, panels, banners, status loops, and user interaction
using Rich.
"""

import sys
import time
from pathlib import Path
from typing import Dict, List

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.markdown import Markdown
from rich.theme import Theme
from rich.live import Live
from rich import box
from rich.syntax import Syntax
from rich.tree import Tree

from google.genai import errors
from assistant import AIAssistant
from config import Config
import utils

# Custom theme for professional developer colors
CLI_THEME = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "error": "bold red",
    "success": "bold green",
    "accent": "bold blue",
    "user_prompt": "bold chartreuse3",
    "system_name": "bold deep_sky_blue1",
})

console = Console(theme=CLI_THEME)


class DeveloperAssistantCLI:
    """Class that drives the interactive CLI user interface."""

    def __init__(self, config: Config, assistant: AIAssistant, project_dir: Path) -> None:
        """Initialize the CLI controller.

        Args:
            config: The loaded Config object.
            assistant: The AIAssistant service logic handler.
            project_dir: The project root directory.
        """
        self.config = config
        self.assistant = assistant
        self.project_dir = project_dir

    def display_banner(self) -> None:
        """Renders the startup banner and prints configurations."""
        banner_text = Text()
        banner_text.append(" ──▄▀▀▀▄▄▄▄▄▄▄▀▀▀▄──\n", style="system_name")
        banner_text.append(" ──█▒▒░░░░░░░░░▒▒█──\n", style="system_name")
        banner_text.append(" ───█░░▄▀░░░▀▄░░█───\n", style="system_name")
        banner_text.append(" ───█░░░░░░░░░░░█───     ", style="system_name")
        banner_text.append("AI DEVELOPER ASSISTANT\n", style="bold white")
        banner_text.append(" ───█░░░░░░░░░░░█───     ", style="system_name")
        banner_text.append("Your Personal Coding Companion\n", style="italic gray")
        banner_text.append(" ────█░░░░░░░░░█────     ", style="system_name")
        banner_text.append("Powered by Gemini\n", style="info")
        banner_text.append(" ─────▀▄▄▄▄▄▄▄▀─────\n", style="system_name")

        sdk_version = "2.11.0"
        try:
            import google.genai
            sdk_version = google.genai.__version__
        except Exception:
            pass

        endpoint_display = self.config.api_base if self.config.api_base else "Default Gemini API"
        
        config_info = (
            f"[bold green]✓[/bold green] [white]Model:[/white]    [cyan]{self.config.model}[/cyan]\n"
            f"[bold green]✓[/bold green] [white]Endpoint:[/white] [cyan]{endpoint_display}[/cyan]\n"
            f"[bold green]✓[/bold green] [white]API Status:[/white] [green]Online[/green]\n"
            f"[bold green]✓[/bold green] [white]SDK Version:[/white] [cyan]{sdk_version}[/cyan]"
        )

        config_panel = Panel(
            config_info,
            title="[bold cyan]System Settings[/bold cyan]",
            border_style="bright_blue",
            box=box.ROUNDED,
            expand=False
        )

        console.print(banner_text)
        console.print(config_panel)

    def display_help(self) -> None:
        """Renders a beautiful list of available commands in a table."""
        table = Table(
            title="Interactive Slash Commands",
            title_style="bold cyan",
            border_style="bright_blue",
            show_header=True,
            header_style="bold magenta",
            box=box.ROUNDED
        )
        table.add_column("Command / Area", style="bold green", width=25)
        table.add_column("Description", style="white")

        # Basic Commands
        table.add_row("[bold cyan]Core CLI[/bold cyan]", "")
        table.add_row("  /help", "Show this interactive commands directory.")
        table.add_row("  /clear", "Reset current session conversation memory.")
        table.add_row("  /exit", "Save session logs and close the interactive terminal.")
        table.add_row("  /history", "Display current session conversation history.")
        table.add_row("  /save <filename>", "Save conversation history to a custom markdown file.")
        table.add_row("  /load <filepath>", "Load conversation history from a markdown file.")
        table.add_row("  /export <filepath>", "Export session chat history to a markdown file.")
        table.add_row("  /model [model_name]", "Change active model or list all available models.")
        
        # File Commands
        table.add_row("[bold cyan]File Operations[/bold cyan]", "")
        table.add_row("  /read <file>", "Load file content directly into conversation context.")
        table.add_row("  /explain <file>", "Explain the functionality of a code file.")
        table.add_row("  /review <file>", "Conduct a senior static code review of a file.")
        table.add_row("  /fix <file>", "Find and diagnose bugs or syntax errors in a file.")
        table.add_row("  /optimize <file>", "Analyze complexity and optimize code performance.")
        table.add_row("  /tests <file>", "Generate pytest or unittest suites for a file.")
        table.add_row("  /doc <file>", "Generate detailed docstrings and comments for a file.")
        
        # Project Commands
        table.add_row("[bold cyan]Project Context[/bold cyan]", "")
        table.add_row("  /project", "Scan and summarize the entire project directory context.")
        table.add_row("  /review-project", "Conduct a static code review of the entire project.")
        table.add_row("  /readme", "Generate a professional README.md for the codebase.")
        table.add_row("  /tree", "Render a styled directory tree diagram of the project.")
        table.add_row("  /dependencies", "Scan and analyze project imports and dependencies.")
        table.add_row("  /architecture", "Map out the architectural layout of the project.")

        # Utilities
        table.add_row("[bold cyan]Utilities[/bold cyan]", "")
        table.add_row("  /copy last", "Copy the last generated code block to the system clipboard.")
        table.add_row("  /save <filename.ext>", "Save the last generated code block to a file.")
        table.add_row("  /error [file/trace]", "Analyze a traceback/stack trace error.")
        table.add_row("  /leetcode <problem>", "Answer in LeetCode/DSA mode (Approach, Complexity, Dry Run).")

        console.print(table)
        console.print()

    def display_error_panel(self, title: str, message: str, solution: str) -> None:
        """Renders a structured, beautiful Rich error panel with suggested solution."""
        error_content = f"[bold red]❌ {message}[/bold red]\n\n[bold green]Suggestion:[/bold green]\n{solution}"
        console.print(
            Panel(
                error_content,
                title=f"[bold red]{title}[/bold red]",
                border_style="red",
                box=box.ROUNDED,
                expand=False
            )
        )

    def handle_command(self, user_input: str) -> bool:
        """Process special CLI slash commands.

        Args:
            user_input: Cleaned command string starting with '/'.

        Returns:
            True if the application loop should continue, False to exit.
        """
        parts = user_input.split(maxsplit=1)
        cmd = parts[0].lower().strip()

        if cmd == "/exit":
            self.shutdown_and_save()
            return False
        elif cmd == "/clear":
            self.assistant.reset_history()
            console.print(
                Panel(
                    "Conversation memory has been cleared successfully.",
                    title="Memory Reset",
                    border_style="success",
                    box=box.ROUNDED
                )
            )
            return True
        elif cmd == "/help":
            self.display_help()
            return True
        elif cmd == "/history":
            table = Table(title="Session History Memory", box=box.ROUNDED, border_style="bright_blue")
            table.add_column("Role", style="bold cyan")
            table.add_column("Preview", style="white")
            for msg in self.assistant.conversation_history:
                if msg["role"] == "system":
                    continue
                role = "You ❯" if msg["role"] == "user" else "Assistant ❯"
                content_preview = msg["content"].replace("\n", " ")[:80] + "..." if len(msg["content"]) > 80 else msg["content"]
                table.add_row(role, content_preview)
            console.print(table)
            console.print()
            return True
        elif cmd == "/save" or cmd == "/export":
            if len(parts) < 2:
                self.shutdown_and_save()
                return True
            filename = parts[1].strip()
            is_code = any(filename.endswith(ext) for ext in [".py", ".js", ".ts", ".go", ".cpp", ".c", ".h", ".rs", ".java", ".html", ".css", ".sh", ".bat", ".sql", ".txt"])
            if is_code:
                code = self.assistant.get_last_code_block()
                if code:
                    filepath = Path(filename)
                    if not filepath.is_absolute():
                        filepath = Path.cwd() / filepath
                    try:
                        filepath.parent.mkdir(parents=True, exist_ok=True)
                        filepath.write_text(code, encoding="utf-8")
                        console.print(f"[success]✔ Last code block successfully saved to file: [info]{filepath}[/info][/success]\n")
                    except Exception as e:
                        console.print(f"[error]Failed to save code to file: {e}[/error]\n")
                else:
                    console.print("[error]No code block found in the last assistant response.[/error]\n")
            else:
                filepath = Path(filename)
                if not filepath.is_absolute():
                    filepath = Path.cwd() / filepath
                try:
                    filepath.parent.mkdir(parents=True, exist_ok=True)
                    lines = [f"# AI Developer Assistant Session Log - {time.strftime('%Y-%m-%d %H:%M:%S')}", "---", ""]
                    for msg in self.assistant.conversation_history:
                        if msg["role"] == "system":
                            continue
                        role = msg["role"].capitalize()
                        lines.append(f"## {role}\n\n{msg['content']}\n\n---")
                    filepath.write_text("\n".join(lines), encoding="utf-8")
                    console.print(f"[success]✔ Conversation saved to [info]{filepath}[/info]\n")
                except Exception as e:
                    console.print(f"[error]Failed to save session history: {e}[/error]\n")
            return True
        elif cmd == "/load":
            if len(parts) < 2:
                console.print("[error]Missing filepath. Usage: /load <filepath>[/error]\n")
                return True
            filepath = Path(parts[1].strip())
            if not filepath.is_absolute():
                filepath = Path.cwd() / filepath
            if not filepath.exists():
                console.print(f"[error]File not found: {filepath}[/error]\n")
                return True
            try:
                loaded_history = utils.load_chat_history(filepath)
                self.assistant.conversation_history = [{"role": "system", "content": self.assistant.system_prompt}] + loaded_history
                console.print(f"[success]✔ Loaded {len(loaded_history)} conversation turns from [info]{filepath.name}[/info]\n")
            except Exception as e:
                console.print(f"[error]Failed to load session history: {e}[/error]\n")
            return True
        elif cmd == "/model":
            if len(parts) < 2:
                console.print("[info]Retrieving available models supporting generateContent...[/info]")
                try:
                    models = self.assistant.client.models.list()
                    table = Table(title="Available Gemini Models", box=box.ROUNDED, border_style="bright_blue")
                    table.add_column("Model ID", style="bold cyan")
                    table.add_column("Display Name", style="white")
                    for m in models:
                        actions = getattr(m, 'supported_actions', [])
                        if "generateContent" in actions:
                            model_id = m.name.replace("models/", "")
                            active_indicator = "[bold green](active)[/bold green]" if model_id == self.config.model else ""
                            table.add_row(model_id, f"{m.display_name} {active_indicator}")
                    console.print(table)
                    console.print()
                except Exception as e:
                    console.print(f"[error]Failed to retrieve model list: {e}[/error]\n")
            else:
                model_name = parts[1].strip()
                self.config.model = model_name
                console.print(f"[success]✔[/success] Active model set to: [info]{model_name}[/info]\n")
            return True
        elif cmd == "/copy":
            if len(parts) > 1 and parts[1].strip().lower() == "last":
                code = self.assistant.get_last_code_block()
                if code:
                    success = utils.copy_to_clipboard(code)
                    if success:
                        console.print("[success]✔ Last generated code block successfully copied to system clipboard![/success]\n")
                    else:
                        console.print("[error]Failed to copy to clipboard.[/error]\n")
                else:
                    console.print("[error]No code block found in the last assistant response.[/error]\n")
            else:
                console.print("[error]Usage: /copy last[/error]\n")
            return True
        elif cmd == "/read":
            if len(parts) < 2:
                console.print("[error]Missing filename. Usage: /read <filename>[/error]\n")
                return True
            filename = parts[1].strip()
            filepath = Path(filename)
            if not filepath.is_absolute():
                filepath = Path.cwd() / filepath
            if not filepath.exists():
                console.print(f"[error]File not found: {filename}[/error]\n")
                return True
            try:
                content = filepath.read_text(encoding="utf-8", errors="ignore")
                syntax = Syntax(content, filepath.suffix.replace(".", "") or "txt", theme="monokai", line_numbers=True)
                console.print(Panel(syntax, title=f"📄 {filename}", box=box.ROUNDED, border_style="bright_blue"))
                acknowledgement_prompt = f"I have read and loaded the contents of the file '{filename}' into context:\n\n```\n{content}\n```"
                self.stream_response(acknowledgement_prompt)
            except Exception as e:
                console.print(f"[error]Failed to read file: {e}[/error]\n")
            return True
        elif cmd in {"/explain", "/review", "/fix", "/optimize", "/tests", "/doc"}:
            cmd_name = cmd.replace("/", "")
            if len(parts) < 2:
                console.print(f"[error]Missing filename. Usage: /{cmd_name} <filename>[/error]\n")
                return True
            filename = parts[1].strip()
            filepath = Path(filename)
            if not filepath.is_absolute():
                filepath = Path.cwd() / filepath
            if not filepath.exists():
                console.print(f"[error]File not found: {filename}[/error]\n")
                return True
            try:
                content = filepath.read_text(encoding="utf-8", errors="ignore")
                prompt_map = {
                    "explain": f"Please explain the functionality and details of the following source code file '{filename}':\n\n```\n{content}\n```",
                    "review": f"Please conduct a senior static code review of the following file '{filename}' for bugs, styles, design patterns, and improvements:\n\n```\n{content}\n```",
                    "fix": f"Please diagnose and fix any bugs, tracebacks, syntax issues, or errors in the following source code file '{filename}':\n\n```\n{content}\n```",
                    "optimize": f"Please analyze time/space complexity and optimize the performance of the following code file '{filename}':\n\n```\n{content}\n```",
                    "tests": f"Please generate comprehensive unit tests (using pytest or unittest as appropriate) for the following code file '{filename}':\n\n```\n{content}\n```",
                    "doc": f"Please generate clean docstrings, comments, and structured documentation for the following code file '{filename}':\n\n```\n{content}\n```",
                }
                self.stream_response(prompt_map[cmd_name])
            except Exception as e:
                console.print(f"[error]Failed to process file operation: {e}[/error]\n")
            return True
        elif cmd in {"/project", "/review-project", "/readme", "/dependencies", "/architecture"}:
            cmd_name = cmd.replace("/", "")
            console.print("[info]Scanning project codebase to build context...[/info]")
            try:
                context = utils.get_codebase_context(self.project_dir)
                prompt_map = {
                    "project": f"Analyze and explain this project codebase, layout, and core modules:\n\n{context}",
                    "review-project": f"Conduct a static code review of the entire project codebase. Identify code quality issues, bugs, architecture improvements, and code smells:\n\n{context}",
                    "readme": f"Generate a professional README.md for this codebase. Include installation, usage, features, tech stack, folder structure, license, and badges:\n\n{context}",
                    "dependencies": f"Scan all files and imports in this project context and summarize all dependencies, libraries used, and their versions if specified:\n\n{context}",
                    "architecture": f"Analyze this project context and explain the system architecture, design patterns, file relationships, and data flow:\n\n{context}",
                }
                self.stream_response(prompt_map[cmd_name])
            except Exception as e:
                console.print(f"[error]Failed to scan project codebase: {e}[/error]\n")
            return True
        elif cmd == "/tree":
            tree = Tree(f"[bold blue]📁 {self.project_dir.name}[/bold blue]")
            utils.build_directory_tree(self.project_dir, tree)
            console.print(tree)
            console.print()
            return True
        elif cmd == "/error":
            if len(parts) < 2:
                console.print("[error]Missing error trace or traceback file path. Usage: /error <traceback file or raw trace>[/error]\n")
                return True
            target = parts[1].strip()
            filepath = Path(target)
            if not filepath.is_absolute():
                filepath = Path.cwd() / filepath
            if filepath.exists():
                try:
                    traceback_text = filepath.read_text(encoding="utf-8", errors="ignore")
                except Exception as e:
                    console.print(f"[error]Failed to read traceback file: {e}[/error]\n")
                    return True
            else:
                traceback_text = target
            prompt = f"Please explain the following Python stack trace traceback error, identify the root cause, and suggest a resolution:\n\n```\n{traceback_text}\n```"
            self.stream_response(prompt)
            return True
        elif cmd == "/leetcode":
            if len(parts) < 2:
                console.print("[error]Missing problem description. Usage: /leetcode <problem description>[/error]\n")
                return True
            problem = parts[1].strip()
            prompt = (
                f"Solve the following LeetCode/DSA problem. Respond using LeetCode/DSA mode guidelines. "
                "Format your response exactly with sections: Approach, Complexity (Time & Space), Python Solution, and Dry Run:\n\n"
                f"{problem}"
            )
            self.stream_response(prompt)
            return True
        else:
            console.print(f"[error]Unknown command: '{user_input}'[/error]. Type [bold green]/help[/bold green] for info.\n")
            return True

    def shutdown_and_save(self) -> None:
        """Save the session history to markdown and exit."""
        history = self.assistant.get_conversation_history()
        
        # Only save if there are messages besides the system prompt
        if len(history) > 1:
            try:
                log_path = utils.save_chat_history(history, self.project_dir)
                console.print(
                    f"\n[success]✔[/success] Session saved to [info]{log_path.name}[/info]"
                )
            except Exception as err:
                console.print(f"\n[warning]⚠ Failed to save session history: {err}[/warning]")
        
        console.print("\n[bold deep_sky_blue1]Goodbye! Keep building great things! 🚀[/bold deep_sky_blue1]\n")

    def stream_response(self, prompt: str) -> None:
        """Add user prompt, send to API, and stream the response to the terminal live."""
        self.assistant.add_user_message(prompt)

        start_time = time.time()
        # 1. Show the thinking spinner
        with console.status("[bold deep_sky_blue1]🤖 Thinking...[/bold deep_sky_blue1]", spinner="dots"):
            try:
                response_stream = self.assistant.get_chat_response_stream()
                # Fetch first token to clear spinner
                try:
                    first_chunk = next(response_stream)
                except StopIteration:
                    first_chunk = ""
            except errors.APIError as api_err:
                self.assistant.conversation_history.pop() # pop last user query
                if api_err.code == 429 or "quota" in api_err.message.lower():
                    self.display_error_panel(
                        "Rate Limit Exceeded",
                        f"Gemini API Error ({api_err.code}): {api_err.message}",
                        "Please check your API quota or wait a few minutes before retrying."
                    )
                elif api_err.code == 403 or "key" in api_err.message.lower():
                    self.display_error_panel(
                        "Invalid API Key",
                        f"Gemini API Error ({api_err.code}): {api_err.message}",
                        "Please update the GEMINI_API_KEY in your .env file."
                    )
                else:
                    self.display_error_panel(
                        "API Error",
                        f"Gemini API Error ({api_err.code}): {api_err.message}",
                        "Please check the Gemini API service status or try again."
                    )
                return
            except Exception as e:
                self.assistant.conversation_history.pop()
                self.display_error_panel(
                    "Connection Failure",
                    f"An error occurred: {e}",
                    "Please check your internet connection or the configured model name."
                )
                return

        # 2. Stream the response live
        full_response = first_chunk
        md = Markdown(full_response)
        panel = Panel(
            md,
            title="[system_name]AI Developer Assistant[/system_name]",
            subtitle="[info]Streaming...[/info]",
            subtitle_align="right",
            border_style="bright_blue",
            box=box.ROUNDED
        )

        with Live(panel, console=console, refresh_per_second=10) as live:
            for chunk in response_stream:
                full_response += chunk
                md = Markdown(full_response)
                panel = Panel(
                    md,
                    title="[system_name]AI Developer Assistant[/system_name]",
                    subtitle="[info]Streaming...[/info]",
                    subtitle_align="right",
                    border_style="bright_blue",
                    box=box.ROUNDED
                )
                live.update(panel)

        # 3. Add to assistant memory history
        self.assistant.add_assistant_message(full_response)

        # 4. Final display with elapsed time
        elapsed = time.time() - start_time
        time_str = utils.format_elapsed_time(elapsed)
        panel = Panel(
            Markdown(full_response),
            title="[system_name]AI Developer Assistant[/system_name]",
            subtitle=f"[info]Completed in {time_str}[/info]",
            subtitle_align="right",
            border_style="bright_blue",
            box=box.ROUNDED
        )
        console.print(panel)
        console.print()

    def run(self) -> None:
        """Runs the main interactive loop for the CLI."""
        # 1. Test basic config validation
        try:
            self.config.validate()
        except Exception as err:
            console.print(Panel(str(err), title="[bold red]Configuration Error[/bold red]", border_style="error"))
            sys.exit(1)

        # 2. Print the model being used
        console.print(f"[info]Configured model: [bold]{self.config.model}[/bold][/info]")

        # 3. Verify model availability before starting chat
        with console.status("[bold deep_sky_blue1]Verifying model availability...[/bold deep_sky_blue1]", spinner="dots"):
            try:
                self.assistant.validate_model()
            except errors.ClientError as err:
                error_msg = (
                    f"The configured model '{self.config.model}' is invalid or not available.\n\n"
                    "Please check the spelling in your .env file or call 'test.py' to list the models "
                    "available for your API key."
                )
                console.print(Panel(error_msg, title="[bold red]Model Unavailable[/bold red]", border_style="error"))
                sys.exit(1)
            except errors.APIError as api_err:
                error_msg = f"Gemini API Error ({api_err.code}): {api_err.message}"
                console.print(Panel(error_msg, title="[bold red]API Error[/bold red]", border_style="error"))
                sys.exit(1)
            except Exception as gen_err:
                error_msg = f"Failed to connect to API or verify model: {gen_err}"
                console.print(Panel(error_msg, title="[bold red]Verification Failed[/bold red]", border_style="error"))
                sys.exit(1)

        # 4. Display startup banner
        self.display_banner()

        # 5. Display professional greeting
        greeting_text = (
            "👋 [bold deep_sky_blue1]Welcome back![/bold deep_sky_blue1]\n\n"
            "I'm [bold white]AI Developer Assistant[/bold white] — your personal coding companion.\n\n"
            "I can help you:\n"
            "  • [cyan]Debug code[/cyan]            • [cyan]Explain code[/cyan]\n"
            "  • [cyan]Generate projects[/cyan]     • [cyan]Review pull requests[/cyan]\n"
            "  • [cyan]Build APIs[/cyan]            • [cyan]Create README files[/cyan]\n"
            "  • [cyan]Generate tests[/cyan]        • [cyan]Optimize performance[/cyan]\n"
            "  • [cyan]Design architecture[/cyan]   • [cyan]Solve DSA problems[/cyan]\n\n"
            "[italic dim white]Ask me anything.[/italic dim white]"
        )
        console.print(Panel(greeting_text, border_style="bright_blue", box=box.ROUNDED, expand=False))
        console.print("\nType [bold green]/help[/bold green] to see available commands or [bold red]/exit[/bold red] to quit.\n")

        while True:
            try:
                # Capture clean input
                user_prompt = console.input("[user_prompt]You[/user_prompt] [bold cyan]❯[/bold cyan] ")
                
                # Check for empty spaces
                if not user_prompt.strip():
                    continue

                # Check if it is a command
                if user_prompt.startswith("/"):
                    should_continue = self.handle_command(user_prompt)
                    if not should_continue:
                        break
                    continue

                user_prompt_lower = user_prompt.lower().strip()
                # Check for project context triggers
                if "explain this project" in user_prompt_lower or "explain the project" in user_prompt_lower:
                    console.print("[info]Scanning project codebase to build context...[/info]")
                    context = utils.get_codebase_context(self.project_dir)
                    user_prompt = f"Analyze and explain this codebase, its layout, and its core modules:\n\n{context}"
                elif "review my codebase" in user_prompt_lower or "review this codebase" in user_prompt_lower or "review the codebase" in user_prompt_lower:
                    console.print("[info]Scanning project codebase to build context...[/info]")
                    context = utils.get_codebase_context(self.project_dir)
                    user_prompt = f"Perform a senior static code review of the entire project context. Identify code quality issues, bugs, architecture improvements, and code smells:\n\n{context}"
                elif "generate readme" in user_prompt_lower or "create readme" in user_prompt_lower:
                    console.print("[info]Scanning project codebase to build context...[/info]")
                    context = utils.get_codebase_context(self.project_dir)
                    user_prompt = f"Generate a professional and modern README.md for this codebase. Include sections for Installation, Usage, Features, Tech Stack, Folder Structure, License, Badges:\n\n{context}"

                # Normal streaming interaction
                self.stream_response(user_prompt)

            except KeyboardInterrupt:
                # Clean exit on Ctrl+C
                console.print("\n[warning]KeyboardInterrupt received.[/warning]")
                self.shutdown_and_save()
                break
            except Exception as e:
                console.print(f"\n[error]An unexpected crash occurred: {e}[/error]")
                break
