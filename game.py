import pygame

BOARD_LENGTH = 64
OFFSET = 8


class Tile(object):
    def __init__(self, img="grass"):
        self.img = img
        

def init_images(tiles_used):
    images = dict()
    for t in tiles_used:
        images[t] = pygame.image.load("res/" + t + "_tile.png").convert()
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

def flush_events(pygame_events):
    for event in pygame_events.get():
        if event.type == pygame.QUIT:
            return 1
    return 0


def process_mouseclick(pos, board):
    x, y = pos[0] // 8, pos[1] // 8
    newTile = Tile("road_ver")
    board[x][y] = newTile


def main():
    pygame.init()
    screen = pygame.display.set_mode([BOARD_LENGTH * OFFSET, BOARD_LENGTH *
                                      OFFSET])
    board = make_board()

    pygame.display.set_caption("SamCity")
    pygame.display.update()

    tiles_used = ["grass", "road_ver", "road_hor"]
    images = init_images(tiles_used)

    display_board(screen, board, images)

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            return
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                process_mouseclick(event.pos, board)
            display_board(screen, board, images)

if __name__ == "__main__":
    main()
