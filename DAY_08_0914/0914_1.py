# folium으로 지도에 마커를 표시하는 예제 코드
# import folium
# 서울 시내 자연(숲/호수/물가 등)과 어우를 수 있는 카페 4곳의 좌표(위도/경도)와 이름을 리스트로 받아 folium 지도를 만들고
# 각 좌표에 이름표가 붙은 마커를 찍은 다음, basic_map.html 파일로 저장하는 예제 코드임
# 저장 basic_map.html을 웹 브라우저로 열어서 확인
# python 0914_1.py

# 지도의 시작 중심 좌표(광화문 기준) 지정해서 folim 지도 객체 생성

# 숫자가 클수록 더 가깝게 보여준다. 

import folium
import streamlit as st
from streamlit_folium import st_folium

# 1. 페이지 브라우저 탭 설정 (최상단 배치)
st.set_page_config(
    page_title="서울 자연 친화 카페 지도",
    page_icon="🌿",
    layout="wide",
)

st.title("🌿 서울 도심 속 자연 친화 카페 추천")
st.caption(
    "광화문을 중심으로 자연과 어우러진 카페 4곳의 위치를 지도에서 확인해 보세요."
)

# 2. 서울 시내 자연과 어우러질 수 있는 카페 4곳 샘플 데이터 (딕셔너리)
cafes = {
    "더피아노": {
        "address": "서울 종로구 평창6길 71",
        "lat": 37.6106,
        "lon": 126.9752,
    },
    "카페 산아래": {
        "address": "서울 강북구 삼양로181길 56",
        "lat": 37.6582,
        "lon": 127.0057,
    },
    "1인1잔": {
        "address": "서울 은평구 연서로 534",
        "lat": 37.6402,
        "lon": 126.9381,
    },
    "스태픽스": {
        "address": "서울 종로구 사직로9길 22",
        "lat": 37.5779,
        "lon": 126.9658,
    },
}

# 3. 지도의 시작 중심 좌표(광화문 기준) 지정 및 Folium 지도 객체 생성
seoul_center = [37.5759, 126.9768]
# zoom_starts 오타 -> zoom_start로 수정
m = folium.Map(location=seoul_center, zoom_start=12)

# 광화문 중심 마커 추가 (기준점 표시)
folium.Marker(
    location=seoul_center,
    popup="<b>광화문 (중심점)</b>",
    tooltip="광화문",
    icon=folium.Icon(color="red", icon="info-sign"),
).add_to(m)

# 4. 반복문(for문)으로 데이터를 하나씩 꺼내 마커 추가
for name, info in cafes.items():
  popup_html = f"<b>{name}</b><br>{info['address']}"

  folium.Marker(
      location=[info["lat"], info["lon"]],
      popup=folium.Popup(popup_html, max_width=250),
      tooltip=name,
      icon=folium.Icon(color="green", icon="leaf"),  # 초록색 자연 테마 아이콘
  ).add_to(m)

# 5. streamlit_folium의 st_folium을 사용하여 지도를 Streamlit 웹 화면에 출력
st_folium(m, width=900, height=600)