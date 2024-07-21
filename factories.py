from cards import Card
from loguru import logger

def generate_all_cards():
    all_cards = [obj() for obj in Card.__subclasses__()]

    # all_cards = [
    #     cards.Abomination(),
    #     cards.Cyclops(),
    #     cards.Hawkeye(),
    #     cards.Hulk(),
    #     cards.IronMan(),
    #     cards.Medusa(),
    #     cards.MistyKnight(),
    #     cards.ThePunisher(),
    #     cards.Quicksilver(),
    #     cards.Sentinel(),
    #     cards.Shocker(),
    #     cards.StarLord(),
    #     cards.TheThing(),
    # ]

    return all_cards
