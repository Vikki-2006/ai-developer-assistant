












# AI Developer Assistant CLI

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A clean, modular, and professional Python command-line interface (CLI) assistant designed for software engineers. This tool runs directly in your terminal, providing rich Markdown formatting, local session logging, and flexible Google Gemini API integration using the official Google GenAI SDK.

Built as **Day 1** of a **"1 Project Per Day"** challenge, the architecture is designed from the ground up to support future developer productivity tools (explaining, debugging, and testing code).

___

## 🚀 Features (Day 1)

*   **Interactive Terminal Chat**: Converse with the AI assistant inside a beautiful, styled terminal layout.
*   **Rich UI Layout**: Employs **Rich** for styled markdown code rendering, custom banners, tables, loading spinners, and color-coded status messages.
*   **Google Gemini Integration**: Connects to Google Gemini API using the official `google-genai` library.
*   **Session History Auto-Saving**: Automatically saves full chat logs in human-readable Markdown inside the `history/` directory upon exit.
*   **Interactive Commands**:
    *   `/help` - Opens the interactive command guide.
    *   `/clear` - Resets current session conversation history.
    *   `/exit` - Gracefully exits the application and logs the history.
*   **Robust Exception Handling**: Captures and formats network timeouts, invalid API keys, and connection failures gracefully without ugly traceback output.

---

## 📁 Project Structure

```text
ai-developer-assistant/
│
├── main.py          # Entry point containing Typer CLI setup and subcommands
├── assistant.py     # AI service agent managing LLM requests and history
├── config.py        # Settings manager parsing .env configuration variables
├── cli.py           # Presentation layer controlling Rich styling and chat loops
├── utils.py         # Helper utilities for formatting and markdown file logging
├── requirements.txt # Project package dependencies
├── README.md        # Documentation and walkthrough guide
├── .env.example     # Environment configuration template
├── .gitignore       # Source control exclusions
├── LICENSE          # MIT Open Source License
├── screenshots/     # Showcase assets folder
└── history/         # Generated local conversation history markdown files
```

---

## 🛠️ Installation & Setup

### 1. Clone the Project
```bash
git clone https://github.com/your-username/ai-developer-assistant.git
cd ai-developer-assistant
```

### 2. Create and Activate a Virtual Environment
**On Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Open `.env` and fill in your settings:
```env
# Gemini API setup
GEMINI_API_KEY=your_real_api_key_here
GEMINI_MODEL=gemini-3.1-flash-lite
```

---

## 💻 Usage

Launch the assistant by executing the main file:

```bash
python main.py
```

### Optional Command Line Overrides
You can override your `.env` configuration directly using CLI options:
```bash
# Override the model
python main.py chat --model gemini-2.5-pro

# Override the model and API base URL (e.g. pointing to a custom proxy or gateway)
python main.py chat -m "gemini-2.5-pro" -b "https://custom-gateway.com"
```

### Interactive Subcommands
Once inside the chat, use standard slash commands:
*   `You ❯ /help` - Show instructions table
*   `You ❯ /clear` - Clear session chat memory
*   `You ❯ /exit` - Save conversation markdown logs and quit

---

## 🖼️ Screenshots

*Interactive screenshot showcase placeholder:*

![Interactive Chat Startup](screenshots/chat_startup.png)

---

## 🗺️ Roadmap & Extension Points

This project is built to expand. The code structure contains clear stubs in `assistant.py` and `main.py` for immediate day-to-day progression:

*   **Day 2: Code Explainer (`python main.py explain <file>`)** - Analyze source code structure and write markdown descriptions of its flow.
*   **Day 3: Bug Debugger (`python main.py debug <file> --error "<log>"`)** - Feed code and tracebacks to get recommended patches.
*   **Day 4: Performance Optimizer** - Evaluate algorithmic complexity and optimize CPU/memory usage.
*   **Day 5: Static Code Reviewer** - Check for style issues, formatting, security flaws, and compliance with PEP 8.
*   **Day 6: Automated Test Suite Generator** - Generate clean unit tests using pytest or unittest frameworks.

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
