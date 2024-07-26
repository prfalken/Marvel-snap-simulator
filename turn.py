from enums import PLAYER1_ID, PLAYER2_ID, Winner
from loguru import logger
import copy
from winconditions import WinConditions


class Turn:
    def __init__(self, turn_id, game):
        self.turn_id = turn_id
        self.game = game

    def play_card(self, card, player_id, location_id):
        player = self.game.players[player_id]
        location = self.game.locations[location_id]
        card_copy = copy.deepcopy(card)
        card_copy.owner_id = player_id
        card_copy.turn_played = self.turn_id
        card_copy.location_id = location_id

        # Ensuring the location does not already have 4 cards from the player.
        if sum(1 for card in location.cards if card.owner_id == player_id) >= 4:
            logger.debug(
                f"Player {player_id+1} cannot play {card.name} at this location. It already has 4 cards from the player."
            )
            return

        if card.energy_cost <= player.energy:
            card_copy.owner_id = player_id
            card_copy.location_id = location_id
            location.cards.append(card_copy)
            logger.info(
                f"Card played by player {player_id+1}: {card_copy} on Location position {location_id}"
            )

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
            logger.debug(
                f"Player {player_id} cannot play {card.name} yet. It costs more energy than the current turn."
            )
            return

    def reveal_cards(self, player_id: int):
        player = self.game.players[player_id]
        if player.played_cards:
            for card in player.played_cards:
                if card.location_id is not None:
                    location = self.game.locations[card.location_id]
                    location_card = next(
                        (
                            c
                            for c in location.cards
                            if c.owner_id == card.owner_id
                            and c.name == card.name
                            and c.location_id == card.location_id
                        ),
                        None,
                    )
                    self.game = location_card.reveal(self.game)
                    location.powers[player_id] += card.power
                    location_card.revealed = True

    def play_turn(self):
        for player_id in PLAYER1_ID, PLAYER2_ID:
            player = self.game.players[player_id]
            player.played_cards = []
            player.played_card_locations = []

            chosen_card_index, location_index = player.choose_card_and_location()

            if chosen_card_index is not None and location_index is not None:
                for card_index, location_id in zip(chosen_card_index, location_index):
                    card = player.hand[card_index]
                    self.play_card(card, player_id, location_id)
                    player.played_cards.append(card)
                    player.played_card_locations.append(location_id)
            else:
                break

        # Determine the order in which players reveal cards
        win_conditions = WinConditions(self.game.locations, self.game.players)
        winner = win_conditions.determine_winner()

        if winner == Winner.PLAYER1.value:
            self.reveal_order = [PLAYER1_ID, PLAYER2_ID]
        elif winner == Winner.PLAYER2.value:
            self.reveal_order = [PLAYER2_ID, PLAYER1_ID]

        # Reveal cards and apply card and location effects in the determined order
        # Also apply any effects that trigger on any card reveal (e.g. Bishop)
        for player_id in self.reveal_order:
            self.reveal_cards(player_id)
            for location in self.game.locations:
                for card in location.cards:
                    if card.owner_id == player_id:
                        self.game, card = card.on_any_card_reveal_effect(
                            self.game, card
                        )

    def end_of_turn(self):
        # Reset energy for each player according to the current turn
        for player in self.game.players:
            player.energy = self.turn_id
            player.turn_energy_spent = 0

        # Reset the cards_this_turn list for each location
        for location in self.game.locations:
            location.player1_played_card = False
            location.player2_played_card = False

        for player in self.game.players:
            player.draw_card()

        # Apply end of turn effects for each location
        for i, location in enumerate(self.game.locations):
            if location.end_of_turn_effect:
                location.end_of_turn_effect(i, self.game, self.turn_id)

        for location in self.game.locations:
            for player_id in PLAYER1_ID, PLAYER2_ID:
                location.powers[player_id] = location.calculate_total_power(player_id)

        self.game.apply_ongoing_abilities()
