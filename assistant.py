"""AI Assistant module.

Handles API communications, maintains conversation history, and provides
stubs/extension points for advanced developer features.
"""

from typing import Dict, List, Any, Optional
from google import genai
from google.genai import types
from google.genai import errors
from config import Config


class AIAssistant:
    """Manages chat conversations and coordinates assistant actions with Google Gemini API."""

    def __init__(self, config: Config) -> None:
        """Initialize the assistant with configuration and conversation history.

        Args:
            config: A validated Config instance.
        """
        self.config = config
        self.system_prompt = (
            "You are AI Developer Assistant, an expert, professional, and friendly AI Coding Assistant. "
            "You help software engineers design, write, test, optimize, and debug code. "
            "Respond using clean Markdown styling. Keep your code samples correct, modern, and documented."
        )
        self.conversation_history: List[Dict[str, str]] = []
        self.reset_history()

        # Initialize the GenAI Client
        http_options = None
        if self.config.api_base:
            http_options = types.HttpOptions(base_url=self.config.api_base)
        self.client = genai.Client(
            api_key=self.config.api_key,
            http_options=http_options
        )

    def reset_history(self) -> None:
        """Clear the current session conversation history and initialize with system prompt."""
        self.conversation_history = [
            {"role": "system", "content": self.system_prompt}
        ]

    def add_user_message(self, content: str) -> None:
        """Add a user message to the conversation history.

        Args:
            content: The text content from the user.
        """
        self.conversation_history.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str) -> None:
        """Add an assistant message to the conversation history.

        Args:
            content: The response text content from the assistant.
        """
        self.conversation_history.append({"role": "assistant", "content": content})

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Return the current conversation history.

        Returns:
            A list of conversation turn dictionaries.
        """
        return self.conversation_history

    def get_chat_response(self) -> str:
        """Send the current conversation history to the API and get a completion.

        Returns:
            The text response from the assistant.

        Raises:
            google.genai.errors.APIError: For errors from the Gemini API.
            Exception: Other unforeseen issues.
        """
        contents = []
        for msg in self.conversation_history:
            role = msg["role"]
            if role == "system":
                continue
            
            gemini_role = "model" if role == "assistant" else "user"
            contents.append({
                "role": gemini_role,
                "parts": [{"text": msg["content"]}]
            })

        config = types.GenerateContentConfig(
            system_instruction=self.system_prompt,
            temperature=self.config.temperature
        )

        response = self.client.models.generate_content(
            model=self.config.model,
            contents=contents,
            config=config
        )

        content = response.text
        if not content:
            raise Exception("Empty response returned from Gemini API.")

        self.add_assistant_message(content)
        return content

    def get_chat_response_stream(self) -> Any:
        """Send conversation history to the API and yield response stream chunks."""
        contents = []
        for msg in self.conversation_history:
            role = msg["role"]
            if role == "system":
                continue
            
            gemini_role = "model" if role == "assistant" else "user"
            contents.append({
                "role": gemini_role,
                "parts": [{"text": msg["content"]}]
            })

        config = types.GenerateContentConfig(
            system_instruction=self.system_prompt,
            temperature=self.config.temperature
        )

        response = self.client.models.generate_content_stream(
            model=self.config.model,
            contents=contents,
            config=config
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text

    def get_last_code_block(self) -> Optional[str]:
        """Extracts the last generated code block (inside ``` ... ```) from the conversation history."""
        for msg in reversed(self.conversation_history):
            if msg.get("role") == "assistant":
                content = msg.get("content", "")
                import re
                # Find all blocks inside triple backticks
                blocks = re.findall(r"```(?:\w+)?\n(.*?)\n```", content, re.DOTALL)
                if blocks:
                    return blocks[-1]
        return None

    def validate_model(self) -> None:
        """Verify that the configured model is available and retrieve its metadata.

        Raises:
            google.genai.errors.ClientError: if the model is not found.
            Exception: if any other API connection or key issue occurs.
        """
        self.client.models.get(model=self.config.model)

    # =========================================================================
    # Extension Points for Future Developer Tasks (Day 2+ Roadmap)
    # =========================================================================

    def explain_code(self, code: str, language: Optional[str] = None) -> str:
        """Explain the functionality of the provided source code.

        Args:
            code: The source code string.
            language: The programming language (optional).
            
        Returns:
            A markdown explanation of the code.
        """
        # Roadmap implementation stub
        raise NotImplementedError("Code explanation feature is on the roadmap for Day 2+.")

    def debug_code(self, code: str, error_message: Optional[str] = None) -> str:
        """Analyze code and error logs to identify bugs and suggest patches.

        Args:
            code: The code with the bug.
            error_message: Optional stack trace or compiler error text.

        Returns:
            A structured report identifying the bug and giving corrected code.
        """
        # Roadmap implementation stub
        raise NotImplementedError("Code debugging feature is on the roadmap for Day 2+.")

    def optimize_code(self, code: str) -> str:
        """Analyze code for performance bottlenecks and return an optimized version.

        Args:
            code: The code to optimize.

        Returns:
            Optimized code block with explanation of complexity improvements.
        """
        # Roadmap implementation stub
        raise NotImplementedError("Code optimization feature is on the roadmap for Day 2+.")

    def generate_readme(self, project_path: str) -> str:
        """Analyze folder layout and file metadata to generate a professional README.

        Args:
            project_path: Directory path to analyze.

        Returns:
            Generated README.md markdown text.
        """
        # Roadmap implementation stub
        raise NotImplementedError("Automated README generation is on the roadmap for Day 2+.")

    def review_code(self, code: str) -> str:
        """Conduct a static code review identifying code smells, security issues, and style.

        Args:
            code: Code content to review.

        Returns:
            A line-by-line review report.
        """
        # Roadmap implementation stub
        raise NotImplementedError("Code review feedback is on the roadmap for Day 2+.")

    def generate_unit_tests(self, code: str, framework: Optional[str] = None) -> str:
        """Generate ready-to-run unit tests for specified codebase module.

        Args:
            code: Target module code.
            framework: Test framework to target (pytest, unittest, etc.).

        Returns:
            Unit test code.
        """
        # Roadmap implementation stub
        raise NotImplementedError("Unit test generation is on the roadmap for Day 2+.")

    def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """Perform high-level analysis of a directory structure, count files, map imports.

        Args:
            project_path: Path to analyze.

        Returns:
            A metadata dictionary mapping file extensions, sizes, and layout imports.
        """
        # Roadmap implementation stub
        raise NotImplementedError("Full project mapping is on the roadmap for Day 2+.")
