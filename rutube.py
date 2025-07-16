import requests

def get_m3u8_url(video_id):
    try:
        url = f"https://rutube.ru/api/play/options/{video_id}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        hls_streams = data.get("live_streams", {}).get("hls", [])
        if hls_streams:
            return hls_streams[0].get("url")
    except requests.exceptions.RequestException as e:
        print(f"HTTP ошибка: {e}")
    except Exception as e:
        print(f"Ошибка обработки: {e}")
    return None

def update_all_streams(channels_dict):
    updated = {}
    for name, video_id in channels_dict.items():
        print(f"🔍 Обновляем {name}...")
        stream_url = get_m3u8_url(video_id)
        if stream_url:
            print(f"✅ Найден поток для {name}: {stream_url}")
            updated[name] = stream_url
        else:
            print(f"❌ Поток не найден для {name}")
    return updated
