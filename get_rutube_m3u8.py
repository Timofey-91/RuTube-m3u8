import requests
import re

def fetch_rutube_m3u8(video_id):
    # 1. Получаем embed-страницу Rutube
    embed_url = f"https://rutube.ru/play/embed/{video_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(embed_url, headers=headers)
        response.raise_for_status()
        
        # 2. Ищем m3u8 в исходном коде (может потребоваться доработка)
        m3u8_match = re.search(r'https?://[^"\s]+\.m3u8', response.text)
        if m3u8_match:
            return m3u8_match.group(0)
        
        # 3. Альтернативный вариант — стандартный URL потока
        return f"https://stream.rutube.ru/hls/{video_id}/master.m3u8"
    
    except Exception as e:
        print(f"Error fetching m3u8: {e}")
        return None

if __name__ == "__main__":
    VIDEO_ID = "3b7d1499da9396462bfd17282d758d30"  # Замените на ваш ID
    m3u8_url = fetch_rutube_m3u8(VIDEO_ID)
    
    if m3u8_url:
        print(f"Found M3U8 URL: {m3u8_url}")
        with open("m3u8_link.txt", "w") as f:
            f.write(m3u8_url)
    else:
        print("Failed to fetch M3U8 URL")
        exit(1)
