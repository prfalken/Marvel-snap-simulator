from card import Card
from loguru import logger
from ai import AIPlayer
class Abomination(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Abomination"
        self.energy_cost = 5
        self.power = 9
        self.base_power = 9
        self.ability_description = "No Ability"

class Cyclops(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Cyclops"
        self.energy_cost = 3
        self.power = 4
        self.base_power = 4
        self.ability_description = "No Ability"


class Medusa(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Medusa"
        self.energy_cost = 2
        self.power = 2
        self.base_power = 2
        self.ability_description = "On Reveal: If this is at the middle Location, +2 Power."

    def reveal(self, game, owner: AIPlayer, location):
        if self.location == 1:
            logger.debug(f"{self.name} is at the middle location. Power +2")
            self.power += 2
        return game, owner, location
    
class Sentinel(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Sentinel"
        self.energy_cost = 2
        self.power = 3
        self.base_power = 3
        self.ability_description = "On Reveal: Add another Sentinel to your hand."

    def reveal(self, game, owner: AIPlayer, location):
        new_sentinel = Sentinel()
        owner.hand.append(new_sentinel)
        logger.debug(f"Player {owner.player_id+1} added another Sentinel to their hand.")
        return game, owner, location
