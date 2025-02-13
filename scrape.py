from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = 'https://www.ukh.edu.krd/news/'
driver.get(url)

WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".title"))
)

mention_count = 0
target_text = "republic of dreams"
unique_articles = set()

last_height = driver.execute_script("return document.body.scrollHeight")
new_articles_found = True

while new_articles_found:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    current_height = driver.execute_script("return document.body.scrollHeight")
    if current_height == last_height:
        new_articles_found = False
    else:
        last_height = current_height

news_articles = driver.find_elements(By.CSS_SELECTOR, ".title")
print(f"Found {len(news_articles)} articles on this page.")

for article in news_articles:
    article_text = article.text.lower().strip()
    if article_text not in unique_articles:
        print(article_text)
        unique_articles.add(article_text)
        mention_count += len(re.findall(target_text, article_text, re.IGNORECASE))

print(f"The term '{target_text}' was mentioned {mention_count} times on this page.")

driver.quit()
