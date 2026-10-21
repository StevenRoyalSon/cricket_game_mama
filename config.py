"""
Separate configuration for model name and API key.
Prefer environment variables / .env over hardcoding secrets.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Project root (folder that contains this file)
ROOT_PATH = Path(__file__).resolve().parent

# Load .env from project root if present
load_dotenv(ROOT_PATH / ".env")

# ---------------------------------------------------------------------------
# MODEL & API KEY  (keep secrets here / in .env — not in other modules)
# ---------------------------------------------------------------------------

# OpenAI chat model (change as needed: gpt-4o-mini, gpt-4o, gpt-3.5-turbo, ...)
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

# API key: set OPENAI_API_KEY in .env  OR  paste below for local testing only
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")

# ---------------------------------------------------------------------------
# PATHS (history & JSON under project root — no database)
# ---------------------------------------------------------------------------

DATA_DIR = ROOT_PATH / "data"
CHAT_HISTORY_CSV = DATA_DIR / "chat_history.csv"
CHAT_IO_JSON = DATA_DIR / "chat_io.json"

# Ensure data folder exists at import time
DATA_DIR.mkdir(parents=True, exist_ok=True)
