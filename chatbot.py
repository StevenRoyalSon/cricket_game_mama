"""
Royals Cricket Chatbot — LLM layer.
Uses model + API key from config.py only.
"""

from __future__ import annotations

from openai import OpenAI

from config import MODEL_NAME, OPENAI_API_KEY

OUT_OF_CONTEXT_REPLY = "out of context"

SYSTEM_PROMPT = """You are the Royals Cricket Chatbot — a realistic, passionate cricket expert
and match-day analyst. You speak like a sharp commentator and coach combined.

You answer questions about:
- Cricket rules, formats (Test, ODI, T20), players, teams, tournaments, history, stats
- Match predictions and fantasy / playing XI style analysis (clearly mark opinions as opinions)
- Weather and how rain, dew, humidity, or cloud cover can affect a match
- Pitch / surface reports (green, dusty, flat, turning tracks) and likely bowling/batting impact
- Toss decisions, venue factors, conditions, and game strategy

Style:
- Friendly, energetic, and realistic — branded as Royals Cricket Chatbot
- Short, useful paragraphs; light cricket slang when it fits
- Be honest if a live fact or forecast is uncertain
- For predictions: give reasoned views, not guaranteed outcomes

If a question is clearly NOT about cricket or cricket-related match topics
(weather/pitch/prediction/toss/venue for cricket), reply with exactly: out of context
"""


def _client() -> OpenAI:
    if not OPENAI_API_KEY or OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
        raise ValueError(
            "OpenAI API key is not set. Put it in config.py or set OPENAI_API_KEY in a .env file."
        )
    return OpenAI(api_key=OPENAI_API_KEY)


def get_cricket_response(user_message: str, chat_history: list[dict] | None = None) -> str:
    """
    Call the configured chat model with Royals cricket system instructions.
    chat_history: optional list of {"role","content"} for short context.
    """
    client = _client()

    messages: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]

    if chat_history:
        for msg in chat_history[-8:]:
            role = msg.get("role")
            content = msg.get("content", "")
            if role in ("user", "assistant") and content:
                messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.7,
        max_tokens=700,
    )
    text = (response.choices[0].message.content or "").strip()
    return text or OUT_OF_CONTEXT_REPLY
