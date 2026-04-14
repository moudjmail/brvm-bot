import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from twilio.rest import Client

# Charger données
data = pd.read_csv("brvm_live.csv")

# Convertir prix en nombre
data["Prix"] = data["Prix"].astype(float)

# Twilio
account_sid = "AC_CeciEstUnFauxSIDPourLaSecurite_12345"
auth_token = "d8e46ac40c1b16de451a5c9b39a29e7c"
client = Client(account_sid, auth_token)

meilleures_actions = []

# 🔁 BOUCLE SUR CHAQUE ACTION
for action in data["Action"].unique():

    df_action = data[data["Action"] == action].copy()

    # Besoin de plusieurs points
    if len(df_action) < 5:
    
    # Calcul RSI
      delta = df_action["Prix"].diff()

      gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
      loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

      rs = gain / loss
      rsi = 100 - (100 / (1 + rs))

      rsi_value = rsi.iloc[-1]


      df_action["Index"] = np.arange(len(df_action))


      # ✅ MACD
      ema12 = df_action["Prix"].ewm(span=12, adjust=False).mean()
      ema26 = df_action["Prix"].ewm(span=26, adjust=False).mean()

      macd = ema12 - ema26
      signal_line = macd.ewm(span=9, adjust=False).mean()

      macd_value = macd.iloc[-1]
      signal_value = signal_line.iloc[-1]



      X = df_action[["Index"]]
      y = df_action["Prix"]

      model = LinearRegression()
      model.fit(X, y)

      future = pd.DataFrame([[len(df_action) + 1]], columns=["Index"])
      prediction = model.predict(future)

      last_price = y.iloc[-1]

      variation = (prediction[0] - last_price) / last_price * 100









    # 🎯 FILTRE INTELLIGENT
      if variation > 2 and rsi_value < 30 and macd_value > signal_value:
       meilleures_actions.append((action, last_price, variation, rsi_value, macd_value, score))

# 📊 Trier les meilleures
    meilleures_actions = sorted(meilleures_actions, key=lambda x: x[5], reverse=True)

# 🏆 TOP 3
top = meilleures_actions[:3]

# 📱 ENVOI WHATSAPP
if top:
    message_text = "🏆 TOP OPPORTUNITÉS BRVM:\n\n"

    for action, prix, var, rsi_val, macd_val, score in top:
      message_text += f"{action} 🏆\nPrix: {prix}\nGain: {round(var,2)}%\nRSI: {round(rsi_val,2)}\nScore: {score}/6\n\n"

    client.messages.create(
        body=message_text,
        from_='whatsapp:+14155238886',
        to='whatsapp:+22997806641'
    )

    print("✅ Top opportunités envoyées !")
else:
    print("Aucune opportunité forte aujourd'hui")