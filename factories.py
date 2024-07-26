from cards import Card
from loguru import logger


def generate_all_cards():
    all_cards = [obj() for obj in Card.__subclasses__()]
    for card in all_cards:
        if not card.ownable:
            all_cards.remove(card)

    return all_cards
