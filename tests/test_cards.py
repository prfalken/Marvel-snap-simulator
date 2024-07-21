import sys
import unittest
import cards
import factories
from card import Card
from game import Game
from enums import PLAYER1_ID, PLAYER2_ID
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="DEBUG")

class TestCards(unittest.TestCase):

    def setUp(self):
        self.all_cards = factories.generate_all_cards()
        self.game = Game()

        self.game.players[1].hand = []
        self.game.players[1].deck = []
        self.game.players[0].deck = []
        self.player = self.game.players[PLAYER1_ID]

    def clear_locations(self):
        for location in self.game.locations:
            location.cards = []

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

    def test_hawkeye_triggered(self):
        self.clear_locations()

        # Create a Hawkeye card
        hawkeye = Card()
        location_id = 0
        for card in self.all_cards:
            if card.name == "Hawkeye":
                hawkeye = card
        hawkeye.energy_cost = 1

        # Add Hawkeye to player's hand
        self.player.hand = []
        self.player.hand.append(hawkeye)

        self.game.play_card(hawkeye, self.player.player_id, location_id)
        self.game.reveal_cards(self.player.player_id)

        self.game.current_turn += 1
        self.player.energy = 1

        some_card = Card("Some Card", 1, 1, "No Ability")
        some_card.energy_cost = 1
        self.player.hand.append(some_card)
        self.game.play_card(some_card, self.player.player_id, location_id)
        self.game.reveal_cards(self.player.player_id)

        # Get the played Hawkeye card from the location
        played_hawkeye = None
        for card in self.game.locations[location_id].cards:
            if card.name == "Hawkeye":
                played_hawkeye = card

        self.assertEqual(played_hawkeye.power, 3)
 
    def test_hawkeye_not_triggered(self):
        self.clear_locations()

        # Create a Hawkeye card
        hawkeye = Card()
        location_id = 0
        for card in self.all_cards:
            if card.name == "Hawkeye":
                hawkeye = card
        hawkeye.energy_cost = 1

        # Add Hawkeye to player's hand
        self.player.hand = []
        self.player.hand.append(hawkeye)

        self.game.play_card(hawkeye, self.player.player_id, location_id)
        self.game.reveal_cards(self.player.player_id)

        self.game.current_turn += 1
        self.player.energy = 1

        # play a card in another location - Hawkeye should not trigger
        some_card = Card("Some Card", 1, 1, "No Ability")
        some_card.energy_cost = 1
        self.player.hand.append(some_card)
        self.game.play_card(some_card, self.player.player_id, location_id + 1)
        self.game.reveal_cards(self.player.player_id)


        # Get the played Hawkeye card from the location
        played_hawkeye = None
        for card in self.game.locations[location_id].cards:
            if card.name == "Hawkeye":
                played_hawkeye = card

        self.assertEqual(played_hawkeye.power, 1)

    def test_hulk(self):
        hulk = cards.Hulk()
        assert hulk.name == "Hulk"
        assert hulk.energy_cost == 6
        assert hulk.power == 12
        assert hulk.base_power == 12
        assert hulk.ability_description == "No Ability"

    def test_ironman(self):
        self.clear_locations()

        # Create an Iron Man card
        ironman = Card()
        location_id = 0
        for card in self.all_cards:
            if card.name == "Iron Man":
                ironman = card
                break
        ironman.energy_cost = 1
        ironman.owner = self.player.player_id

        # Add Iron Man to player's hand
        self.player.hand = []
        self.player.hand.append(ironman)

        self.game.play_card(ironman, self.player.player_id, location_id)
        self.game.reveal_cards(self.player.player_id)

        self.game.current_turn += 1
        self.player.energy = 1

        # play a card in IronMan's location - should be doubled
        some_card = Card("Some Card", 1, 10, "No Ability")
        some_card.energy_cost = 1
        self.player.hand.append(some_card)
        self.game.play_card(some_card, self.player.player_id, location_id)
        self.game.reveal_cards(self.player.player_id)

        location = self.game.locations[location_id]

        self.game.apply_ongoing_abilities()

        self.assertEqual(location.powers[self.player.player_id], 20)


    def test_Medusa(self):
        self.clear_locations()

        # Create a Medusa card
        medusa = Card()
        location_id = 1
        for card in self.all_cards:
            if card.name == "Medusa":
                medusa = card
                break
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
        self.clear_locations()

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

    def test_starlord_triggered(self):
        self.clear_locations()

        # Create a Star Lord card
        starlord = cards.StarLord()
        location_id = 0
        starlord.energy_cost = 1

        # Add Star Lord to player's hand
        self.player.hand = []
        self.player.hand.append(starlord)

        self.game.play_card(starlord, self.player.player_id, location_id)

        some_card = Card("Some Card", 1, 1, "No Ability")
        some_card.energy_cost = 1
        player2 = self.game.players[PLAYER2_ID]
        player2.hand.append(some_card)
        self.game.play_card(some_card, player2.player_id, location_id)

        self.game.reveal_cards(self.player.player_id)

        # Get the played Star Lord card from the location
        played_starlord = None
        for card in self.game.locations[location_id].cards:
            if card.name == "Star Lord":
                played_starlord = card

        self.assertEqual(played_starlord.power, 5)

    def test_starlord_not_triggered(self):
        self.clear_locations()

        # Create a Star Lord card
        starlord = cards.StarLord()
        location_id = 0
        starlord.energy_cost = 1

        # Add Star Lord to player's hand
        self.player.hand = []
        self.player.hand.append(starlord)

        self.game.play_card(starlord, self.player.player_id, location_id)
        self.game.reveal_cards(self.player.player_id)

        # Get the played Star Lord card from the location
        played_starlord = None
        for card in self.game.locations[location_id].cards:
            if card.name == "Star Lord":
                played_starlord = card

        self.assertEqual(played_starlord.power, 2)
