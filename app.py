"""
Royals Cricket Chatbot — main Streamlit UI.
"""

from __future__ import annotations

import streamlit as st

from animations import render_animation
from chatbot import OUT_OF_CONTEXT_REPLY, get_cricket_response
from config import MODEL_NAME, ROOT_PATH
from cricket_filter import detect_animation_topic, is_cricket_related, is_history_request
from history_manager import (
    history_file_path,
    init_session_history,
    load_history_table,
    save_turn,
)

# ---------------------------------------------------------------------------
# Page config — brand title
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Royals Cricket Chatbot",
    page_icon="👑",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Royals theme: royal navy + gold + pitch green, stadium atmosphere
# ---------------------------------------------------------------------------
ROYALS_BG_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Source+Sans+3:wght@400;600;700&display=swap');

  .stApp {
    background-color: #0a1628;
    background-image:
      radial-gradient(ellipse 90% 55% at 50% -10%, rgba(212, 175, 55, 0.22), transparent 55%),
      radial-gradient(ellipse 70% 50% at 15% 90%, rgba(20, 90, 50, 0.45), transparent 50%),
      radial-gradient(ellipse 60% 40% at 90% 70%, rgba(30, 60, 120, 0.35), transparent 45%),
      linear-gradient(165deg, #071018 0%, #0d2137 35%, #123524 70%, #0a1a12 100%);
    background-attachment: fixed;
    font-family: 'Source Sans 3', sans-serif;
  }

  /* Soft cricket watermark layer */
  .stApp::before {
    content: "👑  🏏  🏆  🏏  👑  🏟️  🏏  ⚡  👑  🏏  🎯  🏏";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    font-size: 2.6rem;
    line-height: 4.5rem;
    letter-spacing: 2rem;
    opacity: 0.055;
    white-space: pre-wrap;
    word-break: break-all;
    overflow: hidden;
    padding: 1.2rem;
  }

  .stApp > header, .stApp > div {
    position: relative;
    z-index: 1;
  }

  /* Hide default Streamlit chrome clutter a bit */
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }

  [data-testid="stChatMessage"] {
    background: rgba(12, 28, 48, 0.72) !important;
    border: 1px solid rgba(212, 175, 55, 0.28);
    border-radius: 16px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
  }

  h1, h2, h3, p, label, .stMarkdown, span {
    color: #f3f0e6 !important;
  }

  section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1528 0%, #122a1a 55%, #0d1f14 100%);
    border-right: 1px solid rgba(212, 175, 55, 0.25);
  }
  section[data-testid="stSidebar"] * {
    color: #f3f0e6 !important;
  }

  .brand-wrap {
    text-align: center;
    padding: 0.6rem 0 1.1rem 0;
  }
  .brand-crown {
    font-size: 2rem;
    animation: crownGlow 2.4s ease-in-out infinite;
  }
  .main-title {
    font-family: 'Cinzel', serif !important;
    font-size: 2.55rem;
    font-weight: 800;
    color: #f5e6b8 !important;
    letter-spacing: 0.04em;
    text-shadow:
      0 0 22px rgba(212, 175, 55, 0.55),
      0 2px 10px rgba(0, 0, 0, 0.55);
    margin: 0.15rem 0;
  }
  .sub-title {
    font-family: 'Source Sans 3', sans-serif !important;
    color: #c9d6c8 !important;
    font-size: 1.05rem;
    margin-top: 0.25rem;
  }
  .brand-bar {
    width: min(320px, 70%);
    height: 3px;
    margin: 0.75rem auto 0 auto;
    border-radius: 999px;
    background: linear-gradient(90deg, transparent, #d4af37, #7cffb2, #d4af37, transparent);
  }

  @keyframes crownGlow {
    0%, 100% { transform: translateY(0) scale(1); filter: drop-shadow(0 0 4px #d4af37); }
    50% { transform: translateY(-4px) scale(1.08); filter: drop-shadow(0 0 12px #d4af37); }
  }

  /* Chat input polish */
  [data-testid="stChatInput"] textarea {
    border-radius: 12px !important;
  }
</style>
"""

st.markdown(ROYALS_BG_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 👑 Royals Zone")
    st.markdown("**Royals Cricket Chatbot**")
    st.markdown(f"**Model:** `{MODEL_NAME}`")
    st.markdown(f"**Root path:** `{ROOT_PATH}`")
    st.markdown(f"**History file:** `{history_file_path()}`")
    st.divider()
    st.markdown(
        """
        **Ask about**
        - Players, rules, IPL, World Cup
        - Match **predictions** & analysis
        - **Weather** / dew / rain impact
        - **Pitch** reports & conditions

        Type **chat history** to load the CSV table from the project folder.  
        Unrelated topics → `out of context`
        """
    )
    if st.button("🔄 Clear session chat", use_container_width=True):
        st.session_state.messages = []
        init_session_history()
        st.rerun()

# ---------------------------------------------------------------------------
# Header — brand first
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="brand-wrap">
      <div class="brand-crown">👑</div>
      <div class="main-title">Royals Cricket Chatbot</div>
      <p class="sub-title">Pitch reports · Predictions · Weather · Pure cricket wisdom</p>
      <div class="brand-bar"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session + history storage
# ---------------------------------------------------------------------------
init_session_history()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------
user_input = st.chat_input("Ask Royals Cricket Chatbot…")

if user_input:
    prompt = user_input.strip()

    with st.chat_message("user"):
        st.markdown(prompt)

    # --- 1) Chat history from root_path ---
    if is_history_request(prompt):
        df = load_history_table()
        if df.empty:
            reply = (
                f"No chat history found yet at `{history_file_path()}`. "
                "Start chatting and your conversations will appear here!"
            )
            with st.chat_message("assistant"):
                st.markdown(reply)
        else:
            reply = (
                f"Here’s your chat history loaded from root path:\n`{history_file_path()}`"
            )
            with st.chat_message("assistant"):
                st.markdown(reply)
                st.dataframe(df, use_container_width=True)
                reply = reply + f"\n\n(Rows shown: {len(df)})"
        save_turn(prompt, reply)

    # --- 2) Out of context ---
    elif not is_cricket_related(prompt):
        reply = OUT_OF_CONTEXT_REPLY
        with st.chat_message("assistant"):
            st.markdown(reply)
        save_turn(prompt, reply)

    # --- 3) Cricket / related → animation + LLM ---
    else:
        topic = detect_animation_topic(prompt)
        with st.chat_message("assistant"):
            render_animation(topic)
            try:
                with st.spinner("Royals desk is analysing…"):
                    reply = get_cricket_response(prompt, st.session_state.messages)
            except Exception as exc:
                reply = (
                    f"Couldn't reach the model right now. "
                    f"Check your API key in `config.py` / `.env`. Details: {exc}"
                )
            st.markdown(reply)
        save_turn(prompt, reply)
