from game import Game


# main function
def main():
    # create game object
    game = Game()

    # game loop
    while game.running:
        game.run()


# call main function
if __name__ == '__main__':
    main()
