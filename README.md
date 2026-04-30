# 📦 Gemini CLI Chatbot with Function Calling

A command-line chatbot powered by Google Gemini (gemini-2.5-flash) that supports function calling to interact with the local file system and execute Python scripts.

## 🚀 Features
- 💬 Chat with Gemini via CLI
- 🧠 Uses system prompts for controlled behavior
- 🛠️ Built-in function calling:
- Read file contents
- List directory files
- Write/update files
- Execute Python scripts
- 🔍 Optional verbose mode (token usage + debug logs)
- 🔁 Multi-step tool interaction loop (up to 10 iterations)

## Installation

### 1. Install UV
- Thorugh Curl
```
curl -Ls https://astral.sh/uv/install.sh | sh
```
- Alternatively use pip
```
pip install uv
```
### 2. Install the Project
```
git clone https://github.com/ShyPenguin/gemini-chat-bot-cru-files.git
cd gemini-chat-bot-cru-files
```
### 3. Create virtual environment + install deps
```
uv sync
```
### 4. Run the app
```
uv run python main.py "Hello"
```
