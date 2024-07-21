from loguru import logger

from enums import PLAYER1_ID, PLAYER2_ID


class Displayer:
    def __init__(self, players, locations):
        self.players = players
        self.locations = locations

    def display_game_state(self):
        self.display_deck_and_hands()

        logger.debug("Cards at each location:")

        player1_cards_by_location = []
        player2_cards_by_location = []

        for location in self.locations:
            player1_power = location.powers[PLAYER1_ID]
            player2_power = location.powers[PLAYER2_ID]
            player1_cards = [
                f"{card.name} ({card.power})"
                for card in location.cards
                if card.owner_id == PLAYER1_ID
            ]
            player2_cards = [
                f"{card.name} ({card.power})"
                for card in location.cards
                if card.owner_id == PLAYER2_ID
            ]

            max_cards = max(len(player1_cards), len(player2_cards))
            player1_cards += [""] * (max_cards - len(player1_cards))
            player2_cards += [""] * (max_cards - len(player2_cards))

            if location.revealed:
                logger.debug(
                    f"{location.name} - Position {location.position} - {location.effect_description}"
                )
            else:
                logger.debug(f"Unrevealed Location")
            logger.debug(f"Player 1: {player1_cards}")
            logger.debug(f"Player 2: {player2_cards}")

            loc_winner = location.determine_winner()
            if loc_winner == 0:
                logger.debug(f"Player 1 wins this location")
            elif loc_winner == 1:
                logger.debug(f"Player 2 wins this location")

            logger.debug(
                f"Total power at this location: Player1: {location.powers[PLAYER1_ID]}"
            )
            logger.debug(
                f"Total power at this location: Player2: {location.powers[PLAYER2_ID]}"
            )

            player1_cards_by_location.append(
                player1_cards + [f"Player 1 Power: {player1_power}"]
            )
            player2_cards_by_location.append(
                player2_cards + [f"Player 2 Power: {player2_power}"]
            )

    def display_deck_and_hands(self):
        # Display decks and hands of both players
        for player_id in PLAYER1_ID, PLAYER2_ID:
            deck = [
                f"{card.name} ({card.power})" for card in self.players[player_id].deck
            ]
            logger.debug(f"Player {player_id} Deck: {deck}")
            hand = [
                f"{card.name} ({card.power})" for card in self.players[player_id].hand
            ]
            logger.debug(f"Player {player_id} Hand: {hand}")
