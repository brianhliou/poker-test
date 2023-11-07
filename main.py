import json

from deck import Deck
from card import Card
from hand_evaluation import evaluate_hand, compare_hands

def create_hand(cards):
    """ Helper function to create a hand from string representations of cards. """
    suit_map = {'H': 'Hearts', 'D': 'Diamonds', 'C': 'Clubs', 'S': 'Spades'}
    rank_map = {
        '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', 
        '8': '8', '9': '9', '10': '10', 'J': 'Jack', 'Q': 'Queen', 
        'K': 'King', 'A': 'Ace'
    }
    hand = []
    for card_str in cards:
        rank, suit = card_str[:-1], card_str[-1]  # Split the card string into rank and suit parts
        hand.append(Card(suit_map[suit], rank_map[rank]))
    return hand

def read_test_cases(file_path):
    # This depends on the file format you choose
    # For JSON, it might look like this:
    with open(file_path, 'r') as file:
        test_cases = json.load(file)
    return test_cases

def run_test_case(test_case):
    # Create hands from the string representations
    hands = [create_hand(hand_str) for hand_str in test_case['hands']]
    # Evaluate each hand
    evaluated_hands = [evaluate_hand(hand) for hand in hands]
    # Determine the winner from the evaluated hands
    winner = compare_hands(evaluated_hands)

    # The expected_winner is already a list of card strings, no need to iterate over it
    expected_winner_cards = create_hand(test_case['expected_winner'][0])
    # Evaluate the expected winner hand to get the correct format
    expected_winner_evaluated = evaluate_hand(expected_winner_cards)

    # Compare the evaluated winner to the expected outcome
    # Since 'winner' is a list of tuples, and we expect no ties, we take the first element.
    is_correct = winner[0] == expected_winner_evaluated

    return is_correct, winner, expected_winner_evaluated



def main():
    test_cases = read_test_cases('test_cases.json')  # Or whatever your test file is called
    passed, failed = 0, 0

    for i, test_case in enumerate(test_cases, 1):
        is_correct, winner, expected_winner = run_test_case(test_case)
        print(f"Test Case {i}:")
        print(f"Winner: {winner}")
        print(f"Expected Winner: {expected_winner}")
        print(f"Test {'PASSED' if is_correct else 'FAILED'}")
        print()  # Empty line for readability between test cases
        
        if is_correct:
            passed += 1
        else:
            failed += 1

    print(f"Total Tests: {passed + failed}, Passed: {passed}, Failed: {failed}")

if __name__ == "__main__":
    main()