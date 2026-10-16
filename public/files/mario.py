from casioplot import set_pixel, draw_string as ds, clear_screen as cs
from casioplot import show_screen as ss, getkey as gk
from random import randint

KL, KR, KB = 23, 25, 22
KJ1, KJ2, KJ3 = 24, 95, 14
SW, SH, TS, CS, RW = 384, 192, 16, 24, 12
ACC, MV, FR = 0.45, 3.2, 0.22
GR, JMP, HG, HM = 0.55, -6.6, 0.26, 9
MW, MH = 13, 15

SKY = (104, 176, 248)
GD, GDD, GDL = (196, 108, 44), (120, 60, 16), (240, 168, 96)
BK, BKD = (200, 112, 56), (110, 54, 12)
QB, QBD, QBL = (248, 188, 48), (150, 90, 8), (255, 236, 160)
PP, PPL, PPD = (64, 184, 64), (152, 244, 152), (16, 96, 24)
PL, PLL, PLD = (228, 196, 124), (255, 240, 200), (150, 112, 52)
CO, COD, PO, FG = (252, 216, 60), (176, 132, 12), (200, 200, 208), (48, 200, 72)
CAP, SKN, OVR, SHO = (216, 40, 32), (252, 200, 152), (48, 72, 216), (96, 56, 24)
GO, GOD, EY, PU = (160, 96, 40), (92, 52, 16), (250, 250, 250), (30, 30, 30)
TX, DK = (255, 255, 255), (24, 24, 32)

TI = {
    "#": ((0, 0, 16, 16, GD), (0, 0, 16, 3, GDL), (0, 14, 16, 2, GDD),
          (3, 6, 4, 3, GDD)),
    "B": ((0, 0, 16, 16, BK), (0, 0, 16, 1, BKD), (0, 7, 16, 1, BKD),
          (7, 0, 1, 7, BKD)),
    "?": ((0, 0, 16, 16, QB), (0, 0, 16, 1, QBD), (0, 15, 16, 1, QBD),
          (5, 3, 6, 2, QBL), (7, 11, 2, 2, QBL)),
    "p": ((0, 0, 16, 16, PP), (2, 0, 4, 16, PPL), (14, 0, 2, 16, PPD)),
    "=": ((0, 0, 16, 16, PL), (0, 0, 16, 2, PLL), (0, 14, 16, 2, PLD)),
    "o": ((5, 3, 6, 10, CO), (7, 5, 2, 6, COD)),
    "F": ((7, 0, 3, 16, PO),),
}

SOL = "#B?=p"
gr, gm = [], []

def fl(x, y, w, h, c):
    for j in range(max(y, 0), min(y + h, SH)):
        for i in range(max(x, 0), min(x + w, SW)):
            set_pixel(i, j, c)

def tl(c, r):
    t = gr[r][c]
    p = TI.get(t)
    if not p:
        return
    x, y = c * TS, r * TS
    for (dx, dy, w, h, col) in p:
        fl(x + dx, y + dy, w, h, col)
    if t == "F" and r == 5:
        fl(x + 10, y + 1, 10, 7, FG)

def rs(x, y, w, h):
    fl(x, y, w, h, SKY)
    for r in range(max(0, y // TS), min(RW - 1, (y + h) // TS) + 1):
        for c in range(max(0, x // TS), min(CS - 1, (x + w) // TS) + 1):
            tl(c, r)

def sd(px, py):
    c, r = px // TS, py // TS
    if c < 0 or c >= CS:
        return True
    if r < 0 or r >= RW:
        return False
    return gr[r][c] in SOL

SAVE = []


def gen(n):
    t = []
    for r in range(RW):
        t.append([" "] * CS)
    for c in range(CS):
        t[10][c] = t[11][c] = "#"
    c = 6
    while c < 17:
        r = randint(0, 9)
        if r < 3:
            w = 3 if n > 2 and randint(0, 1) else 2
            for i in range(w):
                t[10][c + i] = t[11][c + i] = " "
            c += w + 4
        elif r < 6:
            for k in range(1 + randint(0, 1)):
                t[9 - k][c] = "p"
            c += 5
        elif r < 9:
            t[9][c] = "g"; c += 5
        else:
            c += 2
    for r in range(5, 10):
        t[r][22] = "F"
    for _i in range(8):
        c = randint(3, 20)
        if t[9][c - 3:c + 4] == [" "] * 7 and t[10][c - 3:c + 4] == ["#"] * 7:
            u = randint(0, 2)
            if u == 2:
                t[9][c - 1:c + 2] = ["o"] * 3
            else:
                t[7][c] = "?" if u else "B"
    SAVE[:] = ["".join(row) for row in t]


def load(n, new):
    if new:
        gen(n)
    del gr[:]
    del gm[:]
    for row in SAVE:
        gr.append(list(row))
    for r in range(RW):
        for c in range(CS):
            if gr[r][c] == "g":
                gm.append([c * TS, r * TS + 1, -1, 1])
                gr[r][c] = " "

def hud(cn, lv, n):
    fl(2, 1, 220, 12, SKY)
    ds(4, 0, "C" + str(cn) + "  x" + str(lv), DK, "small")
    ds(110, 0, "WORLD 1-" + str(n + 1), DK, "small")

def paint(n, cn, lv):
    cs()
    for j in range(RW * TS):
        fl(0, j, SW, 1, SKY)
        if j % 40 == 0:
            ds(134, 80, "STAGE " + str(n + 1), DK, "large")
            ss()
    for r in range(RW):
        for c in range(CS):
            tl(c, r)
    hud(cn, lv, n)

def man(x, y, fc, air):
    fl(x + 1, y, MW - 2, 4, CAP)
    fl(x, y + 2, MW, 2, CAP)
    fl(x + 2, y + 4, MW - 4, 4, SKN)
    fl(x + 8 if fc > 0 else x + 2, y + 5, 2, 2, DK)
    fl(x + 1, y + 8, MW - 2, 3, CAP)
    fl(x + 3, y + 9, MW - 6, 5, OVR)
    if air:
        fl(x + MW - 2, y + 7, 3, 3, SKN)
    fl(x, y + MH - 2, 5, 2, SHO)
    fl(x + MW - 5, y + MH - 2, 5, 2, SHO)

def gmb(x, y):
    fl(x + 1, y + 2, 12, 9, GO)
    fl(x, y + 4, 14, 6, GO)
    fl(x + 1, y + 11, 12, 3, GOD)
    fl(x + 3, y + 5, 3, 4, EY)
    fl(x + 8, y + 5, 3, 4, EY)
    fl(x + 4, y + 6, 2, 2, PU)
    fl(x + 9, y + 6, 2, 2, PU)

def play(n, cn, lv, new):
    load(n, new)
    paint(n, cn, lv)
    x, y, vx, vy = 24.0, 128.0, 0.0, 0.0
    fc, og, hd = 1, False, 99
    ss()
    while True:
        k = gk()
        if k == KB:
            return -1, cn, lv
        jp = k == KJ1 or k == KJ2 or k == KJ3
        if k == KL:
            vx -= ACC; fc = -1
        elif k == KR:
            vx += ACC; fc = 1
        elif og:
            vx = vx - FR if vx > FR else (vx + FR if vx < -FR else 0.0)
        vx = max(-MV, min(MV, vx))
        if jp and og:
            vy, og, hd = JMP, False, 0
        vy += HG if (jp and hd < HM and vy < 0) else GR
        hd += 1
        vy = min(vy, 9)
        ox, oy = int(x), int(y)
        for g in gm:
            rs(g[0] - 1, g[1] - 1, 17, 17)
        rs(ox - 2, oy - 2, MW + 4, MH + 4)
        nx = x + vx
        if vx:
            sx = int(nx) + (MW - 1 if vx > 0 else 0)
            if sd(sx, int(y) + 2) or sd(sx, int(y) + MH - 2):
                nx = float((sx // TS) * TS + (-MW if vx > 0 else TS)); vx = 0.0
        x = nx if nx > 0 else 0.0
        ny = y + vy
        og = False
        if vy >= 0:
            ft = int(ny) + MH
            if sd(int(x) + 2, ft) or sd(int(x) + MW - 3, ft):
                ny = float((ft // TS) * TS - MH); vy, og = 0.0, True
        else:
            hx = int(ny)
            for px in (int(x) + 2, int(x) + MW - 3):
                if sd(px, hx):
                    c, r = px // TS, hx // TS
                    t = gr[r][c]
                    if t == "?":
                        gr[r][c] = "B"; cn += 1; hud(cn, lv, n)
                    elif t == "B":
                        gr[r][c] = " "
                    rs(c * TS, r * TS, TS, TS)
                    ny = float((hx // TS) * TS + TS); vy = 0.0
        y = ny
        cc, cr = (int(x) + MW // 2) // TS, (int(y) + MH // 2) // TS
        if 0 <= cr < RW and 0 <= cc < CS:
            t = gr[cr][cc]
            if t == "o":
                gr[cr][cc] = " "; rs(cc * TS, cr * TS, TS, TS); cn += 1; hud(cn, lv, n)
            elif t == "F":
                man(int(x), int(y), fc, False)
                ds(112, 68, "STAGE CLEAR", DK, "large")
                ss()
                for _w in range(40000):
                    pass
                return 1, cn, lv
        for g in gm:
            g[0] += g[2]
            if sd(g[0] + (14 if g[2] > 0 else 0), g[1] + 7) or not sd(g[0] + 7, g[1] + 16):
                g[2] = -g[2]; g[0] += g[2] * 2
            if abs(g[0] - int(x)) < 12 and abs(g[1] - int(y)) < 13:
                if vy > 0 and int(y) + MH < g[1] + 9:
                    vy, g[3] = -4.5, 0; cn += 1; hud(cn, lv, n)
                else:
                    return 0, cn, lv - 1
        for g in gm:
            if g[3]:
                gmb(g[0], g[1])
        gm[:] = [g for g in gm if g[3]]
        if y > SH:
            return 0, cn, lv - 1
        man(int(x), int(y), fc, not og)
        ss()

def over(msg, c):
    fl(60, 66, 264, 52, DK)
    fl(60, 66, 264, 2, c)
    fl(60, 116, 264, 2, c)
    ds(88, 74, msg, c, "large")
    ds(88, 100, "OK again  BACK stop", TX, "small")
    ss()
    last = -1
    while True:
        k = gk()
        if k == last:
            continue
        last = k
        if k == KJ1:
            return True
        if k == KB:
            return False

n, cn, lv, new = 0, 0, 3, True
while True:
    r, cn, lv = play(n, cn, lv, new)
    new = False
    if r < 0:
        break
    if r > 0:
        n += 1
        new = True
    elif lv <= 0:
        if not over("GAME OVER", (255, 90, 90)):
            break
        n, cn, lv, new = 0, 0, 3, True
