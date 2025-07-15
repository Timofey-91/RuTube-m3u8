import requests
import json

def get_m3u8_url():
    api_url = "https://rutube.ru/api/play/options/3b7d1499da9396462bfd17282d758d30/"
    params = {
        "no_404": "true",
        "referer": "",
        "pver": "v2",
        "client": "wdp"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json"
    }

    try:
        response = requests.get(api_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        m3u8_url = data.get("video_balancer", {}).get("m3u8")
        
        if not m3u8_url:
            raise ValueError("M3U8 URL не найдена в ответе API")
            
        return m3u8_url

    except Exception as e:
        print(f"API Error: {e}")
        return None

if __name__ == "__main__":
    m3u8_url = get_m3u8_url()
    
    if m3u8_url:
        playlist = f"""#EXTM3U
#EXTINF:-1 tvg-id="rutube" tvg-name="Rutube Stream" tvg-logo="https://rutube.ru/favicon.ico",Rutube Live
{m3u8_url}
#EXTGRP:Live Streams
"""
        with open("rutube.m3u", "w", encoding="utf-8") as f:
            f.write(playlist)
        print("Плейлист успешно обновлён")
    else:
        print("Не удалось получить M3U8 URL")
        exit(1)
