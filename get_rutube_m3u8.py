from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import json
import os

def save_debug_info(driver, step):
    if not os.path.exists('debug'):
        os.makedirs('debug')
    timestamp = int(time.time())
    with open(f'debug/page_{step}_{timestamp}.html', 'w') as f:
        f.write(driver.page_source)
    driver.save_screenshot(f'debug/screen_{step}_{timestamp}.png')

def get_m3u8_url():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    try:
        # Шаг 1: Загружаем embed-страницу
        driver.get("https://rutube.ru/play/embed/3b7d1499da9396462bfd17282d758d30")
        time.sleep(5)
        save_debug_info(driver, '1_loaded')

        # Шаг 2: Ищем iframe с плеером
        iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        for iframe in iframes:
            driver.switch_to.frame(iframe)
            time.sleep(2)
            save_debug_info(driver, '2_iframe')
            
            # Шаг 3: Ищем JSON-данные в скриптах
            scripts = driver.find_elements(By.TAG_NAME, 'script')
            for script in scripts:
                if 'm3u8' in script.get_attribute('innerHTML'):
                    content = script.get_attribute('innerHTML')
                    match = re.search(r'"m3u8"\s*:\s*"([^"]+)"', content)
                    if match:
                        return match.group(1)
            
            driver.switch_to.default_content()

        # Шаг 4: Альтернативный поиск в основном контенте
        scripts = driver.find_elements(By.TAG_NAME, 'script')
        for script in scripts:
            content = script.get_attribute('innerHTML')
            if 'm3u8' in content:
                match = re.search(r'https?://[^\s]+\.m3u8', content)
                if match:
                    return match.group(0)

        raise Exception("M3U8 URL не найдена")

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        save_debug_info(driver, 'error')
        return None
    finally:
        driver.quit()

if __name__ == "__main__":
    m3u8_url = get_m3u8_url()
    
    if m3u8_url:
        print(f"Найдена ссылка: {m3u8_url}")
        with open("rutube.m3u", "w") as f:
            f.write(f"""#EXTM3U
#EXTINF:-1,Rutube Stream
{m3u8_url}
""")
        exit(0)
    else:
        print("Не удалось получить M3U8 URL")
        exit(1)
