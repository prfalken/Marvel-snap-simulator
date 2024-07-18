import random
import copy
from location import Location, generate_all_locations
from ai import AIPlayer
from data import update_deck_data, save_deck_data, load_deck_data, get_average_power
from factories import generate_all_cards

from loguru import logger

from enum import Enum

class Winner(Enum):
    PLAYER1 = 0
    PLAYER2 = 1
    DRAW = 2

class PlayerIDs(Enum):
    PLAYER1 = 0
    PLAYER2 = 1

class Game:
    def __init__(self):
        self.current_turn = 1
        self.all_cards = generate_all_cards()
        self.all_locations = generate_all_locations()
        self.players = [AIPlayer(self, 0, copy.deepcopy(self.all_cards)), AIPlayer(self, 1, copy.deepcopy(self.all_cards))]
        self.locations = [Location("Location 1", []), Location("Location 2", []), Location("Location 3", [])]
        self.current_turn = 0
        self.current_location = 0
        self.prepare_game()
        self.winner=2

    def play_card(self, card, player_id, location_number):
        player = self.players[player_id]
        location = self.locations[location_number]
        card_copy = copy.deepcopy(card)
        card_copy.owner = player_id
        card_copy.turn_played = self.current_turn
        card_copy.location = location_number

        # Ensuring the location does not already have 4 cards from the player.
        if sum(1 for card in location.cards if card.owner == player_id) >= 4:
            logger.debug(f"Player {player_id+1} cannot play {card.name} at this location. It already has 4 cards from the player.")
            return

        if card.energy_cost <= player.energy:
            card_copy.owner = player_id
            card_copy.location = location_number
            location.cards.append(card_copy)
            logger.debug(f"Card played by player {player_id+1}: {card_copy}")

            if player_id == PlayerIDs.PLAYER1.value:
                location.player1_played_card = True
            else:
                location.player2_played_card = True

            player.hand.remove(card)
            player.played_cards.append(card_copy)

            player.energy -= card.energy_cost

            # Update the player's turn_energy_spent
            player.turn_energy_spent += card.energy_cost

        # Check for Hawkeye cards and apply the effect if necessary
            hawkeye_cards = [c for c in location.cards if c.name == "Hawkeye" and c.turn_played == self.current_turn - 1 and not c.hawkeye_effect_applied and c.location == location_number]
            if hawkeye_cards:
                for hawkeye_card in hawkeye_cards:
                    last_played_card = location.cards[-1]
                    if last_played_card.owner == hawkeye_card.owner and last_played_card.turn_played == self.current_turn:
                        hawkeye_card.power += 2  # Apply the effect
                        hawkeye_card.hawkeye_effect_applied = True  # Set the flag after applying the effect
        else:
            logger.debug(f"Player {player_id} cannot play {card.name} yet. It costs more energy than the current turn.")
            return

    def reveal_location(self):
        if self.current_location >= len(self.locations):
            return

        location = self.locations[self.current_location]
        logger.debug(f"Location revealed: {location}")
        location.revealed = True

        self.current_location += 1
        location.apply_location_effect(self)

    def generate_locations(self):
        return random.sample(self.all_locations, 3)

    def prepare_game(self):
        self.locations = self.generate_locations()
        self.reveal_location()

    def play_turn(self):
        for player_id in PlayerIDs:
            player_id = player_id.value
            player = self.players[player_id]
            player.played_cards = []
            player.played_card_locations = []

            chosen_card_indices, location_indices = player.choose_card_and_location()

            if chosen_card_indices is not None and location_indices is not None:
                for card_index, location_index in zip(chosen_card_indices, location_indices):
                    card = player.hand[card_index]
                    if card.energy_cost <= player.energy:
                        self.play_card(card, player_id, location_index)
                        player.played_cards.append(card)
                        player.played_card_locations.append(location_index)
                    else:
                        logger.debug(f"{player_id+1} cannot play {card.name} yet. It costs more energy than the current turn.")
                        break
            else:
                break

        # Determine the order in which players reveal cards
        player1_wins = 0
        player2_wins = 0
        for location in self.locations:
            if location.calculate_total_power(0) > location.calculate_total_power(1):
                player1_wins += 1
            elif location.calculate_total_power(0) < location.calculate_total_power(1):
                player2_wins += 1

        if player1_wins > player2_wins:
            reveal_order = [0, 1]
        elif player1_wins < player2_wins:
            reveal_order = [1, 0]
        else:
            player1_total_power = sum(location.calculate_total_power(0) for location in self.locations)
            player2_total_power = sum(location.calculate_total_power(1) for location in self.locations)
            if player1_total_power >= player2_total_power:
                reveal_order = [0, 1]
            else:
                reveal_order = [1, 0]

        # Reveal cards and apply card and location effects in the determined order
        for player_id in reveal_order:
            self.reveal_cards(player_id)

    def reveal_cards(self, player_id):
        player = self.players[player_id]
        if player.played_cards:
            for card in player.played_cards:
                if card.location is not None:
                    location = self.locations[card.location]
                    location_card = next((c for c in location.cards if c.owner == card.owner and c.name == card.name and c.location == card.location), None)
                    if card.ability is not None and card.ability.ability_type == "On Reveal":
                        power_bonus = card.ability.effect(card, self, player_id, location)
                        if power_bonus is not None and power_bonus > 0:
                            card.power += power_bonus
                            # Update the location card's power value as well
                            if location_card is not None:
                                location_card.power = card.power  # Update the power of the card in location.cards
                            logger.debug("Card: ", card.name, "Has increased from ", card.base_power, "to ", card.power)

    def apply_ongoing_abilities(self):
        for player_id in PlayerIDs:
            player_id = player_id.value
            for location in self.locations:
                for card in location.cards:
                    if card.owner == player_id and card.ability is not None and card.ability.ability_type == "Ongoing":
                        card.ability.effect(card, self, player_id, location)
            self.apply_location_effects(player_id)


    def apply_location_effects(self, player_id):
        player = self.players[player_id]
        for location_index, location in enumerate(self.locations):
            if location.effect and location.revealed:
                for card in location.cards:
                    if card.owner == player_id and not card.location_effect_applied:
                        location.effect(card, player, location_index)  # Pass location_index instead of location
                        card.location_effect_applied = True  # Set the flag after applying the effect

    def end_of_turn(self):        
        # Reset energy for each player according to the current turn
        for player in self.players:
            player.energy = self.current_turn + 1
            player.turn_energy_spent = 0

        # Reset the cards_this_turn list for each location
        for location in self.locations:
            location.player1_played_card = False
            location.player2_played_card = False

        for player in self.players:
            player.draw_card()

        # Apply end of turn effects for each location
        for i, location in enumerate(self.locations):
            if location.end_of_turn_effect:
                location.end_of_turn_effect(i, self, self.current_turn)

    def display_game_state(self):
        print("\nCards at each location:")

        player1_cards_by_location = []
        player2_cards_by_location = []

        for location in self.locations:
            player1_power = location.calculate_total_power(0)
            player2_power = location.calculate_total_power(1)
            player1_cards = [f"{card.name} ({card.power})" for card in location.cards if card.owner == 0]
            player2_cards = [f"{card.name} ({card.power})" for card in location.cards if card.owner == 1]

            max_cards = max(len(player1_cards), len(player2_cards))
            player1_cards += [''] * (max_cards - len(player1_cards))
            player2_cards += [''] * (max_cards - len(player2_cards))

            if location.revealed:
                print(f"\n{location.name} - {location.effect_description}")
            else:
                print(f"\nUnrevealed Location")
            print(f"Player 1: {player1_cards}")
            print(f"Player 2: {player2_cards}")
            loc_winner = location.determine_winner()
            if loc_winner == 0:
                print(f"Player 1 wins this location")
            elif loc_winner == 1:
                print(f"Player 2 wins this location")

            player1_cards_by_location.append(player1_cards + [f"Player 1 Power: {player1_power}"])
            player2_cards_by_location.append(player2_cards + [f"Player 2 Power: {player2_power}"])

        max_rows = max(len(cards) for cards in player1_cards_by_location + player2_cards_by_location)
    
        # Display decks and hands of both players
        print("\nPlayer 1 deck and hand:")
        print("Deck:", [f"{card.name} ({card.power})" for card in self.players[0].deck])
        print("Hand:", [f"{card.name} ({card.power})" for card in self.players[0].hand])
        print("\n")
        print("Player 2 deck and hand:")
        print("Deck:", [f"{card.name} ({card.power})" for card in self.players[1].deck])
        print("Hand:", [f"{card.name} ({card.power})" for card in self.players[1].hand])
        print("\n")


    def determine_winner(self):
        player1_score = sum(location.calculate_total_power(0) for location in self.locations)
        player2_score = sum(location.calculate_total_power(1) for location in self.locations)
        logger.debug(f"Player 1 had a total power of {player1_score}")
        logger.debug(f"Player 2 had a total power of {player2_score}")
        player1_wins = 0
        player2_wins = 0
        for location in self.locations:
            if location.calculate_total_power(0) > location.calculate_total_power(1):
                player1_wins += 1
            elif location.calculate_total_power(0) < location.calculate_total_power(1):
                player2_wins += 1

        logger.debug(f"Total won locations for Player 1: {player1_wins}")
        logger.debug(f"Total won locations for Player 2: {player2_wins}")

        decks_data = load_deck_data('decks_data.json')
        if player1_wins > player2_wins:
            logger.debug("Player 1 Wins!")
            update_deck_data(self.players[0].starting_deck, "win", player1_score, decks_data)
            update_deck_data(self.players[1].starting_deck, "loss", player2_score, decks_data)

        elif player1_wins < player2_wins:
            logger.debug("Player 2 Wins!")
            update_deck_data(self.players[0].starting_deck, "loss", player1_score, decks_data)
            update_deck_data(self.players[1].starting_deck, "win", player2_score, decks_data)

        save_deck_data(decks_data, 'decks_data.json')

        if player1_wins > player2_wins:
            self.winner = 0
        elif player2_wins > player1_wins:
            self.winner = 1
        elif player1_score > player2_score:
            self.winner = 0        
        elif player2_score > player1_score:
            self.winner = 1
        else:
            self.winner = 2

        logger.info(f"Player {self.winner + 1} wins!")

    def play_game(self):
        for turn in range(6):  # Loop through the 6 turns
            self.current_turn = turn + 1
            logger.info(f"Turn {self.current_turn}")
            if 4 > self.current_turn > 1:
                self.reveal_location()
            self.play_turn()
            self.apply_ongoing_abilities()
            self.end_of_turn()
            self.display_game_state()

        self.determine_winner()

