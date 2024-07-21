from card import Card, Ability
import cards
from loguru import logger

def generate_all_cards():
    # Define the card abilities/effects here
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
        cards.StarLord(),
        cards.TheThing(),
    ]

    return all_cards
