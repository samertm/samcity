import pygame

BOARD_LENGTH = 256
OFFSET = 8

class Tile(object):
    def __init__(self, type="blank"):
        self.type = type

    def get_tile(self):
        if self.type == "blank":
            return pygame.image.load("grass_tile.png")

def make_board():
    spots = [[] for i in range(BOARD_LENGTH)]
    for row in spots:
        for i in range(BOARD_LENGTH):
            row.append(Tile())
    return spots

def display_board(screen, board):
    for x, row in enumerate(board):
        for y, tile in enumerate(row):
            if tile.get_tile() is None:
                print "what the fuckkk"
            else:
                screen.blit(tile.get_tile(), (x*OFFSET, y*OFFSET))
    pygame.display.update()

def main():
    pygame.init()
    screen = pygame.display.set_mode([BOARD_LENGTH * OFFSET, BOARD_LENGTH *
                                      OFFSET])
    board = make_board()

    pygame.display.set_caption("SamCity")
    pygame.display.update()
    display_board(screen, board)
    x = 0

    while x == 0:
        x = 0

if __name__ == "__main__":
    main()
