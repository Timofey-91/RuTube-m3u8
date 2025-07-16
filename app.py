from flask import Flask, Response, abort
from threading import Thread
import time
from rutube import get_rutube_stream

app = Flask(__name__)

channels_to_update = {
    "kino": "09e51eefa939595a4ac67182c6fb3e4e",
    "kinozhelezo": "4965b7b928c4a143d708ab424be01d37",
    "sreda": "5fa486bf465c8735fff9f41b372610cc"
}

cached_streams = {}

def update_streams():
    while True:
        print("[Updater] Обновление потоков...")
        for name, video_id in channels_to_update.items():
            try:
                stream_url = get_rutube_stream(video_id)
                cached_streams[name] = stream_url
                print(f"[Updater] Обновлено: {name} -> {stream_url}")
            except Exception as e:
                print(f"[Updater] Ошибка при обновлении {name}: {e}")
        print("[Updater] Ожидание 7 дней...")
        time.sleep(7 * 24 * 60 * 60)  # 1 неделя

@app.route("/")
def index():
    return (
        "Доступные каналы:<br>" +
        "<br>".join(f"<a href='/{name}.m3u8'>{name}</a>" for name in channels_to_update)
    )

@app.route("/<channel>.m3u8")
def stream(channel):
    if channel not in cached_streams:
        return abort(404, description="Канал не найден или не обновлён.")
    return Response(cached_streams[channel], mimetype="application/vnd.apple.mpegurl")

if __name__ == "__main__":
    # Начинаем фоновое обновление
    updater = Thread(target=update_streams, daemon=True)
    updater.start()

    # Запуск Flask
    app.run(host="0.0.0.0", port=8000)
