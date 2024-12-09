from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def scrape(url):
    driver_path = "./chromedriver.exe"

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")  # Mimic human behavior
    options.add_argument("--start-maximized")  # Ensures the full page loads
    options.add_argument("--disable-extensions")  # Disable unnecessary browser extensions
    options.add_argument("--no-sandbox")  # Fixes some permission issues

    driver = webdriver.Chrome(service=Service(driver_path), options=options)

    try: 
        driver.get(url)
        # Wait until the DOM is fully loaded
        WebDriverWait(driver, 20).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        
        html = driver.page_source
        
        return html
    finally:
        driver.quit()



def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    body = soup.body
    if body:
        for content in soup(["script", "style"]):
            content.extract() # get rid of tags
        clean_content = soup.get_text(separator="\n")
        clean_content = "\n".join(line.strip() for line in clean_content.splitlines() if line.strip()) # if \n is not seperating anything this will remove it

        return clean_content
    return None


def split(content, max_length=8000):
    batch = [content[i :i +max_length] for i in range(0, len(content), max_length)] # keeps grabbing wtv the max lenght is until the end
    return batch


