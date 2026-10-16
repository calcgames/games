from casioplot import set_pixel, draw_string, clear_screen, show_screen, getkey

K_LEFT, K_RIGHT, K_UP, K_DOWN = 23, 25, 14, 34
K_OK, K_QUIT, K_1, K_2 = 24, 21, 81, 82

SW, SH, CELL = 384, 192, 52
OX = (SW - CELL * 3) // 2
OY = (SH - CELL * 3) // 2

BG, GRID_D, GRID = (6, 4, 16), (0, 70, 110), (40, 235, 255)
X_D, X_C, O_D, O_C = (90, 8, 60), (255, 55, 185), (10, 80, 60), (60, 255, 190)
WIN_D, WIN, CUR = (110, 100, 0), (255, 240, 80), (180, 120, 255)

WINS = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
        (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))

board = [0] * 9


def fill(x, y, w, h, c):
    if x < 0 or y < 0 or x + w > SW or y + h > SH:
        return
    for j in range(y, y + h):
        for i in range(x, x + w):
            set_pixel(i, j, c)


def paint_bg():
    clear_screen()
    draw_string(126, 84, "loading", (120, 120, 140), "medium")
    show_screen()
    for j in range(SH):
        fill(0, j, SW, 1, BG)
        if j % 24 == 0:
            show_screen()
    show_screen()


def clear_board():
    fill(OX, OY, CELL * 3, CELL * 3, BG)


def line(x0, y0, x1, y1, t, c):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        fill(x0 - t // 2, y0 - t // 2, t, t, c)
        if x0 == x1 and y0 == y1:
            return
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def ring(cx, cy, r, t, c):
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            d = (x - cx) * (x - cx) + (y - cy) * (y - cy)
            if (r - t) * (r - t) <= d <= r * r:
                set_pixel(x, y, c)


def grid_lines():
    for i in (1, 2):
        x = OX + CELL * i
        fill(x - 3, OY, 6, CELL * 3, GRID_D)
        fill(x - 1, OY, 2, CELL * 3, GRID)
        y = OY + CELL * i
        fill(OX, y - 3, CELL * 3, 6, GRID_D)
        fill(OX, y - 1, CELL * 3, 2, GRID)


def mark(i, who):
    cx = OX + (i % 3) * CELL + CELL // 2
    cy = OY + (i // 3) * CELL + CELL // 2
    r = CELL // 2 - 9
    if who == 1:
        line(cx - r, cy - r, cx + r, cy + r, 9, X_D)
        line(cx + r, cy - r, cx - r, cy + r, 9, X_D)
        line(cx - r, cy - r, cx + r, cy + r, 3, X_C)
        line(cx + r, cy - r, cx - r, cy + r, 3, X_C)
    else:
        ring(cx, cy, r + 2, 8, O_D)
        ring(cx, cy, r, 3, O_C)


def cursor(i, on):
    cx = OX + (i % 3) * CELL
    cy = OY + (i // 3) * CELL
    c = CUR if on else BG
    for (x, y, w, h) in ((cx + 3, cy + 3, 12, 2), (cx + 3, cy + 3, 2, 12),
                         (cx + CELL - 15, cy + 3, 12, 2), (cx + CELL - 5, cy + 3, 2, 12),
                         (cx + 3, cy + CELL - 5, 12, 2), (cx + 3, cy + CELL - 15, 2, 12),
                         (cx + CELL - 15, cy + CELL - 5, 12, 2),
                         (cx + CELL - 5, cy + CELL - 15, 2, 12)):
        fill(x, y, w, h, c)


def winner(b):
    for w in WINS:
        if b[w[0]] and b[w[0]] == b[w[1]] == b[w[2]]:
            return w
    return None


def full(b):
    for v in b:
        if v == 0:
            return False
    return True


MEMO = {}


def score(b, turn):
    key = (tuple(b), turn)
    v = MEMO.get(key)
    if v is not None:
        return v
    if winner(b):
        MEMO[key] = -1
        return -1
    if full(b):
        MEMO[key] = 0
        return 0
    best = -2
    for i in range(9):
        if b[i]:
            continue
        b[i] = turn
        s = -score(b, 3 - turn)
        b[i] = 0
        if s > best:
            best = s
    MEMO[key] = best
    return best


def best_move(b, me):
    for who in (me, 3 - me):
        for i in range(9):
            if b[i]:
                continue
            b[i] = who
            w = winner(b)
            b[i] = 0
            if w:
                return i
    if b[4] == 0:
        return 4
    best = -2
    pick = -1
    for i in range(9):
        if b[i]:
            continue
        b[i] = me
        s = -score(b, 3 - me)
        b[i] = 0
        if s > best:
            best = s
            pick = i
    return pick


def banner(msg, c):
    fill(OX, OY + 58, CELL * 3, 40, BG)
    fill(OX, OY + 58, CELL * 3, 2, c)
    fill(OX, OY + 96, CELL * 3, 2, c)
    draw_string(OX + 20, OY + 66, msg, c, "large")


def menu():
    clear_board()
    draw_string(OX + 24, OY + 16, "NEON", GRID, "large")
    draw_string(OX + 14, OY + 66, "1  VS CPU", X_C, "medium")
    draw_string(OX + 14, OY + 96, "2  TWO UP", O_C, "medium")
    show_screen()
    last = -1
    while True:
        k = getkey()
        if k == last:
            continue
        last = k
        if k == K_1:
            return 1
        if k == K_2:
            return 2
        if k == K_QUIT:
            return 0


def play(players):
    global board
    board = [0] * 9
    clear_board()
    grid_lines()
    cur = 4
    turn = 1
    last = -1
    cursor(cur, True)
    show_screen()

    while True:
        placed = False
        if players == 1 and turn == 2:
            i = best_move(board, 2)
            board[i] = 2
            mark(i, 2)
            cursor(cur, True)
            turn = 1
            placed = True
            show_screen()
        else:
            k = getkey()
            if k == last:
                continue
            last = k
            if k == K_QUIT:
                return False
            old = cur
            if k == K_LEFT and cur % 3 > 0:
                cur -= 1
            elif k == K_RIGHT and cur % 3 < 2:
                cur += 1
            elif k == K_UP and cur > 2:
                cur -= 3
            elif k == K_DOWN and cur < 6:
                cur += 3
            elif k == K_OK and board[cur] == 0:
                board[cur] = turn
                cursor(cur, False)
                mark(cur, turn)
                cursor(cur, True)
                turn = 3 - turn
                placed = True
                show_screen()
            if cur != old:
                cursor(old, False)
                cursor(cur, True)
                show_screen()
            elif not placed:
                continue

        if placed:
            w = winner(board)
            if w:
                a, b = w[0], w[2]
                ax = OX + (a % 3) * CELL + CELL // 2
                ay = OY + (a // 3) * CELL + CELL // 2
                bx = OX + (b % 3) * CELL + CELL // 2
                by = OY + (b // 3) * CELL + CELL // 2
                line(ax, ay, bx, by, 7, WIN_D)
                line(ax, ay, bx, by, 3, WIN)
                banner("X WINS" if board[w[0]] == 1 else "O WINS", WIN)
                show_screen()
                break
            if full(board):
                banner("  DRAW", GRID)
                show_screen()
                break

    last = -1
    while True:
        k = getkey()
        if k == last:
            continue
        last = k
        if k == K_OK:
            return True
        if k == K_QUIT:
            return False


paint_bg()
while True:
    p = menu()
    if p == 0:
        break
    while play(p):
        pass
