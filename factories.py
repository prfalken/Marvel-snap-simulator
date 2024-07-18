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

    punisher_ability = Ability(punisher_effect, "Ongoing")
    star_lord_ability = Ability(star_lord_effect, "On Reveal")


    all_cards = [
        cards.Abomination(),
        cards.Cyclops(),
        cards.Hawkeye(),
        cards.Hulk(),
        Card("Iron Man", 5, 0, "Ongoing: Your total Power is doubled at this Location."),
        cards.Medusa(),
        Card("Misty Knight", 1, 2, "No ability"),
        Card("The Punisher", 3, 2, "Ongoing: +1 Power for each opposing card at this Location.", punisher_ability),
        Card("Quicksilver", 1, 2, ""),
        cards.Sentinel(),
        Card("Shocker", 2, 3, "No ability"),
        Card("Star Lord", 2, 2, "On Reveal: If your opponent played a card here this turn, +3 Power.", star_lord_ability),
        Card("The Thing", 4, 6, "No ability"),
    ]

    sentinel_card = next(card for card in all_cards if card.name == "Sentinel")

    return all_cards
