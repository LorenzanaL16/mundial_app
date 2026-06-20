import sqlite3
import sqlite3
import os
import csv
import json
from datetime import datetime

DB_PATH = "mundial.db"

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

import app

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Create teams table
cur.execute(
    """
    CREATE TABLE teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        ranking INTEGER,
        flag TEXT,
        group_name TEXT
    )
    """
)

# Create matches table (includes historical and prediction fields)
cur.execute(
    """
    CREATE TABLE matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupo TEXT,
        date TEXT,
        location TEXT,
        teamA TEXT,
        teamB TEXT,
        flagA TEXT,
        flagB TEXT,
        probWinA REAL,
        probDraw REAL,
        probWinB REAL,
        home_score INTEGER,
        away_score INTEGER,
        predicted TEXT,
        pred_probA REAL,
        pred_probD REAL,
        pred_probB REAL,
        source TEXT
    )
    """
)

# Insert teams from app data
teams = getattr(app, "equipos", None)
if teams is None:
    teams = []

for t in teams:
    cur.execute(
        "INSERT OR IGNORE INTO teams (name, ranking, flag, group_name) VALUES (?,?,?,?)",
        (t.get("name"), t.get("ranking"), t.get("flag"), t.get("group")),
    )

# Insert internal matches (simulated / predicted)
matches = getattr(app, "matches", [])
for m in matches:
    flagA = m.get("flagA") if m.get("flagA") is not None else app.flags.get(m.get("teamA"))
    flagB = m.get("flagB") if m.get("flagB") is not None else app.flags.get(m.get("teamB"))

    # normalize probabilities
    try:
        probA = float(m.get("probWinA") or 0)
        probB = float(m.get("probWinB") or 0)
        probD = float(m.get("probDraw") or 0)
    except Exception:
        probA = probB = probD = 0

    total = probA + probB + probD
    if total > 0:
        probA /= total
        probB /= total
        probD /= total

    # predicted outcome from probabilities
    if probA >= probB and probA >= probD:
        predicted = "A"
    elif probB >= probA and probB >= probD:
        predicted = "B"
    else:
        predicted = "D"

    cur.execute(
        "INSERT INTO matches (grupo, date, location, teamA, teamB, flagA, flagB, probWinA, probDraw, probWinB, home_score, away_score, predicted, pred_probA, pred_probD, pred_probB, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (
            m.get("grupo"),
            m.get("date"),
            m.get("location"),
            m.get("teamA"),
            m.get("teamB"),
            flagA,
            flagB,
            m.get("probWinA"),
            m.get("probDraw"),
            m.get("probWinB"),
            None,
            None,
            predicted,
            probA,
            probD,
            probB,
            "simulated",
        ),
    )

# If there's a Kaggle results CSV, import it (heuristic mapping)
CSV_PATH = "results.csv"
if os.path.exists(CSV_PATH):
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # heuristics to find teams and scores
            keys = {k.lower(): k for k in row.keys()}
            # possible column names
            teamA_key = keys.get('home_team') or keys.get('team_a') or keys.get('home') or keys.get('teama') or keys.get('team_a_name') or keys.get('team1')
            teamB_key = keys.get('away_team') or keys.get('team_b') or keys.get('away') or keys.get('teamb') or keys.get('team_b_name') or keys.get('team2')
            home_score_key = keys.get('home_score') or keys.get('home_goals') or keys.get('score_home') or keys.get('home_goals')
            away_score_key = keys.get('away_score') or keys.get('away_goals') or keys.get('score_away') or keys.get('away_goals')
            date_key = keys.get('date') or keys.get('match_date')

            if not teamA_key or not teamB_key:
                continue

            teamA = row[teamA_key]
            teamB = row[teamB_key]
            try:
                home_score = int(row[home_score_key]) if home_score_key and row.get(home_score_key) != '' else None
            except Exception:
                home_score = None
            try:
                away_score = int(row[away_score_key]) if away_score_key and row.get(away_score_key) != '' else None
            except Exception:
                away_score = None

            date_val = row.get(date_key) if date_key else None
            # find flags from app
            flagA = app.flags.get(teamA)
            flagB = app.flags.get(teamB)

            # determine predicted based on scores if present
            if home_score is not None and away_score is not None:
                if home_score > away_score:
                    predicted = 'A'
                elif home_score < away_score:
                    predicted = 'B'
                else:
                    predicted = 'D'
            else:
                predicted = None

            cur.execute(
                "INSERT INTO matches (grupo, date, location, teamA, teamB, flagA, flagB, probWinA, probDraw, probWinB, home_score, away_score, predicted, pred_probA, pred_probD, pred_probB, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    None,
                    date_val,
                    None,
                    teamA,
                    teamB,
                    flagA,
                    flagB,
                    None,
                    None,
                    None,
                    home_score,
                    away_score,
                    predicted,
                    None,
                    None,
                    None,
                    'kaggle',
                ),
            )

conn.commit()

# Export a CSV with matches + predictions
CSV_OUT = 'predictions_export.csv'
with open(CSV_OUT, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id','grupo','date','teamA','teamB','home_score','away_score','predicted','pred_probA','pred_probD','pred_probB','source'])
    for row in cur.execute('SELECT id, grupo, date, teamA, teamB, home_score, away_score, predicted, pred_probA, pred_probD, pred_probB, source FROM matches'):
        writer.writerow(row)

# Quick verification
cur.execute("SELECT COUNT(*) FROM teams")
teams_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM matches")
matches_count = cur.fetchone()[0]

print(f"DB created at {DB_PATH}")
print(f"Teams inserted: {teams_count}")
print(f"Matches inserted: {matches_count}")
print(f"Exported CSV: {CSV_OUT}")

# Show sample teams
cur.execute("SELECT name, ranking, group_name FROM teams ORDER BY ranking ASC LIMIT 10")
rows = cur.fetchall()
print("\nTop sample teams by ranking:")
for r in rows:
    print(f"- {r[0]} (Ranking #{r[1]}) - {r[2]}")

conn.close()
