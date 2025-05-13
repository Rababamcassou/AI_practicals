import pygame
import heapq

# --- Configuration ---
WIDTH = 20
HEIGHT = 20
MARGIN = 2
ROWS = 20
COLS = 20
GRID_OFFSET_X = 40
GRID_OFFSET_Y = 40

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Source and destination
src = (0, 0)
dest = (19, 19)
path = []

# --- Classes ---

class Field:
    def __init__(self, row, col, is_obstacle=False, is_start=False, is_goal=False):
        self.row = row
        self.col = col
        self.is_obstacle = is_obstacle
        self.is_start = is_start
        self.is_goal = is_goal
        self.color = WHITE

    def draw(self, screen):
        color = self.color
        if self.is_obstacle:
            color = BLACK
        elif self.is_start:
            color = GREEN
        elif self.is_goal:
            color = BLUE

        x = (MARGIN + WIDTH) * self.col + MARGIN + GRID_OFFSET_X
        y = size[1] - ((MARGIN + HEIGHT) * (self.row + 1)) - MARGIN - GRID_OFFSET_Y
        pygame.draw.rect(screen, color, [x, y, WIDTH, HEIGHT])


class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[Field(r, c) for c in range(cols)] for r in range(rows)]

        # Obstacles
        for y in range(9, 20):
            self.grid[16][y].is_obstacle = True
        for y in range(0, 10):
            self.grid[9][y].is_obstacle = True
        for x in range(4, 10):
            self.grid[x][9].is_obstacle = True

        # Start and goal
        self.grid[src[0]][src[1]].is_start = True
        self.grid[dest[0]][dest[1]].is_goal = True

    def draw(self, screen):
        for row in self.grid:
            for field in row:
                field.draw(screen)


class Cell:
    def __init__(self):
        self.parent = (-1, -1)
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0


def is_valid(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS

def is_unblocked(grid, row, col):
    return grid[row][col] == 1

def is_destination(row, col, dest):
    return (row, col) == dest

def calculate_h_value(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

def trace_path(cell_details, dest):
    row, col = dest
    path = []

    while cell_details[row][col].parent != (row, col):
        path.append((row, col))
        row, col = cell_details[row][col].parent
    path.append((row, col))
    path.reverse()
    return path


def a_star_search(grid, src, dest):
    closed_list = [[False] * COLS for _ in range(ROWS)]
    cell_details = [[Cell() for _ in range(COLS)] for _ in range(ROWS)]

    sr, sc = src
    cell_details[sr][sc].f = 0
    cell_details[sr][sc].g = 0
    cell_details[sr][sc].parent = (sr, sc)

    open_list = []
    heapq.heappush(open_list, (0.0, sr, sc))

    while open_list:
        _, r, c = heapq.heappop(open_list)
        closed_list[r][c] = True

        directions = [(0,1),(1,0),(-1,0),(0,-1), (1,1),(1,-1),(-1,1),(-1,-1)]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc) and is_unblocked(grid, nr, nc) and not closed_list[nr][nc]:
                if is_destination(nr, nc, dest):
                    cell_details[nr][nc].parent = (r, c)
                    path = trace_path(cell_details, dest)
                    yield {'type': 'done', 'path': path}
                    return

                g_new = cell_details[r][c].g + 1.0
                h_new = calculate_h_value(nr, nc, dest)
                f_new = g_new + h_new

                if cell_details[nr][nc].f > f_new:
                    cell_details[nr][nc].f = f_new
                    cell_details[nr][nc].g = g_new
                    cell_details[nr][nc].h = h_new
                    cell_details[nr][nc].parent = (r, c)
                    heapq.heappush(open_list, (f_new, nr, nc))

        yield {'type': 'searching', 'open': open_list.copy(), 'closed': closed_list.copy()}


# ---
pygame.init()
grid_obj = Grid(ROWS, COLS)
size = (500, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
done = False


grid_matrix = [[1 if not f.is_obstacle else 0 for f in row] for row in grid_obj.grid]
search_gen = a_star_search(grid_matrix, src, dest)

# --- main Loop ---
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(BLACK)
    grid_obj.draw(screen)


    try:
        result = next(search_gen)
        if result['type'] == 'done':
            path = result['path']
            searching = False
        elif result['type'] == 'searching':
            open_nodes = result['open']
            closed_nodes = result['closed']
    except StopIteration:
        pass

    # closed list
    for r in range(ROWS):
        for c in range(COLS):
            if closed_nodes[r][c]:
                x = (MARGIN + WIDTH) * c + MARGIN + GRID_OFFSET_X
                y = size[1] - ((MARGIN + HEIGHT) * (r + 1)) - MARGIN - GRID_OFFSET_Y
                pygame.draw.rect(screen, GREEN, [x, y, WIDTH, HEIGHT])

    #open list
    for _, r, c in open_nodes:
        x = (MARGIN + WIDTH) * c + MARGIN + GRID_OFFSET_X
        y = size[1] - ((MARGIN + HEIGHT) * (r + 1)) - MARGIN - GRID_OFFSET_Y
        pygame.draw.rect(screen, BLUE, [x, y, WIDTH, HEIGHT])

    #draw final path if found
    for row, col in path:
        x = (MARGIN + WIDTH) * col + MARGIN + GRID_OFFSET_X
        y = size[1] - ((MARGIN + HEIGHT) * (row + 1)) - MARGIN - GRID_OFFSET_Y
        pygame.draw.rect(screen, RED, [x, y, WIDTH, HEIGHT])

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
