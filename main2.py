from poker_simulation import PokerSimulation

def format_hand(hand):
    return ', '.join(str(card) for card in hand)

def main():
    # Ask for the number of players
    num_players = int(input("Enter the number of players: "))

    # Initialize the poker simulation with the number of players
    poker_sim = PokerSimulation(num_players)

    # Deal hands to players
    poker_sim.deal_hands()
    print("\nPlayer hands dealt:")
    for i, hand in enumerate(poker_sim.hands, start=1):
        print(f"Player {i}'s hand: {format_hand(hand)}")

    # Deal the flop
    poker_sim.deal_flop()
    print("\nThe flop is dealt:")
    print(f"Flop: {format_hand(poker_sim.community_cards)}")

    # Deal the turn
    poker_sim.deal_turn()
    print("\nThe turn is dealt:")
    print(f"Turn: {format_hand(poker_sim.community_cards[-1:])}")  # Just the turn card

    # Deal the river
    poker_sim.deal_river()
    print("\nThe river is dealt:")
    print(f"River: {format_hand(poker_sim.community_cards[-1:])}")  # Just the river card

    # Evaluate and determine the winner(s)
    winners = poker_sim.evaluate_hands()

    # Output the results
    # If there are multiple winners (a tie), we'll print them all
    print("\nResults:")
    for winner_number, winner_hand in winners:
        formatted_hand = format_hand(winner_hand[1])
        rank_name = winner_hand[0].name
        print(f"Player {winner_number} wins with a hand of: {formatted_hand} with a rank of {rank_name}")
        
if __name__ == "__main__":
    main()
