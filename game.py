from collections import namedtuple
import pygame


BOARD_LENGTH = 64
OFFSET = 8
IMAGES = ("grass", "road_4way", "road_eastnorth", "road_eastsouth", "road_hor",
"road_northeastsouth", "road_ver", "road_westeastsouth", "road_westnortheast",
"road_westnorth", "road_westsouthnorth", "road_westsouth", "house", "bulldozer")

DIRECTIONS = namedtuple('DIRECTIONS',
                        ['North', 'South', 'East', 'West'])(0, 1, 2, 3)

STATE = namedtuple('STATE', ['Roads', 'Houses', 'Bulldozer'])(0, 1, 2)

GREY = (214, 214, 214)

class Tile(object):
    def __init__(self, kind="empty", img="grass"):
        self.kind = kind
        self.img = img

class Overlay(object):
    def __init__(self):
        self.coords = 0, 0
        self.road_rel = 4, 4
        self.house_rel = 16, 4
        self.bulldozer_rel = 4, 16
        self.x_offset = 28
        self.y_offset = 28
        self.state = STATE.Roads


def init_images(tiles_used):
    images = {}
    for t in tiles_used:
        images[t] = pygame.image.load("res/" + t + "_tile.png").convert()
    return images


def make_board():
    spots = [[] for i in range(BOARD_LENGTH)]
    for row in spots:
        for i in range(BOARD_LENGTH):
            row.append(Tile())
    return spots


def display_board(screen, board, overlay, images):
    for x, row in enumerate(board):
        for y, tile in enumerate(row):
            screen.blit(images[tile.img], (x*OFFSET, y*OFFSET))
    overlay_rect = pygame.Rect(overlay.coords, (28, 28))
    screen.fill(GREY, overlay_rect)
    screen.blit(images["road_ver"], 
                (overlay.coords[0] + overlay.road_rel[0],
                 overlay.coords[1] + overlay.road_rel[1]))
    screen.blit(images["house"],
                (overlay.coords[0] + overlay.house_rel[0],
                 overlay.coords[1] + overlay.house_rel[1]))
    screen.blit(images["bulldozer"],
                (overlay.coords[0] + overlay.bulldozer_rel[0],
                 overlay.coords[1] + overlay.bulldozer_rel[1]))
    pygame.display.update()


def validate_points(points):
    valid_points = []
    for point in points:
        x, y = point
        valid = True
        if x < 0 or y < 0:
            valid = False
        if x >= BOARD_LENGTH or y >= BOARD_LENGTH:
            valid = False
        if valid:
            valid_points.append(point)
    return valid_points


def flush_events(pygame_events):
    for event in pygame_events.get():
        if event.type == pygame.QUIT:
            return 1
    return 0

def validate_roads(points, board):
    valid_roads = []
    if points:
        for point in points:
            x, y = point
            if board[x][y].kind == "road":
                valid_roads.append(point)
        return valid_roads
    else:
        return valid_roads


def adjacent_roads(pos, board):
    x, y = pos
    points = ((x, y-1), (x+1, y), (x, y+1), (x-1, y))
    points = validate_points(points)
    return validate_roads(points, board)


def process_overlay(pos, overlay):
    x, y = pos[0] - overlay.coords[0], pos[1] - overlay.coords[1]
    if (x >= overlay.road_rel[0] and y >= overlay.house_rel[1]
        and x <= overlay.road_rel[0] + OFFSET
        and y <= overlay.road_rel[1] + OFFSET):
        overlay.state = STATE.Roads
    elif (x >= overlay.house_rel[0] and y >= overlay.house_rel[1]
        and x <= overlay.house_rel[0] + OFFSET
        and y <= overlay.house_rel[1] + OFFSET):
        overlay.state = STATE.Houses
    elif (x >= overlay.bulldozer_rel[0] and y >= overlay.bulldozer_rel[1]
        and x <= overlay.bulldozer_rel[0] + OFFSET
        and y <= overlay.bulldozer_rel[1] + OFFSET):
        overlay.state = STATE.Bulldozer


def process_house(pos, board):
    x, y = pos
    if board[x][y].kind != "road":
        board[x][y] = Tile("house", "house");


def process_bulldozer(pos, board):
    x, y = pos
    board[x][y] = Tile()


def process_mouseclick(pos, board, overlay, roads):
    x, y = pos[0], pos[1]
    if (x >= overlay.coords[0] and y >= overlay.coords[1]
        and x <= overlay.coords[0] + overlay.x_offset
        and y <= overlay.coords[1] + overlay.y_offset):
        process_overlay((x, y), overlay)
    elif overlay.state == STATE.Roads:
        process_roads((x // 8, y // 8), board, roads)
    elif overlay.state == STATE.Houses:
        process_house((x // 8, y // 8), board)
    elif overlay.state == STATE.Bulldozer:
        process_bulldozer((x // 8, y // 8), board)


def get_directions(pos, points):
    dirs = set()
    x, y = pos
    for point in points:
        xx, yy = point
        if x == xx:
            if y - 1 == yy:
                dirs.add(DIRECTIONS.North)
            if y + 1 == yy:
                dirs.add(DIRECTIONS.South)
        if y == yy:
            if x + 1 == xx:
                dirs.add(DIRECTIONS.East)
            if x - 1 == xx:
                dirs.add(DIRECTIONS.West)
    return dirs


def pick_road_img(dirs):
    dirs_index = 0
    if DIRECTIONS.North in dirs:
        dirs_index += 8
    if DIRECTIONS.South in dirs:
        dirs_index += 4
    if DIRECTIONS.East in dirs:
        dirs_index += 2
    if DIRECTIONS.West in dirs:
        dirs_index += 1
    return dirs_index


def process_roads(pos, board, master_roads):
    roads = adjacent_roads(pos, board)
    x, y = pos
    # If there are no roads next to this one
    if len(roads) == 0:
        board[x][y] = Tile("road", "road_hor")
    else:
        dirs = get_directions(pos, roads) 
        board[x][y] = master_roads[pick_road_img(dirs)]
        for road in roads:
            n_roads = adjacent_roads(road, board)
            n_dirs = get_directions(road, n_roads)
            board[road[0]][road[1]] = master_roads[pick_road_img(n_dirs)]


def init_roads():
    roads = list()
    roads.append(Tile("road", "road_hor")) # None
    roads.append(Tile("road", "road_hor")) # West
    roads.append(Tile("road", "road_hor")) # East
    roads.append(Tile("road", "road_hor")) # East, west
    roads.append(Tile("road", "road_ver")) # South
    roads.append(Tile("road", "road_westsouth")) # South, west
    roads.append(Tile("road", "road_eastsouth")) # South, east
    roads.append(Tile("road", "road_westeastsouth")) # South, east, west
    roads.append(Tile("road", "road_ver")) # North
    roads.append(Tile("road", "road_westnorth")) # North, west
    roads.append(Tile("road", "road_eastnorth")) # North, east
    roads.append(Tile("road", "road_westnortheast")) # North, east, west
    roads.append(Tile("road", "road_ver")) # North, south
    roads.append(Tile("road", "road_westsouthnorth")) # North, south, west
    roads.append(Tile("road", "road_northeastsouth")) # North, south, east
    roads.append(Tile("road", "road_4way")) # North, south, east, west
    return roads
    


def main():
    pygame.init()
    screen = pygame.display.set_mode([BOARD_LENGTH * OFFSET, BOARD_LENGTH *
                                      OFFSET])
    board = make_board()
    overlay = Overlay()

    pygame.display.set_caption("SamCity")
    pygame.display.update()

    images = init_images(IMAGES)
    roads = init_roads()

    display_board(screen, board, overlay, images)

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            return
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                process_mouseclick(event.pos, board, overlay, roads)
            display_board(screen, board, overlay, images)

if __name__ == "__main__":
    main()
