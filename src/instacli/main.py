from __future__ import annotations

import argparse
import asyncio

from instacli.backend.app import build_app
from instacli.cli import InstaApp
from instacli.config import AppConfig


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="InstaCLI - distraction-free Instagram")
    parser.add_argument(
        "--backend",
        action="store_true",
        help="Run the FastAPI backend server",
    )
    return parser


def _run_backend(config: AppConfig) -> None:
    import uvicorn

    app = build_app(config)
    uvicorn.run(app, host=config.api_host, port=config.api_port, log_level="info")


def _run_tui(config: AppConfig) -> None:
    app = InstaApp(config)
    app.run()


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    config = AppConfig.from_env()

    if args.backend:
        _run_backend(config)
        return

    _run_tui(config)


if __name__ == "__main__":
    main()
