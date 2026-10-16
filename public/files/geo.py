from casioplot import set_pixel, draw_string, clear_screen, show_screen, getkey
from random import randint

K_JUMP1, K_JUMP2, K_JUMP3 = 24, 95, 14
K_BACK = 22

SW, SH = 384, 192
GY = 152
CUBE = 16
CX = 56
G = 0.75
V0 = 9.0
SPEED = 5

SKY_T, SKY_B = (26, 14, 56), (82, 30, 104)
GLOW = (150, 52, 130)
GND, GND_T, GND_L = (20, 14, 40), (255, 62, 180), (120, 30, 96)
SPK, SPK_L, SPK_D = (255, 74, 96), (255, 190, 200), (140, 22, 46)
BLK, BLK_L, BLK_D = (56, 214, 236), (190, 252, 255), (18, 96, 122)
CUB, CUB_L, CUB_D = (250, 214, 62), (255, 250, 200), (150, 104, 10)
OUT = (12, 8, 24)
TXT = (240, 240, 255)

ROW = []
obs = []


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
    for j in range(GY):
        t = j / float(GY)
        c = mix(SKY_T, SKY_B, t)
        if j > GY - 34:
            c = mix(c, GLOW, (j - (GY - 34)) / 40.0)
        fill(0, j, SW, 1, c)
        ROW.append(c)
    fill(0, GY, SW, 3, GND_T)
    fill(0, GY + 3, SW, 2, GND_L)
    fill(0, GY + 5, SW, SH - GY - 5, GND)
    for x in range(0, SW, 24):
        fill(x, GY + 10, 12, 2, GND_L)
        fill(x + 12, GY + 20, 12, 2, GND_L)


def bg(x, y, w, h):
    for j in range(max(0, y), min(y + h, GY)):
        fill(x, j, w, 1, ROW[j])


def spike(x, w):
    h = 18
    n = w // 18
    for s in range(n):
        sx = x + s * 18
        for j in range(h):
            ww = (j + 1) * 18 // h
            fill(sx + 9 - ww // 2, GY - h + j, ww, 1, SPK)
        for j in range(0, h, 2):
            ww = (j + 1) * 18 // h
            fill(sx + 9 - ww // 2, GY - h + j, 2, 1, SPK_L)
            fill(sx + 9 + ww // 2 - 2, GY - h + j, 2, 1, SPK_D)


def blockdraw(x, w, h):
    y = GY - h
    fill(x, y, w, h, BLK)
    fill(x, y, w, 2, BLK_L)
    fill(x, y, 2, h, BLK_L)
    fill(x, y + h - 2, w, 2, BLK_D)
    fill(x + w - 2, y, 2, h, BLK_D)
    fill(x + 5, y + 5, w - 10, h - 10, BLK_D)
    fill(x + 7, y + 7, w - 14, h - 14, BLK)


def cube(x, y, spin):
    if spin:
        for j in range(CUBE):
            d = j if j < CUBE // 2 else CUBE - 1 - j
            ww = (d + 1) * 2
            fill(x + CUBE // 2 - ww // 2, y + j, ww, 1, CUB)
        fill(x + CUBE // 2 - 2, y + CUBE // 2 - 2, 4, 4, CUB_D)
    else:
        fill(x, y, CUBE, CUBE, OUT)
        fill(x + 1, y + 1, CUBE - 2, CUBE - 2, CUB)
        fill(x + 1, y + 1, CUBE - 2, 2, CUB_L)
        fill(x + 1, y + CUBE - 3, CUBE - 2, 2, CUB_D)
        fill(x + 4, y + 5, 3, 3, CUB_D)
        fill(x + CUBE - 7, y + 5, 3, 3, CUB_D)


def width_of(kind):
    if kind == 0:
        return 18
    if kind == 1:
        return 36
    if kind == 2:
        return 54
    if kind == 3:
        return 26
    return 34


def height_of(kind):
    return 18 if kind == 3 else 32


def draw_ob(kind, x):
    if kind < 3:
        spike(x, width_of(kind))
    else:
        blockdraw(x, width_of(kind), height_of(kind))


def spawn(after):
    kind = randint(0, 4)
    gap = randint(132, 224)
    if kind == 2:
        gap += 30
    return [kind, after + gap]


def hud(score, tries):
    fill(4, 4, 160, 14, ROW[4])
    draw_string(6, 2, str(score) + "m", TXT, "small")
    draw_string(84, 2, "attempt " + str(tries), (200, 170, 255), "small")


def play(tries):
    scene()
    del obs[:]
    nx = SW + 60
    for _i in range(4):
        o = spawn(nx)
        obs.append(o)
        nx = o[1] + width_of(o[0])
    by = float(GY - CUBE)
    vy = 0.0
    onground = True
    spin = 0
    frame = 0
    score = 0
    for o in obs:
        draw_ob(o[0], o[1])
    cube(CX, int(by), 0)
    hud(0, tries)
    show_screen()

    while True:
        k = getkey()
        if k == K_BACK:
            return False
        if onground and (k == K_JUMP1 or k == K_JUMP2 or k == K_JUMP3):
            vy = -V0
            onground = False

        oy = int(by)
        oldspin = spin
        vy += G
        if vy > 11:
            vy = 11
        by += vy

        for o in obs:
            x = o[1]
            w = width_of(o[0])
            bg(x + w - SPEED, GY - height_of(o[0]) - 2, SPEED, height_of(o[0]) + 2)
            o[1] = x - SPEED

        while obs and obs[0][1] + width_of(obs[0][0]) < -4:
            del obs[0]
        last = obs[-1]
        if last[1] < SW + 40:
            obs.append(spawn(last[1] + width_of(last[0])))

        floor = GY - CUBE
        dead = False
        for o in obs:
            kind, x = o[0], o[1]
            w = width_of(kind)
            if x > CX + CUBE or x + w < CX:
                continue
            if kind < 3:
                if by + CUBE > GY - 14 and x + 4 < CX + CUBE - 3 and x + w - 4 > CX + 3:
                    dead = True
            else:
                top = GY - height_of(kind)
                if oy + CUBE <= top + 3 and by + CUBE >= top and vy >= 0:
                    if top - CUBE < floor:
                        floor = top - CUBE
                elif by + CUBE > top + 3:
                    dead = True

        if by >= floor:
            by = float(floor)
            vy = 0.0
            onground = True
            spin = 0
        else:
            onground = False
            frame += 1
            if frame % 3 == 0:
                spin = 1 - spin

        ny = int(by)
        if ny != oy or spin != oldspin:
            bg(CX - 1, oy - 1, CUBE + 2, CUBE + 2)
        for o in obs:
            draw_ob(o[0], o[1])
        cube(CX, ny, spin)

        score += 1
        if score % 4 == 0:
            hud(score, tries)
        show_screen()

        if dead:
            for c in ((255, 255, 255), SPK):
                fill(CX - 4, ny - 4, CUBE + 8, CUBE + 8, c)
                show_screen()
            fill(72, 62, 240, 58, OUT)
            fill(72, 62, 240, 2, SPK)
            fill(72, 118, 240, 2, SPK)
            draw_string(92, 70, "GAME OVER", SPK, "large")
            draw_string(92, 98, str(score) + "m   OK retry   BACK quit", TXT, "small")
            show_screen()
            last = -1
            while True:
                k = getkey()
                if k == last:
                    continue
                last = k
                if k == K_JUMP1:
                    return True
                if k == K_BACK:
                    return False


def title():
    scene()
    draw_string(76, 40, "GEOMETRY", (56, 214, 236), "large")
    draw_string(120, 66, "DASH", (255, 62, 180), "large")
    cube(180, GY - CUBE, 0)
    spike(230, 36)
    draw_string(60, 112, "OK jumps    BACK stops", TXT, "medium")
    show_screen()
    last = -1
    while True:
        k = getkey()
        if k == last:
            continue
        last = k
        if k == K_JUMP1 or k == K_JUMP2:
            return True
        if k == K_BACK:
            return False


clear_screen()
if title():
    n = 1
    while play(n):
        n += 1
