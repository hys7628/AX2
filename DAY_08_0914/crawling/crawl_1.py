from bs4 import BeautifulSoup
import requests
import pandas as pd

response = requests.get("https://startcoding.pythonanywhere.com/basic")

html = response.text

soup = BeautifulSoup(html, "html.parser") #html을 parser해서 soup에 저장해줘. 

items = soup.select(".product") #product라는 아이 가지고 올거야~

# 몇 번 반복할건데?
for item in items:
    category = item.select_one(".product-category").text # 카테고리에서 가져오기
    category_name = item.select_one(".product-name").text # 상품명에서 가져오기
    category_link = item.select_one(".producet-name > a").attrs["href"] # 상품 상세 페이지 링크, href의 속성 가지고 들어올게
    price = item.select_one(".product-price").text # 가격을 가지고 와~
    print(category, category_name, category_link, price)

				

				