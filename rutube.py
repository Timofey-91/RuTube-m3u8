import requests

def get_m3u8_url(video_id):
    """
    Получает ссылку на m3u8-поток по video_id с Rutube.
    Использует endpoint /api/play/options/{video_id}.
    """
    try:
        url = f"https://rutube.ru/api/play/options/{video_id}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        hls_streams = data.get("live_streams", {}).get("hls", [])
        if hls_streams:
            return hls_streams[0].get("url")
    except requests.exceptions.RequestException as e:
        print(f"HTTP ошибка при получении потока Rutube ({video_id}): {e}")
    except Exception as e:
        print(f"Ошибка при обработке данных от Rutube ({video_id}): {e}")
    return None

