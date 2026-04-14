import pandas as pd

# Charger données
data = pd.read_csv("brvm_live.csv")

data["Prix"] = data["Prix"].astype(float)

capital = 100000  # argent de départ
position = 0
historique = []

for i in range(1, len(data)):

    prix_aujourdhui = data["Prix"].iloc[i]
    prix_hier = data["Prix"].iloc[i-1]

    # Stratégie simple
    if prix_aujourdhui > prix_hier and position == 0:
        position = capital / prix_aujourdhui
        capital = 0
        print(f"ACHAT à {prix_aujourdhui}")

    elif prix_aujourdhui < prix_hier and position > 0:
        capital = position * prix_aujourdhui
        position = 0
        print(f"VENTE à {prix_aujourdhui}")

    historique.append(capital if capital > 0 else position * prix_aujourdhui)

# Résultat final
final = historique[-1]

print("\n💰 Capital final :", round(final, 2))
print("📊 Gain :", round(final - 100000, 2))