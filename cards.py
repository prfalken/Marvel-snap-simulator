from loguru import logger
import random


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
        self.abilities = []
        self.owner_id = None
        self.turn_played = 0
        self.location_id = None
        self.location_effect_applied = False  # Add this flag
        self.revealed = False

    def reveal(self, game: "Game"):
        return game

    def ongoing(self, game: "Game"):
        return game

    def on_any_card_reveal_effect(self, game: "Game", card):
        return game, card

    def destroy(self, game: "Game"):
        for location in game.locations:
            for card in location.cards:
                if card == self:
                    location.cards.remove(card)
                    logger.debug(f"{self.name} was destroyed.")
                    break

    def __repr__(self):
        return f"{self.name} (Energy: {self.energy_cost}, Power: {self.power}, Ability: {self.ability_description})"


class AmericaChavez(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "America Chavez"
        self.energy_cost = 1
        self.power = 2
        self.base_power = 2
        self.abilities = ["reveal"]
        self.ability_description = "On Reveal: Give the top card of your deck +2 Power."

    def reveal(self, game: "Game"):
        player = game.players[self.owner_id]
        if len(player.deck) == 0:
            return game
        top_card = player.deck.pop(0)
        top_card.power += 2
        logger.debug(f"America Chavez: {top_card.name} was given +2 Power")
        player.deck.insert(0, top_card)
        return game


class Abomination(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Abomination"
        self.energy_cost = 5
        self.power = 9
        self.base_power = 9
        self.ability_description = "No Ability"


class AntMan(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Ant Man"
        self.energy_cost = 1
        self.power = 1
        self.base_power = 1
        self.ongoing_applied = False
        self.abilities = ["ongoing"]
        self.ability_description = (
            "Ongoing: If your side of this location is full, +4 Power."
        )

    def ongoing(self, game: "Game"):
        location = game.locations[self.location_id]
        own_cards = [c for c in location.cards if c.owner_id == self.owner_id]
        if len(own_cards) >= 4 and self.ongoing_applied == False:
            logger.debug(f"AntMan: Location is full. Power +4")
            self.power += 4

            self.ongoing_applied = True
        return game


class Bishop(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Bishop"
        self.energy_cost = 3
        self.power = 1
        self.base_power = 1
        self.ability_description = "After you play a card, this gains +1 Power."

    def on_any_card_reveal_effect(self, game: "Game", card):
        for location in game.locations:
            if card.owner_id == self.owner_id and card != self:
                self.power += 1
                logger.debug(f"{card.name} played. Bishop gains Power +1")
        return game, card


class BlackPanther(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Black Panther"
        self.energy_cost = 5
        self.power = 4
        self.base_power = 4
        self.ability_description = "On Reveal: Double this card’s Power."

    def reveal(self, game: "Game"):
        self.power *= 2
        logger.debug(f"Black Panther: Power doubled to {self.power}")
        return game


class Blade(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Blade"
        self.energy_cost = 1
        self.power = 3
        self.base_power = 3
        self.ability_description = (
            "On Reveal: Discard the rightmost card from your hand."
        )

    def reveal(self, game: "Game"):
        player = game.players[self.owner_id]
        if len(player.hand) > 0:
            discarded_card = player.hand.pop()
            player.discard_stack.append(discarded_card)
            logger.debug(f"Blade: Discarded {discarded_card.name}")
            logger.debug(f"Discard stack is now : {player.discard_stack}")
        return game


class BlueMarvel(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Blue Marvel"
        self.energy_cost = 5
        self.power = 3
        self.base_power = 3
        self.abilities = ["ongoing"]
        self.ability_description = "Ongoing: Your other cards have +1 Power."

    def ongoing(self, game: "Game"):
        location = game.locations[self.location_id]
        for c in location.cards:
            if c != self:
                c.power += 1
                logger.debug(f"{c.name} has been given +1 Power")
        return game


class Cyclops(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Cyclops"
        self.energy_cost = 3
        self.power = 4
        self.base_power = 4
        self.ability_description = "No Ability"


class Colossus(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Colossus"
        self.energy_cost = 2
        self.power = 3
        self.base_power = 3
        self.abilities = ["ongoing"]
        self.ability_description = "Ongoing: Can't be destroyed or moved."

    def destroy(self, game: "Game"):
        return game

    def ongoing(self, game: "Game"):
        return game


class Gamora(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Gamora"
        self.energy_cost = 5
        self.power = 7
        self.base_power = 7
        self.ability_description = (
            "On Reveal: If your opponent played a card here this turn, +5 Power."
        )

    def reveal(self, game: "Game"):
        opponent_id = 1 if self.owner_id == 0 else 0
        location = game.locations[self.location_id]
        opponent_card_played = False
        for c in location.cards:
            if c.owner_id == opponent_id and c.turn_played == game.turn.turn_id:
                opponent_card_played = True
                break

        if opponent_card_played:
            self.power += 5
            logger.debug(
                f"Gamora: A card was played by the opponent this turn. Power +5"
            )
            return game

        return game


class IronHeart(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Iron Heart"
        self.energy_cost = 3
        self.power = 0
        self.base_power = 0
        self.ability_description = "On Reveal: Give 3 other cards +2 Power."

    def reveal(self, game: "Game"):
        location = game.locations[self.location_id]
        other_cards = [c for c in location.cards if c != self]
        random.shuffle(other_cards)
        for c in other_cards[:3]:
            c.power += 2
            logger.debug(f"{c.name} was given +2 Power")
        return game


class Nightcrawler(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Nightcrawler"
        self.energy_cost = 1
        self.power = 2
        self.base_power = 2
        self.ability_description = "You can move this once."
        self.moved = False

    def move(self, game: "Game"):
        if not self.moved:
            location = game.locations[self.location_id]
            location.cards.remove(self)
            location_id = (self.location_id + 1) % 3
            location = game.locations[location_id]
            location.cards.append(self)
            self.location_id = location_id
            self.moved = True
            logger.debug(f"{self.name} has been moved to location {location_id}")
        return game


class MisterFantastic(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Mister Fantastic"
        self.energy_cost = 3
        self.power = 2
        self.base_power = 2
        self.abilities = ["ongoing"]
        self.ability_description = "Ongoing: Adjacent locations have +2 Power."

    def ongoing(self, game: "Game"):
        location = game.locations[self.location_id]
        for i in range(3):
            if i != self.location_id:
                location = game.locations[i]
                location.powers[self.owner_id] += 2
                logger.debug(f"{location} has been given +2 Power")
        return game


class Kazar(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Kazar"
        self.energy_cost = 4
        self.power = 5
        self.base_power = 5
        self.abilities = ["ongoing"]
        self.ability_description = "Ongoing: Your 1-Cost cards have +1 Power."

    def ongoing(self, game: "Game"):
        for location in game.locations:
            for c in location.cards:
                if c.energy_cost == 1 and c.owner_id == self.owner_id:
                    c.power += 1
                    logger.debug(f"{c.name} has been given +1 Power by Kazar")
            return game


class JessicaJones(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Jessica Jones"
        self.energy_cost = 4
        self.power = 5
        self.base_power = 5
        self.ability_description = (
            "On Reveal: If you don't play a card here next turn, +4 Power."
        )
        self.jessica_jones_triggered = False

    def reveal(self, game: "Game"):
        if not self.revealed:
            self.revealed = True
            self.turn_played = game.current_turn
            return game

        if (
            self.revealed
            and not self.jessica_jones_triggered
            and game.current_turn == self.turn_played + 1
        ):
            location = game.locations[self.location_id]
            if len(location.cards) == 1:
                self.power += 4
                logger.debug(f"{self.name} was not played last turn. Power +4")
                self.jessica_jones_triggered = True
                return game

        return game


class Tiger(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Tiger"
        self.energy_cost = 5
        self.power = 8
        self.base_power = 8
        self.ability_description = "No Ability"


class Odin(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Odin"
        self.energy_cost = 6
        self.power = 8
        self.base_power = 8
        self.ability_description = "On Reveal: Activate the On Reveal abilities of your other cards at this location."

    def reveal(self, game: "Game"):
        location = game.locations[self.location_id]
        for c in location.cards:
            if c != self and c.owner == self.owner_id:
                game = c.reveal(game)
        return game


class Spectrum(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Spectrum"
        self.energy_cost = 6
        self.power = 7
        self.base_power = 7
        self.ability_description = "On Reveal: Give your Ongoing cards +2 Power."

    def reveal(self, game: "Game"):
        for location in game.locations:
            for c in location.cards:
                if (
                    c != self
                    and c.owner_id == self.owner_id
                    and "ongoing" in c.abilities
                ):
                    c.power += 2
        return game


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
        self.abilities = ["ongoing"]
        self.ability_description = (
            "Ongoing: Your total Power is doubled at this Location."
        )

    def ongoing(self, game: "Game"):
        location = game.locations[self.location_id]
        total_power = location.calculate_total_power(self.owner_id)
        location.powers[self.owner_id] = total_power * 2
        return game


class LadySif(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Lady Sif"
        self.energy_cost = 3
        self.power = 5
        self.base_power = 5
        self.ability_description = (
            "On Reveal: Discard the highest-cost card from your hand."
        )

    def reveal(self, game: "Game"):
        player = game.players[self.owner_id]
        highest_cost_card = max(player.hand, key=lambda x: x.energy_cost)
        player.hand.remove(highest_cost_card)
        player.discard_stack.append(highest_cost_card)
        logger.debug(f"Lady Sif: Discarded {highest_cost_card.name}")
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
        opponend_card_played = False
        for c in location.cards:
            if c.owner_id == opponent_id and c.turn_played == game.turn.turn_id:
                opponend_card_played = True
                break

        if opponend_card_played:
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
        self.abilities = ["ongoing"]
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


class WhiteTiger(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "White Tiger"
        self.energy_cost = 5
        self.power = 1
        self.base_power = 1
        self.ability_description = "On Reveal: Add a 8-Power Tiger to another location."

    def reveal(self, game: "Game"):
        location = game.locations[(self.location_id + 1) % 3]
        tiger = Tiger()
        tiger.owner_id = self.owner_id
        location.cards.append(tiger)
        logger.debug(
            f"White Tiger: A 8-Power Tiger has been added to location {location.location_id}"
        )
        return game


class Wolfsbane(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Wolfsbane"
        self.energy_cost = 3
        self.power = 1
        self.base_power = 1
        self.ability_description = (
            "On Reveal: +2 Power for each other card you have here."
        )

    def reveal(self, game: "Game"):
        location = game.locations[self.location_id]
        for c in location.cards:
            if c != self and c.owner_id == self.owner_id:
                self.power += 2
                logger.debug(f"{self.name} has been given +2 Power")
        return game


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


class Elektra(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Elektra"
        self.energy_cost = 1
        self.power = 1
        self.base_power = 1
        self.ability_description = (
            "On Reveal: Destroy a random enemy 1-Cost card at this location."
        )

    def reveal(self, game: "Game"):
        location = game.locations[self.location_id]
        enemy_cards = [c for c in location.cards if c.owner_id != self.owner_id]
        if len(enemy_cards) > 0:
            card_to_destroy = random.choice(enemy_cards)
            card_to_destroy.destroy(game)
            logger.debug(f"Elektra: Destroyed {card_to_destroy.name}")
        return game


class Korg(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Korg"
        self.energy_cost = 1
        self.power = 2
        self.base_power = 2
        self.ability_description = (
            "On Reveal: Shuffle a Rock into your opponent's deck."
        )

    def reveal(self, game: "Game"):
        opponent = 1 if self.owner_id == 0 else 0
        opponent_deck = game.players[opponent].deck
        rock = Rock()
        rock.owner_id = opponent
        opponent_deck.append(rock)
        logger.debug(f"Korg: A Rock was added to Player {opponent+1}'s deck.")
        return game


class Rock(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Rock"
        self.energy_cost = 1
        self.power = 0
        self.base_power = 0
        self.ability_description = "No Ability"


class Mantis(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Mantis"
        self.energy_cost = 2
        self.power = 3
        self.base_power = 3
        self.ability_description = "On Reveal: If you played a card here this turn, draw a card from their deck."

    def reveal(self, game: "Game"):
        opponent = 1 if self.owner_id == 0 else 0
        location = game.locations[self.location_id]
        if location.player1_played_card and self.owner_id == 0:
            card_drawn = game.players[opponent].deck.pop(0)
            game.players[self.owner_id].hand.append(card_drawn)
            logger.debug(f"Mantis: Player {opponent+1} drew a card.")
        elif location.player2_played_card and self.owner_id == 1:
            card_drawn = game.players[opponent].deck.pop(0)
            game.players[self.owner_id].hand.append(card_drawn)
            logger.debug(f"Mantis: Player {opponent+1} drew a card.")
        return game


class RocketRaccoon(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Rocket Raccoon"
        self.energy_cost = 1
        self.power = 2
        self.base_power = 2
        self.ability_description = (
            "On Reveal: If your opponent played a card here this turn, +2 Power."
        )

    def reveal(self, game: "Game"):
        opponent = 1 if self.owner_id == 0 else 0
        location = game.locations[self.location_id]
        if location.player1_played_card and self.owner_id == 0:
            self.power += 2
            logger.debug(f"Rocket Raccoon: Power +2")
        elif location.player2_played_card and self.owner_id == 1:
            self.power += 2
            logger.debug(f"Rocket Raccoon: Power +2")
        return game


class ScarletWitch(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Scarlet Witch"
        self.energy_cost = 2
        self.power = 3
        self.base_power = 3
        self.ability_description = (
            "On Reveal: Replace this location with a random new one."
        )

    def reveal(self, game: "Game"):
        location = game.locations[self.location_id]
        location.cards.remove(self)
        new_location = random.choice(game.all_locations)
        for c in location.cards:
            new_location.cards.append(c)
        game.locations[self.location_id] = new_location
        logger.debug(f"Scarlet Witch: Location changed to {new_location.name}")
        return game


class SquirrelGirl(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Squirrel Girl"
        self.energy_cost = 1
        self.power = 2
        self.base_power = 2
        self.ability_description = (
            "On Reveal: Add a 1-Power Squirrel to each other location."
        )

    def reveal(self, game: "Game"):
        for location in game.locations:
            if location.position != self.location_id:
                squirrel = Squirrel()
                squirrel.owner_id = self.owner_id
                location.cards.append(squirrel)
                logger.debug(
                    f"Squirrel girl added a squirrel to location {location.position}"
                )
        return game


class Squirrel(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Squirrel"
        self.energy_cost = 1
        self.power = 1
        self.base_power = 1
        self.ability_description = "No Ability"


class Angela(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Angela"
        self.energy_cost = 2
        self.power = 2
        self.base_power = 2
        self.ability_description = "When you play a card here, +1 Power."

    def on_any_card_reveal_effect(self, game: "Game", card: Card):
        if card.location_id == self.location_id:
            self.power += 1
            logger.debug(f"Angela: Power +1")
        return game, card


class Cable(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Cable"
        self.energy_cost = 3
        self.power = 4
        self.base_power = 4
        self.ability_description = (
            "On reveal: Put the bottom card of your opponent's deck into your hand."
        )

    def reveal(self, game: "Game"):
        opponent = 1 if self.owner_id == 0 else 0
        opponent_deck = game.players[opponent].deck
        card = opponent_deck.pop()
        game.players[self.owner_id].hand.append(card)
        logger.debug(f"Cable: Player {opponent+1} lost a card.")
        return game


class Forge(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Forge"
        self.energy_cost = 2
        self.power = 3
        self.base_power = 3
        self.ability_description = "On reveal: Give the next card you play +2 Power."

    def on_any_card_reveal_effect(self, game: "Game", card: Card):
        if card.owner_id == self.owner_id:
            card.power += 2
        logger.debug(f"Forge: giving +2 Power to {card.name}")
        return game, card


class Groot(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Groot"
        self.energy_cost = 3
        self.power = 4
        self.base_power = 4
        self.ability_description = (
            "On Reveal: If your opponent played a card here this turn, +4 Power."
        )

    def reveal(self, game: "Game"):
        opponent = 1 if self.owner_id == 0 else 0
        location = game.locations[self.location_id]
        if location.player1_played_card and self.owner_id == 0:
            self.power += 4
            logger.debug(f"Groot: Power +4")
        elif location.player2_played_card and self.owner_id == 1:
            self.power += 4
            logger.debug(f"Groot: Power +4")
        return game


class Heimdall(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Heimdall"
        self.energy_cost = 6
        self.power = 9
        self.base_power = 9
        self.ability_description = (
            "On Reveal: Move your other cards one location to the left."
        )

    def reveal(self, game: "Game"):
        location = game.locations[self.location_id]
        for c in location.cards:
            if c != self:
                location.cards.remove(c)
                new_location_id = (c.location_id - 1) % 3
                new_location = game.locations[new_location_id]
                new_location.cards.append(c)
                c.location_id = new_location_id
                logger.debug(f"{c.name} moved to location {new_location_id}")
        return game


# class IronFist(Card):
#     def __init__(self):
#         Card.__init__(self)
#         self.name = "Iron Fist"
#         self.energy_cost = 1
#         self.power = 2
#         self.base_power = 2
#         self.ability_description = "On Reveal: Move the next card you play one location to the left after it reveals."
#         self.iron_fist_triggered = False

#     def on_any_card_reveal_effect(self, game: "Game", card):
#         if self.iron_fist_triggered:
#             return game

#         if card.owner_id == self.owner_id:
#             new_location_id = (card.location_id - 1) % 3
#             new_location = game.locations[new_location_id]
#             new_location.cards.append(card)
#             card.location_id = new_location_id
#             self.iron_fist_triggered = True
#             logger.debug(f"{card.name} moved to location {new_location_id}")
#         return game


class Namor(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Namor"
        self.energy_cost = 4
        self.power = 6
        self.base_power = 6
        self.ability_description = "Ongoing: +5 Power if this is your only card here."

    def ongoing(self, game: "Game"):
        location = game.locations[self.location_id]
        if len(location.cards) == 1:
            self.power += 5
            logger.debug(f"Namor: Power +5")
        else:
            self.power = self.base_power
        return game


class Nova(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Nova"
        self.energy_cost = 1
        self.power = 1
        self.base_power = 1
        self.ability_description = "When this is destroyed, give your cards +1 Power."

    def destroy(self, game: "Game"):
        for location in game.locations:
            for c in location.cards:
                if c.owner_id == self.owner_id:
                    c.power += 1
                    logger.debug(f"{c.name} has been given +1 Power by Nova")
        return game


class HulkBuster(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Hulk Buster"
        self.energy_cost = 2
        self.power = 3
        self.base_power = 3
        self.ability_description = (
            "On Reveal: Merge this card with a random friendly card at this location."
        )

    def reveal(self, game: "Game"):
        location = game.locations[self.location_id]
        friendly_cards = [
            c for c in location.cards if c.owner_id == self.owner_id and c != self
        ]
        if len(friendly_cards) > 0:
            card_to_merge = random.choice(friendly_cards)
            card_to_merge.power += self.power
            location.cards.remove(self)
            logger.debug(f"{self.name} merged with {card_to_merge.name}")
        return game


class Lizard(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Lizard"
        self.energy_cost = 2
        self.power = 5
        self.base_power = 5
        self.abilities = ["ongoing"]
        self.ability_description = (
            "Ongoing: -3 Power if your opponent has 4 cards here."
        )

    def ongoing(self, game: "Game"):
        location = game.locations[self.location_id]
        opponent_card_count = sum(
            1 for c in location.cards if c.owner_id != self.owner_id
        )
        if opponent_card_count >= 4:
            self.power -= 3
            logger.debug(f"Lizard: Power -3")
        return game


class MisterSinister(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Mister Sinister"
        self.energy_cost = 2
        self.power = 2
        self.base_power = 2
        self.ability_description = (
            "On Reveal: Add a Sinister Clone to this location with the same Power."
        )

    def reveal(self, game: "Game"):
        clone = SinisterClone()
        clone.owner_id = self.owner_id
        location = game.locations[self.location_id]
        location.cards.append(clone)
        logger.debug(f"Added a Sinister Clone to location {self.location_id}")
        return game


class SinisterClone(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Sinister Clone"
        self.energy_cost = 2
        self.power = 2
        self.base_power = 2
        self.ability_description = "No Ability"


class MoonGirl(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Moon Girl"
        self.energy_cost = 4
        self.power = 4
        self.base_power = 4
        self.ability_description = "On Reveal: Duplicate your hand."

    def reveal(self, game: "Game"):
        player = game.players[self.owner_id]
        player.hand = player.hand * 2
        logger.debug(f"Moongirl duplicated the hand : {player.hand}")
        return game


class Morph(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Morph"
        self.energy_cost = 3
        self.power = 0
        self.base_power = 0
        self.ability_description = (
            "On Reveal: Become a copy of a random card in your opponent's hand."
        )

    def reveal(self, game: "Game"):
        opponent = 1 if self.owner_id == 0 else 0
        opponent_hand = game.players[opponent].hand
        card_to_copy = random.choice(opponent_hand)
        self.name = card_to_copy.name
        self.energy_cost = card_to_copy.energy_cost
        self.power = card_to_copy.power
        self.abilities = card_to_copy.abilities
        self.ability_description = card_to_copy.ability_description
        logger.debug(f"Morph: Became a copy of {card_to_copy.name}")
        return game


class MultipleMan(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Multiple Man"
        self.energy_cost = 2
        self.power = 3
        self.base_power = 3

    def on_move(self, game: "Game"):
        location = game.locations[self.location_id]
        new_card = MultipleMan()
        new_card.owner_id = self.owner_id
        location.cards.append(new_card)
        logger.debug(f"Added a copy of Multiple Man to location {self.location_id}")
        return game


class SpiderWoman(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Spider Woman"
        self.energy_cost = 5
        self.power = 8
        self.base_power = 8
        self.ability_description = (
            "On Reveal: Afflict all enemy cards here with -1 Power."
        )

    def reveal(self, game: "Game"):
        location = game.locations[self.location_id]
        for c in location.cards:
            if c.owner_id != self.owner_id:
                c.power -= 1
                logger.debug(
                    f"{c.name} has been afflicted with -1 power by Spider Woman"
                )
        return game


class StrongGuy(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = "Strong Guy"
        self.energy_cost = 3
        self.power = 3
        self.base_power = 3
        self.ability_description = (
            "Ongoing: +6 Power if your hand has one or fewer cards."
        )

    def ongoing(self, game: "Game"):
        player = game.players[self.owner_id]
        if len(player.hand) <= 1:
            self.power += 6
            logger.debug(f"{self.name} has been given +6 Power")
        return game


# Marvel Snap Starter Cards
# Card 	Cost	Power	Card Ability
# Abomination	5	9	No ability.
# Ant-Man	1	1	Ongoing If your side of this location is full, +4 Power.
# Cyclops	3	4	No ability.
# Gamora	5	8	On Reveal: If your opponent played a card here this turn, +4 Power.
# Hawkeye	1	1	On Reveal: If you play a card here next turn, +3 Power.
# Hulk	6	12	No ability.
# Iron Man	5	0	Ongoing: Your total Power is doubled at this Location.
# Jessica Jones	4	5	On Reveal: If you don’t play a card at this location next turn, +4 Power.
# Medusa	2	2	On Reveal: If this is at the middle Location, +3 Power.
# Misty Knight	1	2	No ability.
# The Punisher	3	3	Ongoing: +1 Power for each opposing card at this Location.
# Quicksilver	1	2	Starts in your opening hand.
# Sentinel	2	3	On Reveal: Add another Sentinel to your hand.
# Shocker	2	3	No ability.
# Spectrum	6	6	On Reveal: Give your Ongoing cards +2 Power.
# Star Lord	2	2	On Reveal: If your opponent played a card here this turn, +4 Power.
# The Thing	4	6	No ability.
# Marvel Snap Series 1 Cards (Collection Level 18 – 215)
# Card 	Cost	Power	Card Ability
# America Chavez	1	2	On Reveal: Give the top card of your deck +2 Power.
# Angel	1	2	When one of your cards is destroyed, this flies out of your hand or deck to replace it.
# Angela	2	0	When you play a card here, +2 Power.
# Apocalypse	6	6	When you discard this from your hand, put it back with +4 Power.
# Armor	2	3	Ongoing: Cards at this location can’t be destroyed.
# Bishop	3	1	When you play a card, this gains +1 Power.
# Blade	1	3	On Reveal: Discard the rightmost card from your hand.
# Cable	2	3	On Reveal: Put the bottom card of your opponent’s deck into your hand.
# Captain America	3	3	Ongoing: Your other cards at this location have +2 Power.
# Carnage	2	2	On Reveal: Destroy your other cards here. +2 Power for each destroyed.
# Cosmo	3	3
# Ongoing: On Reveal abilities won’t happen at this location.
# Deathlok	3	5
# On Reveal: Destroy your other cards at this location.
# Devil Dinosaur	5	3
# Ongoing: +2 Power for each card in your hand.
# Doctor Strange	2	3	On Reveal: Move your highest power cards to this location.
# Domino	2	3
# You always draw this card on turn 2, and not before.
# Elektra	1	2	On Reveal: Destroy a random enemy 1-Cost card at this location.
# Enchantress	4	5	On Reveal: Remove the abilities from all Ongoing cards at this location.
# Forge	2	2
# On Reveal: Give the next card you play +2 Power.
# Groot	3	4
# On Reveal: If your opponent played a card here this turn, +4 Power.
# Heimdall	6	9
# On Reveal: Move your other cards one location to the left.
# Hulkbuster	2	3
# On Reveal: Merge this card with a random friendly card at this location.
# Iron Fist	1	2	On Reveal: Move the next card you play one location to the left after it reveals.
# Klaw	5	4	Ongoing: The location to the right has +8 Power.
# Korg	1	2
# On Reveal: Shuffle a Rock into your opponent’s deck.
# Kraven	2	2
# When a card moves here, this gets +2 Power.
# Lady Sif	3	5
# On Reveal: Discard the highest-cost card from your hand.
# Lizard	2	5
# Ongoing: -3 Power if your opponent has 4 cards here.
# Mantis	1	2	If your opponent played any cards here this turn, copy one of them into your hand.
# Mister Sinister	2	2	On Reveal: Add a Sinister Clone to this location with the same Power.
# Moon Girl	4	4	On Reveal: Duplicate your hand.
# Morph	3	0
# On Reveal: Become a copy of a random card in your opponent’s hand.
# Multiple Man	2	3	When this moves, add a copy to the old location.
# Namor	4	6	Ongoing: +5 Power if this is your only card here.
# Nova	1	1
# When this is destroyed, give your cards +1 Power.
# Onslaught	6	7
# Ongoing: Double your other Ongoing effects at this location.
# Professor X	5	2
# Ongoing: Moving is the only way to add or remove a card from here.
# Rocket Raccoon	1	1
# On Reveal: If your opponent played a card here this turn, +4 Power.
# Scarlet Witch	2	3
# On Reveal: Replace this location with a random new one.
# Spider-Woman	5	8
# On Reveal: Afflict all enemy cards here with -1 Power.
# Squirrel Girl	1	2	On Reveal: Add a 1-Power Squirrel to each other location.
# Strong Guy	3	3	Ongoing: +6 Power if your hand has one or fewer cards.
# Sword Master	3	7	On Reveal: Discard a card from your hand.
# Uatu the Watcher	1	2
# At the start of the game, shows the right location to you.
# White Queen	4	6
# On Reveal: Draw a copy of the highest Cost card in your opponent’s hand.
# White Tiger	5	1
# On Reveal: Add a 8-Power Tiger to another location.
# Wolverine	2	2	When this is discarded or destroyed, regenerate it at a random location with +2 Power.
# Yondu	1	2
# On Reveal: Destroy the lowest-Cost card in your opponent’s deck.
# Marvel Snap Series 2 Cards (Collection Level 222 – 474)
# Card 	Cost	Power	Card Ability
# Agent 13	1	2	On Reveal: Add a random card to your hand.
# Bucky Barnes	2	1	When this is destroyed, create the Winter Soldier in its place.
# Cloak	2	4	On Reveal: Next turn, both players can move cards to this location.
# Ebony Maw	1	7	You can’t play this after turn 3.
# Ongoing: You can’t play cards here.
# Hobgoblin	5	-8	On Reveal: Your Opponent gains control of this.
# Iceman	1	2	On Reveal: Give a random card in your opponent’s hand +1 Cost (maximum 6).
# Jubilee	4	1	On Reveal: Add the top card of your deck at this location.
# Killmonger	3	3	On Reveal: Destroy ALL 1-Cost cards.
# Leech	5	5	On Reveal: Remove the text from each card with an On Reveal ability in your opponent’s hand.
# Morbius	2	0	Ongoing: +2 Power for each card you have discarded from your hand this game.
# Nakia	3	3	On Reveal: Give the 2 leftmost cards in your hand +2 Power.
# Okoye	2	2	On Reveal: Give every card in your deck +1 Power.
# Rhino	3	3	On Reveal: Ruin this location (remove it’s ability).
# Sabretooth	3	5	When this is destroyed, return it to your hand. It costs 0.
# Sandman	5	7	On Reveal: Players can only play 1 card next turn.
# Scorpion	2	2	On Reveal: Afflict cards in your opponent’s hand with -1 Power.
# Shang-Chi	4	3	On Reveal: Destroy all enemy cards at this location that have 10 or more Power.
# Storm	3	2	On Reveal: Flood this location. Next turn is the last turn cards can be played here.
# Sunspot	1	0	At the end of each turn, gain +1 Power for each unspent Energy.
# Swarm	2	3	When this is discarded from your hand, add two 0-Cost copies to your hand.
# The Collector	2	2	When a card enters your hand from anywhere (except your deck), +1 Power.
# The Infinaut	6	20	If you played a card last turn, you can’t play this.
# Vision	5	8	You can move this each turn.
# Vulture	3	3	When this card moves, +6 Power.
# Warpath	4	5	Ongoing: If any of your locations are empty, +5 Power.
# Marvel Snap Series 3 Cards (Collection Level 486+)
# Card 	Cost	Power	Card Ability
# Absorbing Man	4	4	On Reveal: If the last card you played has an On Reveal ability, this card copies it.
# Adam Warlock	5	5
# At the end of each turn, if you are winning this location, draw a card.
# Aero	5	9
# On Reveal: Move all enemy cards played this turn to this location.
# Agatha Harkness	6	14
# Agatha starts in your hand and plays your cards for you.
# Agent Coulson	3	4
# On Reveal: Add a random 4-cost and 5-cost card to your hand.
# Arnim Zola	6	0
# On Reveal: Destroy a random friendly card here. Add copies of it to the other locations.
# Attuma	4	10
# If you have another card here at the end of your turn, destroy this.
# Baron Mordo	2	3
# On Reveal: The top card of your opponent’s deck costs 6 until turn 6.
# Beast	2	2
# On Reveal: Return your other cards at this location to your hand. They cost 1 less.
# Bast	1	1
# On Reveal: Set the Power of all cards in your hand to 3.
# Black Bolt	5	7
# On Reveal: Your opponent must discard the lowest-Cost card in their hand.
# Black Cat	4	9
# If this is in your hand at the end of your turn, discard it.
# Black Panther	5	4
# On Reveal: Double this card’s Power.
# Black Widow	3	3
# On Reveal: Add a Widow’s Bite to your opponent’s hand.
# Brood	3	2
# On Reveal: Add 2 Broodlings to this location with the same Power.
# Captain Marvel	4	5
# At the end of the game, move to a location that wins you the game. (If possible)
# Cerebro	3	0
# Ongoing: Your highest Power cards get +2 Power.
# Colleen Wing	2	4
# On Reveal: Discard the lowest-cost card from your hand.
# Crossbones	4	10
# You can only play this at locations where you are winning.
# Crystal	3	3
# On Reveal: Each player draws a card.
# Dagger	2	0
# When this moves to a location, +3 Power for each card your opponent has there.
# Daredevil	2	2
# On turn 5, you get to see your opponent’s plays before you make your own.
# Dazzler	2	2
# Ongoing: +2 Power for each location that’s full on your side.
# Deadpool	1	1
# When this is destroyed, return it to your hand with double the Power.
# Death	8	12
# Costs 1 less for each card destroyed this game.
# Debrii	3	3
# On Reveal: Add a Rock to each other location, for both players.
# Destroyer	6	16
# On Reveal: Destroy your other cards.
# Doctor Octopus	5	10
# On Reveal: Pull 4 random cards from your opponent’s hand to their side of this location.
# Doctor Doom	6	5
# On Reveal: Add a 5-Power DoomBot to each other location.
# Dracula	4	1
# At the end of the game, discard a card from your hand to gain its Power.
# Drax	4	5
# On Reveal: If your opponent played a card here this turn, +4 Power.
# Echo	1	2
# After your opponent plays an Ongoing card here, remove its abilities.
# Electro	3	2
# On Reveal: +1 Max Energy. Ongoing: You can only play 1 card a turn.
# Falcon	2	3
# On Reveal: Return your 1-Cost cards to your hand.
# Gambit	3	3
# On Reveal: Discard a card from your hand. Destroy a random enemy card.
# Ghost	3	5
# Ongoing: Your cards are always revealed last. (Their On Reveal abilities happen last)
# Ghost Rider	4	3
# On Reveal: Bring back one of your discarded cards to this location.
# Giganto	6	14
# You can only play this at the left location.
# Goose	2	2
# Ongoing: Nobody can play cards that cost 4, 5, or 6 at this location.
# Green Goblin	3	-3
# On Reveal: Your opponent gains control of this.
# Hazmat	2	2
# On Reveal: Afflict all other cards with -1 Power.
# Hela	6	6
# On Reveal: Play all cards you discarded from your hand to random locations with -2 power.
# Helicarrier	6	10
# When you discard this from your hand, fill your hand with random cards.
# Hellcow	4	8
# On Reveal: Discard 2 cards from your hand.
# Howard the Duck	1	2
# Ongoing: Tap this to see the top card of your deck.
# Human Torch	1	2
# When this moves, double its Power.
# Invisible Woman	2	3
# Ongoing: Cards you play here are not revealed until the game ends.
# Jane Foster the Mighty Thor	5	9
# On Reveal: Draw all cards that Cost 0 from your deck.
# Juggernaut	3	3
# On Reveal: Move away all enemy cards played here this turn (including unrevealed cards).
# Kingpin	2	6
# When an enemy card moves here, afflict it with -2 Power.
# Leader	6	3
# On Reveal: Copy the enemy card(s) with the highest Power played this turn, but on your side.
# Lockjaw	4	5
# After you play a card here, swap it with a card in your deck. (Once per turn)
# Luke Cage	3	3	Ongoing: Your cards can’t have their Power reduced.
# M’Baku	1	2	At the end of the game, this jumps from your deck to your lowest-Power location (that isn’t full).
# Magik	3	2
# You can’t play this on turn 6. On Reveal: Change this location to ‘Limbo’.
# Magneto	6	12
# On Reveal: Move all opposing 3 and 4-Cost cards to this location.
# Maria Hill	1	2
# On Reveal:Add a random 2-Cost card to your hand.
# Martyr	1	5
# At the end of the game, move to a location that LOSES you the game (if possible).
# Master Mold	2	2
# On Reveal: Add 2 Sentinels to your opponent’s hand
# Maximus	2	6
# On Reveal: Your opponent draws 2 cards.
# Miles Morales	4	5
# If a card moved last turn, this costs 1.
# Mirage	2	2
# On Reveal: Copy the lowest-Cost card in your opponent’s hand into your hand. Give it +2 power.
# Mojo	2	2
# Ongoing: If both sides here are full, +6 Power.
# Moon Knight	3	3
# On Reveal: Discard a card from each player’s hand.
# Mister Negative	4	-1
# On Reveal: Swap the Power and Cost of all cards in your deck.
# Mysterio	2	4
# As you play this, play Illusions to other locations. Disguise this as an Illusion until the game ends.
# Mystique	3	0
# On Reveal: If the last card you played has an Ongoing ability, this card gains it.
# Negasonic Teenage Warhead	3	2
# After an enemy card is played here, destroy it (once per game).
# Nick Fury	4	5
# On Reveal: Add 3 random 6-Cost cards to your hand.
# Omega Red	4	5
# Ongoing: If you’re winning here, +3 Power to other locations.
# Orka	6	11
# Ongoing: + 5 Power if this is your only card here.
# Patriot	3	1
# Ongoing: Your cards with no abilities have +2 Power.
# Polaris	3	5
# On Reveal: Move an opposing 1 or 2-Cost card to this location.
# Psylocke	2	2
# On Reveal: Next turn, you get +1 Energy.
# Quake	2	3
# On Reveal: Swap the positions of the other two locations.
# Quinjet	1	2
# Ongoing: Cards that didn’t start in your deck cost 1 less.
# Red Skull	5	14
# Ongoing: Enemy cards at this location have +2 Power.
# Rescue	4	4
# On Reveal: If you play a card here next turn, +5 Power.
# Rockslide	3	3
# On Reveal: Shuffle 2 Rocks into your opponent’s deck.
# Rogue	3	2
# On Reveal: Steal an Ongoing ability from a random enemy card at this location.
# Ronan the Accuser	5	5
# Ongoing: +2 Power for each card in your opponent’s hand.
# Sauron	3	3
# On Reveal: Remove the abilities from all Ongoing cards in your hand and deck.
# Sentry	4	8
# Cannot be played at the right Location. On Reveal: Add a -8 Power Void to the right Location.
# Sera	5	5
# Ongoing: Cards in your hand cost 1 less. (minimum 1)
# Shadow King	2	2
# On Reveal: Set all cards here to their base Power.
# Shanna	3	4	On Reveal: Add a random 1-Cost card to each Location.
# She-Hulk	6	10
# Costs 1 less for each unspent Energy last turn.
# Shuri	4	1
# On Reveal: If you play your next card here, double its Power.
# Silver Samurai	4	5
# On Reveal: Each player discards the lowest-Power card from their hand.
# Silver Surfer	3	2
# On Reveal: Give your other 3-Cost cards +2 Power
# Spider-Man	3	5
# On Reveal: Move to another location and pull an enemy card from here to there.
# Spider-Man 2099	5	9
# The first time this moves to a location, destroy an enemy card there.
# Stature	5	7
# Costs 1 if your opponent discarded a card from their hand this game.
# Stegron	4	7
# On Reveal: Move an enemy card from here one location to the right.
# Super Skrull	4	2
# Ongoing: Has the Ongoing effects of all enemy cards.
# Taskmaster	5	0
# On Reveal: Set this card’s Power equal to the Power of the last card you played (if that card’s in play).
# The Hood	1	-3
# On Reveal: Add a Demon to your hand.
# Thor	3	4
# On Reveal: Shuffle Mjolnir into your deck.
# Titania	1	5	When ANY card is played at this location, this card switches sides.
# Typhoid Mary	4	10
# Ongoing: Your other cards have -1 Power.
# Ultron	6	8
# On Reveal: Create four 2-Power Drones at each other location.
# Valkyrie	5	3
# On Reveal: Set ALL cards at this location to 3 Power.
# Venom	3	3
# On Reveal: Destroy your other cards at this location. Add their Power to this card.
# Viper	3	5
# On Reveal: Your opponent gains control of one of your other cards at this location.
# Wasp	0	1
# No ability.
# Wave	3	6
# On Reveal: All cards cost a maximum of 4 until the end of the next turn.
# Wong	4	2
# Ongoing: Your On Reveal abilities at this location happen twice.
# Yelowjacket	0	2
# On Reveal: Afflict your other cards at this location with -1 Power.
# Zero	1	3
# On Reveal: Remove the abilities on the next card you play.
# Marvel Snap Series 4 Cards (Collection Level 486+)
# Card 	Cost	Power	Card Ability
# Daken	3	4	On Reveal: Add the Muramasa Shard to your hand.
# Darkhawk	5	3	Ongoing: + 2 Power for each card in your opponent’s deck.
# Ghost Spider	1	2	On Reveal: The last card you played moves here.
# Gladiator	3	8	On Reveal: Add a card from your opponent’s deck to their side of this location. If it has less Power, destroy it.
# Havok	2	1	After each turn, you lose 1 Max Energy and this gains +3 Power.
# Hercules	4	7	The first time another card moves here each turn, move it to another location.
# Hit Monkey	3	2	On Reveal: Gain +2 Power for each other card you played this turn.
# Jean Grey	3	4	Ongoing:Players must play their first card here each turn (if possible).
# Kitty Pryde	1	1	When this returns to your hands, +1 Power. Returns at the start of each turn.
# Knull	6	0	Ongoing: Has the combined Power of all cards destroyed this game.
# Lady Deathstrike	5	6	On Reveal: Destroy each card here with 3 or less Power.
# Legion	5	7	On Reveal: Replace each other location with this one.
# Miek	1	0	When you discard a card, this gains +1 Power and can move next turn
# MODOK	5	8	On Reveal: Discard your hand.
# Nebula	1	1	Each turn your opponent doesn’t play a card here, +2 Power. (except the turn you play this)
# Nimrod	5	6	When this card is destroyed, add a copy to each other location.
# Phoenix Force	4	5	On Reveal: Revive one of your destroyed cards and merge with it. That card can move each turn.
# Selene	1	2	On Reveal: Afflict the lowest-Power card in each player’s hand with -3 Power.
# Silk	2	5	When anyone plays a card here, move this to another location.
# Snowguard	1	2	On Reveal: Add the Hawk and Bear auroras to your hand.Hawk [3/3] On Reveal: Ignore all location abilities until the end of next turn (or the game).Bear [3/4] On Reveal: Trigger the effect of this location.
# Spider-Ham	1	1	On Reveal:Transform the leftmost card in your opponent’s hand into a Pig, keeping its Power and Cost.
# Supergiant	1	2	On Reveal: All cards played this turn and next turn don’t reveal until the game ends.
# The Living Tribunal	6	9	At the end of the game, split your Power evenly among all Locations.
# Zabu	4	2	Ongoing: Until the end of the next turn, your 4-Cost cards cost 1 less.
# Marvel Snap Series 5 Cards (Collection Level 486+)
# Card 	Cost	Power	Card Ability
# Ajax (releases July 16)	4	4	Ongoing: +1 Power for each card in play afflicted with negative Power.
# Alioth	6	8	On Reveal: Remove the text from all unrevealed enemy cards here.
# Annihilus	4	6	On Reveal: Your cards with Power below 0 switch sides. Destroy those that can’t.
# Araña (Releases September 17)	2	2	Activate: Give the last card you played +2 Power and move it to the right.
# Arishem (releases July 2)	7	7	At the start of the game, +1 Max Energy. Shuffle 12 random cards into your deck.
# Baron Zemo	3	5	On Reveal: Recruit the lowest-Cost card from your opponent’s deck to your side of this location.
# Beta Ray Bill	4	5	On Reveal: Shuffle Stormbreaker into your deck.
# Black Knight	1	2	After you discard a card, add the Ebony Blade to your hand with that card’s Power (once per game)
# Black Swan	2	3	On Reveal: Until the end of your next turn, your 1-Cost cards cost 0.
# Blink	5	7	On Reveal: Swap the last card you played with a higher-Cost card from your deck.
# Blob	6	0	On Reveal: Merge cards from your deck into this until it gains 15 or more Power.
# Ongoing: Can’t be moved.
# Caiera	3	4	Ongoing: Your 1 and 6-Cost cards can’t be destroyed.
# Cassandra Nova (releases July 30)	3	1	On Reveal: Drain 1 Power from each card in your opponent’s deck.
# Cannonball	5	7	On Reveal: Move an enemy card away from here and add a Rock where it was. If it can’t move, destroy it to add the Rock.
# Copycat (releases July 23)	3	5	When you draw this, steal the text from the bottom card of your opponent’s deck.
# Corvus Glaive	3	5	On Reveal: Discard 2 cards from your hand to get +1 Max Energy.
# Cull Obsidian	4	10	You can only play this at a location with an Infinity Stone.
# Ongoing: Can’t be destroyed.
# Elsa Bloodstone	3	3	Each card you play to fill your side of a location gains +2 Power.
# Firestar ()	6	3	On Reveal: Each card you played last turn gains this card’s Power.ds
# Galactus	6	5	On Reveal: If you’re winning this location and this is your only card here, destroy all other locations.
# Gilgamesh	5	9
# On Reveal: +1 Power for each of your other cards in play with increased Power.

# Gorr the God Butcher (release date unknown)	0	0	On Reveal: Destroy all 6-cost cards, wherever they are.
# Grand Master	2	2	On Reveal: Move one of your other On Reveal cards here to the middle location. Its ability happens again.
# Gwenpool (releases July 9)	4	4	On Reveal: Pick a random card in your hand 4 times. Give +2 Power each time.
# High Evolutionary	4	4	At the start of the game, unlock the secret ability of all your cards with no abilities.
# Hope Summers	3	3	After you play a card here, you get +2 Energy next turn.
# Hulkling (Releases August 28)	6	11	At the start of the game, copy the text of a random 6-cost card.
# Hydra Bob (releases July 9)	2	5	After each turn, move to another location if you’re losing here.
# Iron Lad	4	6	On Reveal: Copy the text of your deck’s top card.
# Jeff the Baby Land Shark	2	3	You can move this once. Nothing can stop you from moving or playing this to any location.
# Kang	5	0	On Reveal: Look at what your opponent did, then restart the turn (without Kang).
# Loki	4	6	On Reveal: Transform your hand into cards from your opponent’s starting deck and give them -1 Cost.
# Ms. Marvel	4	4	Ongoing: Your adjacent locations with 2+ cards and no repeated Costs have +5 Power.
# Madame Web (Releases September 10)	2	3	Ongoing: You can move one of your other cards away from here each turn.
# Makkari	3	3	After the turn, runs from your hand to a random location. (if possible)
# Man-Thing	4	5	Ongoing: 1, 2, and 3-cost cards here have -2 Power.
# Marvel Boy (releases August 7)	3	2	After each turn, give 3 of your 1-cost cards +1 power
# Mobius M. Mobius	3	3	On Reveal: Your card’s costs can’t be increased and your opponent’s costs can’t be reduced.
# Mockingbird	5	9	Costs 1 less for each card you have in play that didn’t start in your deck.
# Namora	5	5	On Reveal: Give +5 Power to each of your cards alone at another location.
# Nico Minoru	1	2	On Reveal: After you play your next card, cast a spell (the spell changes each turn).
# Nocturne	3	5	You can move this once. When this moves, replace its location with a random new one.
# Pixie	1	3	On Reveal: Shuffle the base Costs of all cards in your deck that started there.
# Phastos	3	3	On Reveal: Give each card in your deck -1 Cost or +2 Power.
# Proxima Midnight	4	6	When this is discarded, jumps to your lowest-Power location (that isn’t full).
# Ravonna Renslayer	2	3	Ongoing: Your cards with 1 or less Power cost 1 less (minimum 1)
# Red Guardian	3	4	On Reveal: Remove the text of the lowest-Power enemy card here.
# Red Hulk	6	10	When your opponent ends a turn with unspent Energy, +3 Power (if in hand or in play)
# Sage	4	1	On Reveal: +2 Power for each different Power among all other cards here.
# Sasquatch	6	10	Costs 1 less for each card you played last turn.
# Scarlet Spider (Releases September 24)	4	5	Activate: Add an exact clone of this to another location.
# Sebastian Shaw	3	4	When this card permanently gains Power, gain +2 more Power (wherever this is).
# Sersei	5	7	On Reveal: Transform your other cards here into random cards that cost 1 more. (if able)
# Silver Sable (Releases September 3)	1	1	On Reveal: Steal 2 Power from the top card of your opponent’s deck.
# Skaar	6	11	Costs 2 less for each of your cards that has 10 or more power.
# Speed (releases August 21)	3	3	Ongoing: +1 Power for each turn in which you spent all your Energy.
# Thanos	6	10	Starts in your opening hand and shuffles the six Infinity Stones into your deck.
# Thanos (Mind Stone)	2	1	On Reveal: Draw 2 Stones from your deck.
# Thanos (Power Stone)	1	3	Ongoing: If you’ve played all 6 stones, Thanos has +10 Power. (wherever he is)
# Thanos (Reality Stone)	1	1	On Reveal: Transform this location into a new one.
# Thanos (Soul Stone)	1	1	On Reveal: Draw a card. Ongoing: Thanos can’t be discarded or destroyed.
# Thanos (Space Stone)	1	1	On Reveal: Draw a card. Ongoing: Nothing can stop you from playing or moving Thanos.
# Thanos (Time Stone)	1	1	On Reveal: Give Thanos -1 Cost. Draw a card.
# Thena	2	1	After each turn, +3 Power if you played (exactly) 2 cards.
# War Machine	4	6	On Reveal: Until the end of next turn, nothing can stop you from playing cards anywhere.
# Werewolf By Night	3	1	After you play an On Reveal card at another location, move there and gain +2 Power.
# White Widow	2	2	On Reveal: Add a -1-Power Widow’s Kiss to your opponent’s side here.
# Wiccan (releases August 14)	4	5	On Reveal: If you’ve spent all your Energy this game, +2 Max Energy
# US Agent	2	6	Ongoing: 4, 5, and 6-Cost cards here have -4 Power.
# Valentina	2	2	On Reveal: Add a random 6-cost card to your hand. Give it -2 Cost and -2 Power.
# X-23	1	2	On Reveal: Each player discards the lowest-Power card from their hand.
