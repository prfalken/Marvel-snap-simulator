import sys
import unittest
from unittest.mock import MagicMock, call
from loguru import logger

from game import Game
from cards import Card
from location import Location

from enums import PLAYER1_ID, PLAYER2_ID

logger.remove()
# logger.add(sys.stderr, level="INFO")


class TestGame(unittest.TestCase):

    def test_game(self):
        Game.prepare_game = MagicMock()
        game = Game()
        game.all_locations = [
            Location("Location 1", "Description 1"), 
            Location("Location 2", "Description 2"), 
            Location("Location 3", "Description 3"),
            ]

        player1_startswith = [
            Card("Card 1", 1, 200),
            Card("Card 2", 1, 1),
            Card("Card 3", 1, 1),
            ]
        player2_startswith = [
            Card("Card 2", 1, 100),
            Card("Card 2", 1, 100),
            Card("Card 3", 1, 100),
            ]
        player1 = game.players[0]
        player2 = game.players[1]
        player1.deck = player1_startswith
        player2.deck = player2_startswith
        player1.starting_deck = player1.deck
        player2.starting_deck = player2.deck
        player1.hand = player1_startswith
        player2.hand = player2_startswith
        game.play_game()


    def test_play_card(self):
        game = Game()
        card = Card("Card 1", 1, 1)
        player_id = 0
        location_number = 0
        player = game.players[player_id]
        player.hand.append(card)

        # Test playing a card with sufficient energy
        game.play_card(card, player_id, location_number)
        self.assertEqual(len(game.locations[location_number].cards), 1)
        self.assertEqual(player.energy, 0)

        # Test playing a card with insufficient energy
        card2 = Card("Card 2", 10)
        player.hand.append(card2)
        game.play_card(card2, player_id, location_number)
        self.assertEqual(len(game.locations[location_number].cards), 1)
        self.assertEqual(game.players[player_id].energy, 0)

    def test_reveal_location(self):
        game = Game()
        game.reveal_location()
        self.assertTrue(game.locations[0].revealed)

    def test_generate_locations(self):
        game = Game()
        locations = game.generate_locations()
        self.assertEqual(len(locations), 3)

    def test_play_turn(self):
        game = Game()
        game.players[PLAYER1_ID].hand = [Card("Card 1", 1, 1)]
        game.players[PLAYER2_ID].hand = [Card("Card 2", 1, 100)]
        game.reveal_cards = MagicMock()
        game.play_turn()
        game.reveal_cards.assert_has_calls([call(1), call(0)])

    def test_reveal_cards(self):
        game = Game()
        card = Card("Card 1", 1, 1)
        player = game.players[PLAYER1_ID]
        player.hand.append(card)
        player.played_cards.append(card)
        card.location = 0
        card.owner = PLAYER1_ID
        location = game.locations[0]
        location.cards.append(card)
        game.reveal_cards(PLAYER1_ID)
        self.assertTrue(card.revealed)

    def test_apply_ongoing_abilities(self):
        game = Game()
        game.apply_ongoing_abilities()
        # Add assertions for the expected behavior of the apply_ongoing_abilities method

    def test_apply_location_effects(self):
        game = Game()
        game.apply_location_effects(1)
        # Add assertions for the expected behavior of the apply_location_effects method

    def test_end_of_turn(self):
        game = Game()
        game.end_of_turn()
        # Add assertions for the expected behavior of the end_of_turn method

    def test_determine_winner(self):
        game = Game()
        game.determine_winner()
        # Add assertions for the expected behavior of the determine_winner method

    def test_play_game(self):
        game = Game()
        game.play_game()
        # Add assertions for the expected behavior of the play_game method

    # Additional tests

    def test_play_card_insufficient_energy(self):
        game = Game()
        card = Card("Card 1", 5)
        player_id = 0
        location_number = 0

        # Set player's energy to 0
        game.players[player_id].energy = 0

        # Test playing a card with insufficient energy
        game.play_card(card, player_id, location_number)
        self.assertEqual(len(game.locations[location_number].cards), 0)
        self.assertEqual(game.players[player_id].energy, 0)

    def test_reveal_location_multiple_times(self):
        game = Game()
        game.reveal_location()
        self.assertTrue(game.locations[0].revealed)

        game.reveal_location()
        self.assertTrue(game.locations[1].revealed)

        game.reveal_location()
        self.assertTrue(game.locations[2].revealed)

        # Additional assertion to ensure no more locations are revealed
        self.assertEqual(game.current_location, 3)

    def test_generate_locations_unique(self):
        game = Game()
        locations1 = game.generate_locations()
        locations2 = game.generate_locations()

        # Test that generated locations are unique
        self.assertNotEqual(locations1, locations2)

    def test_prepare_game_reset(self):
        game = Game()
        # Reset the game
        game.prepare_game()

        # Assert that locations are reset
        self.assertEqual(len(game.locations), 3)

        # Assert that player's played cards are reset
        self.assertEqual(len(game.players[0].played_cards), 0)
        self.assertEqual(len(game.players[1].played_cards), 0)

        # Assert that player's turn energy spent is reset
        self.assertEqual(game.players[0].turn_energy_spent, 0)
        self.assertEqual(game.players[1].turn_energy_spent, 0)

        # Assert that location's player played card flags are reset
        self.assertFalse(game.locations[0].player1_played_card)
        self.assertFalse(game.locations[0].player2_played_card)
        self.assertFalse(game.locations[1].player1_played_card)
        self.assertFalse(game.locations[1].player2_played_card)
        self.assertFalse(game.locations[2].player1_played_card)
        self.assertFalse(game.locations[2].player2_played_card)

    def test_play_turn_no_cards(self):
        game = Game()
        game.play_turn()

        # Add assertions for the expected behavior when players have no cards to play

    def test_reveal_cards_no_cards(self):
        game = Game()
        game.reveal_cards(1)

        # Add assertions for the expected behavior when player has no cards to reveal

    def test_apply_ongoing_abilities_no_abilities(self):
        game = Game()
        game.apply_ongoing_abilities()

        # Add assertions for the expected behavior when no ongoing abilities are present

    def test_apply_location_effects_no_effects(self):
        game = Game()
        game.apply_location_effects(1)

        # Add assertions for the expected behavior when no location effects are present

    def test_end_of_turn_reset(self):
        game = Game()
        game.end_of_turn()
        game.end_of_turn()

        # Assert that player's energy is reset
        self.assertEqual(game.players[0].energy, 1)
        self.assertEqual(game.players[1].energy, 1)

        # Assert that location's player played card flags are reset
        self.assertFalse(game.locations[0].player1_played_card)
        self.assertFalse(game.locations[0].player2_played_card)
        self.assertFalse(game.locations[1].player1_played_card)
        self.assertFalse(game.locations[1].player2_played_card)
        self.assertFalse(game.locations[2].player1_played_card)
        self.assertFalse(game.locations[2].player2_played_card)

        # Add assertions for the expected behavior of the end_of_turn method

    def test_determine_winner(self):
        game = Game()
        game.determine_winner()

        # Add assertions for the expected behavior of the determine_winner method

    def test_play_game(self):
        game = Game()
        game.play_game()

        # Add assertions for the expected behavior of the play_game method