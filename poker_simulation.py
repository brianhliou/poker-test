from card import Card
from deck import Deck
from hand_evaluation import evaluate_hand, compare_hands

class PokerSimulation:
    def __init__(self, num_players):
        self.deck = Deck()
        self.deck.shuffle()
        self.num_players = num_players
        self.hands = []
        self.community_cards = []

    def deal_hands(self):
        # Deal two cards to each player
        hands = self.deck.deal(self.num_players, 2)
        # Check if any hand is a list of lists, which should not be the case
        for hand in hands:
            assert all(isinstance(card, Card) for card in hand), "A hand contains nested lists instead of Card objects."
        self.hands = hands

    def deal_flop(self):
        # Deal the flop (first three community cards)
        self.community_cards.extend(self.deck.deal_community_cards(3))

    def deal_turn(self):
        # Deal the turn (fourth community card)
        self.community_cards.extend(self.deck.deal_community_cards(1))

    def deal_river(self):
        # Deal the river (fifth community card)
        self.community_cards.extend(self.deck.deal_community_cards(1))

    def deal_community_cards(self, num_cards):
        # Incrementally deal the specified number of community cards
        for _ in range(num_cards):
            card = self.deck.deal_community_cards(1)[0]
            assert isinstance(card, Card), "Dealt community card is not a Card object."
            self.community_cards.append(card)

    def evaluate_hands(self):
        # Evaluate each player's hand in combination with the community cards
        evaluated_hands = []
        for hand in self.hands:
            # Ensure hand is a flat list of Card objects
            flat_hand = [card for sublist in hand for card in sublist] if any(isinstance(el, list) for el in hand) else hand
            full_hand = flat_hand + self.community_cards
            
            for card in full_hand:
                if not isinstance(card, Card):
                    print(f"Non-card element found: {card}")
            
            # Ensure that full_hand is a list of Card objects
            assert all(isinstance(card, Card) for card in full_hand), "full_hand contains non-Card elements"
            evaluated_hand = evaluate_hand(full_hand)
            evaluated_hands.append(evaluated_hand)

        # Determine the winner(s) among the evaluated hands
        winners = compare_hands(evaluated_hands)
        return winners