import unittest
from game import Game
from turn import Turn
from cards import Card
from enums import PLAYER1_ID, PLAYER2_ID
from unittest.mock import MagicMock, call


class TestTurn(unittest.TestCase):

    def test_play_card(self):
        game = Game()
        turn = Turn(1, game)

        card = Card("Card 1", 1, 1)
        player_id = 0
        location_number = 0
        player = game.players[player_id]
        player.hand.append(card)

        # Test playing a card with sufficient energy
        turn.play_card(card, player_id, location_number)
        self.assertEqual(len(game.locations[location_number].cards), 1)
        self.assertEqual(player.energy, 0)

        # Test playing a card with insufficient energy
        card2 = Card("Card 2", 10)
        player.hand.append(card2)
        turn.play_card(card2, player_id, location_number)
        self.assertEqual(len(game.locations[location_number].cards), 1)
        self.assertEqual(game.players[player_id].energy, 0)

    def test_reveal_cards(self):
        game = Game()
        turn = Turn(1, game)
        card = Card("Card 1", 1, 1)
        player = game.players[PLAYER1_ID]
        player.hand.append(card)
        player.played_cards.append(card)
        card.location_id = 0
        card.owner_id = PLAYER1_ID
        location = game.locations[0]
        location.cards.append(card)
        turn.reveal_cards(PLAYER1_ID)
        self.assertTrue(card.revealed)

    def test_play_turn(self):
        game = Game()
        turn = Turn(1, game)
        game.players[PLAYER1_ID].hand = [Card("Card 1", 1, 1)]
        game.players[PLAYER2_ID].hand = [Card("Card 2", 1, 100)]
        turn.reveal_cards = MagicMock()
        turn.play_turn()
        turn.reveal_cards.assert_has_calls([call(1), call(0)])

    def test_end_of_turn_reset(self):
        game = Game()
        turn = Turn(1, game)
        turn.end_of_turn()

        # Assert that player's energy is reset
        self.assertEqual(turn.game.players[0].energy, 2)
        self.assertEqual(turn.game.players[1].energy, 2)

        # Assert that location's player played card flags are reset
        self.assertFalse(game.locations[0].player1_played_card)
        self.assertFalse(game.locations[0].player2_played_card)
        self.assertFalse(game.locations[1].player1_played_card)
        self.assertFalse(game.locations[1].player2_played_card)
        self.assertFalse(game.locations[2].player1_played_card)
        self.assertFalse(game.locations[2].player2_played_card)

        # Add assertions for the expected behavior of the end_of_turn method

    def test_end_of_turn(self):
        game = Game()
        turn = Turn(1, game)
        turn.end_of_turn()
        # Add assertions for the expected behavior of the end_of_turn method)

    def test_play_card_insufficient_energy(self):
        game = Game()
        turn = Turn(1, game)
        card = Card("Card 1", 5)
        player_id = 0
        location_number = 0

        # Set player's energy to 0
        game.players[player_id].energy = 0

        # Test playing a card with insufficient energy
        turn.play_card(card, player_id, location_number)
        self.assertEqual(len(game.locations[location_number].cards), 0)
        self.assertEqual(game.players[player_id].energy, 0)

    def test_play_turn_no_cards(self):
        game = Game()
        turn = Turn(1, game)
        turn.play_turn()

        # Add assertions for the expected behavior when players have no cards to play

    def test_reveal_cards_no_cards(self):
        game = Game()
        turn = Turn(1, game)
        turn.reveal_cards(1)

        # Add assertions for the expected behavior when player has no cards to reveal