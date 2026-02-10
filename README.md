# InstaCLI

InstaCLI is a distraction-free, terminal-based Instagram client with an AI-assisted workflow. It pairs a beautiful Textual TUI with a FastAPI backend, a modular AI layer, and a data layer powered by SQLAlchemy.

## Highlights

- **Textual TUI** with smooth navigation, themes, and keyboard shortcuts.
- **FastAPI backend** with REST + WebSocket support.
- **AI providers** (OpenAI, Anthropic, Ollama, or no-AI mode) with fallback logic.
- **SQLite by default**, optional PostgreSQL support.
- **Instagram Graph API integration** with a mock-data fallback.
- **Distraction-free features**: content filtering, AI summaries, and smart notifications.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
instacli
```

Run the API server:

```bash
instacli --backend
```

## Configuration

Configuration is driven by environment variables (optionally via `.env`).

| Variable | Purpose | Default |
| --- | --- | --- |
| `INSTACLI_DATABASE_URL` | SQLAlchemy database URL | `sqlite+aiosqlite:///./instacli.db` |
| `INSTACLI_AI_PROVIDER` | `openai`, `anthropic`, `ollama`, or `none` | `none` |
| `INSTACLI_INSTAGRAM_MODE` | `live` or `mock` | `mock` |
| `INSTACLI_THEME` | `dark` or `light` | `dark` |
| `INSTACLI_API_HOST` | FastAPI host | `127.0.0.1` |
| `INSTACLI_API_PORT` | FastAPI port | `8000` |
| `INSTACLI_API_KEY` | Optional API key for REST/WebSocket | unset |

## Architecture

```
CLI (Textual)  <->  FastAPI  <->  Services  <->  SQLAlchemy
                        |            |
                        |            +--> AI Providers
                        |
                        +--> Instagram Graph API / Mock
```

## Feature Tour

- **Feed**: infinite scroll with AI-filtered highlights.
- **Post viewer**: media preview, summaries, and smart actions.
- **Profile**: stats, follower insights, and timeline summary.
- **Compose**: AI caption assistance with tone control.
- **Notifications**: intelligent digest summaries.
- **Settings**: theme, moderation rules, and provider toggles.

## Development Notes

- The project uses async/await throughout the backend, AI, and data layers.
- AI integrations are optional; install extras for provider SDKs.
- Instagram Graph API calls are encapsulated in the `instagram` module.

## Roadmap

- Real Graph API OAuth flow and media upload.
- Richer media rendering in the TUI.
- Advanced filtering with customizable policies.

