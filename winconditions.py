from loguru import logger
from enums import PLAYER1_ID, PLAYER2_ID, Winner
from data import update_deck_data, save_deck_data, load_deck_data


class WinConditions:
    def __init__(self, locations, players):
        self.locations = locations
        self.players = players

    def determine_winner(self) -> int:
        player1_total_power = sum(
            location.powers[PLAYER1_ID] for location in self.locations
        )
        player2_total_power = sum(
            location.powers[PLAYER2_ID] for location in self.locations
        )
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

    def declare_winner(self):
        decks_data = load_deck_data("decks_data.json")
        total_power_player1 = sum(
            location.powers[PLAYER1_ID] for location in self.locations
        )
        total_power_player2 = sum(
            location.powers[PLAYER2_ID] for location in self.locations
        )

        winner = self.determine_winner()
        if winner == Winner.PLAYER1.value:
            logger.info("Player 1 Wins!")
            update_deck_data(
                self.players[0].starting_deck, "win", total_power_player1, decks_data
            )
            update_deck_data(
                self.players[1].starting_deck, "loss", total_power_player2, decks_data
            )

        elif winner == Winner.PLAYER2.value:
            logger.info("Player 2 Wins!")
            update_deck_data(
                self.players[0].starting_deck, "loss", total_power_player1, decks_data
            )
            update_deck_data(
                self.players[1].starting_deck, "win", total_power_player2, decks_data
            )
        else:
            logger.info("It's a draw!")
            update_deck_data(
                self.players[0].starting_deck, "draw", total_power_player1, decks_data
            )
            update_deck_data(
                self.players[1].starting_deck, "draw", total_power_player2, decks_data
            )

        save_deck_data(decks_data, "decks_data.json")
