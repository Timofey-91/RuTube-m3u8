from flask import Flask, redirect
from rutube import update_all_streams
import threading
import time

app = Flask(__name__)

# Каналы и их ID
channels_to_update = {
    "kino_i_zhizn": "09e51eefa939595a4ac67182c6fb3e4e",
    "kinozhelezo": "4965b7b928c4a143d708ab424be01d37",
    "sreda": "5fa486bf465c8735fff9f41b372610cc"
}

# Кэш ссылок
m3u8_cache = {}

def auto_update_streams():
    """
    Обновление потоков раз в неделю в фоновом потоке.
    """
    while True:
        print("🔄 Обновление ссылок на потоки...")
        updated = update_all_streams(channels_to_update)
        m3u8_cache.update(updated)
        time.sleep(7 * 24 * 60 * 60)  # раз в 7 дней

@app.route("/channel/<channel_name>")
def serve_channel(channel_name):
    """
    Перенаправление сразу на прямую m3u8 ссылку.
    """
    m3u8_url = m3u8_cache.get(channel_name)
    if not m3u8_url:
        return "Channel not found or stream unavailable", 404
    return redirect(m3u8_url, code=302)

if __name__ == "__main__":
    # начальное обновление и запуск сервера
    m3u8_cache.update(update_all_streams(channels_to_update))

    # поток для автообновления
    updater_thread = threading.Thread(target=auto_update_streams, daemon=True)
    updater_thread.start()

    app.run(host="0.0.0.0", port=8000)
