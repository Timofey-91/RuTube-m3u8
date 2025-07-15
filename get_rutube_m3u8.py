import requests
import re

def get_m3u8(video_id):
    try:
        # Пробуем получить m3u8 через API Rutube
        api_url = f"https://rutube.ru/api/play/options/{video_id}/?no_404=true"
        response = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"})
        data = response.json()
        return data["video_balancer"]["m3u8"]
    except:
        # Если API не работает, парсим страницу
        embed_url = f"https://rutube.ru/play/embed/{video_id}"
        html = requests.get(embed_url).text
        m3u8 = re.search(r'(https?://[^\s]+\.m3u8)', html).group(0)
        return m3u8 if m3u8 else None

if __name__ == "__main__":
    VIDEO_ID = "3b7d1499da9396462bfd17282d758d30"
    m3u8_url = get_m3u8(VIDEO_ID)
    
    if m3u8_url:
        with open("playlist.m3u", "w") as f:
            f.write(f"#EXTM3U\n#EXTINF:-1,Rutube Stream\n{m3u8_url}")
        print("M3U-плейлист обновлён!")
    else:
        print("Ошибка: не удалось получить ссылку")
        exit(1)
