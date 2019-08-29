import requests
from bs4 import BeautifulSoup

website = requests.get('https://www.wikipedia.org/')

website_content = website.content

soup = BeautifulSoup(website_content, 'html.parser')

soup = soup.encode('utf-8').find_all('a')

print (soup)
