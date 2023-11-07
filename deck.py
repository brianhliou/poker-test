import random
from card import Card

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_hands, cards_per_hand):
        if num_hands * cards_per_hand > len(self.cards):
            raise ValueError('Not enough cards in the deck to deal')
        return [[self.cards.pop() for _ in range(cards_per_hand)] for _ in range(num_hands)]

    def deal_community_cards(self, num_cards):
        if num_cards > len(self.cards):
            raise ValueError('Not enough cards in the deck to deal community cards')
        return [self.cards.pop() for _ in range(num_cards)]