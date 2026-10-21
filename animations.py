"""
Crazy cricket-themed CSS / HTML animations keyed to question topics.
"""

from __future__ import annotations

import streamlit as st

# Topic → floating emoji set + label
ANIMATION_THEMES: dict[str, dict] = {
    "six": {
        "label": "SIX! Ball sailing into the stands!",
        "emojis": ["🏏", "🚀", "💥", "🏟️", "🔥", "⚡"],
        "color": "#ff6b35",
    },
    "four": {
        "label": "FOUR! Racing to the ropes!",
        "emojis": ["🏏", "💨", "🟩", "✨", "🎯", "👏"],
        "color": "#2ecc71",
    },
    "wicket": {
        "label": "WICKET! Stumps flying!",
        "emojis": ["🏏", "🪓", "💥", "😱", "🔥", "📌"],
        "color": "#e74c3c",
    },
    "world_cup": {
        "label": "World Cup vibes!",
        "emojis": ["🏆", "🌍", "🏏", "🥇", "✨", "🎉"],
        "color": "#f1c40f",
    },
    "ipl": {
        "label": "IPL fireworks!",
        "emojis": ["🎆", "🏏", "💜", "🧡", "⚡", "🏟️"],
        "color": "#9b59b6",
    },
    "bat": {
        "label": "Sweet timing with the willow!",
        "emojis": ["🏏", "💪", "📈", "⭐", "🟢", "🙌"],
        "color": "#27ae60",
    },
    "bowl": {
        "label": "Pace & spin magic!",
        "emojis": ["🌀", "⚡", "🎯", "🔥", "🏏", "💨"],
        "color": "#3498db",
    },
    "trophy": {
        "label": "Champions lift the cup!",
        "emojis": ["🏆", "🥇", "🎊", "🏏", "👑", "✨"],
        "color": "#f39c12",
    },
    "cheer": {
        "label": "Crowd goes wild!",
        "emojis": ["📣", "👏", "🏟️", "🎉", "🏏", "🙌"],
        "color": "#e67e22",
    },
    "weather": {
        "label": "Weather watch — dew & clouds!",
        "emojis": ["🌧️", "☁️", "💧", "🌤️", "🏏", "⚡"],
        "color": "#5dade2",
    },
    "pitch": {
        "label": "Pitch report incoming!",
        "emojis": ["🟩", "🔍", "🏏", "🌀", "📏", "🔥"],
        "color": "#58d68d",
    },
    "predict": {
        "label": "Match prediction mode!",
        "emojis": ["🔮", "📊", "🏏", "🏆", "⚡", "👑"],
        "color": "#d4af37",
    },
    "cricket": {
        "label": "Royals cricket fever!",
        "emojis": ["👑", "🏏", "🏟️", "⚡", "💥", "🙌"],
        "color": "#d4af37",
    },
}


def _build_animation_html(topic: str) -> str:
    theme = ANIMATION_THEMES.get(topic, ANIMATION_THEMES["cricket"])
    emojis = theme["emojis"]
    color = theme["color"]
    label = theme["label"]

    spans = "".join(
        f'<span class="float-emoji e{i}">{emoji}</span>'
        for i, emoji in enumerate(emojis)
    )

    return f"""
    <style>
      .anim-box {{
        position: relative;
        overflow: hidden;
        height: 110px;
        margin: 0.4rem 0 0.8rem 0;
        border-radius: 16px;
        background: linear-gradient(135deg, {color}33, #0b3d1f55);
        border: 2px dashed {color};
        display: flex;
        align-items: center;
        justify-content: center;
      }}
      .anim-label {{
        position: relative;
        z-index: 2;
        font-weight: 800;
        font-size: 1.15rem;
        color: {color};
        text-shadow: 0 2px 8px rgba(0,0,0,0.35);
        letter-spacing: 0.5px;
        animation: pulse 1.2s ease-in-out infinite;
      }}
      .float-emoji {{
        position: absolute;
        font-size: 1.8rem;
        animation: crazyFloat 2.4s ease-in-out infinite;
        z-index: 1;
        opacity: 0.95;
      }}
      .e0 {{ left: 6%;  animation-delay: 0s; }}
      .e1 {{ left: 22%; animation-delay: 0.25s; }}
      .e2 {{ left: 38%; animation-delay: 0.5s; }}
      .e3 {{ left: 54%; animation-delay: 0.15s; }}
      .e4 {{ left: 70%; animation-delay: 0.4s; }}
      .e5 {{ left: 86%; animation-delay: 0.65s; }}
      @keyframes crazyFloat {{
        0%   {{ transform: translateY(40px) rotate(0deg) scale(0.7); opacity: 0; }}
        30%  {{ opacity: 1; }}
        50%  {{ transform: translateY(-18px) rotate(20deg) scale(1.25); }}
        100% {{ transform: translateY(-55px) rotate(-15deg) scale(0.85); opacity: 0; }}
      }}
      @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.08); }}
      }}
    </style>
    <div class="anim-box">
      {spans}
      <div class="anim-label">{label}</div>
    </div>
    """


def render_animation(topic: str | None) -> None:
    """Render a themed animation in Streamlit when topic is known."""
    if not topic:
        return
    st.markdown(_build_animation_html(topic), unsafe_allow_html=True)
