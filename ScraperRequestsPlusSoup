import requests
from replit import db
from bs4 import BeautifulSoup

urls = db["urls"]

for url in urls:
  print("Loading url", url)
  response = requests.get(url)
  # print(response.text)
  soup = BeautifulSoup(response.text, 'html.parser')
  # print(soup.title)
  prices = soup.select('KnVez')
  for price in prices:
    print (price.text)

#blog_titles = soup.select('h2.blog-card__content-title')
#for title in blog_titles:
 #   print(title.text)

