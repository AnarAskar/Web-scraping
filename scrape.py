from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# Step 1: Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no GUI)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Step 2: Visit the direct news page URL
url = 'https://www.ukh.edu.krd/news/'
driver.get(url)

# Step 3: Wait for the page to load
time.sleep(5)  # Wait for page load, increase time if necessary

# Step 4: Initialize the mention counter
mention_count = 0

# Step 5: Loop through all pages until no "Next" anchor tag is found
while True:
    # Step 5.1: Scrape the articles on the current page
    news_articles = driver.find_elements(By.CSS_SELECTOR, ".title")  # Update this CSS selector to match the actual class

    for article in news_articles:
        article_text = article.text.lower()  # Convert text to lowercase for case-insensitive search
        mention_count += len(re.findall(r"medical kurdistan conference", article_text))

    # Step 5.2: Try to find and click the "Next" anchor tag
    # Step 5.2: Try to find and click the "Next" anchor tag
    try:
        # Wait until the "Next" anchor tag is both visible and clickable
        next_anchor_tag = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[@class='next page-numbers']"))
        )
        next_anchor_tag = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='next page-numbers']"))
        )

        # Scroll the "Next" anchor tag into view
        driver.execute_script("arguments[0].scrollIntoView(true);", next_anchor_tag)

        # Wait for a small amount of time after scrolling
        time.sleep(3)

        print("Found the 'Next' anchor tag, clicking...")
        next_anchor_tag.click()  # Click the "Next" anchor tag to go to the next page

        # Wait for the next page to load (wait for the articles to load)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".title"))  # Wait for articles to load
        )

        print("Going to the next page...")

    except Exception as e:
        print("Error or no more pages:", e)
        break  # Exit the loop if no "Next" anchor tag is found or there's an error (i.e., we're on the last page)


# Step 6: Output the final count of mentions
print(f"The term 'medical conference' was mentioned {mention_count} times across all pages.")

# Step 7: Close the browser
driver.quit()
