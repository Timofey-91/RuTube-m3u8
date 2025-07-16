import requests

def get_m3u8_url(video_id):
    """
    Получает ссылку на m3u8-поток по video_id с Rutube.
    """
    try:
        url = f"https://rutube.ru/api/play/options/{video_id}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        hls_streams = data.get("live_streams", {}).get("hls", [])
        if hls_streams:
            return hls_streams[0].get("url")
    except Exception as e:
        print(f"Ошибка для {video_id}: {e}")
    return None

def update_all_streams(channel_dict):
    """
    Обновляет все каналы и возвращает словарь {channel_name: m3u8_url}
    """
    result = {}
    for name, video_id in channel_dict.items():
        url = get_m3u8_url(video_id)
        if url:
            result[name] = url
    return result
