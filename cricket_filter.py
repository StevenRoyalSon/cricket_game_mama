"""
Detect whether a user message is cricket-related (or cricket-adjacent)
or out of context. Also detect "show chat history" style requests.

In-scope includes direct cricket topics AND related match-day topics:
predictions, weather, pitch/conditions, toss, venue, form analysis, etc.
"""

from __future__ import annotations

import re

# Core cricket keywords
CRICKET_KEYWORDS = [
    "cricket", "bat", "batsman", "batter", "bowler", "bowling", "batting",
    "wicket", "wickets", "stumps", "bail", "bails", "innings", "over", "overs",
    "run", "runs", "six", "four", "boundary", "boundaries", "century", "fifty",
    "duck", "yorker", "googly", "doosra", "swing", "spin", "pace", "fast bowler",
    "spinner", "all-rounder", "allrounder", "keeper", "wicketkeeper", "fielder",
    "fielding", "catch", "caught", "lbw", "run out", "stumped", "no ball",
    "wide", "maiden", "powerplay", "dls", "duckworth", "super over",
    "odi", "t20", "t20i", "test match", "test cricket", "ipl", "bbl", "psl",
    "world cup", "ashes", "champions trophy", "asia cup", "wpl", "ranji",
    "icc", "bcci", "ecb", "crease", "outfield", "midwicket",
    "cover drive", "pull shot", "hook", "sweep", "slog", "strike rate",
    "economy rate", "net run rate", "nrr", "man of the match", "hat-trick",
    "hat trick", "hattrick", "debut", "captain", "scorecard",
    "score", "chasing", "target", "declaration", "follow on", "follow-on",
    "virat", "kohli", "dhoni", "sachin", "tendulkar", "rohit", "sharma",
    "bumrah", "jadeja", "ashwin", "rahul", "hardik", "pandya", "gilchrist",
    "ponting", "warne", "mcgrath", "lara", "ganguly", "dravid", "sehwag",
    "babar", "stokes", "root", "smith", "warner", "williamson", "rashid",
    "afghanistan", "australia", "england", "india", "pakistan", "sri lanka",
    "south africa", "new zealand", "west indies", "bangladesh", "zimbabwe",
    "ireland", "netherlands", "match", "tournament", "franchise", "jersey",
    "helmet", "pads", "gloves", "umpire", "third umpire", "drs", "review",
    "red ball", "white ball", "pink ball", "nightwatchman", "tailender",
    "royals", "rajasthan royals",
]

# Cricket-adjacent topics that should still be answered (not out of context)
RELATED_KEYWORDS = [
    # Predictions / analysis
    "predict", "prediction", "predictions", "forecast", "who will win",
    "who wins", "winner", "likely", "chance", "odds", "betting",
    "fantasy", "dream11", "team prediction", "match prediction",
    "analysis", "preview", "review match", "form", "head to head",
    "head-to-head", "h2h", "strength", "weakness", "xi", "playing xi",
    "lineup", "line-up", "squad",
    # Weather / conditions
    "weather", "rain", "raining", "cloudy", "cloud", "humidity", "dew",
    "temperature", "climate", "drizzle", "storm", "wet", "dry weather",
    "overcast", "sunny", "heat", "conditions", "match conditions",
    # Pitch / surface
    "pitch", "pitches", "surface", "wicket condition", "green top",
    "green pitch", "dusty", "dusty pitch", "dead pitch", "flat pitch",
    "turner", "spinning track", "seaming", "seam track", "two-paced",
    "cracks", "grass cover", "pitch report", "track", "deck",
    # Toss / venue / strategy
    "toss", "opt to bat", "opt to bowl", "venue", "stadium", "ground",
    "home advantage", "day night", "day-night", "floodlight",
    "strategy", "tactics", "game plan", "approach",
]

HISTORY_PHRASES = [
    "chat history",
    "chathistory",
    "chat_history",
    "show history",
    "show chat history",
    "my history",
    "previous chats",
    "previous messages",
    "conversation history",
    "past chats",
]


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def is_history_request(user_input: str) -> bool:
    """True when the user is asking to see stored chat history."""
    text = _normalize(user_input)
    return any(phrase in text for phrase in HISTORY_PHRASES)


def is_cricket_related(user_input: str) -> bool:
    """
    Return True if the message is cricket-related OR cricket-adjacent
    (predictions, weather, pitch, toss, venue, form, etc.).
    History requests are in-scope (handled specially by the app).
    """
    if is_history_request(user_input):
        return True

    text = _normalize(user_input)
    if any(keyword in text for keyword in CRICKET_KEYWORDS):
        return True
    if any(keyword in text for keyword in RELATED_KEYWORDS):
        return True
    return False


def detect_animation_topic(user_input: str) -> str | None:
    """Map user question to an animation theme key, or None."""
    text = _normalize(user_input)

    topic_map = {
        "six": ["six", "maximum", "big hit", "over the ropes"],
        "four": ["four", "boundary", "boundaries"],
        "wicket": ["wicket", "out", "bowled", "lbw", "caught", "stumped", "run out"],
        "world_cup": ["world cup", "icc world", "champions trophy", "asia cup"],
        "ipl": ["ipl", "indian premier league", "wpl", "royals"],
        "bat": ["bat", "batting", "batsman", "batter", "century", "fifty", "innings"],
        "bowl": ["bowl", "bowler", "bowling", "yorker", "googly", "spin", "pace"],
        "trophy": ["trophy", "cup", "champion", "winner", "title"],
        "cheer": ["cheer", "fan", "stadium", "crowd", "celebrate", "celebration"],
        "weather": ["weather", "rain", "dew", "humidity", "cloudy", "overcast", "climate"],
        "pitch": ["pitch", "surface", "green top", "dusty", "turner", "pitch report", "track"],
        "predict": ["predict", "prediction", "forecast", "who will win", "odds", "fantasy"],
    }

    for topic, keys in topic_map.items():
        if any(k in text for k in keys):
            return topic
    if is_cricket_related(user_input) and not is_history_request(user_input):
        return "cricket"
    return None
