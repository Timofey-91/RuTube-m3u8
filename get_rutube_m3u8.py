import requests
import re
import json
from urllib.parse import unquote

def get_m3u8_url():
    # Метод 1: Через основной API
    try:
        api_url = "https://rutube.ru/api/play/options/3b7d1499da9396462bfd17282d758d30/"
        params = {
            "no_404": "true",
            "pver": "v2",
            "client": "wdp"
        }
        response = requests.get(api_url, params=params, timeout=10)
        data = response.json()
        if "video_balancer" in data and "m3u8" in data["video_balancer"]:
            return data["video_balancer"]["m3u8"]
    except:
        pass

    # Метод 2: Через embed-страницу
    try:
        embed_url = "https://rutube.ru/play/embed/3b7d1499da9396462bfd17282d758d30"
        response = requests.get(embed_url, timeout=10)
        match = re.search(r'"m3u8":"(https?://[^"]+)"', response.text)
        if match:
            return unquote(match.group(1))
    except:
        pass

    # Метод 3: Через публичный API
    try:
        public_api = "https://rutube.ru/api/video/3b7d1499da9396462bfd17282d758d30/"
        response = requests.get(public_api, timeout=10)
        data = response.json()
        if "video_balancer" in data and "m3u8" in data["video_balancer"]:
            return data["video_balancer"]["m3u8"]
    except:
        pass

    return None

if __name__ == "__main__":
    m3u8_url = get_m3u8_url()
    
    if m3u8_url:
        # Проверяем доступность ссылки
        try:
            test = requests.head(m3u8_url, timeout=5)
            if test.status_code == 200:
                with open("rutube.m3u", "w", encoding="utf-8") as f:
                    f.write(f"""#EXTM3U
#EXTINF:-1 tvg-id="rutube" tvg-name="Rutube Stream",Rutube Live
{m3u8_url}
""")
                print("M3U8 URL успешно получена и проверена")
                exit(0)
        except:
            pass
    
    print("Все методы получения M3U8 URL не сработали")
    exit(1)
