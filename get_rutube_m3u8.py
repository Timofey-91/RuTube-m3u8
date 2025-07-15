import requests
import re
import json
from urllib.parse import unquote

def get_m3u8_from_embed():
    embed_url = "https://rutube.ru/play/embed/3b7d1499da9396462bfd17282d758d30"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://rutube.ru"
    }

    try:
        # Получаем HTML страницы
        response = requests.get(embed_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Ищем JSON-данные в скрипте
        json_match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.+?});', response.text)
        if not json_match:
            raise Exception("Не найден INITIAL_STATE в HTML")
            
        data = json.loads(json_match.group(1))
        
        # Извлекаем m3u8 из структуры JSON
        m3u8_url = data.get('currentVideo', {}).get('videoBalancer', {}).get('m3u8')
        if not m3u8_url:
            raise Exception("M3U8 не найдена в JSON-данных")
            
        return m3u8_url

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
        print("Ссылка успешно обновлена!")
    else:
        print("Не удалось получить ссылку")
        exit(1)
