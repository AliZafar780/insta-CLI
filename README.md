# 📸 InstaCLI - Terminal-Based Instagram Client

> A distraction-free, terminal-based Instagram client with AI-assisted workflow

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python" alt="Python" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat" alt="License" />
  <img src="https://img.shields.io/badge/FastAPI-Ready-009688?style=flat" alt="FastAPI" />
</p>

---

## ✨ Highlights

- 🎨 **Textual TUI** — Beautiful terminal interface with smooth navigation
- ⚡ **FastAPI Backend** — REST + WebSocket support
- 🤖 **AI Providers** — OpenAI, Anthropic, Ollama support
- 🗄️ **SQLite/PostgreSQL** — Flexible data storage
- 📱 **Instagram Graph API** — Real Instagram integration
- 🔕 **Distraction-Free** — Content filtering, AI summaries

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/AliZafar780/insta-CLI.git
cd insta-CLI

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -e .

# Run the CLI
instacli

# Or run API server
instacli --backend
```

## 🛠️ Tech Stack

| Component | Technology |
|:----------|:-----------|
| TUI | Textual |
| Backend | FastAPI |
| Database | SQLite / PostgreSQL |
| AI | OpenAI, Anthropic, Ollama |
| API | Instagram Graph API |

## 📁 Project Structure

```
insta-CLI/
├── instacli/         # Main package
├── backend/         # FastAPI server
├── ai/             # AI integrations
└── requirements.txt # Dependencies
```

## ⚙️ Configuration

Create a `.env` file:

```bash
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
AI_PROVIDER=ollama  # or openai, anthropic
AI_API_KEY=your_api_key
```

## 📜 License

MIT License

---

*Instagram in your terminal 📸*
