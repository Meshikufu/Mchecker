from bs4 import BeautifulSoup
import time, requests, random, csv, os

url = "https://www.g2g.com/"
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

# Prettify the HTML content
prettified_html = soup.prettify()

print(prettified_html)