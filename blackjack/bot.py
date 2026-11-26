"""Compatibility exports for the local Blackjack GUI."""

from zanylegoat.bot import (
    BOT_NAME,
    DECK_COUNT,
    EV_TIE_MARGIN,
    analyze_hand,
    count_info,
    decide_action,
    get_move,
    hand_value,
    learn_from_result,
    place_bet,
    start_hand,
)


__all__ = [
    "BOT_NAME",
    "DECK_COUNT",
    "EV_TIE_MARGIN",
    "analyze_hand",
    "count_info",
    "decide_action",
    "get_move",
    "hand_value",
    "learn_from_result",
    "place_bet",
    "start_hand",
]
