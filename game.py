import random
import copy
from location import Location, generate_all_locations
from ai import AIPlayer
from data import update_deck_data, save_deck_data, load_deck_data, get_average_power
from factories import generate_all_cards
from enums import PLAYER1_ID, PLAYER2_ID, Winner

from loguru import logger

class Game:
    def __init__(self):
        self.current_turn = 1
        self.all_cards = generate_all_cards()
        self.all_locations = generate_all_locations()
        self.players = [AIPlayer(self, 0, copy.deepcopy(self.all_cards)), AIPlayer(self, 1, copy.deepcopy(self.all_cards))]
        self.locations = [Location("Location 1", [], position=0), Location("Location 2", [], position=1), Location("Location 3", [], position=2)]
        self.current_turn = 0
        self.current_location = 0
        self.prepare_game()
        self.reveal_order = [PLAYER1_ID, PLAYER2_ID]
        random.shuffle(self.reveal_order)


    def play_card(self, card, player_id, location_id):
        player = self.players[player_id]
        location = self.locations[location_id]
        card_copy = copy.deepcopy(card)
        card_copy.owner = player_id
        card_copy.turn_played = self.current_turn
        card_copy.location = location_id

        # Ensuring the location does not already have 4 cards from the player.
        if sum(1 for card in location.cards if card.owner == player_id) >= 4:
            logger.debug(f"Player {player_id+1} cannot play {card.name} at this location. It already has 4 cards from the player.")
            return

        if card.energy_cost <= player.energy:
            card_copy.owner = player_id
            card_copy.location = location_id
            location.cards.append(card_copy)
            logger.debug(f"Card played by player {player_id+1}: {card_copy} on Location position {location_id}")

            if player_id == PLAYER1_ID:
                location.player1_played_card = True
            else:
                location.player2_played_card = True

            player.hand.remove(card)
            player.played_cards.append(card_copy)

            player.energy -= card.energy_cost

            # Update the player's turn_energy_spent
            player.turn_energy_spent += card.energy_cost

        else:
            logger.debug(f"Player {player_id} cannot play {card.name} yet. It costs more energy than the current turn.")
            return

    def reveal_location(self):
        if self.current_location >= len(self.locations):
            return

        location = self.locations[self.current_location]
        logger.debug(f"Location revealed: {location} at position {self.current_location}")
        location.revealed = True
        location.position = self.current_location
        self.locations[self.current_location] = location
        self.current_location += 1
        location.apply_location_effect(self)

    def generate_locations(self):
        return random.sample(self.all_locations, 3)

    def prepare_game(self):
        self.locations = self.generate_locations()
        self.reveal_location()
        for location in self.locations:
            location.position = self.locations.index(location)

    def determine_winner(self) -> int:
        player1_total_power = sum(location.powers[PLAYER1_ID] for location in self.locations)
        player2_total_power = sum(location.powers[PLAYER2_ID] for location in self.locations)
        logger.info(f"Player 1 had a total power of {player1_total_power}")
        logger.info(f"Player 2 had a total power of {player2_total_power}")

        player1_wins = 0
        player2_wins = 0
        for location in self.locations:
            if location.powers[PLAYER1_ID] > location.powers[PLAYER2_ID]:
                player1_wins += 1
            elif location.powers[PLAYER2_ID] < location.powers[PLAYER2_ID]:
                player2_wins += 1

        logger.info(f"Total won locations for Player 1: {player1_wins}")
        logger.info(f"Total won locations for Player 2: {player2_wins}")

        if player1_wins > player2_wins:
            return Winner.PLAYER1.value
        elif player1_wins < player2_wins:
            return Winner.PLAYER2.value
        elif player1_wins == player2_wins:
            if player1_total_power > player2_total_power:
                return Winner.PLAYER1.value
            else:
                return Winner.PLAYER2.value
        
        return Winner.DRAW.value
            

    def play_turn(self):
        for player_id in PLAYER1_ID, PLAYER2_ID:
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
        winner = self.determine_winner()
        if winner == Winner.PLAYER1.value:
            self.reveal_order = [PLAYER1_ID, PLAYER2_ID]
        elif winner == Winner.PLAYER2.value:
            self.reveal_order = [PLAYER2_ID, PLAYER1_ID]

        # Reveal cards and apply card and location effects in the determined order
        for player_id in self.reveal_order:
            self.reveal_cards(player_id)

    def reveal_cards(self, player_id: int):
        player = self.players[player_id]
        if player.played_cards:
            for card in player.played_cards:
                if card.location is not None:
                    location = self.locations[card.location]
                    location_card = next((c for c in location.cards if c.owner == card.owner and c.name == card.name and c.location == card.location), None)
                    self, player, location = location_card.reveal(self, player, location)
                    if card.ability is not None and card.ability.ability_type == "On Reveal":
                        power_bonus = card.ability.effect(card, self, player_id, location)
                        if power_bonus is not None and power_bonus > 0:
                            card.power += power_bonus
                            # Update the location card's power value as well
                            if location_card is not None:
                                location_card.power = card.power  # Update the power of the card in location.cards
                                location.powers[player_id] += card.power # Update the total power of the location
                            logger.debug(f"Card {card.name} has increased from {card.base_power} to {card.power}")
                    card.revealed = True

    def apply_ongoing_abilities(self):
        for player_id in PLAYER1_ID, PLAYER2_ID:
            player_id = player_id
            player = self.players[player_id]
            for location in self.locations:
                for card in location.cards:
                    self, player, location = card.ongoing(self, player, location)
                    self.locations[location.position] = location
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

        for location in self.locations:
            for player_id in PLAYER1_ID, PLAYER2_ID:
                location.powers[player_id] = location.calculate_total_power(player_id)

        self.apply_ongoing_abilities()

    def display_game_state(self):
        self.display_deck_and_hands()

        logger.debug("Cards at each location:")

        player1_cards_by_location = []
        player2_cards_by_location = []

        for location in self.locations:
            player1_power = location.powers[PLAYER1_ID]
            player2_power = location.powers[PLAYER2_ID]
            player1_cards = [f"{card.name} ({card.power})" for card in location.cards if card.owner == 0]
            player2_cards = [f"{card.name} ({card.power})" for card in location.cards if card.owner == 1]

            max_cards = max(len(player1_cards), len(player2_cards))
            player1_cards += [''] * (max_cards - len(player1_cards))
            player2_cards += [''] * (max_cards - len(player2_cards))

            if location.revealed:
                logger.debug(f"{location.name} - Position {location.position} - {location.effect_description}")
            else:
                logger.debug(f"Unrevealed Location")
            logger.debug(f"Player 1: {player1_cards}")
            logger.debug(f"Player 2: {player2_cards}")

            loc_winner = location.determine_winner()
            if loc_winner == 0:
                logger.debug(f"Player 1 wins this location")
            elif loc_winner == 1:
                logger.debug(f"Player 2 wins this location")

            logger.debug(f"Total power at this location: Player1: {location.powers[PLAYER1_ID]}")
            logger.debug(f"Total power at this location: Player2: {location.powers[PLAYER2_ID]}")

            player1_cards_by_location.append(player1_cards + [f"Player 1 Power: {player1_power}"])
            player2_cards_by_location.append(player2_cards + [f"Player 2 Power: {player2_power}"])
    
    def display_deck_and_hands(self):
        # Display decks and hands of both players
        for player_id in PLAYER1_ID, PLAYER2_ID:
            deck = [f"{card.name} ({card.power})" for card in self.players[player_id].deck]
            logger.debug(f"Player {player_id} Deck: {deck}")
            hand = [f"{card.name} ({card.power})" for card in self.players[player_id].hand]
            logger.debug(f"Player {player_id} Hand: {hand}")


    def declare_winner(self):
        decks_data = load_deck_data('decks_data.json')
        total_power_player1 = sum(location.powers[PLAYER1_ID] for location in self.locations)
        total_power_player2 = sum(location.powers[PLAYER2_ID] for location in self.locations)

        winner = self.determine_winner()
        if winner == Winner.PLAYER1.value:
            logger.info("Player 1 Wins!")
            update_deck_data(self.players[0].starting_deck, "win", total_power_player1, decks_data)
            update_deck_data(self.players[1].starting_deck, "loss", total_power_player2, decks_data)

        elif winner == Winner.PLAYER2.value:
            logger.info("Player 2 Wins!")
            update_deck_data(self.players[0].starting_deck, "loss", total_power_player1, decks_data)
            update_deck_data(self.players[1].starting_deck, "win", total_power_player2, decks_data)
        else:
            logger.info("It's a draw!")
            update_deck_data(self.players[0].starting_deck, "draw", total_power_player1, decks_data)
            update_deck_data(self.players[1].starting_deck, "draw", total_power_player2, decks_data)

        save_deck_data(decks_data, 'decks_data.json')

    def play_game(self):
        for turn in range(6):  # Loop through the 6 turns
            self.current_turn = turn + 1
            logger.info(f"Turn {self.current_turn}")
            if 4 > self.current_turn > 1:
                self.reveal_location()
            self.play_turn()
            self.end_of_turn()
            self.display_game_state()

        self.declare_winner()

