# 날씨 api 실습
# openweathermap 현재 날씨 api로 특정 도시의 날씨를 가져와 출력한다.
# 사전준비 : openweathermap 회원 가입 후 api 발급
# pip install requests python-dotenv
# .env 파일을 생성하고 이곳에 OPENWEATHER_API_KEY = 발급받은_API_키
# .env.example OPENWEATHER_API_KEY = your_key
# .env.example 받아서 .env로 이름바꾸고 자기 api를 채운다.

import os
from pathlib import Path
import requests
import streamlit as st
from dotenv import load_dotenv


# load_dotenv() # 같은 경로에서 .env 파일을 읽어서 환경 변수로 등록한다. 근데 지금 경로가 다르니까 코드 하나 더 필요함


# 1. 상위 폴더의 .env 파일 로드 (방법 1: 상대 경로 지정)
# load_dotenv(dotenv_path="../.env")

# 1-1. 실행 위치에 영향받지 않는 더 안전한 방법 (현재 파일 기준 상위 디렉터리 탐색)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# 2. 환경 변수에서 API 키 불러오기
API_KEY = os.getenv("OPENWEATHER_API_KEY")

st.title("🌤️ OpenWeather 현재 날씨 조회")

# API 키 유효성 체크
if not API_KEY:
    st.error(".env 파일에서 OPENWEATHER_API_KEY를 찾을 수 없습니다. 경로와 키 값을 확인하세요.")
    st.stop()

# 3. 사용자 도시 입력
city = st.text_input("도시 이름을 영문으로 입력하세요 (예: Seoul, Tokyo, London):", "Seoul")

if st.button("날씨 확인"):
    # OpenWeatherMap Current Weather Data 엔드포인트
    # units=metric: 섭씨온도로 설정
    # lang=kr: 날씨 설명을 한국어로 번역 제공
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=kr"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather_desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            icon_code = data["weather"][0]["icon"]

            st.subheader(f"📍 {data['name']}의 현재 날씨")
            
            # OpenWeatherMap 기본 날씨 아이콘 렌더링
            icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
            st.image(icon_url, width=100)

            col1, col2, col3 = st.columns(3)
            col1.metric("기온", f"{temp}°C")
            col2.metric("체감 온도", f"{feels_like}°C")
            col3.metric("습도", f"{humidity}%")

            st.write(f"**상태 요약:** {weather_desc}")

        elif response.status_code == 401:
            st.error("API 키 인증 실패: 발급받은 지 얼마 되지 않았다면 활성화까지 10~30분 정도 걸릴 수 있습니다.")
        elif response.status_code == 404:
            st.warning("도시를 찾을 수 없습니다. 도시 철자를 확인해 주세요.")
        else:
            st.error(f"오류가 발생했습니다: {data.get('message', '알 수 없는 에러')}")

    except Exception as e:
        st.error(f"요청 중 오류가 발생했습니다: {e}")
