import unittest
import cards
import factories
from card import Card
from game import Game
from loguru import logger

class TestCards(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.player = self.game.players[0]
        self.all_cards = factories.generate_all_cards()

    def test_abomination(self):
        abo = cards.Abomination()
        assert abo.name == "Abomination"
        assert abo.energy_cost == 5
        assert abo.power == 9
        assert abo.base_power == 9
        assert abo.ability_description == "No Ability"
        assert abo.owner == None


    def test_cyclops(self):
        cyc = cards.Cyclops()
        assert cyc.name == "Cyclops"
        assert cyc.energy_cost == 3
        assert cyc.power == 4
        assert cyc.base_power == 4
        assert cyc.ability_description == "No Ability"

    def test_Medusa(self):

        # Create a Medusa card
        medusa = Card()
        location_id = 1
        for card in self.all_cards:
            if card.name == "Medusa":
                medusa = card
        medusa.energy_cost = 1

        # Add Medusa to player's hand
        self.player.hand = []
        self.player.hand.append(medusa)

        self.game.play_card(medusa, self.player.player_id, location_id)
        self.game.reveal_cards(self.player.player_id)

        # Get the played Medusa card from the location
        played_medusa = None
        for card in self.game.locations[location_id].cards:
            if card.name == "Medusa":
                played_medusa = card

        # Check the power of the played Medusa card 
        self.assertEqual(played_medusa.power, 4)

    def test_Sentinel(self):
        # Create a Sentinel card
        sentinel = Card()
        location_id = 0
        for card in self.all_cards:
            if card.name == "Sentinel":
                sentinel = card
        sentinel.energy_cost = 1

        # Add Sentinel to player's hand
        self.player.hand = []
        self.player.hand.append(sentinel)
        logger.debug(f"Player {self.player.player_id+1} hand: {self.player.hand}")

        self.game.play_card(sentinel, self.player.player_id, location_id)
        self.game.reveal_cards(self.player.player_id)

        logger.debug(f"Player {self.player.player_id+1} hand: {self.player.hand}")

        # Check that player has 1 Sentinel card in hand        
        self.assertEqual(len(self.player.hand), 1)
        self.assertEqual(self.player.hand[0].name, "Sentinel")