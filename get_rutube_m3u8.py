import requests
import re
import json
from urllib.parse import unquote

def get_m3u8():
    try:
        # Прямой запрос к API Rutube
        api_url = "https://rutube.ru/api/play/options/3b7d1499da9396462bfd17282d758d30/"
        params = {
            "no_404": "true",
            "pver": "v2",
            "client": "wdp"
        }
        response = requests.get(api_url, params=params, timeout=10)
        data = response.json()
        
        # Основной способ получения ссылки
        m3u8_url = data.get("video_balancer", {}).get("m3u8")
        if m3u8_url:
            return m3u8_url
        
        # Альтернативный способ для старых версий API
        embed_url = "https://rutube.ru/play/embed/3b7d1499da9396462bfd17282d758d30"
        html = requests.get(embed_url).text
        match = re.search(r'"m3u8":"(https?://[^"]+)"', html)
        if match:
            return unquote(match.group(1))
        
        # Если ничего не найдено
        raise Exception("Ссылка не найдена в API и HTML")
    
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

if __name__ == "__main__":
    m3u8_url = get_m3u8()
    
    if m3u8_url:
        # Формируем M3U-плейлист
        playlist = f"""#EXTM3U
#EXTINF:-1,Rutube Stream
{m3u8_url}
"""
        print(playlist)  # Выводим результат в консоль
        
        with open("rutube.m3u", "w", encoding="utf-8") as f:
            f.write(playlist)
    else:
        print("Не удалось получить ссылку на поток")
        exit(1)
