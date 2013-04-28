import pygame

BOARD_LENGTH = 64
OFFSET = 8


class Tile(object):
    def __init__(self, img="grass"):
        self.img = img
        
def init_images(tiles_used):
    images = dict()
    for t in tiles_used:
        if t == "grass":
            images[t] = pygame.image.load("grass_tile.png").convert()
    return images


def make_board():
    spots = [[] for i in range(BOARD_LENGTH)]
    for row in spots:
        for i in range(BOARD_LENGTH):
            row.append(Tile())
    return spots

def display_board(screen, board, images):
    for x, row in enumerate(board):
        for y, tile in enumerate(row):
            screen.blit(images[tile.img], (x*OFFSET, y*OFFSET))
    pygame.display.update()

def main():
    pygame.init()
    screen = pygame.display.set_mode([BOARD_LENGTH * OFFSET, BOARD_LENGTH *
                                      OFFSET])
    board = make_board()

    pygame.display.set_caption("SamCity")
    pygame.display.update()

    tiles_used = ["grass"]
    images = init_images(tiles_used)

    display_board(screen, board, images)
    x = 0

    while x == 0:
        x = 0

if __name__ == "__main__":
    main()
