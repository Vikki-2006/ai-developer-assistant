"""Utility functions module.

Provides supporting functions for history logging, message formatting,
and system metric updates.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List
import os
import subprocess
from rich.tree import Tree
from rich.filesize import decimal


def save_chat_history(history: List[Dict[str, str]], base_dir: Path) -> Path:
    """Save the chat history to a formatted Markdown file in the history directory.

    Args:
        history: A list of roles and content message dictionaries.
        base_dir: The project root directory where the 'history' folder resides.

    Returns:
        The Path to the newly written markdown log file.
    """
    history_dir = base_dir / "history"
    history_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = history_dir / f"chat_history_{timestamp}.md"

    # Human readable header
    readable_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# AI Developer Assistant Session Log - {readable_time}",
        "This file records the conversation session history with the CLI Assistant.",
        "---",
        ""
    ]

    for message in history:
        role = message.get("role", "unknown").capitalize()
        content = message.get("content", "").strip()

        # Skip system message in developer log to make it more clean
        if role.lower() == "system":
            continue

        # Format user prompt and assistant response
        lines.append(f"## {role}")
        lines.append("")
        lines.append(content)
        lines.append("")
        lines.append("---")
        lines.append("")

    # Write contents
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    return file_path


def format_elapsed_time(seconds: float) -> str:
    """Format elapsed time in seconds into a friendly human-readable format.

    Args:
        seconds: Time interval in seconds.

    Returns:
        Formatted string (e.g. '12.45s').
    """
    if seconds < 0.01:
        return "< 0.01s"
    return f"{seconds:.2f}s"


def build_directory_tree(path: Path, tree: Tree, ignore_dirs=None) -> None:
    """Recursively builds a Rich Tree representing the project folder directory structure."""
    if ignore_dirs is None:
        ignore_dirs = {".git", "venv", "__pycache__", ".vscode", "history", ".system_generated"}

    try:
        # Sort directories first, then files
        entries = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    except PermissionError:
        return
    except Exception:
        return

    for entry in entries:
        if entry.name in ignore_dirs:
            continue
        if entry.is_dir():
            branch = tree.add(f"[bold blue]📁 {entry.name}[/bold blue]")
            build_directory_tree(entry, branch, ignore_dirs)
        else:
            size = decimal(entry.stat().st_size)
            tree.add(f"[green]📄 {entry.name}[/green] [dim]({size})[/dim]")


def get_codebase_context(project_dir: Path, ignore_dirs=None) -> str:
    """Aggregates all source code files in the codebase to build structural context."""
    if ignore_dirs is None:
        ignore_dirs = {".git", "venv", "__pycache__", ".vscode", "history", ".system_generated"}

    context_parts = []
    valid_extensions = {".py", ".md", ".txt", ".json", ".env", ".env.example", "requirements.txt", "LICENSE"}

    for root, dirs, files in os.walk(project_dir):
        # In-place skip ignored folders
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix in valid_extensions or file in valid_extensions:
                try:
                    rel_path = file_path.relative_to(project_dir)
                    # Limit to files under 50KB to avoid hitting API token limits
                    if file_path.stat().st_size < 50000:
                        content = file_path.read_text(encoding="utf-8", errors="ignore")
                        context_parts.append(f"--- File: {rel_path} ---\n{content}\n")
                except Exception:
                    pass

    return "\n".join(context_parts)


def load_chat_history(file_path: Path) -> List[Dict[str, str]]:
    """Parse a saved markdown log session file back into structural conversation history."""
    content = file_path.read_text(encoding="utf-8", errors="ignore")
    sections = content.split("---")
    history = []

    for section in sections:
        section = section.strip()
        if not section:
            continue
        if section.startswith("## User"):
            lines = section.splitlines()
            user_content = "\n".join(lines[1:]).strip()
            history.append({"role": "user", "content": user_content})
        elif section.startswith("## Assistant"):
            lines = section.splitlines()
            assistant_content = "\n".join(lines[1:]).strip()
            history.append({"role": "assistant", "content": assistant_content})

    return history


def copy_to_clipboard(text: str) -> bool:
    """Copies text directly to the Windows system clipboard using clip.exe."""
    try:
        subprocess.run(["clip"], input=text, text=True, check=True)
        return True
    except Exception:
        return False

