# hand_evaluation.py

from collections import Counter
from card import Card
from enum import Enum, auto

# Define the hand rankings
class HandRanking(Enum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    STRAIGHT = auto()
    FLUSH = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    STRAIGHT_FLUSH = auto()
    ROYAL_FLUSH = auto()

"""
Hand Evaluation Functions Documentation:

These functions evaluate a Texas Hold'em hand against standard poker hand rankings. Each function accepts a list of Card objects representing a player's hand (including community cards) and returns a tuple. The first element of the tuple is a boolean indicating whether the hand meets the specific criteria (e.g., is a flush, straight, etc.). The second element is a list of Card objects (`sorted_hand`), which is sorted based on the significance of the cards in forming the hand rank. The `sorted_hand` places the most significant cards at the front (those that form the hand rank, such as a pair or three of a kind) and then follows with the remaining cards in descending rank order to facilitate tie-breaking and hand comparison. These functions are designed to work in a sequence, checking from the highest hand rank to the lowest, allowing for an efficient determination of the hand's rank in the game.
"""


# Function to identify if there is a royal flush in the hand
def is_royal_flush_corrected(hand):
    # Check for a straight flush first
    straight_flush_result = is_straight_flush(hand)
    if straight_flush_result[0]:
        # Get the ranks of the straight flush cards
        ranks = [card.rank for card in straight_flush_result[1][:5]]  # We only need to check the first five cards
        if set(ranks) == {'10', 'Jack', 'Queen', 'King', 'Ace'}:
            # We have a royal flush
            return (True, straight_flush_result[1])
    
    # If no royal flush is found, return False with the sorted hand as it could be a high card hand
    return (False, sorted(hand, key=lambda card: Card.RANKS.index(card.rank), reverse=True))

# Function to identify if there is a straight flush in the hand
def is_straight_flush(hand):
    # Sort the hand by rank first
    sorted_hand = sorted(hand, key=lambda card: Card.RANKS.index(card.rank), reverse=True)

    # Group cards by suit and check for a straight in each suit
    for suit in Card.SUITS:
        suited_cards = [card for card in sorted_hand if card.suit == suit]
        if len(suited_cards) < 5:
            continue  # Not enough cards for a straight flush in this suit
        
        # Check for a straight within the suited cards
        straight_result = is_straight(suited_cards)
        if straight_result[0]:
            # Since it's a straight flush, all cards are already in suited straight order
            return (True, straight_result[1])
    
    # If no straight flush is found, return False with the sorted hand as it could be a high card hand
    return (False, sorted_hand)

# Function to identify if there is a four of a kind in the hand
def is_four_of_a_kind(hand):
    # Sort the hand by rank first
    sorted_hand = sorted(hand, key=lambda card: Card.RANKS.index(card.rank), reverse=True)

    # Count the occurrences of each rank in the sorted hand
    rank_counts = Counter(card.rank for card in sorted_hand)

    # Find the rank that has a count of 4
    for rank, count in rank_counts.items():
        if count == 4:
            # Identify the four cards of this rank
            four_of_a_kind_cards = [card for card in sorted_hand if card.rank == rank]
            # Get the remaining cards excluding the four of a kind, which are already sorted
            kickers = [card for card in sorted_hand if card.rank != rank]
            # Return a tuple with a boolean and the sorted list including the four of a kind first
            return (True, four_of_a_kind_cards + kickers)

    # If no four of a kind is found, return False with the sorted hand as it could be a high card hand
    return (False, sorted_hand)

# Function to identify if there is a full house in the hand
def is_full_house(hand):
    # Sort the hand by rank first
    sorted_hand = sorted(hand, key=lambda card: Card.RANKS.index(card.rank), reverse=True)
    
    # Count the occurrences of each rank in the sorted hand
    rank_counts = Counter(card.rank for card in sorted_hand)
    
    # Find ranks that have three and two cards respectively
    three_cards_rank = [rank for rank, count in rank_counts.items() if count == 3]
    two_cards_rank = [rank for rank, count in rank_counts.items() if count == 2]
    
    # Check if we have both a three of a kind and a pair
    if three_cards_rank and two_cards_rank:
        # Get the three of a kind and pair cards
        three_of_a_kind_cards = [card for card in sorted_hand if card.rank == three_cards_rank[0]]
        pair_cards = [card for card in sorted_hand if card.rank == two_cards_rank[0]]
        # The remaining cards excluding the full house
        kickers = [card for card in sorted_hand if card.rank not in [three_cards_rank[0], two_cards_rank[0]]]
        # Return a tuple with a boolean and the sorted list including the full house first
        return (True, three_of_a_kind_cards + pair_cards + kickers)
    
    # If no full house is found, return False with the sorted hand as it could be a high card hand
    return (False, sorted_hand)

def is_flush_updated(hand):
    # Assuming the hand is already sorted by rank
    suits = [card.suit for card in hand]
    # Find the suit with at least 5 cards
    for suit in set(suits):
        flush_cards = [card for card in hand if card.suit == suit]
        if len(flush_cards) >= 5:
            # We have a flush, sort the flush cards by rank
            flush_cards_sorted = sorted(flush_cards, key=lambda card: Card.RANKS.index(card.rank), reverse=True)
            # Now, the first five cards are the flush
            flush_hand = flush_cards_sorted[:5]
            # Return the flush hand as the second value
            return True, flush_hand
    # If no flush is found, return False and the original hand
    return False, hand

# Function to identify if there is a straight in the hand
def is_straight(hand):
    # Sort the hand by rank with Ace high
    sorted_hand = sorted(hand, key=lambda card: Card.RANKS.index(card.rank), reverse=True)
    
    # Helper function to get the rank's index with Ace high
    def rank_index_high(card):
        return Card.RANKS.index(card.rank)

    # Helper function to check for a straight
    def check_straight(cards):
        for i in range(len(cards) - 4):
            # Check if the sequence is continuous
            is_sequential = all(rank_index_high(cards[i + j]) == rank_index_high(cards[i]) - j for j in range(5))
            if is_sequential:
                return True, cards[i:i + 5]
        return False, []

    # Check for regular straight
    is_straight, straight_cards = check_straight(sorted_hand)
    if is_straight:
        # Get the remaining cards excluding the straight, which are already sorted
        kickers = [card for card in sorted_hand if card not in straight_cards]
        return (True, straight_cards + kickers)
    
    # Check for Ace-low straight (A-2-3-4-5)
    if 'Ace' in [card.rank for card in hand]:
        # Ace is treated as '1' here, placed at the end
        ace_low_hand = sorted(hand, key=lambda card: (Card.RANKS + ['Ace']).index(card.rank), reverse=True)
        is_straight, straight_cards = check_straight(ace_low_hand)
        if is_straight:
            kickers = [card for card in ace_low_hand if card not in straight_cards]
            return (True, straight_cards + kickers)

    # If no straight is found, return False with the hand sorted as it could be a high card hand
    return (False, sorted_hand)

# Function to identify if there is a three of a kind in the hand
def is_three_of_a_kind(hand):
    # Sort the hand by rank first
    sorted_hand = sorted(hand, key=lambda card: Card.RANKS.index(card.rank), reverse=True)
    
    # Count the occurrences of each rank in the sorted hand
    rank_counts = Counter(card.rank for card in sorted_hand)
    
    # Find the rank that has a count of 3
    for rank, count in rank_counts.items():
        if count == 3:
            # Identify the three cards of this rank
            three_of_a_kind_cards = [card for card in sorted_hand if card.rank == rank]
            # Get the remaining cards excluding the three of a kind, which are already sorted
            kickers = [card for card in sorted_hand if card.rank != rank]
            # Return a tuple with a boolean and the sorted list including the three of a kind first
            return (True, three_of_a_kind_cards + kickers)
    
    # If no three of a kind is found, return False with the sorted hand as it could be a high card hand
    return (False, sorted_hand)

# Function to identify if there are two pairs in the hand
def is_two_pair(hand):
    # Sort the hand by rank first
    sorted_hand = sorted(hand, key=lambda card: Card.RANKS.index(card.rank), reverse=True)
    
    # Count the occurrences of each rank in the sorted hand
    rank_counts = Counter(card.rank for card in sorted_hand)
    
    # Find all ranks that have a count of 2
    pairs = [rank for rank, count in rank_counts.items() if count == 2]
    
    # If there are at least two distinct ranks with a count of 2, we have two pairs
    if len(pairs) >= 2:
        # Sort the pairs by the rank index, highest first
        sorted_pairs = sorted(pairs, key=lambda rank: Card.RANKS.index(rank), reverse=True)
        # Identify the top two pairs
        top_two_pairs = sorted_pairs[:2]
        # Get all the cards that make up the top two pairs
        pair_cards = [card for card in sorted_hand if card.rank in top_two_pairs]
        # The remaining cards excluding the pairs, which are already sorted
        kickers = [card for card in sorted_hand if card.rank not in top_two_pairs]
        # Return a tuple with a boolean and the sorted list including the pair cards first
        return (True, pair_cards + kickers)
    
    # If no two pairs are found, return False with the sorted hand as it could be a high card hand
    return (False, sorted_hand)

# Function to identify if there is a pair in the hand
def is_one_pair(hand):
    # Sort the hand by rank first
    sorted_hand = sorted(hand, key=lambda card: Card.RANKS.index(card.rank), reverse=True)
    
    # Count the occurrences of each rank in the sorted hand
    rank_counts = Counter(card.rank for card in sorted_hand)
    
    # Find the rank that forms a pair (count of 2)
    for rank, count in rank_counts.items():
        if count == 2:
            # Find the cards that make up the pair
            pair = [card for card in sorted_hand if card.rank == rank]
            # Get the remaining cards excluding the pair, which are already sorted
            kickers = [card for card in sorted_hand if card not in pair]
            # Return a tuple with a boolean and the sorted list including the pair first
            return (True, pair + kickers)
    
    # If no pair is found, return False with the sorted hand as it could be a high card hand
    return (False, sorted_hand)

# Function to identify the high card in a hand
def is_high_card(hand):
    # Sort the hand by rank
    sorted_hand = sorted(hand, key=lambda card: Card.RANKS.index(card.rank), reverse=True)
    # Return a tuple with a boolean and the sorted hand
    return (True, sorted_hand)

def evaluate_hand(hand):
    # Sort the hand by rank
    sorted_hand = sorted(hand, key=lambda card: Card.RANKS.index(card.rank), reverse=True)

    # Iterate over the hand evaluation functions in order of hand strength
    for func, rank in zip(
            [is_royal_flush_corrected, is_straight_flush, is_four_of_a_kind,
             is_full_house, is_flush_updated, is_straight, is_three_of_a_kind,
             is_two_pair, is_one_pair],
            [HandRanking.ROYAL_FLUSH, HandRanking.STRAIGHT_FLUSH, HandRanking.FOUR_OF_A_KIND,
             HandRanking.FULL_HOUSE, HandRanking.FLUSH, HandRanking.STRAIGHT,
             HandRanking.THREE_OF_A_KIND, HandRanking.TWO_PAIR, HandRanking.ONE_PAIR]):
        is_hand, all_cards_sorted = func(sorted_hand)
        if is_hand:  # If the hand matches the pattern
            return rank, all_cards_sorted  # Return the hand ranking enum and the sorted cards

    # If no pattern matches, return the hand as a high card hand, already sorted
    return HandRanking.HIGH_CARD, sorted_hand


def compare_hands(hands):
    """
    Compares a list of poker hands and determines the winning hand(s).

    Parameters:
    - hands (list): A list of tuples, each representing an evaluated hand, where
                    the first element is the hand rank (as a HandRanking enum value) and
                    the second element is a list of Card objects sorted by their importance in the hand.

    Returns:
    - list: A list of tuples representing the winning hand(s). In the case of a tie, all winning hands are returned.
    """

    def hand_rank_key(hand):
        """
        Returns a tuple representing the rank of the hand for sorting purposes.
        It uses the hand rank value and the ranks of the individual cards.
        """
        return (hand[0].value, [Card.RANKS.index(card.rank) for card in hand[1]])

    hands_sorted_by_rank = sorted(hands, key=hand_rank_key, reverse=True)

    # Determine the highest hand rank
    highest_rank = hands_sorted_by_rank[0][0]

    # Filter out all hands that have the highest rank
    potential_winners = [hand for hand in hands_sorted_by_rank if hand[0] == highest_rank]

    # If there's more than one potential winner, we need to break the tie
    if len(potential_winners) > 1:
        # Compare the card ranks within the hands to break the tie
        # This assumes the cards within each hand are sorted by rank
        for i in range(1, len(potential_winners[0][1])):
            highest_card_rank = Card.RANKS.index(potential_winners[0][1][i-1].rank)
            potential_winners = [hand for hand in potential_winners if Card.RANKS.index(hand[1][i-1].rank) == highest_card_rank]

            # If we have a single winner after this comparison, break out of the loop
            if len(potential_winners) == 1:
                break

    # Return the winning hand(s)
    return potential_winners
