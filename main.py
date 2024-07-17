from card import generate_all_cards
from location import generate_all_locations
from game import Game
from data import load_deck_data, printwinrate

from loguru import logger

def main():
    logger.info('Started')

    all_cards = generate_all_cards()
    all_locations = generate_all_locations()
    for i in range (1,1):
        game = Game()
        game.play_game()

    decks_data = load_deck_data('decks_data.json')
    printwinrate(decks_data)

    logger.info('Finished')


if __name__ == '__main__':
    main()







