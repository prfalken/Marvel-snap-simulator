from location import generate_all_locations
from game import Game
from data import load_deck_data
from data import printwinrate

from loguru import logger

def main():
    logger.info('Started')

    for i in range (0,10):
        game = Game()
        game.play_game()

    decks_data = load_deck_data('decks_data.json')
    printwinrate(decks_data)

    logger.info('Finished')


if __name__ == '__main__':
    main()







