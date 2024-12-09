from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


def scrape(url, max_scroll=10):
    driver_path = "./chromedriver.exe"

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")  # Mimic human behavior
    options.add_argument("--start-maximized")  # Ensures the full page loads
    options.add_argument("--disable-extensions")  # Disable unnecessary browser extensions
    options.add_argument("--no-sandbox")  # Fixes some permission issues

    driver = webdriver.Chrome(service=Service(driver_path), options=options)

    try: 
        driver.get(url)
        for _ in range(max_scroll):
            # Scroll down the page incase website uses lazy loading
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
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


model = OllamaLLM(model="llama3.1")

template = (
    "You are tasked with extracting specific information from the following text content: {content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {user_prompt}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def llm_parse(chunks, user_prompt):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    res = []

    for i, chunk in enumerate(chunks, start=0):
        response = chain.invoke({"content": chunk, "user_prompt": user_prompt})
        res.append(response)
    
    return "\n".join(res) 