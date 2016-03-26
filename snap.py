from __future__ import print_function
import random
import sys

if sys.version_info.major < 3:  # A bit or py2/3 compatibility
    input = raw_input


class Card(object):
    """
    Card object to hold value and suit, makes comparisons nice and easy.

    Also prints out the card name which looks nice.
    """
    VALUES_TO_NAME = {1: 'Ace',
                      2: 'Two',
                      3: 'Three',
                      4: 'Four',
                      5: 'Five',
                      6: 'Six',
                      7: 'Seven',
                      8: 'Eight',
                      9: 'Nine',
                      10: 'Ten',
                      11: 'Jack',
                      12: 'Queen',
                      13: 'King'}

    SUITS = ('Hearts', 'Clubs', 'Diamonds', 'Spades')

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

        if self.value not in self.VALUES_TO_NAME:
            raise ValueError('The given value is not valid, needs to be between 1-13')

        if self.suit not in self.SUITS:
            raise ValueError('The given suit is not valid, needs to be in {}.'.format(self.SUITS))

    def __repr__(self):
        """
        Builds the card name from value and suit and returns it when printed.

        :return: str, the name of the card.
        """
        return self.VALUES_TO_NAME[self.value] + ' of ' + self.suit


def compare_suit(card1, card2):
    """
    Compares the suits of two cards.

    :param card1: card object.
    :param card2: card object.
    :return: bool, if the cards match suit.
    """
    return card1.suit == card2.suit


def compare_value(card1, card2):
    """
    Compares the values of two cards.

    :param card1: card object.
    :param card2: card object.
    :return: bool, if the cards match value.
    """
    return card1.value == card2.value


def compare_suit_and_value(card1, card2):
    """
    Compares both the suit and value of a card.

    :param card1: card object.
    :param card2: card object.
    :return: bool, if the cards match by either suit or value.
    """
    return compare_suit(card1, card2) or compare_value(card1, card2)


def get_input():
    """
    Take user input to get the number of decks used and the ruleset required.

    Does some sense checking of the input to ensure everything is as expected.

    :return: tuple (int, func), a tuple containing the number of decks needed and the function holding the ruleset used.
    """

    n_of_decks = None

    # Below keys are strs to make using input that little bit easier.
    rulesets = {'1': compare_suit, '2': compare_value, '3': compare_suit_and_value}

    rule_choice = None

    while not n_of_decks:  # Lets find out how many decks of cars we will use.
        n_of_decks_inp = input("How many decks of cards are being used? ")

        try:
            n_of_decks = int(n_of_decks_inp)

            if n_of_decks < 1:  # Could in theory allow 0, negative numbers will likely cause problems though.
                print("That number is too low, try again.")
                n_of_decks = None  # reset to None so we can keep looping.

        except ValueError:  # The input isn't a number try again.
            print("Sorry that wasn't a number, try again.")

    print('Thanks, you chose ' + n_of_decks_inp)

    while rule_choice not in rulesets:  # Now lets get the ruleset.
        # The below is too long for PEP8 standards, but I don't think that is reason enough to chop it down.
        rule_choice = input('Please choose a ruleset:\n1) Compare suits.\n2) Compare values.\n3) Compare both.\nPick a number: ')

        if rule_choice not in rulesets:
            print('That was not a valid choice, please choose 1, 2 or 3. Try again.')

    print('Thanks, you chose rule ' + rule_choice)

    return n_of_decks, rulesets[rule_choice]


def set_up_game(n_decks):
    """
    Set up the deck of cards.

    :param n_decks: int, number of decks being used.
    :return: lst, the shuffled deck.
    """

    assert n_decks > 0  # We shouldn't have a negative or 0 deck.

    deck = []

    for suit in Card.SUITS:
        for value in range(1,14):
            deck.append(Card(suit, value))

    deck *= n_decks

    random.shuffle(deck)

    return deck


def run_game(deck, rule, num_players=2):
    """
    Lets create the players and run through the deck until it is finished.

    :param deck: lst, the shuffled deck.
    :param rule: func, the ruleset being used in this game.
    :param num_players: int, the number of players playing the game.
    :return: dict, a dictionary holding all the players and their hands.
    """
    keys = []  # Holding a list of player keys makes random.choice easier to use.

    players = {}

    for x in range(1, num_players + 1):
        player = 'Player ' + str(x)
        keys.append(player)
        players[player] = []

    used_pile = []  # This will hold the shown cards until a match is found.

    used_pile.append(deck.pop())

    while deck:  # This is the main loop running the card drawing.
        used_pile.append(deck.pop())  # Draw a card.

        if rule(used_pile[-1], used_pile[-2]):
            players[random.choice(keys)] += used_pile  # The cards match, pick a player and give them the cards.

            used_pile = []  # reset the used pile.

            # We need at least one card in the used_cards deck to start.
            # But at this point it is possible the deck has already been used up.
            # We could check the deck to see if it is empty.
            # But as this is an unlikely occurence it would be more efficient to use a try/except.
            try:
                used_pile.append(deck.pop())

            except IndexError:
                break

    return players


def decide_winner(players):
    """
    Find the person with the most cards.

    :param players: dict, a dict of player names as keys and their hand of cards as values.
    :return: str, the winning players name.
    """
    return max(players, key= lambda x: len(players[x]))


def main():
    """
    Run the game.
    """
    n_of_decks, rule = get_input()
    deck = set_up_game(n_of_decks)
    players = run_game(deck, rule)
    winner = decide_winner(players)

    print(winner + ' is the winner!')


if __name__ == '__main__':
    main()

