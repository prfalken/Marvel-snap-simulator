import random
import copy
from location import Location, generate_all_locations
from ai import AIPlayer
from turn import Turn
from winconditions import WinConditions
from factories import generate_all_cards
from display import Displayer
from enums import PLAYER1_ID, PLAYER2_ID

from loguru import logger


class Game:
    def __init__(self):
        self.all_cards = generate_all_cards()
        self.all_locations = generate_all_locations()
        self.players = [
            AIPlayer(self, 0, copy.deepcopy(self.all_cards)),
            AIPlayer(self, 1, copy.deepcopy(self.all_cards)),
        ]
        self.locations = [
            Location("Location 1", [], position=0),
            Location("Location 2", [], position=1),
            Location("Location 3", [], position=2),
        ]
        self.turn = Turn(1, self)
        self.current_turn = 0
        self.current_location = 0
        self.prepare_game()
        self.reveal_order = [PLAYER1_ID, PLAYER2_ID]
        random.shuffle(self.reveal_order)

        self.displayer = Displayer(self.players, self.locations)

    def reveal_location(self):
        if self.current_location >= len(self.locations):
            return

        location = self.locations[self.current_location]
        logger.debug(
            f"Location revealed: {location} at position {self.current_location}"
        )
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

    def apply_ongoing_abilities(self):
        for player_id in PLAYER1_ID, PLAYER2_ID:
            for location in self.locations:
                for card in location.cards:
                    self = card.ongoing(self)
            self.apply_location_effects(player_id)

    def apply_location_effects(self, player_id):
        player = self.players[player_id]
        for location_id, location in enumerate(self.locations):
            if location.effect and location.revealed:
                for card in location.cards:
                    if card.owner_id == player_id and not card.location_effect_applied:
                        location.effect(
                            card, player, location_id
                        )  # Pass location_id instead of location
                        card.location_effect_applied = (
                            True  # Set the flag after applying the effect
                        )

    def play_game(self):
        for turn_id in range(6):  # Loop through the 6 turns
            self.current_turn = turn_id
            self.turn = Turn(turn_id, self)
            logger.info(f"Turn {self.current_turn}")
            if 4 > self.current_turn > 1:
                self.reveal_location()
            self.turn.play_turn()
            self.turn.end_of_turn()
            self.displayer.display_game_state()

        WinConditions(self.locations, self.players).declare_winner()
