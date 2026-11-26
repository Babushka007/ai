# Blackjack — You Deal, Bot Plays

The standalone tournament bot is [`zanylegoat/bot.py`](zanylegoat/bot.py),
named `zanylegoat`. It implements the required API:

```python
place_bet(bankroll: int, history: list[str], decks_remaining: float) -> int
decide_action(
    hand: list[str],
    dealer_upcard: str,
    history: list[str],
    can_double: bool,
    can_split: bool,
) -> str
```

Actions are returned in uppercase: `"HIT"`, `"STAND"`, `"DOUBLE"`, or
`"SPLIT"`. Cards use strings like `"AS"`, `"TH"`, `"KD"`, and `"2C"`.
History must contain exposed cards from the current shoe, including other
players' revealed cards and the current hand/upcard; do not include the
dealer's hidden card.

The bot estimates action EV by sampling card draws without replacement from a
four-deck composition, uses Hi-Lo true count with conservative Kelly sizing
for bets, and evaluates splits (including one-card-only split aces). Bets are
capped at 10% of bankroll and 200 chips. The local GUI uses the same four-deck
shoe and reshuffles with 52 cards remaining. Tournament decisions use the
specified stand-on-soft-17 rule.

The tournament interface provides no round-result callback, so tournament
Q-learning cannot be updated reliably; tournament decisions use the shoe-aware
EV calculations. The local GUI's optional learning hooks are not needed by the
tournament runner.

There are no third-party dependencies. The tournament bot uses only Python's
standard library and does not print or prompt for input.

## Run

On Windows, double-click `Play Blackjack.bat`, or run:

```powershell
py blackjack.py
```

Run the game-logic and bot-strategy tests with:

```powershell
py -m unittest -v
```
