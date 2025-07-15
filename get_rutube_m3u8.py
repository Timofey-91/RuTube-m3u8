from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import re

def get_m3u8_url():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    try:
        driver.get("https://rutube.ru/play/embed/3b7d1499da9396462bfd17282d758d30")
        time.sleep(5)  # Ожидаем загрузки страницы
        
        # Ищем данные в JavaScript
        page_source = driver.page_source
        m3u8_match = re.search(r'"m3u8":"(https?://[^"]+)"', page_source)
        
        if m3u8_match:
            return m3u8_match.group(1)
            
        raise Exception("M3U8 URL не найдена")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    try:
        m3u8_url = get_m3u8_url()
        
        with open("rutube.m3u", "w") as f:
            f.write(f"""#EXTM3U
#EXTINF:-1,Rutube Stream
{m3u8_url}
""")
        print("M3U8 URL успешно получена!")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        exit(1)
