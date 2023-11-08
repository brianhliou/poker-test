from card import Card

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

def main2():
    # Create a hand from the example provided
    hand = [
        Card('Diamonds', 'Ace'),
        Card('Hearts', 'King'),
        Card('Diamonds', 'Queen'),
        Card('Spades', '10'),
        Card('Clubs', '10'),
        Card('Spades', '4'),
        Card('Hearts', '2')
    ]

    # Test the is_straight function
    is_straight_result, straight_cards = is_straight(hand)

    # Print the result
    print(f"Is the hand a straight? {is_straight_result}")
    if is_straight_result:
        print(f"Straight cards: {[str(card) for card in straight_cards]}")

# Call the main2 function
main2()