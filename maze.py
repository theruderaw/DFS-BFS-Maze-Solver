import pygame
import sys
from collections import deque

ROWS, COLS = 15, 15
CELL_SIZE = 40
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE + 140
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREY = (200, 200, 200)
PURPLE = (160, 32, 240)
DARK_GREY = (100, 100, 100)

color_map = {
    0: WHITE,   # empty
    1: BLACK,   # wall
    2: GREEN,   # start
    3: RED,     # end
    4: BLUE,    # visited (BFS/DFS)
    5: YELLOW,  # algorithm path
    6: ORANGE   # user path
}

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
start_cell = None
end_cell = None
placing_mode = "start"  # start, end, wall, user_solve
active_mode = "start"
user_path = []

buttons = [
    {"rect": pygame.Rect(10, ROWS*CELL_SIZE + 10, 80, 40), "color": GREEN, "text": "Start", "mode": "start"},
    {"rect": pygame.Rect(100, ROWS*CELL_SIZE + 10, 80, 40), "color": RED, "text": "End", "mode": "end"},
    {"rect": pygame.Rect(190, ROWS*CELL_SIZE + 10, 80, 40), "color": BLACK, "text": "Wall", "mode": "wall"},
    {"rect": pygame.Rect(280, ROWS*CELL_SIZE + 10, 80, 40), "color": BLUE, "text": "BFS", "mode": "bfs"},
    {"rect": pygame.Rect(370, ROWS*CELL_SIZE + 10, 80, 40), "color": ORANGE, "text": "DFS", "mode": "dfs"},
    {"rect": pygame.Rect(460, ROWS*CELL_SIZE + 10, 100, 40), "color": DARK_GREY, "text": "Reset", "mode": "reset"},
    {"rect": pygame.Rect(10, ROWS*CELL_SIZE + 60, 120, 40), "color": ORANGE, "text": "User Solve", "mode": "user_solve"},
    {"rect": pygame.Rect(140, ROWS*CELL_SIZE + 60, 120, 40), "color": PURPLE, "text": "Submit", "mode": "submit"}
]

def draw_grid():
    WIN.fill(WHITE)
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(WIN, color_map[grid[r][c]], (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(WIN, GREY, (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
    
    for button in buttons:
        rect = button["rect"]
        color = button["color"]
        if button["mode"] == active_mode:
            pygame.draw.rect(WIN, color, rect)
            pygame.draw.rect(WIN, YELLOW, rect, 4)
        else:
            pygame.draw.rect(WIN, color, rect)
            pygame.draw.rect(WIN, BLACK, rect, 2)

        text_surf = font.render(button["text"], True, WHITE)
        WIN.blit(text_surf, (rect.x + 5, rect.y + 10))

def get_cell_from_mouse(pos):
    x, y = pos
    if y >= ROWS * CELL_SIZE:
        return None
    return y // CELL_SIZE, x // CELL_SIZE

def show_message(text, duration=1500):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0,0,0,150))
    WIN.blit(overlay, (0,0))
    
    box_w, box_h = 400, 100
    box_rect = pygame.Rect((WIDTH-box_w)//2, (HEIGHT-box_h)//2, box_w, box_h)
    pygame.draw.rect(WIN, WHITE, box_rect, border_radius=10)
    pygame.draw.rect(WIN, BLACK, box_rect, 2, border_radius=10)

    msg_font = pygame.font.SysFont("Arial", 28)
    text_surf = msg_font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=box_rect.center)
    WIN.blit(text_surf, text_rect)

    pygame.display.update()
    pygame.time.delay(duration)

def run_algorithm(algo):
    if start_cell is None or end_cell is None:
        show_message("Place Start and End first!")
        return

    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] in (4,5):
                grid[r][c] = 0

    path = []

    if algo == "bfs":
        m, n = ROWS, COLS
        visited = [[False]*n for _ in range(m)]
        parent = [[None]*n for _ in range(m)]
        queue = deque([start_cell])
        visited[start_cell[0]][start_cell[1]] = True

        while queue:
            x, y = queue.popleft()
            if (x,y) == end_cell:
                break
            if (x,y) not in (start_cell, end_cell):
                grid[x][y] = 4
                draw_grid()
                pygame.display.update()
                pygame.time.delay(30)
            for dx, dy in [(1,0),(0,1),(0,-1),(-1,0)]:
                nx, ny = x+dx, y+dy
                if 0<=nx<m and 0<=ny<n and not visited[nx][ny] and grid[nx][ny]!=1:
                    visited[nx][ny] = True
                    parent[nx][ny] = (x,y)
                    queue.append((nx,ny))

        curr = end_cell
        while curr != start_cell:
            path.append(curr)
            curr = parent[curr[0]][curr[1]]
            if curr is None:
                path = []
                break
        path.append(start_cell)
        path.reverse()

    elif algo == "dfs":
        m, n = ROWS, COLS
        visited = [[False]*n for _ in range(m)]
        parent = [[None]*n for _ in range(m)]
        found = [False]

        def dfs_visit(x,y):
            if found[0]:
                return
            visited[x][y] = True
            if (x,y) not in (start_cell,end_cell):
                grid[x][y] = 4
                draw_grid()
                pygame.display.update()
                pygame.time.delay(30)
            if (x,y) == end_cell:
                found[0] = True
                return
            for dx, dy in [(1,0),(0,1),(0,-1),(-1,0)]:
                nx, ny = x+dx, y+dy
                if 0<=nx<m and 0<=ny<n and not visited[nx][ny] and grid[nx][ny]!=1:
                    parent[nx][ny] = (x,y)
                    dfs_visit(nx,ny)

        dfs_visit(*start_cell)

        curr = end_cell
        while curr != start_cell:
            path.append(curr)
            curr = parent[curr[0]][curr[1]]
            if curr is None:
                path = []
                break
        path.append(start_cell)
        path.reverse()

    for r,c in path:
        if grid[r][c] not in (2,3):
            grid[r][c] = 5
        draw_grid()
        pygame.display.update()
        pygame.time.delay(30)

def check_user_path():
    global grid, start_cell, end_cell, user_path
    if start_cell is None or end_cell is None:
        show_message("Place Start and End first!")
        return False
    if not user_path:
        show_message("Path is empty!")
        return False

    path_to_check = [start_cell] + user_path + [end_cell]

    for r,c in path_to_check:
        if grid[r][c] == 1:
            show_message("Hit a wall!")
            return False

    show_message("Maze solved correctly!", duration=1200)

    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    start_cell = None
    end_cell = None
    user_path = []
    return True

running = True
mouse_held = False

while running:
    clock.tick(FPS)
    draw_grid()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_held = True
            pos = pygame.mouse.get_pos()
            clicked_button = None
            for button in buttons:
                if button["rect"].collidepoint(pos):
                    clicked_button = button
                    break

            if clicked_button:
                mode = clicked_button["mode"]
                active_mode = mode
                if mode in ("start","end","wall","user_solve"):
                    placing_mode = mode
                    if mode=="user_solve":
                        user_path = []
                    print(f"Mode: {mode}")
                elif mode in ("bfs","dfs"):
                    run_algorithm(mode)
                elif mode=="reset":
                    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
                    start_cell = None
                    end_cell = None
                    user_path = []
                elif mode=="submit":
                    check_user_path()
                continue

            cell = get_cell_from_mouse(pos)
            if cell:
                r, c = cell
                if placing_mode=="start":
                    if start_cell:
                        sr,sc = start_cell
                        grid[sr][sc]=0
                    grid[r][c] = 2
                    start_cell = (r,c)
                elif placing_mode=="end":
                    if end_cell:
                        er,ec = end_cell
                        grid[er][ec]=0
                    grid[r][c] = 3
                    end_cell = (r,c)
                elif placing_mode=="wall":
                    if grid[r][c] not in (2,3):
                        grid[r][c] = 0 if grid[r][c]==1 else 1
                elif placing_mode=="user_solve":
                    if grid[r][c]==0 and (r,c) not in user_path:
                        grid[r][c] = 6
                        user_path.append((r,c))

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_held = False

        if event.type == pygame.MOUSEMOTION and mouse_held and placing_mode=="user_solve":
            cell = get_cell_from_mouse(pygame.mouse.get_pos())
            if cell:
                r, c = cell
                if grid[r][c]==0 and (r,c) not in user_path:
                    grid[r][c] = 6
                    user_path.append((r,c))

pygame.quit()
sys.exit()