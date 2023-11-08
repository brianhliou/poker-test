import tkinter as tk
from poker_simulation import PokerSimulation

class PokerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Poker Simulation")
        self.simulation = PokerSimulation(num_players=2)  # Initialize with the desired number of players
        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack()
        self.dealer_button = tk.Button(self.root, text="Next Action", command=self.next_action)
        self.test_button = tk.Button(self.root, text="Test Draw", command=self.test_draw)
        self.test_button.pack()
        self.dealer_button.pack()
        self.stage = "deal"
        self.card_width = 50  # Set as class attribute
        self.card_height = 70  # Set as class attribute

    def test_draw(self):
        self.canvas.create_rectangle(50, 50, 100, 100, outline="blue", width=3)
        self.canvas.create_text(75, 75, text="Test", font=('Helvetica', 16), fill="blue")
        self.canvas.tag_raise("winner")
        self.canvas.update()

    def draw_card(self, card, x, y):
        # Use self.card_width and self.card_height since they're now class attributes
        self.canvas.create_rectangle(x, y, x + self.card_width, y + self.card_height, fill="white")
        self.canvas.create_text(x + self.card_width / 2, y + self.card_height / 2, text=str(card))

    def next_action(self):
        if self.stage == "deal":
            self.simulation.deal_hands()
            self.stage = "flop"
        elif self.stage == "flop":
            self.simulation.deal_community_cards(3)  # Deal the flop
            self.stage = "turn"
        elif self.stage == "turn":
            self.simulation.deal_community_cards(1)  # Deal the turn
            self.stage = "river"
        elif self.stage == "river":
            self.simulation.deal_community_cards(1)  # Deal the river
            self.stage = "showdown"
        elif self.stage == "showdown":
            winners = self.simulation.evaluate_hands()
            # Handle displaying winners here
            self.display_winners(winners)
            self.stage = "complete"  # Or reset to "deal" for a new game
        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")  # Clear the canvas
        
        # Define starting positions for the cards
        x_offset = 20
        y_offset = 20
        card_spacing = 15  # Spacing between cards
        
        # Draw player hands
        for i, hand in enumerate(self.simulation.hands):
            for j, card in enumerate(hand):
                x_position = x_offset + j * (self.card_width + card_spacing)
                y_position = y_offset + i * (self.card_height + card_spacing)
                self.draw_card(card, x_position, y_position)

        # Draw community cards
        community_card_x_offset = x_offset
        community_card_y_offset = y_offset + len(self.simulation.hands) * (self.card_height + card_spacing) + 50  # Adjust 50 to whatever spacing you want below the hands
        for i, card in enumerate(self.simulation.community_cards):
            x_position = community_card_x_offset + i * (self.card_width + card_spacing)
            y_position = community_card_y_offset
            self.draw_card(card, x_position, y_position)

        # Additional updates to the canvas go here

    def display_winners(self, winners):
        print("Displaying winners...")  # Debugging statement to confirm the method is called

        # Clear any previous winner indications
        self.canvas.delete("winner")

        if not winners:
            print("No winners to display.")  # If there are no winners, we should not proceed
            return

        for winner in winners:
            print("Winner's hand:", winner[1])  # Debugging statement to print the winning hand

            player_index = None
            for i, hand in enumerate(self.simulation.hands):
                full_hand = hand + self.simulation.community_cards
                print("Full hand for player", i+1, ":", full_hand)  # Debugging statement to print the full hand
                if all(winner_card in full_hand for winner_card in winner[1]):
                    player_index = i
                    break

            if player_index is None:
                print("Winner's hand not found in player hands.")  # Debugging statement
                continue  # If the winner's hand isn't found, skip to the next winner

            print("Player index:", player_index)  # Debugging statement to print player index

            x_offset = 20
            y_offset = 20 + player_index * (self.card_height + 15)  # Adjust y_offset for each player's cards

            # Draw highlight for the entire hand
            rect_id = self.canvas.create_rectangle(
                x_offset - 5, y_offset - 5,
                x_offset + self.card_width * 2 + 5,  # only two cards in a poker hand are unique to the player
                y_offset + self.card_height + 5,
                outline="gold",  # Use a more visible color
                width=3,
                tags="winner"
            )
            print(f"Created rectangle with ID {rect_id}")  # Debugging statement to confirm creation

            # Bring the winner indicator to the front
            self.canvas.tag_raise(rect_id)

            # Add text indicating the winner's hand rank
            for i, winner in enumerate(winners):
                player_number = player_index + 1 if player_index is not None else '?'
                text_id = self.canvas.create_text(
                    300,  # X position for the text; you may want to adjust this
                    350 + i * 20,  # Y position for the text; you may want to adjust this
                    text=f"Player {player_number} wins with a {winner[0].name}",
                    font=('Helvetica', 16),
                    fill="gold",  # Use a more visible color
                    tags="winner"
                )
                print(f"Created text with ID {text_id}")  # Debugging statement to confirm creation

                # Bring the text to the front
                self.canvas.tag_raise(text_id)

        # Force redraw/update of the canvas
        self.canvas.update_idletasks()
        self.update_canvas()  # Call this method if it's responsible for redrawing the canvas

         # Force redraw/update of the canvas
        self.canvas.update_idletasks()

        # Test with hard-coded values
        self.canvas.create_rectangle(50, 50, 100, 100, outline="blue", width=3)
        self.canvas.create_text(75, 75, text="Test", font=('Helvetica', 16), fill="blue")

        # Bring the winner tags to the top
        self.canvas.tag_raise("winner")

        self.update_canvas()  # Call this method if it's responsible for redrawing the canvas

        print("Winners displayed.")  # Debugging statement to confirm the method completed



    def run(self):
        self.root.mainloop()
