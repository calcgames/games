from casioplot import set_pixel, draw_string as ds, clear_screen as cs
from casioplot import show_screen as ss, getkey as gk
from random import randint

KL, KR, KU, KD, KOK, KB = 23, 25, 14, 34, 24, 22
SW, SH, N, CZ = 384, 192, 8, 18
BX, BY = 120, 26
BG, BG2 = (46, 30, 70), (60, 42, 90)
PAN, TXT, HI = (36, 22, 56), (250, 246, 255), (255, 214, 88)
SUB, EDG, CUR, SEL = (192, 178, 220), (136, 90, 182), (255, 255, 255), (255, 206, 56)
COL = ((232, 62, 74), (246, 140, 40), (250, 224, 70),
       (86, 206, 96), (70, 152, 244), (188, 104, 232))
LIT = ((255, 150, 160), (255, 200, 140), (255, 250, 190),
       (180, 250, 190), (170, 210, 255), (238, 190, 255))
g = []
pv = []


def fl(x, y, w, h, c):
    if x < 0 or y < 0 or x + w > SW or y + h > SH:
        return
    for j in range(y, y + h):
        for i in range(x, x + w):
            set_pixel(i, j, c)


def shape(x, y, t, lit):
    c = LIT[t] if lit else COL[t]
    if t == 0:
        fl(x + 2, y + 3, 12, 10, c); fl(x + 4, y + 1, 8, 14, c)
    elif t == 1:
        fl(x + 2, y + 2, 12, 12, c); fl(x + 4, y + 1, 8, 14, c)
    elif t == 2:
        for i in range(7): fl(x + 7 - i, y + 1 + i, 2 + i * 2, 1, c)
        for i in range(7): fl(x + 1 + i, y + 8 + i, 14 - i * 2, 1, c)
    elif t == 3:
        for i in range(12): fl(x + 8 - i // 2, y + 2 + i, 1 + i, 1, c)
    elif t == 4:
        fl(x + 3, y + 3, 10, 10, c); fl(x + 1, y + 5, 14, 6, c)
        fl(x + 5, y + 1, 6, 14, c)
    else:
        fl(x + 2, y + 4, 12, 8, c); fl(x + 4, y + 2, 8, 12, c)


def wrap(x, y, t):
    fl(x, y, CZ, 2, CUR); fl(x, y + CZ - 2, CZ, 2, CUR)
    fl(x, y, 2, CZ, CUR); fl(x + CZ - 2, y, 2, CZ, CUR)
    shape(x + 3, y + 3, t, True)


def bomb(x, y):
    fl(x + 2, y + 2, 14, 14, (22, 14, 30))
    for i in range(6): fl(x + 3 + (i % 3) * 5, y + 4 + (i // 3) * 6, 3, 3, COL[i])


def cell(r, c):
    v = g[r][c]
    x, y = BX + c * CZ, BY + r * CZ
    fl(x, y, CZ, CZ, BG if (r + c) % 2 else BG2)
    if v < 0: return
    t, sp = v % 8, v // 8
    if sp == 2: bomb(x, y); return
    shape(x, y, t, False)
    if sp == 1: wrap(x, y, t)


def sync():
    for r in range(N):
        for c in range(N):
            if g[r][c] != pv[r][c]: cell(r, c); pv[r][c] = g[r][c]
    ss()


def box(r, c, col):
    x, y = BX + c * CZ, BY + r * CZ
    fl(x, y, CZ, 2, col); fl(x, y + CZ - 2, CZ, 2, col)
    fl(x, y, 2, CZ, col); fl(x + CZ - 2, y, 2, CZ, col)


def runs():
    out = []
    for r in range(N):
        c = 0
        while c < N - 2:
            v = g[r][c]
            if v < 0: c += 1; continue
            j = c
            while j < N and g[r][j] >= 0 and g[r][j] % 8 == v % 8: j += 1
            if j - c >= 3: out.append((r, c, j - c, 1))
            c = j if j > c else c + 1
    for c in range(N):
        r = 0
        while r < N - 2:
            v = g[r][c]
            if v < 0: r += 1; continue
            j = r
            while j < N and g[j][c] >= 0 and g[j][c] % 8 == v % 8: j += 1
            if j - r >= 3: out.append((r, c, j - r, 0))
            r = j if j > r else r + 1
    return out


def blast(r0, c0, hit):
    st = [(r0, c0)]
    while st:
        r, c = st.pop()
        v = g[r][c]
        if v < 0 or (r, c) in hit: continue
        hit.add((r, c))
        sp = v // 8
        if sp == 1:
            for j in range(r - 1, r + 2):
                for i in range(c - 1, c + 2):
                    if 0 <= j < N and 0 <= i < N: st.append((j, i))
        elif sp == 2:
            t = randint(0, 5)
            for j in range(N):
                for i in range(N):
                    if g[j][i] >= 0 and g[j][i] % 8 == t: st.append((j, i))


def fall():
    for c in range(N):
        w = N - 1
        for r in range(N - 1, -1, -1):
            if g[r][c] >= 0: g[w][c] = g[r][c]; w -= 1
        while w >= 0: g[w][c] = randint(0, 5); w -= 1


def panel(score, chain):
    fl(12, 44, 88, 22, PAN)
    ds(14, 44, str(score), TXT, "medium")
    fl(12, 76, 88, 14, PAN)
    if chain > 1: ds(14, 76, "combo x" + str(chain), HI, "small")


def resolve(score):
    chain = 0
    while True:
        rr = runs()
        if not rr: panel(score, 0); ss(); return score
        chain += 1
        hit = set()
        make = []
        for (r, c, n, hz) in rr:
            for i in range(n): blast(r + (0 if hz else i), c + (i if hz else 0), hit)
            if n >= 4:
                make.append((r + (0 if hz else n // 2), c + (n // 2 if hz else 0),
                             g[r][c] % 8, 2 if n >= 5 else 1))
        score += len(hit) * 10 * chain
        for (r, c) in hit: g[r][c] = -1
        for (r, c, t, sp) in make: g[r][c] = t + sp * 8
        panel(score, chain)
        sync()
        fall()
        sync()


def pbox(x, y, w, h):
    fl(x, y, w, h, EDG); fl(x + 2, y + 2, w - 4, h - 4, PAN)


def legend():
    ds(278, 30, "SPECIALS", HI, "small")
    shape(280, 48, 0, False); wrap(280, 48, 0)
    ds(304, 48, "match 4", TXT, "small")
    ds(304, 60, "3x3 blast", SUB, "small")
    bomb(280, 84)
    ds(304, 84, "match 5", TXT, "small")
    ds(304, 96, "clears a", SUB, "small")
    ds(304, 108, "whole colour", SUB, "small")
    ds(278, 132, "arrows move", SUB, "small")
    ds(278, 144, "OK picks", SUB, "small")
    ds(278, 156, "arrow swaps", SUB, "small")


def scene():
    cs()
    ds(140, 84, "loading", SUB, "medium")
    ss()
    for j in range(SH):
        t = j / float(SH)
        fl(0, j, SW, 1, (int(26 + 44 * t), int(14 + 24 * t), int(48 + 62 * t)))
    fl(0, 0, SW, 16, (18, 10, 30))
    fl(0, 16, SW, 1, EDG)
    ds(6, 1, "CANDY CG100", HI, "small")
    ds(286, 1, "BACK to quit", SUB, "small")
    pbox(8, 24, 96, 72)
    ds(14, 28, "SCORE", HI, "small")
    pbox(272, 24, 104, 104)
    legend()
    fl(BX - 5, BY - 5, N * CZ + 10, N * CZ + 10, EDG)
    fl(BX - 3, BY - 3, N * CZ + 6, N * CZ + 6, (30, 18, 46))


def reset():
    for r in range(N):
        for c in range(N): pv[r][c] = -9


def start():
    del g[:]
    del pv[:]
    for r in range(N):
        g.append([randint(0, 5) for _c in range(N)])
        pv.append([-9] * N)
    while runs():
        for (r, c, n, hz) in runs():
            for i in range(n):
                g[r + (0 if hz else i)][c + (i if hz else 0)] = randint(0, 5)


def movable():
    for r in range(N):
        for c in range(N):
            if g[r][c] // 8 == 2: return True
            for (dr, dc) in ((0, 1), (1, 0)):
                r2, c2 = r + dr, c + dc
                if r2 >= N or c2 >= N: continue
                g[r][c], g[r2][c2] = g[r2][c2], g[r][c]
                ok = runs()
                g[r][c], g[r2][c2] = g[r2][c2], g[r][c]
                if ok: return True
    return False


start()
scene()
score = 0
panel(score, 0)
sync()
cr, cc = 4, 4
pick = None
box(cr, cc, CUR)
ss()
last = -1
while True:
    k = gk()
    if k == last:
        continue
    last = k
    if k == KB:
        break
    if k in (KL, KR, KU, KD):
        dr = 1 if k == KD else (-1 if k == KU else 0)
        dc = 1 if k == KR else (-1 if k == KL else 0)
        nr, nc = cr + dr, cc + dc
        if not (0 <= nr < N and 0 <= nc < N): continue
        if pick:
            r1, c1 = pick
            a, b = g[r1][c1], g[nr][nc]
            g[r1][c1], g[nr][nc] = b, a
            if a // 8 == 2 or b // 8 == 2:
                hit = set()
                blast(r1, c1, hit); blast(nr, nc, hit)
                score += len(hit) * 20
                for (r, c) in hit: g[r][c] = -1
                sync(); fall(); sync()
                score = resolve(score)
            elif runs():
                sync()
                score = resolve(score)
            else:
                g[r1][c1], g[nr][nc] = a, b
            pick = None
            cell(r1, c1)
            sync()
            if not movable(): start(); reset(); sync()
            panel(score, 0)
            box(cr, cc, CUR)
            ss()
        else:
            cell(cr, cc)
            cr, cc = nr, nc
            box(cr, cc, CUR)
            ss()
    elif k == KOK:
        if pick:
            cell(pick[0], pick[1]); pick = None; box(cr, cc, CUR)
        else:
            pick = (cr, cc); box(cr, cc, SEL)
        ss()
cs()
ds(120, 76, "final score", TXT, "medium")
ds(120, 100, str(score), HI, "large")
ss()
