from casioplot import set_pixel, draw_string, clear_screen, show_screen, getkey
from random import randint

K_UP, K_DOWN, K_LEFT, K_RIGHT, K_OK = 14, 34, 23, 25, 24
K_1, K_2, K_3, K_4 = 81, 82, 83, 71
SW, CW, GW, GH, TOP, POLL = 384, 12, 32, 15, 12, 5
DELAYS = (9000, 6000, 4000, 2500)
NAMES = ("1 snail", "2 slow", "3 normal", "4 fast")
NCOL = ((90, 200, 255), (110, 230, 120), (255, 214, 70), (255, 110, 90))

LAWN = ((120, 198, 86), (104, 182, 72))
WALL, WALL_L = (74, 52, 120), (120, 92, 176)
BODY = ((52, 104, 224), (86, 140, 250))
HEAD, EYE, PUP = (30, 68, 180), (255, 255, 255), (20, 20, 40)
RED, RED_L, LEAF, STEM = (226, 50, 56), (255, 170, 170), (40, 150, 60), (110, 70, 30)
BAR, GOLD, CYAN, TEXT = (24, 22, 44), (255, 214, 70), (90, 200, 255), (240, 240, 250)


def fill(x, y, w, h, c):
    for j in range(y, y + h):
        for i in range(x, x + w):
            set_pixel(i, j, c)


def lawn(cx, cy):
    fill(cx * CW, TOP + cy * CW, CW, CW, LAWN[(cx + cy) & 1])


def block(cx, cy, c):
    fill(cx * CW + 1, TOP + cy * CW + 1, CW - 2, CW - 2, c)


def head(cx, cy, dx, dy):
    x, y = cx * CW, TOP + cy * CW
    fill(x + 1, y + 1, CW - 2, CW - 2, HEAD)
    if dx:
        ex = x + (7 if dx > 0 else 2)
        pairs = ((ex, y + 2), (ex, y + 7))
    else:
        ey = y + (7 if dy > 0 else 2)
        pairs = ((x + 2, ey), (x + 7, ey))
    for p in pairs:
        fill(p[0], p[1], 3, 3, EYE)
        set_pixel(p[0] + 1 + dx, p[1] + 1 + dy, PUP)


def apple(cx, cy):
    x, y = cx * CW, TOP + cy * CW
    fill(x + 2, y + 4, 8, 6, RED)
    fill(x + 3, y + 3, 6, 8, RED)
    fill(x + 3, y + 4, 2, 2, RED_L)
    fill(x + 6, y + 1, 1, 3, STEM)
    fill(x + 7, y + 1, 3, 2, LEAF)


def walls():
    for cx in range(GW):
        for cy in range(GH):
            if cx == 0 or cy == 0 or cx == GW - 1 or cy == GH - 1:
                fill(cx * CW, TOP + cy * CW, CW, CW, WALL)
                fill(cx * CW, TOP + cy * CW, CW, 2, WALL_L)
            else:
                lawn(cx, cy)


def hud(score, best, name, col):
    fill(0, 0, SW, TOP, BAR)
    draw_string(6, 0, "SCORE", CYAN, "small")
    draw_string(50, 0, str(score), TEXT, "small")
    draw_string(130, 0, "BEST", GOLD, "small")
    draw_string(166, 0, str(best), TEXT, "small")
    draw_string(300, 0, name, col, "small")


def title():
    clear_screen()
    draw_string(112, 14, "SNAKE", (40, 140, 70), "large")
    for i in range(7):
        fill(112 + i * 12, 46, 10, 10, BODY[i & 1])
    fill(196, 46, 10, 10, HEAD)
    fill(226, 46, 10, 10, RED)
    draw_string(110, 70, "pick a speed", (90, 90, 110), "small")
    for i in range(4):
        draw_string(120, 88 + i * 20, NAMES[i], NCOL[i], "medium")
    show_screen()
    while True:
        k = getkey()
        if k == K_1:
            return 0
        if k == K_2:
            return 1
        if k == K_3:
            return 2
        if k == K_4:
            return 3
        if k == 21 or k == 22:
            return -1


def place_food(snake):
    while True:
        fx = randint(1, GW - 2)
        fy = randint(1, GH - 2)
        if (fx, fy) not in snake:
            return fx, fy


def play(sp, best):
    walls()
    snake = [(16, 7), (15, 7), (14, 7)]
    sh = 0
    block(14, 7, BODY[0])
    block(15, 7, BODY[1])
    head(16, 7, 1, 0)
    dx, dy = 1, 0
    fx, fy = place_food(snake)
    apple(fx, fy)
    score = 0
    hud(0, best, NAMES[sp][2:], NCOL[sp])
    show_screen()
    wait = DELAYS[sp] // POLL
    while True:
        nd = (dx, dy)
        for _p in range(POLL):
            k = getkey()
            if k == 21 or k == 22:
                return False, best
            if k == K_LEFT and dx == 0:
                nd = (-1, 0)
            elif k == K_RIGHT and dx == 0:
                nd = (1, 0)
            elif k == K_UP and dy == 0:
                nd = (0, -1)
            elif k == K_DOWN and dy == 0:
                nd = (0, 1)
            for _w in range(wait):
                pass
        dx, dy = nd
        hx, hy = snake[0]
        nx, ny = hx + dx, hy + dy
        if nx < 1 or nx > GW - 2 or ny < 1 or ny > GH - 2:
            break
        if (nx, ny) in snake[:-1]:
            break
        sh = 1 - sh
        block(hx, hy, BODY[sh])
        snake.insert(0, (nx, ny))
        head(nx, ny, dx, dy)
        if nx == fx and ny == fy:
            score += 1
            if score > best:
                best = score
            hud(score, best, NAMES[sp][2:], NCOL[sp])
            fx, fy = place_food(snake)
            apple(fx, fy)
        else:
            tx, ty = snake.pop()
            block(tx, ty, LAWN[(tx + ty) & 1])
        show_screen()
    fill(80, 70, 224, 64, BAR)
    fill(80, 70, 224, 3, RED)
    fill(80, 131, 224, 3, RED)
    draw_string(100, 78, "GAME OVER", (255, 90, 90), "large")
    draw_string(100, 108, "score " + str(score) + "   OK retry", TEXT, "small")
    show_screen()
    while True:
        k = getkey()
        if k == K_OK:
            return True, best
        if k == 21 or k == 22:
            return False, best


def main():
    best = 0
    while True:
        sp = title()
        if sp < 0:
            return
        again = True
        while again:
            again, best = play(sp, best)


main()
