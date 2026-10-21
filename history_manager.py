"""
Persist chat turns in:
  - Streamlit session_state (in-memory)
  - CSV table under ROOT_PATH/data  (tabular history, no database)
  - JSON file under ROOT_PATH/data  (input/output pairs)
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from config import CHAT_HISTORY_CSV, CHAT_IO_JSON, DATA_DIR


CSV_COLUMNS = ["timestamp", "role", "message"]


def ensure_storage() -> None:
    """Create data directory and empty history files if missing."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not CHAT_HISTORY_CSV.exists():
        pd.DataFrame(columns=CSV_COLUMNS).to_csv(CHAT_HISTORY_CSV, index=False)

    if not CHAT_IO_JSON.exists():
        CHAT_IO_JSON.write_text("[]", encoding="utf-8")


def init_session_history() -> None:
    """Initialize chat messages in Streamlit session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Welcome to **Royals Cricket Chatbot** 👑🏏 "
                    "Ask about cricket, match **predictions**, **weather**, **pitch** reports, "
                    "toss strategy, and more. "
                    "Say **chat history** anytime to see past chats from the project folder."
                ),
            }
        ]


def append_to_session(role: str, content: str) -> None:
    st.session_state.messages.append({"role": role, "content": content})


def append_to_csv(role: str, message: str) -> None:
    """Append one row to the tabular chat history CSV under root_path/data."""
    ensure_storage()
    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "role": role,
        "message": message,
    }
    df = pd.DataFrame([row])
    header = not CHAT_HISTORY_CSV.exists() or CHAT_HISTORY_CSV.stat().st_size == 0
    df.to_csv(CHAT_HISTORY_CSV, mode="a", header=header, index=False)


def append_io_json(user_input: str, bot_output: str) -> None:
    """Append input/output pair to JSON log under root_path/data."""
    ensure_storage()
    try:
        data = json.loads(CHAT_IO_JSON.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            data = []
    except (json.JSONDecodeError, FileNotFoundError):
        data = []

    data.append(
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "input": user_input,
            "output": bot_output,
        }
    )
    CHAT_IO_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def save_turn(user_input: str, bot_output: str) -> None:
    """Save one full turn to session + CSV + JSON."""
    append_to_session("user", user_input)
    append_to_session("assistant", bot_output)
    append_to_csv("user", user_input)
    append_to_csv("assistant", bot_output)
    append_io_json(user_input, bot_output)


def load_history_table(csv_path: Path | None = None) -> pd.DataFrame:
    """
    Load chat history from root_path/data/chat_history.csv as a table.
    Used when the user asks for chat history.
    """
    path = csv_path or CHAT_HISTORY_CSV
    ensure_storage()
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame(columns=CSV_COLUMNS)
    try:
        df = pd.read_csv(path)
        if df.empty:
            return pd.DataFrame(columns=CSV_COLUMNS)
        return df
    except Exception:
        return pd.DataFrame(columns=CSV_COLUMNS)


def history_file_path() -> str:
    """Absolute path string for display (root_path based)."""
    return str(CHAT_HISTORY_CSV.resolve())
