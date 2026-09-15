from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl
import time

data = []

# 웹 브라우저처럼 보이도록 요청 헤더 추가
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for i in range(1, 5):
    url = f"https://startcoding.pythonanywhere.com/basic?page={i}"
    response = requests.get(url, headers=headers)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    items = soup.select(".product")
    
    print(f"[{i}페이지] 가져온 상품 개수: {len(items)}개")

    for item in items:
        category = item.select_one(".product-category").text.strip()
        category_name = item.select_one(".product-name").text.strip()
        category_link = item.select_one(".product-name > a").attrs["href"]
        price = item.select_one(".product-price").text.split("원")[0].replace(",","")
        
        data.append([category, category_name, category_link, price])

    # 서버 차단 방지를 위한 짧은 대기 시간
    time.sleep(1)

# 누적된 데이터 엑셀 저장
df = pd.DataFrame(data, columns=["카테고리", "상품명", "상세 페이지 링크", "가격"])
df.to_excel("data.xlsx", index=False)

print(f"총 {len(df)}건 저장 완료 (data.xlsx)")