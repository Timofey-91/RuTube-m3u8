from flask import Flask, redirect, abort
import requests
import threading
import time

app = Flask(__name__)

# Список каналов и их Rutube video_id
channels_to_update = {
    "Кино и жизнь": "09e51eefa939595a4ac67182c6fb3e4e",
    "Киножелезо": "4965b7b928c4a143d708ab424be01d37",
    "Среда": "5fa486bf465c8735fff9f41b372610cc"
}

# Хранилище актуальных ссылок
channel_links = {}

def get_m3u8_url(video_id):
    try:
        response = requests.get("https://rutube.ru/api/play/options", params={"video_id": video_id})
        response.raise_for_status()
        data = response.json()
        hls_streams = data.get("live_streams", {}).get("hls", [])
        if hls_streams:
            return hls_streams[0].get("url")
    except Exception as e:
        print(f"Ошибка при получении потока для {video_id}: {e}")
    return None

def update_links():
    global channel_links
    print("⏳ Обновление ссылок...")
    for name, video_id in channels_to_update.items():
        url = get_m3u8_url(video_id)
        if url:
            channel_links[name] = url
            print(f"✅ Обновлено: {name} → {url}")
        else:
            print(f"⚠️ Не удалось обновить {name}")
    print("✅ Обновление завершено.")
    
    # Запускаем следующее обновление через 7 дней (604800 секунд)
    threading.Timer(604800, update_links).start()

# Обновим ссылки при старте
update_links()

@app.route("/stream/<channel>")
def stream(channel):
    if channel not in channel_links:
        return abort(404, description="Канал не найден или ссылка не обновлена")
    
    return redirect(channel_links[channel])

@app.route("/")
def home():
    return "✅ RuTube Stream Proxy работает! Используй /stream/Кино и жизнь и т.п."
