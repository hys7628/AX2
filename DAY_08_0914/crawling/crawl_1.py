from bs4 import BeautifulSoup
import requests
import pandas as pd

response = requests.get("https://startcoding.pythonanywhere.com/basic")

html = response.text

soup = BeautifulSoup(html, "html.parser") #html을 parser해서 soup에 저장해줘. 

logo = soup.select_one("col-md-12").text

print(logo)

				