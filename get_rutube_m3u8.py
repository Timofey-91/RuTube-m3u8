import requests
import re
import sys
from urllib.parse import unquote

def get_m3u8_url():
    try:
        # Попробуем получить через API
        api_url = "https://rutube.ru/api/play/options/3b7d1499da9396462bfd17282d758d30/"
        response = requests.get(api_url, params={
            "no_404": "true",
            "pver": "v2",
            "client": "wdp"
        }, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if "video_balancer" in data and "m3u8" in data["video_balancer"]:
                return data["video_balancer"]["m3u8"]

        # Если API не сработало, парсим embed-страницу
        embed_url = "https://rutube.ru/play/embed/3b7d1499da9396462bfd17282d758d30"
        response = requests.get(embed_url, timeout=10)
        match = re.search(r'"m3u8"\s*:\s*"([^"]+)"', response.text)
        if match:
            return unquote(match.group(1))

        raise Exception("Ссылка не найдена ни в API, ни на странице")

    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    url = get_m3u8_url()
    if url:
        print(url)
        sys.exit(0)
    sys.exit(1)
