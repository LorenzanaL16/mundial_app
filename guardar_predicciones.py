import pickle
import sqlite3
import os
import math
from collections import defaultdict

DB = 'mundial.db'
MODEL_PKL = 'model.pkl'

if not os.path.exists(DB):
    print('Base de datos no encontrada. Ejecuta crear_bd.py primero.')
    exit(1)

if not os.path.exists(MODEL_PKL):
    print('Modelo model.pkl no encontrado. Asegúrate de entrenarlo con model.py.')
    exit(1)

# load model
with open(MODEL_PKL, 'rb') as f:
    model = pickle.load(f)

# determine class order if available
classes = getattr(model, 'classes_', None)
# model trained with labels: 1=home win,0=draw,2=away win
# we'll map indices accordingly

# helper: poisson pmf
def poisson_pmf(k, lam):
    return (lam**k) * math.exp(-lam) / math.factorial(k)

# helper: ensure columns exist
def ensure_columns(conn):
    cur = conn.cursor()
    cols = [r[1] for r in cur.execute("PRAGMA table_info(matches)")]
    needed = ["predicted_home_score", "predicted_away_score", "pred_confidence"]
    for n in needed:
        if n not in cols:
            cur.execute(f"ALTER TABLE matches ADD COLUMN {n} INTEGER")
    conn.commit()

conn = sqlite3.connect(DB)
cur = conn.cursor()
ensure_columns(conn)

# fetch matches to update predictions using the trained model
cur.execute("SELECT id, teamA, teamB, flagA, flagB, pred_probA, pred_probD, pred_probB, source FROM matches")
rows = cur.fetchall()

# load team rankings for strength estimation
team_rank = {}
for row in cur.execute('SELECT name, ranking FROM teams'):
    team_rank[row[0]] = row[1]

updated = 0
for r in rows:
    mid, teamA, teamB, flagA, flagB, pA, pD, pB, source = r

    rankA = team_rank.get(teamA, 50)
    rankB = team_rank.get(teamB, 50)

    # estimate expected goals (lambda) from ranking
    # stronger teams (lower ranking) get higher lambda
    # baseline = 1.2
    lamA = max(0.2, 1.2 + (40 - rankA) / 30.0)
    lamB = max(0.2, 1.2 + (40 - rankB) / 30.0)

    # compute distribution over goals 0..5
    max_goal = 5
    dist = []
    for ga in range(max_goal+1):
        pa = poisson_pmf(ga, lamA)
        for gb in range(max_goal+1):
            pb = poisson_pmf(gb, lamB)
            prob_combo = pa * pb
            dist.append((ga, gb, prob_combo))

    # normalize
    total = sum(x[2] for x in dist)
    if total == 0:
        continue
    dist = [(ga, gb, pc/total) for ga, gb, pc in dist]

    # aggregate predicted probabilities using model
    prob_acc = None
    # prepare feature list for batch predict
    X = [[ga, gb, ga-gb] for ga, gb, _ in dist]
    try:
        probs = model.predict_proba(X)
        # find class indices mapping
        # classes might be in arbitrary order
        if classes is None:
            # assume order [0,1,2] or similar; find indices
            class_idx = {c:i for i,c in enumerate(model.classes_)}
        else:
            class_idx = {c:i for i,c in enumerate(classes)}
        # mapping: 1 -> home win, 0 -> draw, 2 -> away win
        idx_home = class_idx.get(1)
        idx_draw = class_idx.get(0)
        idx_away = class_idx.get(2)

        pred_probA = 0.0
        pred_probD = 0.0
        pred_probB = 0.0
        exp_home = 0.0
        exp_away = 0.0

        for (ga, gb, pc), prob_row in zip(dist, probs):
            pred_probA += prob_row[idx_home] * pc if idx_home is not None else 0
            pred_probD += prob_row[idx_draw] * pc if idx_draw is not None else 0
            pred_probB += prob_row[idx_away] * pc if idx_away is not None else 0
            exp_home += ga * pc
            exp_away += gb * pc

        # normalize
        s = pred_probA + pred_probD + pred_probB
        if s > 0:
            pred_probA /= s
            pred_probD /= s
            pred_probB /= s

        predicted = 'A' if pred_probA >= pred_probB and pred_probA >= pred_probD else ('B' if pred_probB >= pred_probA and pred_probB >= pred_probD else 'D')
        pred_scoreA = int(round(exp_home))
        pred_scoreB = int(round(exp_away))
        pred_conf = max(pred_probA, pred_probD, pred_probB)

        # update DB
        cur.execute("UPDATE matches SET pred_probA=?, pred_probD=?, pred_probB=?, predicted=?, predicted_home_score=?, predicted_away_score=?, pred_confidence=?, source=? WHERE id=?",
                    (pred_probA, pred_probD, pred_probB, predicted, pred_scoreA, pred_scoreB, pred_conf, 'model', mid))
        conn.commit()
        updated += 1
    except Exception as e:
        print('Error al predecir para', teamA, teamB, e)

print(f'Predicciones guardadas/actualizadas: {updated}')
conn.close()
