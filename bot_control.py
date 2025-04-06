import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AUTHORIZED_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Para evitar que cualquiera lo active
FILE_ESTADO = "estado.txt"

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message", {})
    chat_id = str(message.get("chat", {}).get("id"))
    text = message.get("text", "").strip().lower()

    if chat_id != AUTHORIZED_CHAT_ID:
        return "Unauthorized", 403

    if text == "/activar":
        with open(FILE_ESTADO, "w") as f:
            f.write("activo")
        enviar_telegram("✅ Monitorización ACTIVADA")
    elif text == "/desactivar":
        with open(FILE_ESTADO, "w") as f:
            f.write("inactivo")
        enviar_telegram("🛑 Monitorización DESACTIVADA")
    else:
        enviar_telegram("Comandos válidos: /activar /desactivar")

    return "OK", 200

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": AUTHORIZED_CHAT_ID, "text": mensaje}
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
