import pandas as pd
import numpy as np

data = pd.read_csv("brvm_live.csv")
data["Prix"] = data["Prix"].astype(float)

results = []

# 🔁 BOUCLE SUR TOUTES LES ACTIONS
for action in data["Action"].unique():

    df = data[data["Action"] == action].copy()

    if len(df) < 30:
        continue

    capital = 100000
    position = 0

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

    # 🤖 OPTIMISATION AUTOMATIQUE
    best_gain = 0
    best_params = None

    for rsi_buy in [25, 30, 35]:
        for rsi_sell in [65, 70, 75]:

            capital = 100000
            position = 0

            for i in range(30, len(df)):

                prix = df["Prix"].iloc[i]
                rsi = df["RSI"].iloc[i]
                macd = df["MACD"].iloc[i]
                signal = df["Signal"].iloc[i]

                # STRATÉGIE
                if rsi < rsi_buy and macd > signal and position == 0:
                    position = capital / prix
                    capital = 0

                elif rsi > rsi_sell and macd < signal and position > 0:
                    capital = position * prix
                    position = 0

            final = capital if capital > 0 else position * df["Prix"].iloc[-1]
            gain = final - 100000

            if gain > best_gain:
                best_gain = gain
                best_params = (rsi_buy, rsi_sell)

    results.append((action, best_gain, best_params))

# 🏆 TRI DES MEILLEURES ACTIONS
results = sorted(results, key=lambda x: x[1], reverse=True)

print("\n🏆 TOP ACTIONS RENTABLES :\n")

for action, gain, params in results[:5]:
    print(f"{action}")
    print(f"Gain: {round(gain,2)}")
    print(f"RSI Buy: {params[0]} | RSI Sell: {params[1]}")
    print("----------------------")



    from twilio.rest import Client

    account_sid = "FAUX_SID_POUR_GITHUB"
    auth_token = "d8e46ac40c1b16de451a5c9b39a29e7c"
    client = Client(account_sid, auth_token)

    message = "🏆 TOP ACTIONS BRVM:\n\n"

    for action, gain, params in results[:5]:

     message += f"{action}\nGain: {round(gain,2)}\nRSI: {params[0]}/{params[1]}\n\n"

     client.messages.create(
     body=message,
     from_='whatsapp:+14155238886',
     to='whatsapp:+22997806641'
)

print("📱 TOP envoyés sur WhatsApp !")


df_result = pd.DataFrame(results, columns=["Action", "Gain", "Parametres"])
df_result.to_csv("top_actions.csv", index=False)