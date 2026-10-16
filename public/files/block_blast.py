from casioplot import set_pixel, draw_string as ds, clear_screen as cs
from casioplot import show_screen as ss, getkey as gk
from random import randint

KL, KR, KU, KD, KOK = 23, 25, 14, 34, 24
SW, SH, N, CZ = 384, 192, 8, 18
OX, OY = 126, 24
PAN, BOR, TX, DM = (22, 16, 44), (70, 220, 240), (240, 244, 255), (150, 150, 190)
GOLD, RED, EM, DOT, FRM = (255, 214, 80), (230, 60, 80), (34, 28, 64), (58, 50, 96), (96, 66, 160)
BASE = [(56, 194, 220), (232, 76, 126), (104, 208, 96),
        (232, 174, 54), (164, 104, 224), (74, 132, 232)]
LT = [tuple([min(255, v + 80) for v in c]) for c in BASE]
DK = [tuple([v * 5 // 10 for v in c]) for c in BASE]
ST = ("X", "XX", "X/X", "XXX", "X/X/X", "XX/X.", "XX/.X", "X./XX", ".X/XX", "XX/XX",
      "XXXX", "X/X/X/X", "XXX/.X.", ".X./XXX", "X./XX/X.", ".X/XX/.X", "XX./.XX", ".XX/XX.",
      "X./XX/.X", ".X/XX/X.", "X./X./XX", ".X/.X/XX", "XX/X./X.", "XX/.X/.X", "XXX/X..",
      "XXX/..X", "X../XXX", "..X/XXX", "XXX/XXX", "XX/XX/XX", "XXX/X../X..", "XXX/..X/..X",
      "X../X../XXX", "..X/..X/XXX", "XXX/XXX/XXX")
SHP, WD, HT = [], [], []
for s in ST:
    rows = s.split("/")
    cells = []
    for y in range(len(rows)):
        for x in range(len(rows[y])):
            if rows[y][x] == "X":
                cells.append((x, y))
    SHP.append(cells)
    WD.append(len(rows[0]))
    HT.append(len(rows))
bd, pc, pcol = [], [-1, -1, -1], [0, 0, 0]
best = 0


def fl(x, y, w, h, c):
    for j in range(y, y + h):
        for i in range(x, x + w):
            set_pixel(i, j, c)


def pause(n):
    for _w in range(n):
        pass


def blk(px, py, v, s):
    fl(px, py, s, s, BASE[v])
    fl(px, py, s, 2, LT[v])
    fl(px, py, 2, s, LT[v])
    fl(px, py + s - 2, s, 2, DK[v])
    fl(px + s - 2, py, 2, s, DK[v])


def cell(x, y):
    px, py = OX + x * CZ, OY + y * CZ
    if bd[y][x] < 0:
        fl(px, py, CZ - 1, CZ - 1, EM)
        fl(px + 7, py + 7, 3, 3, DOT)
    else:
        blk(px, py, bd[y][x], CZ - 1)


def fits(s, x, y):
    for (dx, dy) in SHP[s]:
        if bd[y + dy][x + dx] >= 0:
            return False
    return True


def anywhere(s):
    for y in range(N - HT[s] + 1):
        for x in range(N - WD[s] + 1):
            if fits(s, x, y):
                return True
    return False


def ghost(s, x, y, on):
    good = fits(s, x, y)
    for (dx, dy) in SHP[s]:
        if not on:
            cell(x + dx, y + dy)
            continue
        px, py = OX + (x + dx) * CZ, OY + (y + dy) * CZ
        u = bd[y + dy][x + dx]
        fl(px, py, CZ - 1, CZ - 1, LT[pcol[sel]] if good else RED)
        fl(px + 3, py + 3, CZ - 7, CZ - 7, EM if u < 0 else BASE[u])


def newset():
    for _t in range(40):
        for i in range(3):
            pc[i] = min(randint(0, len(ST) - 1), randint(0, len(ST) - 1))
            pcol[i] = randint(0, 5)
        for i in range(3):
            if anywhere(pc[i]):
                return


def slot(i):
    x, y = 276, 6 + i * 62
    fl(x, y, 102, 56, GOLD if i == sel else FRM)
    fl(x + 2, y + 2, 98, 52, PAN)
    ds(x + 6, y + 4, str(i + 1), GOLD if i == sel else DM, "small")
    s = pc[i]
    if s < 0:
        ds(x + 38, y + 22, "used", DM, "small")
        return
    ox, oy = x + 51 - WD[s] * 5, y + 28 - HT[s] * 5
    for (dx, dy) in SHP[s]:
        blk(ox + dx * 10, oy + dy * 10, pcol[i], 9)


def stat(score, streak):
    fl(14, 78, 94, 16, PAN)
    ds(14, 78, str(score), TX, "medium")
    fl(14, 116, 94, 16, PAN)
    ds(14, 116, str(max(best, score)), GOLD, "medium")
    fl(14, 136, 94, 12, PAN)
    if streak > 1:
        ds(14, 136, "combo x" + str(streak), (255, 90, 170), "small")


def side():
    fl(6, 6, 108, 180, BOR)
    fl(8, 8, 104, 176, PAN)
    ds(14, 12, "BLOCK", (255, 90, 170), "large")
    ds(14, 36, "BLAST", BOR, "large")
    ds(14, 66, "SCORE", DM, "small")
    ds(14, 104, "BEST", DM, "small")
    ds(14, 152, "arrows move", DM, "small")
    ds(14, 162, "1 2 3  pick", DM, "small")
    ds(14, 172, "OK place", DM, "small")
    fl(OX - 5, OY - 5, 154, 154, BOR)
    fl(OX - 3, OY - 3, 150, 150, FRM)
    fl(OX - 1, OY - 1, 146, 146, PAN)


def wait():
    last = -1
    while True:
        k = gk()
        if k != last:
            last = k
            if k == 24 or k == 22 or k == 21:
                return k == 24


def play():
    global best, sel
    del bd[:]
    for _y in range(N):
        bd.append([-1] * N)
    newset()
    score, streak, setclr, cx, cy, sel = 0, 0, False, 3, 3, 0
    side()
    for y in range(N):
        for x in range(N):
            cell(x, y)
    for i in range(3):
        slot(i)
    stat(score, streak)
    cx, cy = max(0, min(cx, N - WD[pc[sel]])), max(0, min(cy, N - HT[pc[sel]]))
    ghost(pc[sel], cx, cy, True)
    ss()
    last, rep = -1, 0
    while True:
        k = gk()
        if k == last:
            rep += 1
            if k in (KL, KR, KU, KD):
                if rep < 6 or rep % 3:
                    k = 0
            else:
                k = 0
        else:
            rep, last = 0, k
        if k == 22 or k == 21:
            return False
        s0, x0, y0, sel0, placed = pc[sel], cx, cy, sel, False
        if k == KL:
            cx -= 1
        elif k == KR:
            cx += 1
        elif k == KU:
            cy -= 1
        elif k == KD:
            cy += 1
        elif k in (81, 82, 83) and pc[k - 81] >= 0:
            sel = k - 81
        elif k == KOK and fits(s0, cx, cy):
            placed = True
        if not placed:
            s = pc[sel]
            cx, cy = max(0, min(cx, N - WD[s])), max(0, min(cy, N - HT[s]))
            if (cx, cy, sel) != (x0, y0, sel0):
                ghost(s0, x0, y0, False)
                ghost(s, cx, cy, True)
                if sel != sel0:
                    slot(sel0)
                    slot(sel)
                ss()
            continue
        for (dx, dy) in SHP[s0]:
            bd[cy + dy][cx + dx] = pcol[sel]
            cell(cx + dx, cy + dy)
        score += len(SHP[s0])
        rows = [y for y in range(N) if -1 not in bd[y]]
        cols = [x for x in range(N) if -1 not in [bd[y][x] for y in range(N)]]
        n = len(rows) + len(cols)
        if n:
            for y in rows:
                fl(OX, OY + y * CZ, N * CZ - 1, CZ - 1, TX)
            for x in cols:
                fl(OX + x * CZ, OY, CZ - 1, N * CZ - 1, TX)
            ss()
            pause(9000)
            for y in rows:
                bd[y] = [-1] * N
            for x in cols:
                for y in range(N):
                    bd[y][x] = -1
            for y in range(N):
                for x in range(N):
                    cell(x, y)
            streak += 1
            setclr = True
            score += n * n * 10 + streak * 10
            empty = 0
            for row in bd:
                empty += row.count(-1)
            if empty == N * N:
                score += 100
        pc[sel] = -1
        left = 0
        for i in range(3):
            if pc[i] >= 0:
                left += 1
                if pc[sel] < 0:
                    sel = i
        if left == 0:
            if not setclr:
                streak = 0
            setclr = False
            newset()
            sel = 0
        if score > best:
            best = score
        dead = True
        for i in range(3):
            if pc[i] >= 0 and anywhere(pc[i]):
                dead = False
        for i in range(3):
            slot(i)
        stat(score, streak)
        if dead:
            fl(130, 70, 140, 58, GOLD)
            fl(132, 72, 136, 54, PAN)
            ds(140, 76, "NO MOVES", RED, "large")
            ds(140, 100, str(score) + "  OK retry", TX, "small")
            ds(140, 112, "BACK to quit", DM, "small")
            ss()
            return wait()
        cx, cy = max(0, min(cx, N - WD[pc[sel]])), max(0, min(cy, N - HT[pc[sel]]))
        ghost(pc[sel], cx, cy, True)
        ss()


cs()
for j in range(SH):
    fl(0, j, SW, 1, (16 + 48 * j // SH, 12 + 10 * j // SH, 40 + 44 * j // SH))
while play():
    pass
cs()
ss()
