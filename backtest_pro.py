import pandas as pd
import numpy as np

data = pd.read_csv("brvm_live.csv")
data["Prix"] = data["Prix"].astype(float)

# Choisir une action (ex: première)
action = data["Action"].unique()[0]
df = data[data["Action"] == action].copy()

capital = 100000
position = 0

df["Index"] = np.arange(len(df))

# RSI
delta = df["Prix"].diff()
gain = (delta.where(delta > 0, 0)).rolling(14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
rs = gain / loss
df["RSI"] = 100 - (100 / (1 + rs))

# MACD
ema12 = df["Prix"].ewm(span=12).mean()
ema26 = df["Prix"].ewm(span=26).mean()
df["MACD"] = ema12 - ema26
df["Signal"] = df["MACD"].ewm(span=9).mean()

historique = []

for i in range(30, len(df)):

    prix = df["Prix"].iloc[i]
    rsi = df["RSI"].iloc[i]
    macd = df["MACD"].iloc[i]
    signal = df["Signal"].iloc[i]

    # 🎯 STRATÉGIE
    if rsi < 35 and macd > signal and position == 0:
        position = capital / prix
        capital = 0
        print(f"ACHAT à {prix}")

    elif rsi > 70 and macd < signal and position > 0:
        capital = position * prix
        position = 0
        print(f"VENTE à {prix}")

    valeur = capital if capital > 0 else position * prix
    historique.append(valeur)

# Résultat
final = historique[-1] if historique else capital

print("\n💰 Capital final :", round(final, 2))
print("📊 Gain :", round(final - 100000, 2))