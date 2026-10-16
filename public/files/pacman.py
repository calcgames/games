from casioplot import set_pixel, draw_string, clear_screen, show_screen, getkey
from random import randint

K_LEFT = 23
K_RIGHT = 25
K_UP = 14
K_DOWN = 34
K_OK = 24
K_QUIT = 21

CW = 12
GW = 32
GH = 16
POLL = 5
DELAY = 700

BG = (8, 8, 20)
WALL = (36, 48, 200)
WALL_L = (90, 110, 255)
DOT = (250, 232, 180)
POW = (255, 190, 60)
PAC = (255, 226, 40)
EYE = (250, 250, 250)
PUP = (30, 30, 90)
SCARED = (60, 80, 220)
TEXT = (255, 255, 255)
GCOL = [(230, 50, 50), (245, 150, 200), (80, 220, 230), (245, 165, 60)]


grid = []


def fill(x, y, w, h, c):
    for j in range(y, y + h):
        for i in range(x, x + w):
            set_pixel(i, j, c)


def draw_cell(cx, cy):
    x, y = cx * CW, cy * CW
    t = grid[cy][cx]
    if t == "#":
        fill(x, y, CW, CW, WALL)
        fill(x, y, CW, 2, WALL_L)
        fill(x, y, 2, CW, WALL_L)
    else:
        fill(x, y, CW, CW, BG)
        if t == ".":
            fill(x + 5, y + 5, 3, 3, DOT)
        elif t == "o":
            fill(x + 3, y + 3, 6, 6, POW)
            fill(x + 4, y + 2, 4, 8, POW)


def draw_pac(cx, cy, d):
    x, y = cx * CW, cy * CW
    fill(x + 1, y + 1, CW - 2, CW - 2, PAC)
    fill(x + 1, y + 1, 2, 2, BG)
    fill(x + CW - 3, y + 1, 2, 2, BG)
    fill(x + 1, y + CW - 3, 2, 2, BG)
    fill(x + CW - 3, y + CW - 3, 2, 2, BG)
    for i in range(4):
        if d == 0:
            fill(x + CW - 1 - i, y + 5 - i, 1, 2 + i * 2, BG)
        elif d == 1:
            fill(x + i, y + 5 - i, 1, 2 + i * 2, BG)
        elif d == 2:
            fill(x + 5 - i, y + i, 2 + i * 2, 1, BG)
        else:
            fill(x + 5 - i, y + CW - 1 - i, 2 + i * 2, 1, BG)


def draw_ghost(cx, cy, n, scared):
    x, y = cx * CW, cy * CW
    c = SCARED if scared else GCOL[n]
    fill(x + 1, y + 2, CW - 2, CW - 4, c)
    fill(x + 2, y + 1, CW - 4, 2, c)
    for i in range(0, CW - 2, 4):
        fill(x + 1 + i, y + CW - 2, 2, 2, c)
    fill(x + 3, y + 4, 3, 3, EYE)
    fill(x + 7, y + 4, 3, 3, EYE)
    if not scared:
        fill(x + 4, y + 5, 2, 2, PUP)
        fill(x + 8, y + 5, 2, 2, PUP)


DX = (1, -1, 0, 0)
DY = (0, 0, -1, 1)
BS = ((15, 7), (29, 13), (29, 1), (1, 13))
DIRS = {25: 0, 23: 1, 14: 2, 34: 3}


def pause(n):
    for _w in range(n):
        pass


def gen():
    global grid
    grid = [["#"] * GW for _r in range(GH)]
    grid[1][1] = " "
    st = [(1, 1)]
    while st:
        x, y = st[-1]
        nb = []
        for d in range(4):
            nx, ny = x + DX[d] * 2, y + DY[d] * 2
            if 1 <= nx <= GW - 3 and 1 <= ny <= GH - 3 and grid[ny][nx] == "#":
                nb.append(d)
        if nb:
            d = nb[randint(0, len(nb) - 1)]
            grid[y + DY[d]][x + DX[d]] = " "
            grid[y + DY[d] * 2][x + DX[d] * 2] = " "
            st.append((x + DX[d] * 2, y + DY[d] * 2))
        else:
            st.pop()
    for y in range(1, GH - 1):
        grid[y][GW - 2] = " "
    for x in range(1, GW - 1):
        grid[GH - 2][x] = " "
    for _i in range(45):
        x, y = randint(2, GW - 3), randint(2, GH - 3)
        if grid[y][x] == "#" and ((grid[y][x - 1] == " " and grid[y][x + 1] == " ") or
                                  (grid[y - 1][x] == " " and grid[y + 1][x] == " ")):
            grid[y][x] = " "
    n = 0
    for y in range(GH):
        for x in range(GW):
            if grid[y][x] == " ":
                grid[y][x] = "."
                n += 1
    for (x, y) in ((1, 7), (29, 7), (15, 1), (15, 13)):
        grid[y][x] = "o"
    for (x, y) in BS + ((1, 1),):
        if grid[y][x] == ".":
            grid[y][x] = " "
            n -= 1
    return n


def open_at(cx, cy):
    return 0 <= cx < GW and 0 <= cy < GH and grid[cy][cx] != "#"


def hud(score, lv, lives):
    fill(100, 0, 190, 12, BG)
    draw_string(102, 0, "score " + str(score) + "  lv" + str(lv), TEXT, "small")
    draw_string(246, 0, "lives " + str(lives), PAC, "small")


def banner(msg, col, sub):
    fill(70, 76, 250, 46, BG)
    draw_string(84, 80, msg, col, "large")
    draw_string(84, 106, sub, TEXT, "small")
    show_screen()


def wait():
    last = -1
    while True:
        k = getkey()
        if k != last:
            last = k
            if k == K_OK or k == K_QUIT or k == 22:
                return k


def play(lv, score, lives):
    left = gen()
    clear_screen()
    for cy in range(GH):
        for cx in range(GW):
            draw_cell(cx, cy)
    px, py, pd, nd, sc = 1, 1, 0, 0, 0
    bs = []
    for n in range(4):
        bs.append([BS[n][0], BS[n][1], n, n])
    poll = max(2, POLL - lv // 3)
    draw_pac(px, py, pd)
    for b in bs:
        draw_ghost(b[0], b[1], b[2], 0)
    hud(score, lv, lives)
    hs = score
    show_screen()
    while True:
        for _p in range(poll):
            k = getkey()
            if k == K_QUIT or k == 22:
                return -1, score, lives
            nd = DIRS.get(k, nd)
            pause(DELAY)
        if open_at(px + DX[nd], py + DY[nd]):
            pd = nd
        if open_at(px + DX[pd], py + DY[pd]):
            draw_cell(px, py)
            px += DX[pd]
            py += DY[pd]
            t = grid[py][px]
            if t == "." or t == "o":
                grid[py][px] = " "
                left -= 1
                score += 10 if t == "." else 50
                if t == "o":
                    sc = 14
        for b in bs:
            draw_cell(b[0], b[1])
            ops = []
            for d in range(4):
                if d != (b[3] ^ 1) and open_at(b[0] + DX[d], b[1] + DY[d]):
                    ops.append(d)
            if not ops and open_at(b[0] + DX[b[3] ^ 1], b[1] + DY[b[3] ^ 1]):
                ops.append(b[3] ^ 1)
            if ops:
                if sc or randint(0, 3) == 0:
                    d = ops[randint(0, len(ops) - 1)]
                else:
                    d = ops[0]
                    bd = 999
                    for c in ops:
                        dist = abs(b[0] + DX[c] - px) + abs(b[1] + DY[c] - py)
                        if dist < bd:
                            d, bd = c, dist
                b[3] = d
                b[0] += DX[d]
                b[1] += DY[d]
        for b in bs:
            if b[0] == px and b[1] == py:
                if sc:
                    score += 200
                    b[0], b[1] = BS[b[2]]
                else:
                    lives -= 1
                    if lives <= 0:
                        banner("GAME OVER", (255, 80, 80), str(score) + "  OK retry  BACK quit")
                        return (0 if wait() == K_OK else -1), score, lives
                    draw_cell(px, py)
                    for m in bs:
                        draw_cell(m[0], m[1])
                        m[0], m[1] = BS[m[2]]
                    px, py = 1, 1
                    hud(score, lv, lives)
        for b in bs:
            draw_ghost(b[0], b[1], b[2], sc)
        draw_pac(px, py, pd)
        if sc:
            sc -= 1
        if hs != score:
            hud(score, lv, lives)
            hs = score
        show_screen()
        if left <= 0:
            banner("CLEARED", (120, 255, 140), "new maze coming...")
            pause(60000)
            return 1, score, lives


lv, score, lives = 1, 0, 3
while True:
    r, score, lives = play(lv, score, lives)
    if r < 0:
        break
    if r > 0:
        lv += 1
    else:
        lv, score, lives = 1, 0, 3
clear_screen()
show_screen()
