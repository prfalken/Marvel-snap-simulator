from card import Card
from loguru import logger
from location import Location
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

class Hulk(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Hulk"
        self.energy_cost = 6
        self.power = 12
        self.base_power = 12
        self.ability_description = "No Ability"

class Hawkeye(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Hawkeye"
        self.energy_cost = 1
        self.power = 1
        self.base_power = 1
        self.ability_description = "On Reveal: If you play a card here next turn, +2 Power."
        self.number_of_cards_here = 0
        self.hawkeye_triggered = False

    def reveal(self, game: 'Game', owner: 'AIPlayer', location: Location):
        if not self.revealed:
            self.revealed = True
            self.turn_played = game.current_turn
            self.number_of_cards_here = len(location.cards)
            return game, owner, location

        if self.revealed and not self.hawkeye_triggered and game.current_turn == self.turn_played + 1:
            if len(location.cards) > self.number_of_cards_here:
                self.power += 2
                logger.debug(f"{self.name} was played last turn. Power +2")
                self.hawkeye_triggered = True
                return game, owner, location
            
        return game, owner, location

class IronMan(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Iron Man"
        self.energy_cost = 5
        self.power = 0
        self.base_power = 0
        self.ability_description = "Ongoing: Your total Power is doubled at this Location."

    def ongoing(self, game: 'Game', owner: 'AIPlayer', location: Location):
        total_power = location.calculate_total_power(owner.player_id)
        location.powers[owner.player_id] = total_power * 2
        return game, owner, location

class Medusa(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Medusa"
        self.energy_cost = 2
        self.power = 2
        self.base_power = 2
        self.ability_description = "On Reveal: If this is at the middle Location, +2 Power."

    def reveal(self, game: 'Game', owner: 'AIPlayer', location: Location):
        if self.location == 1:
            logger.debug(f"{self.name} is at the middle location. Power +2")
            self.power += 2
        return game, owner, location

class MistyKnight(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Misty Knight"
        self.energy_cost = 1
        self.power = 2
        self.base_power = 2
        self.ability_description = "No Ability"

class Sentinel(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Sentinel"
        self.energy_cost = 2
        self.power = 3
        self.base_power = 3
        self.ability_description = "On Reveal: Add another Sentinel to your hand."

    def reveal(self, game, owner: 'AIPlayer', location):
        new_sentinel = Sentinel()
        owner.hand.append(new_sentinel)
        logger.debug(f"Player {owner.player_id+1} added another Sentinel to their hand.")
        return game, owner, location

class Shocker(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Shocker"
        self.energy_cost = 2
        self.power = 3
        self.base_power = 3
        self.ability_description = "No Ability"

class StarLord(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Star Lord"
        self.energy_cost = 2
        self.power = 2
        self.base_power = 2
        self.ability_description = "On Reveal: If your opponent played a card here this turn, +3 Power."

    def reveal(self, game: 'Game', owner: 'AIPlayer', location: Location):
        opponent = 1 if owner.player_id == 0 else 0
        for c in location.cards:
            if any(c.owner == opponent and c.turn_played == game.current_turn for c in location.cards):
                self.power += 3
                logger.debug(f"Star Lord : A card was played by the opponent this turn. Power +3")
                return game, owner, location
        return game, owner, location

class ThePunisher(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "The Punisher"
        self.energy_cost = 3
        self.power = 2
        self.base_power = 2
        self.ability_description = "Ongoing: +1 Power for each opposing card at this Location."

    def ongoing(self, game: 'Game', owner: 'AIPlayer', location: Location):
        location = game.locations[self.location]
        enemy_card_count = sum(1 for c in location.cards if c.owner != owner and c != self)  # Include the current card
        bonus_power = 1 * enemy_card_count
        self.power = self.base_power + bonus_power
        logger.debug("The Punisher's power is now: " + str(self.power))
        return game, owner, location

class TheThing(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "The Thing"
        self.energy_cost = 4
        self.power = 6
        self.base_power = 6
        self.ability_description = "No Ability"