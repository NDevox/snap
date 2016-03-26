import unittest

import snap


class TestCard(unittest.TestCase):
    """
    Tests for the card class.
    """
    def test_suit(self):
        """
        Make sure that cards can only accept the given suits.
        """
        with self.assertRaises(ValueError):
            snap.Card('xyz', 1)
        for suit in snap.Card.SUITS:
            snap.Card(suit, 1)

    def test_value(self):
        """
        Make sure that cards can only accept values between 1-13.
        """
        suit = snap.Card.SUITS[0]
        with self.assertRaises(ValueError):
            snap.Card(suit, 0)
        for x in range(1, 14):
            snap.Card(suit, x)


class TestSnapGame(unittest.TestCase):
    """
    Test the snap game itself.
    """
    def test_deck_size(self):
        """
        Test deck creation.

        We can't have negative or 0 decks.

        And positive decks should be a multiple of 52.
        :return:
        """
        with self.assertRaises(AssertionError):
            snap.set_up_game(0)
        with self.assertRaises(AssertionError):
            snap.set_up_game(-1)

        for x in range(1, 100):
            self.assertEqual(52 * x, len(snap.set_up_game(x)))

    def test_rulesets(self):
        """
        Make sure the rulesets compare correctly.
        """
        card1 = snap.Card('Hearts', 1)
        card2 = snap.Card('Hearts', 2)
        card3 = snap.Card('Spades', 1)
        card4 = snap.Card('Hearts', 1)
        card5 = snap.Card('Spades', 2)

        self.assertEqual(False, snap.compare_suit(card1, card3))
        self.assertEqual(True, snap.compare_suit(card1, card2))
        self.assertEqual(True, snap.compare_suit(card1, card4))
        self.assertEqual(False, snap.compare_suit(card1, card5))

        self.assertEqual(True, snap.compare_value(card1, card3))
        self.assertEqual(False, snap.compare_value(card1, card2))
        self.assertEqual(True, snap.compare_value(card1, card4))
        self.assertEqual(False, snap.compare_value(card1, card5))

        self.assertEqual(True, snap.compare_suit_and_value(card1, card3))
        self.assertEqual(True, snap.compare_suit_and_value(card1, card2))
        self.assertEqual(True, snap.compare_suit_and_value(card1, card4))
        self.assertEqual(False, snap.compare_suit_and_value(card1, card5))


    def test_end_on_deck(self):
        """
        Make sure that by the end of the game the deck has been depleted.
        """

        ###########################small deck################################

        deck = snap.set_up_game(1)  # single deck

        snap.run_game(deck, snap.compare_suit)

        self.assertEqual(len(deck), 0)

        ###########################large deck################################

        deck = snap.set_up_game(100)

        snap.run_game(deck, snap.compare_suit)

        self.assertEqual(len(deck), 0)

        ###########################all rules#################################

        deck = snap.set_up_game(1)

        snap.run_game(deck, snap.compare_value)

        self.assertEqual(len(deck), 0)

        deck = snap.set_up_game(1)

        snap.run_game(deck, snap.compare_suit_and_value)

        self.assertEqual(len(deck), 0)

if __name__ == '__main__':
    unittest.main()