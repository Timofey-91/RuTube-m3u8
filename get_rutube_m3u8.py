import requests
import re
from urllib.parse import unquote
from datetime import datetime

def get_m3u8_from_embed():
    embed_url = "https://rutube.ru/play/embed/3b7d1499da9396462bfd17282d758d30"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://rutube.ru"
    }

    try:
        # Получаем HTML страницы
        response = requests.get(embed_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Основной метод: поиск в JSON-данных
        json_data = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.+?});', response.text)
        if json_data:
            m3u8_match = re.search(r'"m3u8":"(https?%3A%2F%2F[^"]+)', json_data.group(1))
            if m3u8_match:
                return unquote(m3u8_match.group(1))

        # Резервный метод: прямой поиск в HTML
        m3u8_match = re.search(r'(https?://[^\s]+\.m3u8)', response.text)
        if m3u8_match:
            return m3u8_match.group(0)

        raise Exception("M3U8 не найдена в исходном коде")

    except Exception as e:
        print(f"Ошибка: {e}")
        return None

if __name__ == "__main__":
    m3u8_url = get_m3u8_from_embed()
    
    if m3u8_url:
        with open("rutube.m3u", "w") as f:
            f.write(f"""#EXTM3U
#EXTINF:-1 tvg-id="Rutube" tvg-name="Rutube Stream",Rutube Live
{m3u8_url}
#EXTGRP:Лайв
""")
        print(f"{datetime.now()}: Ссылка успешно обновлена")
    else:
        print("Не удалось получить ссылку")
        exit(1)
