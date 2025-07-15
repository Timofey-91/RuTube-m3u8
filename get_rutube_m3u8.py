from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os
import sys

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    service = Service(executable_path="/usr/bin/chromedriver")
    return webdriver.Chrome(service=service, options=options)

def save_debug(driver, step):
    os.makedirs("debug", exist_ok=True)
    with open(f"debug/page_{step}.html", "w") as f:
        f.write(driver.page_source)
    driver.save_screenshot(f"debug/screen_{step}.png")

def get_m3u8():
    driver = setup_driver()
    try:
        # Этап 1: Загрузка страницы
        driver.get("https://rutube.ru/play/embed/3b7d1499da9396462bfd17282d758d30")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        save_debug(driver, "1_loaded")

        # Этап 2: Работа с iframe
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "script"))
        )
        save_debug(driver, "2_iframe")

        # Этап 3: Поиск m3u8
        scripts = driver.find_elements(By.TAG_NAME, "script")
        for script in scripts:
            content = script.get_attribute("innerHTML")
            if "m3u8" in content:
                match = re.search(r'(https?://[^\s]+\.m3u8)', content)
                if match:
                    return match.group(1)

        raise Exception("M3U8 не найдена")
    finally:
        driver.quit()

if __name__ == "__main__":
    try:
        m3u8_url = get_m3u8()
        if m3u8_url:
            with open("rutube.m3u", "w") as f:
                f.write(f"""#EXTM3U
#EXTINF:-1,Rutube Stream
{m3u8_url}
""")
            sys.exit(0)
    except Exception as e:
        print(f"Ошибка: {str(e)}", file=sys.stderr)
    
    sys.exit(1)
