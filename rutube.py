import requests
import re

def get_stream_link(video_id):
    url = f"https://rutube.ru/api/play/options/{video_id}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    data = res.json()
    return data.get("m3u8", "")
