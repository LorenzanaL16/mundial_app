import sqlite3
import math
import os

DB = 'mundial.db'
if not os.path.exists(DB):
    print('No se encontró mundial.db. Ejecuta crear_bd.py primero.')
    exit(1)

def ensure_columns(conn):
    cur = conn.cursor()
    cols = [r[1] for r in cur.execute("PRAGMA table_info(matches)")]
    needed = ["pred_probA", "pred_probD", "pred_probB", "predicted", "predicted_home_score", "predicted_away_score", "pred_confidence", "source"]
    for n in needed:
        if n not in cols:
            cur.execute(f"ALTER TABLE matches ADD COLUMN {n}")
    conn.commit()

def poisson_pmf(k, lam):
    return (lam**k) * math.exp(-lam) / math.factorial(k)

conn = sqlite3.connect(DB)
cur = conn.cursor()
ensure_columns(conn)

# load team ranking
team_rank = {}
for name, ranking in cur.execute('SELECT name, ranking FROM teams'):
    try:
        team_rank[name] = float(ranking) if ranking is not None else 50.0
    except:
        team_rank[name] = 50.0

# select matches needing predictions
rows = cur.execute("SELECT id, teamA, teamB FROM matches WHERE pred_probA IS NULL OR pred_confidence IS NULL OR pred_confidence < 0.01").fetchall()

updated = 0
for mid, teamA, teamB in rows:
    rankA = team_rank.get(teamA, 50.0)
    rankB = team_rank.get(teamB, 50.0)
    lamA = max(0.1, 1.2 + (40 - rankA) / 30.0)
    lamB = max(0.1, 1.2 + (40 - rankB) / 30.0)
    max_goal = 5
    winA = 0.0
    draw = 0.0
    winB = 0.0
    expA = 0.0
    expB = 0.0
    total = 0.0
    for ga in range(max_goal+1):
        pa = poisson_pmf(ga, lamA)
        for gb in range(max_goal+1):
            pb = poisson_pmf(gb, lamB)
            p = pa * pb
            total += p
            expA += ga * p
            expB += gb * p
            if ga > gb:
                winA += p
            elif ga == gb:
                draw += p
            else:
                winB += p
    if total == 0:
        continue
    winA /= total
    draw /= total
    winB /= total
    s = winA + draw + winB
    if s > 0:
        winA /= s; draw /= s; winB /= s
    pred = 'A' if winA >= winB and winA >= draw else ('B' if winB >= winA and winB >= draw else 'D')
    ph = int(round(expA/total))
    pa = int(round(expB/total))
    conf = max(winA, draw, winB)
    cur.execute(
        "UPDATE matches SET pred_probA=?, pred_probD=?, pred_probB=?, predicted=?, predicted_home_score=?, predicted_away_score=?, pred_confidence=?, source=? WHERE id=?",
        (winA, draw, winB, pred, ph, pa, conf, 'heuristic', mid)
    )
    updated += 1

conn.commit()
conn.close()
print(f'Predicciones heurísticas aplicadas: {updated}')
