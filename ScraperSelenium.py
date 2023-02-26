
from replit import db
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
chrome_options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.image': 2})

driver = webdriver.Chrome(options=chrome_options)

urls = db["urls"]

for url in urls:
  print("Loading url", url)
  response = driver.get(url)
  price_text = driver.find_element(By.CSS_SELECTOR, "span[data-auto='mainPrice']").text

  print(price_text)


