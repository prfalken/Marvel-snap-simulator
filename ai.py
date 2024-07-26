import random
from location import Location
import copy

from loguru import logger


class AIPlayer:
    def __init__(self, game, player_id, all_cards):
        self.game = game
        self.player_id = player_id
        self.turn_energy_spent = 0
        self.energy = 1
        self.deck = self.draw_starting_deck(all_cards)
        self.starting_deck = copy.deepcopy(self.deck)
        self.discard_stack = []
        self.hand = self.draw_starting_hand(self.deck)
        self.played_cards = []

    def choose_card_and_location(self):
        valid_plays = []
        hand_ordered_by_energy_cost = sorted(
            self.hand, key=lambda card: card.energy_cost
        )
        for card in hand_ordered_by_energy_cost:
            if card.energy_cost <= self.energy:
                for location_id, location in enumerate(self.game.locations):
                    if Location.can_play_card_at_location(
                        card, location, self.game.current_turn, self.energy
                    ):
                        valid_plays.append((card, location_id))

        if valid_plays:
            return valid_plays[0], valid_plays[1]
        else:
            return None, None

    def draw_starting_deck(self, all_cards):
        deck = random.sample(all_cards, 12)
        for card in deck:
            card.owner_id = self.player_id
        return deck

    def draw_starting_hand(self, deck):
        quicksilver_card = next(
            (card for card in deck if card.name == "Quicksilver"), None
        )

        if quicksilver_card:
            deck.remove(quicksilver_card)  # Remove Quicksilver from the deck
            hand = random.sample(deck, 3)  # Draw only 3 cards
            for card in hand:  # Add this loop to remove the 3 cards from the deck
                deck.remove(card)
            hand.append(quicksilver_card)  # Add Quicksilver to the hand
            logger.debug(f"Player {self.player_id} starts with Quicksilver")
        else:
            hand = random.sample(deck, 4)  # Draw 4 cards
            for card in hand:
                deck.remove(card)  # Remove drawn cards from the deck

        return hand

    def draw_card(self):
        if not self.deck:
            return
        new_card = random.choice(self.deck)
        if len(self.hand) < 7:
            self.hand.append(new_card)
            self.deck.remove(new_card)
