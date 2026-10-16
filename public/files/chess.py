from casioplot import set_pixel, draw_string, clear_screen, show_screen, getkey
from random import randint
ds = draw_string
K_UP, K_DOWN, K_LEFT, K_RIGHT = 14, 34, 23, 25
PX = 196
LT, DK, SELC = (240, 217, 181), (181, 136, 99), (250, 226, 110)
CYAN, GRN, RED, WHITE = (40, 190, 250), (50, 160, 80), (230, 60, 60), (255, 255, 255)
BAR, GOLD, TXT = (24, 22, 44), (255, 214, 70), (30, 30, 50)
DIM, NAVY = (130, 130, 150), (40, 60, 140)
PC = (((46, 46, 66), (232, 232, 245)), ((252, 250, 242), (30, 30, 44)))
VAL = (0, 10, 30, 30, 50, 90, 0)
CM = {60: 3, 63: 1, 56: 2, 4: 12, 7: 4, 0: 8}
HOME = (4, 2, 3, 5, 6, 3, 2, 4)
KN = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
DG = ((-1, -1), (-1, 1), (1, -1), (1, 1))
ST = ((-1, 0), (1, 0), (0, -1), (0, 1))
SPR = ("00001@3H3H1@3H3H7L?N", "307H?L=LMLIL1L3L7N?N", "1@3H7L7<7L3H7L1@3H?N",
 "=F?N7L7L7L7L7L?N?NOO", "EE;J?N7L3H3H7L7L?NOO", "1@7L1@3H7L?N7L7L?NOO")
B = [0] * 66
CS = [52, -1]
TG = []
def mk():
 out = []
 for p in SPR:
  m = [0] * 168
  for r in range(10):
   v = (ord(p[2 * r]) - 48) * 32 + ord(p[2 * r + 1]) - 48
   for c in range(10):
    if v >> (9 - c) & 1:
     m[r * 12 + c + 25] = 1
  out.append([1 if m[n + 12] else 2 if m[n + 11] or m[n + 13] or m[n] or m[n + 24] else 0
     for n in range(144)])
 return out
G = mk()
def fill(x, y, w, h, c):
 for j in range(y, y + h):
  for i in range(x, x + w):
   set_pixel(i, j, c)
def spr(x, y, i, w, k):
 g = G[i]
 for n in range(144):
  if g[n]:
   fill(x + n % 12 * k, y + n // 12 * k, k, k, PC[w][g[n] - 1])
def ring(x, y, c):
 fill(x, y, 24, 2, c)
 fill(x, y + 22, 24, 2, c)
 fill(x, y, 2, 24, c)
 fill(x + 22, y, 2, 24, c)
def sq(s):
 r, c = s // 8, s % 8
 x, y = c * 24, r * 24
 p = B[s]
 fill(x, y, 24, 24, SELC if s == CS[1] else (DK if (r + c) & 1 else LT))
 if p:
  spr(x, y, abs(p) - 1, p > 0, 2)
 if s in TG:
  if p:
   ring(x, y, RED)
  else:
   fill(x + 9, y + 9, 6, 6, GRN)
 if s == CS[0]:
  ring(x, y, CYAN)
def gen(b, s):
 p = b[s]
 t = abs(p)
 sd = 1 if p > 0 else -1
 r, c = s // 8, s % 8
 out = []
 if t == 1:
  f = s - sd * 8
  if 0 <= f < 64:
   if b[f] == 0:
    out.append(f)
    if r == (6 if sd > 0 else 1) and b[f - sd * 8] == 0:
     out.append(f - sd * 8)
   for dc in (-1, 1):
    if 0 <= c + dc < 8 and (b[f + dc] * sd < 0 or f + dc == b[64]):
     out.append(f + dc)
  return out
 rng = 1 if t == 2 or t == 6 else 7
 for dr, dc in (0, 0, KN, DG, ST, DG + ST, DG + ST)[t]:
  nr, nc = r, c
  for _ in range(rng):
   nr += dr
   nc += dc
   if nr < 0 or nr > 7 or nc < 0 or nc > 7:
    break
   q = b[nr * 8 + nc]
   if q * sd > 0:
    break
   out.append(nr * 8 + nc)
   if q:
    break
 return out
def mv(b, a, z):
 n = b[:]
 p = n[a]
 t = abs(p)
 if t == 1 and z % 8 != a % 8 and n[z] == 0:
  n[a // 8 * 8 + z % 8] = 0
 if t == 6 and abs(z - a) == 2:
  rk = a + 3 if z > a else a - 4
  n[a + (z - a) // 2] = n[rk]
  n[rk] = 0
 n[z] = p
 n[a] = 0
 n[64] = (a + z) // 2 if t == 1 and abs(z - a) == 16 else -1
 n[65] &= ~(CM.get(a, 0) | CM.get(z, 0))
 if t == 1 and (z < 8 or z > 55):
  n[z] = 5 * p
 return n
def chk(b, sd):
 ks = b.index(6 * sd)
 for s in range(64):
  if b[s] * sd < 0 and ks in gen(b, s):
   return True
 return False
def cast(b, sd):
 k = 60 if sd > 0 else 4
 out = []
 if b[k] == 6 * sd and not chk(b, sd):
  for d, n, m in ((1, 2, 1), (-1, 3, 2)):
   if b[65] & m * (1 if sd > 0 else 4) and b[k + d * (n + 1)] == 4 * sd:
    if not any(b[k + d * i] for i in range(1, n + 1)):
     if not chk(mv(b, k, k + d), sd):
      out.append(k + 2 * d)
 return out
def can(b, sd):
 for s in range(64):
  if b[s] * sd > 0:
   for z in gen(b, s):
    if not chk(mv(b, s, z), sd):
     return True
 return False
def ai(b, sd):
 cand = []
 for s in range(64):
  if b[s] * sd > 0:
   t = abs(b[s])
   for z in gen(b, s) + (cast(b, sd) if t == 6 else []):
    n = mv(b, s, z)
    sc = VAL[abs(b[z])] + randint(0, 3)
    if t < 4:
     sc += 3 - abs(2 * (z % 8) - 7) // 2
    if t in (2, 3) and s // 8 == (7 if sd > 0 else 0):
     sc += 5
    elif t == 5:
     sc -= 3
    if t == 1 and (z < 8 or z > 55):
     sc += 80
    if t == 6 and abs(z - s) == 2:
     sc += 8
    rp = 0
    for q in range(64):
     if n[q] * sd < 0:
      for w in gen(n, q):
       if n[w] == 6 * sd:
        rp = 999
       rp = max(rp, VAL[abs(n[w])])
    if rp == 999:
     continue
    sc -= rp
    if chk(n, -sd):
     sc += 6
     if not can(n, -sd):
      sc += 5000
    cand.append((sc, s, z))
 cand.sort()
 for i in range(len(cand) - 1, -1, -1):
  n = mv(b, cand[i][1], cand[i][2])
  if can(n, -sd) or chk(n, -sd):
   break
 return cand[i][1], cand[i][2]
def clr():
 old = TG[:] + [CS[1]]
 del TG[:]
 CS[1] = -1
 for s in old:
  if s >= 0:
   sq(s)
def rel():
 while getkey():
  pass
def pick(turn):
 while True:
  k = getkey()
  if k in (21, 22):
   return None
  c = CS[0]
  dr = (k == K_DOWN) - (k == K_UP)
  dc = (k == K_RIGHT) - (k == K_LEFT)
  nr, nc = c // 8 + dr, c % 8 + dc
  if (dr or dc) and 0 <= nr < 8 and 0 <= nc < 8:
   CS[0] = nr * 8 + nc
   sq(c)
   sq(CS[0])
   show_screen()
   rel()
  elif k in (24, 95):
   a, hit = CS[1], c in TG
   clr()
   if a >= 0 and hit:
    rel()
    return a, c
   if B[c] * turn > 0:
    CS[1] = c
    ts = gen(B, c)
    if abs(B[c]) == 6:
     ts += cast(B, turn)
    TG.extend([z for z in ts if not chk(mv(B, c, z), turn)])
    for s in TG + [c]:
     sq(s)
   show_screen()
   rel()
def panel(turn, ck, alive, mode):
 fill(PX, 30, 188, 36, WHITE)
 spr(PX + 2, 32, 5, turn > 0, 2)
 ds(PX + 34, 32, "White" if turn > 0 else "Black", TXT, "medium")
 ds(PX + 34, 52, "to move", DIM, "small")
 fill(PX, 72, 188, 52, WHITE)
 if not alive:
  ds(PX + 4, 74, "CHECKMATE" if ck else "STALEMATE", RED, "medium")
  w = "Black wins" if turn > 0 else "White wins"
  ds(PX + 4, 96, w if ck else "draw", TXT, "small")
  ds(PX + 4, 112, "OK = new game", DIM, "small")
 elif ck:
  ds(PX + 4, 76, "CHECK!", RED, "medium")
 elif mode == 2 and turn < 0:
  ds(PX + 4, 78, "thinking...", DIM, "small")
def play(mode):
 B[:] = [-x for x in HOME] + [-1] * 8 + [0] * 32 + [1] * 8 + list(HOME) + [-1, 15]
 CS[0], CS[1] = 52, -1
 del TG[:]
 clear_screen()
 for s in range(64):
  sq(s)
 fill(192, 0, 192, 24, BAR)
 ds(204, 4, "CHESS", GOLD, "medium")
 ds(PX, 152, "arrows + OK to play", DIM, "small")
 turn = 1
 while True:
  ck = chk(B, turn)
  alive = can(B, turn)
  panel(turn, ck, alive, mode)
  show_screen()
  if not alive:
   while True:
    k = getkey()
    if k in (24, 95):
     return True
    if k in (21, 22):
     return False
  if mode == 2 and turn < 0:
   a, z = ai(B, turn)
  else:
   r = pick(turn)
   if r is None:
    return False
   a, z = r
  old = B[:]
  B[:] = mv(B, a, z)
  for s in range(64):
   if old[s] != B[s]:
    sq(s)
  turn = -turn
def title():
 clear_screen()
 ds(120, 6, "CHESS", NAVY, "large")
 for i in range(6):
  spr(76 + i * 40, 40, i, 1, 3)
  spr(76 + i * 40, 80, i, 0, 3)
 ds(108, 134, "1  two players", TXT, "medium")
 ds(108, 158, "2  vs computer", TXT, "medium")
 show_screen()
 while True:
  k = getkey()
  if k == 81:
   return 1
  if k == 82:
   return 2
  if k in (21, 22):
   return 0
def main():
 while True:
  m = title()
  if not m:
   return
  while play(m):
   pass
main()
