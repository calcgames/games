from casioplot import set_pixel, draw_string, clear_screen, show_screen, getkey
from random import randint

K_UP = 14
K_OK = 24
K_QUIT = 21
K_EXE = 95

SW = 384
SH = 192
GROUND = 168
BUSH = 150

SKY_T = (78, 192, 236)
SKY_B = (168, 226, 240)
BUSH_C = (108, 196, 122)
BUSH_D = (66, 158, 94)
GRND = (222, 216, 152)
GRND_D = (186, 176, 112)
GRND_L = (238, 234, 190)

PIPE = (92, 188, 66)
PIPE_L = (156, 226, 118)
PIPE_D = (58, 130, 44)
PIPE_E = (34, 76, 30)

BODY = (250, 216, 78)
BELLY = (252, 242, 196)
WING = (238, 238, 238)
WING_D = (206, 206, 206)
BEAK = (246, 146, 48)
EYEW = (252, 252, 252)
EYEB = (36, 36, 44)
OUTL = (48, 44, 40)
TXT = (255, 255, 255)
SHDW = (60, 56, 52)

PW = 30
CAPW = 38
CAPH = 12
GAP = 62
STEP = 6
BX = 64
BW = 17
BH = 13

ROW = []


def fill(x, y, w, h, c):
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


def mix(a, b, t):
    return (int(a[0] + (b[0] - a[0]) * t), int(a[1] + (b[1] - a[1]) * t),
            int(a[2] + (b[2] - a[2]) * t))


def scene():
    del ROW[:]
    for j in range(BUSH):
        c = mix(SKY_T, SKY_B, j / float(BUSH))
        fill(0, j, SW, 1, c)
        ROW.append(c)
    for j in range(BUSH, GROUND):
        c = BUSH_C if j > BUSH + 3 else BUSH_D
        fill(0, j, SW, 1, c)
        ROW.append(c)
    fill(0, GROUND, SW, 3, GRND_L)
    fill(0, GROUND + 3, SW, SH - GROUND - 3, GRND)
    for x in range(0, SW, 14):
        fill(x, GROUND + 6, 7, 3, GRND_D)
        fill(x + 7, GROUND + 12, 7, 3, GRND_D)


def bg_strip(x, y, w, h):
    for j in range(max(0, y), min(y + h, GROUND)):
        fill(x, j, w, 1, ROW[j])


def cap(x, gy, up):
    y = gy - CAPH if up else gy + GAP
    cx = x - (CAPW - PW) // 2
    fill(cx, y, CAPW, CAPH, PIPE)
    fill(cx + 2, y + 2, 5, CAPH - 4, PIPE_L)
    fill(cx + CAPW - 8, y + 2, 5, CAPH - 4, PIPE_D)
    fill(cx, y, CAPW, 1, PIPE_E)
    fill(cx, y + CAPH - 1, CAPW, 1, PIPE_E)
    fill(cx, y, 1, CAPH, PIPE_E)
    fill(cx + CAPW - 1, y, 1, CAPH, PIPE_E)


def shaft(x, y, h):
    if h <= 0:
        return
    fill(x, y, PW, h, PIPE)
    fill(x + 3, y, 6, h, PIPE_L)
    fill(x + PW - 9, y, 5, h, PIPE_D)
    fill(x, y, 1, h, PIPE_E)
    fill(x + PW - 1, y, 1, h, PIPE_E)


def draw_pipe(x, gy):
    shaft(x, 0, gy - CAPH)
    cap(x, gy, True)
    shaft(x, gy + GAP + CAPH, GROUND - (gy + GAP + CAPH))
    cap(x, gy, False)


def clear_pipe(x, gy):
    cx = x - (CAPW - PW) // 2
    bg_strip(cx, 0, CAPW, gy)
    bg_strip(cx, gy + GAP, CAPW, GROUND - gy - GAP)


def bird(x, y, vy, gone):
    if gone:
        bg_strip(x - 1, y - 1, BW + 3, BH + 3)
        return
    fill(x + 1, y + 1, BW - 2, BH - 2, BODY)
    fill(x + 1, y + BH - 5, BW - 5, 4, BELLY)
    fill(x + 2, y, BW - 5, 1, OUTL)
    fill(x + 2, y + BH - 1, BW - 5, 1, OUTL)
    fill(x, y + 2, 1, BH - 4, OUTL)
    fill(x + BW - 1, y + 2, 1, BH - 5, OUTL)
    wy = y + 3 if vy < 0 else y + 6
    fill(x + 2, wy, 7, 4, WING)
    fill(x + 2, wy + 3, 7, 1, WING_D)
    fill(x + 1, wy, 1, 4, OUTL)
    fill(x + BW - 7, y + 2, 5, 5, EYEW)
    fill(x + BW - 7, y + 2, 5, 1, OUTL)
    fill(x + BW - 4, y + 3, 2, 3, EYEB)
    fill(x + BW - 2, y + 6, 5, 4, BEAK)
    fill(x + BW - 2, y + 9, 5, 1, OUTL)
    fill(x + BW + 2, y + 6, 1, 4, OUTL)


def score_at(n):
    s = str(n)
    w = len(s) * 14 + 8
    fill(SW // 2 - w // 2, 8, w, 26, ROW[8])
    draw_string(SW // 2 - w // 2 + 6, 12, s, SHDW, "large")
    draw_string(SW // 2 - w // 2 + 4, 10, s, TXT, "large")


def title():
    clear_screen()
    scene()
    draw_string(96, 44, "FLAPPY", (250, 216, 78), "large")
    draw_string(94, 42, "FLAPPY", SHDW, "large")
    draw_string(96, 44, "FLAPPY", (250, 216, 78), "large")
    bird(180, 90, -1, False)
    draw_string(78, 120, "EXE to flap    OK to start", SHDW, "medium")
    show_screen()
    while True:
        k = getkey()
        if k == K_OK or k == K_EXE:
            return True
        if k == K_QUIT:
            return False


def play():
    clear_screen()
    scene()
    by = 70.0
    vy = 0.0
    pipes = [[SW + 20, randint(26, GROUND - GAP - 34)],
             [SW + 20 + 176, randint(26, GROUND - GAP - 34)]]
    for p in pipes:
        draw_pipe(p[0], p[1])
    bird(BX, int(by), vy, False)
    score_at(0)
    show_screen()
    score = 0

    while True:
        k = getkey()
        if k == K_QUIT:
            return False
        if k == K_EXE or k == K_UP:
            vy = -4.4

        oy = int(by)
        vy += 1.0
        if vy > 7:
            vy = 7
        by += vy
        ny = int(by)
        bird(BX, oy, vy, True)

        for p in pipes:
            ox = p[0]
            p[0] -= STEP
            cx = ox - (CAPW - PW) // 2
            bg_strip(cx + CAPW - STEP, 0, STEP, p[1] + CAPH)
            bg_strip(cx + CAPW - STEP, p[1] + GAP, STEP, GROUND)
            if p[0] + CAPW < 0:
                clear_pipe(ox, p[1])
                p[0] = pipes[0][0] if p is pipes[1] else pipes[1][0]
                p[0] += 176
                p[1] = randint(26, GROUND - GAP - 34)
                score += 1
                score_at(score)
            draw_pipe(p[0], p[1])

        dead = False
        if ny + BH >= GROUND:
            ny = GROUND - BH
            dead = True
        if ny < 0:
            ny = 0
        for p in pipes:
            if p[0] < BX + BW and p[0] + PW > BX:
                if ny < p[1] or ny + BH > p[1] + GAP:
                    dead = True

        bird(BX, ny, vy, False)
        show_screen()

        if dead:
            fill(86, 68, 214, 56, (222, 216, 152))
            fill(86, 68, 214, 2, (160, 150, 100))
            fill(86, 122, 214, 2, (160, 150, 100))
            draw_string(106, 76, "GAME OVER", (232, 104, 60), "large")
            draw_string(106, 102, "score " + str(score) + "   OK", SHDW, "small")
            show_screen()
            while True:
                k = getkey()
                if k == K_OK:
                    return True
                if k == K_QUIT:
                    return False


if title():
    while play():
        pass
