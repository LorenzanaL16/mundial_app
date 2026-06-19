import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
import pickle

# =========================
# 1. CARGAR DATASET
# =========================

df = pd.read_csv("results.csv")

# =========================
# 2. LIMPIEZA BÁSICA
# =========================

df = df.dropna()

# =========================
# 3. FEATURE ENGINEERING
# =========================

df["goal_diff"] = df["home_score"] - df["away_score"]

# Etiqueta: 1 = gana local, 0 = empate, 2 = gana visita
def resultado(row):
    if row["home_score"] > row["away_score"]:
        return 1
    elif row["home_score"] < row["away_score"]:
        return 2
    else:
        return 0

df["result"] = df.apply(resultado, axis=1)

# =========================
# 4. FEATURES
# =========================

X = df[["home_score", "away_score", "goal_diff"]]
y = df["result"]

# =========================
# 5. TRAIN / TEST
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# 6. MODELO
# =========================

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# =========================
# 7. PREDICCIONES
# =========================

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average="macro")

print("\n📊 RESULTADOS DEL MODELO")
print("Accuracy:", round(accuracy, 4))
print("F1-score:", round(f1, 4))

# =========================
# 8. GUARDAR MODELO
# =========================

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\n✅ Modelo guardado como model.pkl")