import requests
import re
from urllib.parse import unquote

def extract_m3u8_from_embed(embed_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://rutube.ru"
    }
    
    try:
        # Получаем HTML embed-страницы
        response = requests.get(embed_url, headers=headers)
        response.raise_for_status()
        
        # Ищем закодированную ссылку на m3u8 в JavaScript-данных
        encoded_m3u8 = re.search(r'videoBalancer":{"m3u8":"(https?%3A%2F%2F[^"]+)', response.text)
        if encoded_m3u8:
            return unquote(encoded_m3u8.group(1))
        
        # Альтернативный поиск (если Rutube изменил структуру)
        direct_m3u8 = re.search(r'(https?://[^\s]+\.m3u8)', response.text)
        if direct_m3u8:
            return direct_m3u8.group(0)
            
        raise Exception("M3U8 not found in embed page")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

if __name__ == "__main__":
    EMBED_URL = "https://rutube.ru/play/embed/3b7d1499da9396462bfd17282d758d30"
    m3u8_url = extract_m3u8_from_embed(EMBED_URL)
    
    if m3u8_url:
        # Формируем M3U-плейлист
        with open("rutube_stream.m3u", "w") as f:
            f.write(f"#EXTM3U\n#EXTINF:-1,Rutube Live\n{m3u8_url}")
        print("M3U-плейлист обновлён!")
    else:
        print("Не удалось извлечь M3U8")
        exit(1)
