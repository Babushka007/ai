import unittest

from blackjack import (
    Card,
    DECK_COUNT as GAME_DECK_COUNT,
    RESHUFFLE_REMAINING,
    is_blackjack,
    new_shoe,
)
import zanylegoat.bot as bot
from bot import (
    BOT_NAME,
    DECK_COUNT,
    EV_TIE_MARGIN,
    analyze_hand,
    count_info,
    decide_action,
    get_move,
    hand_value,
    place_bet,
)


class BlackjackLogicTests(unittest.TestCase):
    def test_aces_count_as_eleven_when_possible_and_one_when_needed(self):
        self.assertEqual(hand_value([Card("A", "♠"), Card("6", "♦")]), (17, True))
        self.assertEqual(hand_value([Card("A", "♠"), Card("6", "♦"), Card("9", "♣")]), (16, False))

    def test_multiple_aces_reduce_without_busting(self):
        self.assertEqual(
            hand_value([Card("A", "♠"), Card("A", "♦"), Card("9", "♣")]),
            (21, True),
        )

    def test_blackjack_requires_two_cards(self):
        self.assertTrue(is_blackjack([Card("A", "♠"), Card("K", "♦")]))
        self.assertFalse(is_blackjack([Card("7", "♠"), Card("7", "♦"), Card("7", "♣")]))

    def test_bot_uses_hard_and_soft_totals_against_upcard(self):
        self.assertEqual(
            get_move([Card("10", "♠"), Card("6", "♦")], Card("10", "♣")),
            "hit",
        )
        self.assertEqual(
            get_move([Card("10", "♠"), Card("6", "♦")], Card("5", "♣")),
            "stand",
        )
        self.assertEqual(
            get_move([Card("A", "♠"), Card("7", "♦")], Card("7", "♣")),
            "stand",
        )

    def test_double_is_only_recommended_on_first_decision(self):
        hand = [Card("5", "♠"), Card("4", "♦")]
        self.assertEqual(get_move(hand, Card("5", "♣")), "double")
        self.assertEqual(get_move(hand + [Card("2", "♥")], Card("5", "♣")), "hit")

    def test_soft_nineteen_decision_changes_with_dealer_rule(self):
        hand = [Card("A", "♠"), Card("8", "♦")]
        upcard = Card("6", "♣")
        _, stand_values, _, _ = analyze_hand(
            hand, upcard, seen_cards=hand + [upcard], simulations=2048
        )
        _, hit_values, _, _ = analyze_hand(
            hand,
            upcard,
            dealer_hits_soft_17=True,
            seen_cards=hand + [upcard],
            simulations=2048,
        )
        self.assertLess(hit_values["stand"], stand_values["stand"])

    def test_tournament_name(self):
        self.assertEqual(BOT_NAME, "zanylegoat")
        self.assertEqual(DECK_COUNT, 4)
        self.assertEqual(GAME_DECK_COUNT, 4)
        self.assertEqual(len(new_shoe()), 208)
        self.assertEqual(RESHUFFLE_REMAINING, 52)

    def test_tournament_string_cards_are_parsed(self):
        self.assertEqual(hand_value(["AS", "10H"]), (21, True))
        self.assertEqual(get_move(["10S", "KC"], "10H"), "stand")
        self.assertEqual(hand_value(["AS", "TH"]), (21, True))

    def test_tournament_betting_uses_count_and_bankroll_caps(self):
        neutral_history = ["AS", "10H"] * 8
        positive_history = ["2C"] * 16
        self.assertEqual(place_bet(1000, neutral_history, 3.0), 10)
        bet = place_bet(1000, positive_history, 3.0)
        self.assertGreater(bet, 10)
        self.assertLessEqual(bet, 100)

    def test_tournament_actions_respect_legal_action_flags(self):
        hand = ["8S", "8H"]
        history = hand + ["6C"]
        _, values, _, _ = analyze_hand(
            hand,
            "6C",
            seen_cards=history,
            simulations=128,
            can_double=False,
            can_split=True,
            use_learning=False,
        )
        self.assertIn("split", values)
        self.assertIn(
            decide_action(hand, "6C", history, can_double=False, can_split=True),
            {"HIT", "STAND", "SPLIT"},
        )
        self.assertNotEqual(
            decide_action(hand, "6C", history, can_double=True, can_split=False),
            "SPLIT",
        )

    def test_pair_of_aces_splits_against_weak_dealer_card(self):
        hand = ["AS", "AD"]
        history = hand + ["5C"]
        self.assertEqual(
            decide_action(hand, "5C", history, can_double=True, can_split=True),
            "SPLIT",
        )

    def test_hi_lo_count_uses_only_exposed_cards(self):
        running, true_count = count_info(["2C", "KD", "AS"])
        self.assertEqual(running, -1)
        self.assertLess(true_count, 0)

    def test_ev_analysis_selects_an_action_with_near_maximum_ev(self):
        hand = [Card("10", "♠"), Card("6", "♦")]
        upcard = Card("10", "♣")
        action, values, _, _ = analyze_hand(
            hand, upcard, seen_cards=hand + [upcard], simulations=256
        )
        self.assertIn(action, values)
        self.assertLessEqual(max(values.values()) - values[action], EV_TIE_MARGIN)

    def test_q_learning_updates_after_a_completed_hand(self):
        hand = [Card("2", "♠"), Card("3", "♦")]
        upcard = Card("4", "♣")
        seen = hand + [upcard]
        bot.start_hand()
        action, _, _, _ = bot.analyze_hand(
            hand, upcard, seen_cards=seen, simulations=32
        )
        state = bot._state_key(hand, upcard, seen)
        previous_count = bot._Q_COUNTS.get((state, action), 0)
        bot.learn_from_result(1)
        self.assertEqual(bot._Q_COUNTS[(state, action)], previous_count + 1)


if __name__ == "__main__":
    unittest.main()
