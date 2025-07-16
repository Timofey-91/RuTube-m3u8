import requests

def get_m3u8_url(video_id):
    """
    Получает ссылку на m3u8-поток по video_id с Rutube.
    Возвращает строку URL или None при ошибке.
    """
    try:
        response = requests.get("https://rutube.ru/api/play/options", params={"video_id": video_id}, timeout=10)
        response.raise_for_status()
        data = response.json()
        hls_streams = data.get("live_streams", {}).get("hls", [])
        if hls_streams:
            return hls_streams[0].get("url")
    except requests.exceptions.RequestException as e:
        print(f"HTTP ошибка при получении потока Rutube: {e}")
    except Exception as e:
        print(f"Ошибка при обработке данных от Rutube: {e}")
    return None
