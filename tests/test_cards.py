import unittest
import cards

class TestCards(unittest.TestCase):
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