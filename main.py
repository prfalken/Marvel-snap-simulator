from game import Game
from data import load_deck_data, printwinrate
from loguru import logger


def main():
    logger.info("Started")

    for _ in range(0, 1):
        game = Game()
        game.play_game()

    decks_data = load_deck_data("decks_data.json")
    printwinrate(decks_data)

    logger.info("Finished")


if __name__ == "__main__":
    main()
