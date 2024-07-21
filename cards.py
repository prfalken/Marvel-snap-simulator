from loguru import logger
from location import Location


class Card:
    def __init__(
        self,
        name=None,
        energy_cost=None,
        power=None,
        ability_description=None,
        ability=None,
    ):
        self.name = name
        self.game = None
        self.energy_cost = energy_cost
        self.power = power
        self.base_power = power
        self.ability_description = ability_description
        self.ability = ability
        self.owner_id = None
        self.turn_played = 0
        self.location_id = None
        self.location_effect_applied = False  # Add this flag
        self.revealed = False

    def reveal(self, game: "Game"):
        return game

    def ongoing(self, game: "Game"):
        return game

    def __repr__(self):
        return f"{self.name} (Energy: {self.energy_cost}, Power: {self.power}, Ability: {self.ability_description})"


class Abomination(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Abomination"
        self.energy_cost = 5
        self.power = 9
        self.base_power = 9
        self.ability_description = "No Ability"


# # class Aero(Card):
# #     def __init__(self):
# #         Card.__init__(self)
# #         self.name = "Aero"
# #         self.energy_cost = 5
# #         self.power = 9
# #         self.base_power = 9
# #         self.ability_description = "On Reveal: Move the last enemy card played anywhere to this location."

# #     def reveal(self, game: 'Game', owner: 'AIPlayer', location: Location):
# #         opponent_id = 1 if owner.player_id == 0 else 0
# #         opponent = game.players[opponent_id]

# #         if len(opponent.played_cards) == 0:
# #             logger.debug("Aero: No enemy card to move.")
# #             return game, owner, location

#         last_opponent_card = opponent.played_cards[-1]
#         last_opponent_card_location = game.locations[last_opponent_card.location.position]
#         if last_opponent_card_location == location:
#             logger.debug("Aero: The last enemy card played is already at Aero's location.")
#             return game, owner, location

#         # if there are already 4 cards in opponents's target location, do nothing
#         if len([card for card in game.locations[location.position].cards if card.owner == opponent_id ]) == 4:
#             logger.debug("Aero: The target location is full.")
#             return game, owner, location

#         last_opponent_card_location.cards.remove(last_opponent_card)
#         game.locations[self.location].cards.append(last_opponent_card)
#         logger.debug(f"Aero reveal: {last_opponent_card.name} was moved to location {location.position}")
#         return game, owner, location


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
        self.ability_description = (
            "On Reveal: If you play a card here next turn, +3 Power."
        )
        self.number_of_cards_here = 0
        self.hawkeye_triggered = False

    def reveal(self, game: "Game"):
        if not self.revealed:
            self.revealed = True
            self.turn_played = game.current_turn
            location = game.locations[self.location_id]
            self.number_of_cards_here = len(location.cards)
            return game

        if (
            self.revealed
            and not self.hawkeye_triggered
            and game.current_turn == self.turn_played + 1
        ):
            location = game.locations[self.location_id]
            if len(location.cards) > self.number_of_cards_here:
                self.power += 3
                logger.debug(f"{self.name} was played last turn. Power +2")
                self.hawkeye_triggered = True
                return game

        return game


class IronMan(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Iron Man"
        self.energy_cost = 5
        self.power = 0
        self.base_power = 0
        self.ability_description = (
            "Ongoing: Your total Power is doubled at this Location."
        )

    def ongoing(self, game: "Game"):
        location = game.locations[self.location_id]
        total_power = location.calculate_total_power(self.owner_id)
        location.powers[self.owner_id] = total_power * 2
        return game


class Medusa(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Medusa"
        self.energy_cost = 2
        self.power = 2
        self.base_power = 2
        self.ability_description = (
            "On Reveal: If this is at the middle Location, +3 Power."
        )

    def reveal(self, game: "Game"):
        if self.location_id == 1:
            logger.debug(f"{self.name} is at the middle location. Power +3")
            self.power += 3
        return game


class MistyKnight(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Misty Knight"
        self.energy_cost = 1
        self.power = 2
        self.base_power = 2
        self.ability_description = "No Ability"


class Quicksilver(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Quicksilver"
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

    def reveal(self, game: "Game"):
        new_sentinel = Sentinel()
        new_sentinel.owner_id = self.owner_id
        owner = game.players[self.owner_id]
        owner.hand.append(new_sentinel)
        logger.debug(f"Player {self.owner_id} added another Sentinel to their hand.")
        return game


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
        self.ability_description = (
            "On Reveal: If your opponent played a card here this turn, +4 Power."
        )

    def reveal(self, game: "Game"):
        opponent_id = 1 if self.owner_id == 0 else 0
        location = game.locations[self.location_id]
        for c in location.cards:
            if any(
                c.owner_id == opponent_id and c.turn_played == game.current_turn
                for c in location.cards
            ):
                self.power += 4
                logger.debug(
                    f"Star Lord : A card was played by the opponent this turn. Power +4"
                )
                return game
        return game


class ThePunisher(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "The Punisher"
        self.energy_cost = 3
        self.power = 3
        self.base_power = 3
        self.ability_description = (
            "Ongoing: +1 Power for each opposing card at this Location."
        )

    def ongoing(self, game: "Game"):
        location = game.locations[self.location_id]
        enemy_card_count = sum(
            1 for c in location.cards if c.owner_id != self.owner_id and c != self
        )  # Include the current card
        bonus_power = 1 * enemy_card_count
        self.power = self.base_power + bonus_power
        logger.debug("The Punisher's power is now: " + str(self.power))
        return game


class TheThing(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "The Thing"
        self.energy_cost = 4
        self.power = 6
        self.base_power = 6
        self.ability_description = "No Ability"


class Wasp(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Wasp"
        self.energy_cost = 0
        self.power = 1
        self.base_power = 1
        self.ability_description = "No Ability"


class YellowJacket(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Yellow Jacket"
        self.energy_cost = 0
        self.power = 2
        self.base_power = 2
        self.ability_description = (
            "On Reveal: Afflict your other cards here with -1 Power."
        )

    def reveal(self, game: "Game"):
        location = game.locations[self.location_id]
        if not self.revealed:
            for c in location.cards:
                if c != self and c.owner_id == self.owner_id:
                    c.power -= 1
                    logger.debug(
                        f"{c.name} has been afflicted by Yellow Jacket. Power -1"
                    )
            return game
        logger.debug(f"No effect triggerred for Yellow Jacket")
        return game


class Yondu(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Yondu"
        self.energy_cost = 1
        self.power = 2
        self.base_power = 2
        self.ability_description = (
            "On Reveal: Destroy the lowest-Cost card in your opponent’s deck."
        )

    def reveal(self, game: "Game"):
        opponent = 1 if self.owner_id == 0 else 0
        opponent_deck = game.players[opponent].deck
        lowest_cost_card = min(opponent_deck, key=lambda x: x.energy_cost)
        opponent_deck.remove(lowest_cost_card)
        logger.debug(
            f"Yondu Reveal: Player {opponent+1} lost their lowest cost card: {lowest_cost_card.name}"
        )
        return game
