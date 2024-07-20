from card import Card, Ability
import cards
from loguru import logger

def generate_all_cards():
    # Define the card abilities/effects here
    def punisher_effect(card, game, card_owner, location_index):
        location = game.locations[card.location]
        enemy_card_count = sum(1 for c in location.cards if c.owner != card_owner and c != card)  # Include the current card
        bonus_power = 1 * enemy_card_count
        card.power = card.base_power + bonus_power

    def star_lord_effect(card, game, card_owner, location_index):
        location = location_index
        opponent = 1 if card_owner == 0 else 0
        if any(c.owner == opponent and c.turn_played == game.current_turn for c in location.cards):
            return 3
        return 0

    star_lord_ability = Ability(star_lord_effect, "On Reveal")


    all_cards = [
        cards.Abomination(),
        cards.Cyclops(),
        cards.Hawkeye(),
        cards.Hulk(),
        cards.IronMan(),
        cards.Medusa(),
        cards.MistyKnight(),
        cards.ThePunisher(),
        Card("Quicksilver", 1, 2, ""),
        cards.Sentinel(),
        cards.Shocker(),
        Card("Star Lord", 2, 2, "On Reveal: If your opponent played a card here this turn, +3 Power.", star_lord_ability),
        cards.TheThing(),
    ]

    return all_cards
