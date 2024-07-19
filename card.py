
class Card:
    def __init__(self, name=None, energy_cost=None, power=None, ability_description=None, ability=None):
        self.name = name
        self.game = None
        self.energy_cost = energy_cost
        self.power = power
        self.base_power = power
        self.ability_description = ability_description
        self.ability = ability
        self.owner = None
        self.turn_played = 0
        self.location = None
        self.location_effect_applied = False  # Add this flag
        self.revealed = False

    def reveal(self, game: 'Game', owner: 'AIPlayer', location: 'Location'):
        return game, owner, location

    def ongoing(self, game: 'Game', owner: 'AIPlayer', location: 'Location'):
        return game, owner, location

    def __repr__(self):
        return f"{self.name} (Energy: {self.energy_cost}, Power: {self.power}, Ability: {self.ability_description})"


class Ability:
    def __init__(self, effect, ability_type):
        self.effect = effect
        self.ability_type = ability_type
