from casioplot import set_pixel, draw_string, clear_screen, show_screen, getkey
from random import randint

K_LEFT, K_RIGHT, K_UP, K_OK, K_EXE = 23, 25, 14, 24, 95
SW, SH, X0, LW, OW = 384, 192, 108, 56, 44
PY, PW, PH, RX = 146, 24, 22, 284

GRASS, TREE_D, TREE_L = (84, 170, 92), (30, 112, 52), (56, 156, 80)
ROAD, EDGE, DASH = (58, 60, 74), (236, 236, 244), (250, 214, 90)
SHADOW, GOLD, GOLD_L = (30, 32, 42), (255, 200, 40), (255, 244, 170)
BAR, TEXT, CYAN, DIM = (24, 22, 44), (240, 240, 250), (90, 200, 255), (170, 170, 190)
CARS = ((214, 48, 60), (52, 110, 224), (150, 70, 200), (240, 130, 40))
SKIN, HAIR, CAP = (244, 204, 168), (60, 40, 30), (230, 60, 72)
COAT, PACK, PANT = (60, 190, 230), (250, 170, 60), (50, 50, 70)

trees = []
dashes = []


def fl(x, y, w, h, c):
    if x < 0:
        w += x
        x = 0
    if y < 0:
        h += y
        y = 0
    if x + w > SW:
        w = SW - x
    if y + h > SH:
        h = SH - y
    if w <= 0 or h <= 0:
        return
    for j in range(y, y + h):
        for i in range(x, x + w):
            set_pixel(i, j, c)


def tree_x():
    return RX + randint(8, 70)


def scene():
    clear_screen()
    fl(0, 0, X0 - 4, SH, BAR)
    fl(RX + 4, 0, SW - RX - 4, SH, GRASS)
    fl(X0, 0, 3 * LW, SH, ROAD)
    fl(X0 - 4, 0, 4, SH, EDGE)
    fl(X0 + 3 * LW, 0, 4, SH, EDGE)
    del trees[:]
    del dashes[:]
    for i in range(5):
        t = [tree_x(), i * 44 - 10]
        trees.append(t)
        fl(t[0], t[1], 9, 18, TREE_D)
        fl(t[0] + 9, t[1], 9, 18, TREE_L)
    for i in range(7):
        dashes.append(i * 30 - 12)
        for d in (1, 2):
            fl(X0 + d * LW - 1, i * 30 - 12, 3, 14, DASH)


def scroll(dy):
    for t in trees:
        t[1] += dy
        if t[1] > SH:
            t[1] -= 220
            t[0] = tree_x()
        fl(t[0], t[1] - dy, 18, dy, GRASS)
        fl(t[0], t[1] + 18 - dy, 9, dy, TREE_D)
        fl(t[0] + 9, t[1] + 18 - dy, 9, dy, TREE_L)
    for i in range(len(dashes)):
        y = dashes[i] + dy
        if y > SH:
            y -= 210
        dashes[i] = y
        for d in (1, 2):
            fl(X0 + d * LW - 1, y - dy, 3, dy, ROAD)
            fl(X0 + d * LW - 1, y + 14 - dy, 3, dy, DASH)


def car(o, dy):
    x, y, h, c = o[1], o[2], o[3], o[4]
    dk = (c[0] // 2, c[1] // 2, c[2] // 2)
    fl(x, y - dy, OW, dy, ROAD)
    fl(x, y + h - dy, OW, dy, c)
    fl(x, y + h - dy, 3, dy, dk)
    fl(x + OW - 3, y + h - dy, 3, dy, dk)
    fl(x + 14, y + h - dy, OW - 28, dy, TEXT)


def barrier(o, dy):
    x, y = o[1], o[2]
    fl(x, y - dy, OW, dy, ROAD)
    fl(x, y, OW, 10, GOLD)
    for i in range(0, OW, 8):
        fl(x + i, y, 4, 10, SHADOW)


def coin(o, dy):
    x, y = o[1], o[2]
    fl(x, y - dy, 12, 12, ROAD)
    fl(x + 2, y, 8, 12, GOLD)
    fl(x, y + 2, 12, 8, GOLD)
    fl(x + 3, y + 3, 3, 3, GOLD_L)


def runner(lane, air, on):
    x = X0 + lane * LW + (LW - PW) // 2
    y = PY - (14 if air else 0)
    if not on:
        fl(x - 3, y - 3, PW + 6, PH + 20, ROAD)
        return
    if air:
        fl(x + 3, PY + 14, PW - 6, 6, SHADOW)
    fl(x + 6, y + 14, 5, 8, PANT)
    fl(x + 13, y + 14, 5, 8, PANT)
    fl(x + 2, y + 5, PW - 4, 11, COAT)
    fl(x + 16, y + 6, 6, 8, PACK)
    fl(x + 8, y, 9, 8, SKIN)
    fl(x + 7, y, 11, 3, CAP)
    fl(x + 8, y + 3, 9, 2, HAIR)


def hud_back():
    draw_string(6, 2, "DIST", CYAN, "small")
    draw_string(6, 30, "COINS", GOLD, "small")
    draw_string(6, 48, "BEST", DIM, "small")


def hud_dist(n):
    fl(6, 13, 90, 14, BAR)
    draw_string(6, 13, str(n) + " m", TEXT, "small")


def hud_coins(n, best):
    fl(6, 39, 90, 8, BAR)
    draw_string(6, 39, str(n), TEXT, "small")
    fl(40, 48, 60, 12, BAR)
    draw_string(40, 48, str(best), TEXT, "small")


def title():
    clear_screen()
    fl(0, 0, SW, 68, BAR)
    draw_string(120, 10, "RUNNER", GOLD, "large")
    draw_string(78, 42, "dodge  jump  collect", CYAN, "small")
    draw_string(56, 84, "LEFT / RIGHT  change lane", (40, 40, 60), "small")
    draw_string(56, 100, "UP  jump over yellow bars", (40, 40, 60), "small")
    draw_string(56, 116, "cars  steer around them", (200, 50, 60), "small")
    draw_string(56, 132, "coins  run through them", (190, 140, 0), "small")
    draw_string(110, 158, "OK to start", (40, 140, 70), "medium")
    show_screen()
    while True:
        k = getkey()
        if k == K_OK or k == K_EXE:
            return True
        if k == 21 or k == 22:
            return False


def play(best):
    scene()
    lane, air = 1, 0
    obs = []
    score, coins, gap, tick, speed = 0, 0, 40, 0, 6
    hud_back()
    hud_dist(0)
    hud_coins(0, best)
    runner(lane, 0, True)
    show_screen()
    while True:
        pd = False
        k = getkey()
        if k == 21 or k == 22:
            return False, best
        if (k == K_LEFT and lane > 0) or (k == K_RIGHT and lane < 2) or (k == K_UP and air == 0):
            runner(lane, air, False)
            pd = True
            if k == K_LEFT:
                lane -= 1
            elif k == K_RIGHT:
                lane += 1
            else:
                air = 6
        scroll(speed)
        gap -= speed
        if gap <= 0:
            free = randint(0, 2)
            for ln in range(3):
                x = X0 + ln * LW + (LW - OW) // 2
                if ln == free:
                    if randint(0, 2) == 0:
                        obs.append([2, x + 16, -12, 12, GOLD, ln])
                else:
                    r = randint(0, 5)
                    if r < 3:
                        h = randint(40, 70)
                        obs.append([0, x, -h, h, CARS[randint(0, 3)], ln])
                    elif r == 3:
                        obs.append([1, x, -10, 10, GOLD, ln])
            gap = randint(90, 140)
        dead = False
        keep = []
        for o in obs:
            o[2] += speed
            if o[2] > SH:
                continue
            if o[0] == 0:
                car(o, speed)
            elif o[0] == 1:
                barrier(o, speed)
            else:
                coin(o, speed)
            if o[5] == lane and o[2] < PY + PH + 12 and o[2] + o[3] > PY - 16:
                pd = True
            if o[5] == lane and o[2] < PY + PH and o[2] + o[3] > PY:
                if o[0] == 2:
                    coins += 1
                    fl(o[1], o[2], 12, 12, ROAD)
                    hud_coins(coins, best)
                    continue
                if o[0] == 0 or air == 0:
                    dead = True
            keep.append(o)
        obs = keep
        if air:
            air -= 1
            pd = True
            if air == 0:
                runner(lane, 1, False)
        if pd:
            runner(lane, air, True)
        tick += 1
        if tick % 4 == 0:
            score += 1
            hud_dist(score)
            if speed < 12 and score % 30 == 0:
                speed += 1
        show_screen()
        if dead:
            if score > best:
                best = score
            fl(70, 60, 244, 70, BAR)
            fl(70, 60, 244, 3, (255, 90, 90))
            fl(70, 127, 244, 3, (255, 90, 90))
            draw_string(96, 70, "WIPEOUT", (255, 90, 90), "large")
            draw_string(96, 100, str(score) + " m   " + str(coins) + " coins   OK", TEXT, "small")
            show_screen()
            while True:
                k = getkey()
                if k == K_OK or k == K_EXE:
                    return True, best
                if k == 21 or k == 22:
                    return False, best


best = 0
while title():
    again = True
    while again:
        again, best = play(best)
