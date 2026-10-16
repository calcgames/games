from casioplot import set_pixel, draw_string, clear_screen, show_screen, getkey
from random import randint

K_UP = 14
K_DOWN = 34
K_LEFT = 23
K_RIGHT = 25
K_OK = 24
K_QUIT = 21

CW = 10
BW = 10
BH = 18
X0 = 216
Y0 = 8
SW = 384
SH = 192

BG = (16, 16, 26)
WELL = (30, 30, 44)
WELL_G = (42, 42, 60)
FRAME = (110, 115, 140)
FRAME_D = (58, 60, 78)
TXT = (232, 236, 248)
DIM = (128, 134, 160)

SHAPES = [
    [[(0, 1), (1, 1), (2, 1), (3, 1)], [(2, 0), (2, 1), (2, 2), (2, 3)]],
    [[(1, 0), (2, 0), (1, 1), (2, 1)]],
    [[(1, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (1, 1), (2, 1), (1, 2)],
     [(0, 1), (1, 1), (2, 1), (1, 2)], [(1, 0), (0, 1), (1, 1), (1, 2)]],
    [[(1, 0), (2, 0), (0, 1), (1, 1)], [(1, 0), (1, 1), (2, 1), (2, 2)]],
    [[(0, 0), (1, 0), (1, 1), (2, 1)], [(2, 0), (1, 1), (2, 1), (1, 2)]],
    [[(0, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (2, 0), (1, 1), (1, 2)],
     [(0, 1), (1, 1), (2, 1), (2, 2)], [(1, 0), (1, 1), (0, 2), (1, 2)]],
    [[(2, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (1, 1), (1, 2), (2, 2)],
     [(0, 1), (1, 1), (2, 1), (0, 2)], [(0, 0), (1, 0), (1, 1), (1, 2)]],
]

BASE = [(40, 200, 224), (232, 196, 48), (174, 74, 200), (72, 198, 88),
        (220, 66, 66), (58, 96, 214), (236, 142, 44)]
LIT = [(150, 244, 255), (255, 244, 150), (232, 170, 250), (170, 250, 178),
       (255, 160, 160), (140, 178, 255), (255, 206, 140)]
SHD = [(16, 110, 130), (130, 104, 12), (92, 30, 110), (26, 110, 38),
       (118, 22, 22), (22, 44, 120), (128, 68, 10)]

board = []
DLY = 300


def pause(n):
    for _w in range(n):
        pass


def fill(x, y, w, h, c):
    if x < 0 or y < 0 or x + w > SW or y + h > SH:
        return
    for j in range(y, y + h):
        for i in range(x, x + w):
            set_pixel(i, j, c)


def block(x, y, k):
    fill(x, y, CW - 1, CW - 1, BASE[k])
    fill(x, y, CW - 1, 1, LIT[k])
    fill(x, y, 1, CW - 1, LIT[k])
    fill(x, y + CW - 2, CW - 1, 1, SHD[k])
    fill(x + CW - 2, y, 1, CW - 1, SHD[k])


def empty(cx, cy):
    x, y = X0 + cx * CW, Y0 + cy * CW
    fill(x, y, CW - 1, CW - 1, WELL)
    set_pixel(x + CW // 2, y + CW // 2, WELL_G)


def cell(cx, cy, k):
    if k < 0:
        empty(cx, cy)
    else:
        block(X0 + cx * CW, Y0 + cy * CW, k)


def well():
    fill(X0 - 4, Y0 - 4, BW * CW + 7, BH * CW + 7, FRAME_D)
    fill(X0 - 2, Y0 - 2, BW * CW + 3, BH * CW + 3, FRAME)
    fill(X0, Y0, BW * CW, BH * CW, WELL)
    for cy in range(BH):
        for cx in range(BW):
            empty(cx, cy)


def panel():
    draw_string(22, 10, "TETRIS", TXT, "large")
    fill(22, 34, 150, 2, FRAME)
    draw_string(22, 46, "NEXT", DIM, "small")
    fill(20, 58, 74, 62, FRAME_D)
    fill(22, 60, 70, 58, WELL)
    draw_string(22, 130, "SCORE", DIM, "small")
    draw_string(22, 160, "LINES", DIM, "small")
    draw_string(110, 130, "LEVEL", DIM, "small")


def stats(score, lines, level):
    fill(22, 142, 84, 16, BG)
    draw_string(22, 142, str(score), TXT, "medium")
    fill(22, 172, 60, 16, BG)
    draw_string(22, 172, str(lines), TXT, "medium")
    fill(110, 142, 40, 16, BG)
    draw_string(110, 142, str(level), TXT, "medium")


def next_box(kind):
    fill(22, 60, 70, 58, WELL)
    for (dx, dy) in SHAPES[kind][0]:
        block(30 + dx * CW, 70 + dy * CW, kind)


def redraw_rows(top):
    for y in range(top + 1):
        for x in range(BW):
            cell(x, y, board[y][x])


def hit(shape, px, py):
    for (dx, dy) in shape:
        x, y = px + dx, py + dy
        if x < 0 or x >= BW or y >= BH:
            return True
        if y >= 0 and board[y][x] >= 0:
            return True
    return False


def flash(rows):
    for c in ((255, 255, 255), (200, 210, 230)):
        for y in rows:
            fill(X0, Y0 + y * CW, BW * CW - 1, CW - 1, c)
        show_screen()


def play():
    global board
    board = [[-1] * BW for _ in range(BH)]
    clear_screen()
    fill(0, 0, SW, SH, BG)
    well()
    panel()
    score = 0
    lines = 0
    level = 1
    stats(score, lines, level)

    kind = randint(0, 6)
    nxt = randint(0, 6)
    next_box(nxt)
    rot = 0
    px, py = 3, -1
    tick = 0
    speed = 10
    prev = []
    last = -1
    rep = 0
    show_screen()

    while True:
        shape = SHAPES[kind][rot]
        k = getkey()
        pause(DLY)
        if k == last:
            rep += 1
            if k == K_LEFT or k == K_RIGHT:
                if rep < 4 or rep % 2:
                    k = 0
            elif k != K_DOWN and k != K_QUIT and k != 22:
                k = 0
        else:
            rep = 0
            last = k
        moved = False
        landed = False

        if k == K_QUIT or k == 22:
            return False
        elif k == K_LEFT:
            if not hit(shape, px - 1, py):
                px -= 1
                moved = True
        elif k == K_RIGHT:
            if not hit(shape, px + 1, py):
                px += 1
                moved = True
        elif k == K_UP:
            nr = (rot + 1) % len(SHAPES[kind])
            ns = SHAPES[kind][nr]
            if not hit(ns, px, py):
                rot, shape, moved = nr, ns, True
            elif not hit(ns, px - 1, py):
                rot, px, shape, moved = nr, px - 1, ns, True
        elif k == K_DOWN:
            if not hit(shape, px, py + 1):
                py += 1
                moved = True
                tick = 0
        elif k == K_OK:
            while not hit(shape, px, py + 1):
                py += 1
            landed = True
            moved = True

        if not landed:
            tick += 1
            if tick >= speed:
                tick = 0
                if hit(shape, px, py + 1):
                    landed = True
                else:
                    py += 1
                    moved = True

        if moved or landed:
            for (x, y) in prev:
                if y >= 0:
                    empty(x, y)
            prev = []
            for (dx, dy) in shape:
                x, y = px + dx, py + dy
                if y >= 0:
                    cell(x, y, kind)
                    prev.append((x, y))

        if landed:
            for (dx, dy) in shape:
                x, y = px + dx, py + dy
                if y < 0:
                    fill(X0 - 4, 76, BW * CW + 7, 40, BG)
                    draw_string(X0 - 2, 84, "GAME", (255, 90, 90), "large")
                    draw_string(X0 - 2, 104, "OVER", (255, 90, 90), "large")
                    show_screen()
                    while True:
                        k = getkey()
                        if k == K_OK:
                            return True
                        if k == K_QUIT:
                            return False
                board[y][x] = kind
            prev = []

            full = []
            for y in range(BH):
                done = True
                for x in range(BW):
                    if board[y][x] < 0:
                        done = False
                        break
                if done:
                    full.append(y)

            if full:
                flash(full)
                for y in full:
                    del board[y]
                    board.insert(0, [-1] * BW)
                lines += len(full)
                score += (40, 100, 300, 1200)[len(full) - 1] * level
                level = 1 + lines // 10
                speed = max(4, 10 - lines // 6)
                redraw_rows(full[-1])
                stats(score, lines, level)

            kind = nxt
            nxt = randint(0, 6)
            next_box(nxt)
            rot = 0
            px, py = 3, -1

        if moved or landed:
            show_screen()


while play():
    pass
