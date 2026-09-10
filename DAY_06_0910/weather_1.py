import os
import requests
import streamlit as st
from dotenv import find_dotenv, load_dotenv

# 상위 폴더의 .env 자동 탐색 및 로드
load_dotenv(find_dotenv())

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

# 페이지 와이드 설정
st.set_page_config(page_title="날씨 & 환율 대시보드", page_icon="🌍", layout="wide")

st.title("🌍 실시간 날씨 & 주요 통화 환율 대시보드")
st.caption("OpenWeatherMap과 ExchangeRate-API를 연동한 실시간 정보 서비스입니다.")

# API 키 유효성 검사
if not WEATHER_API_KEY or not EXCHANGE_API_KEY:
    st.error(".env 파일에 OPENWEATHER_API_KEY 및 EXCHANGE_API_KEY가 올바르게 설정되어 있는지 확인해 주세요.")
    st.stop()

# --------------------------------------------------
# 화면 분할: 좌측(날씨) | 우측(환율)
# --------------------------------------------------
col_weather, col_exchange = st.columns([1, 1], gap="large")

# ==================================================
# 1. 좌측: 날씨 정보 섹션
# ==================================================
with col_weather:
    st.subheader("🌤️ 실시간 날씨 조회")
    city = st.text_input("도시명을 영문으로 입력하세요 (예: Seoul, Tokyo, New York):", "Seoul")

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=kr"

    try:
        w_res = requests.get(weather_url)
        w_data = w_res.json()

        if w_res.status_code == 200:
            temp = w_data["main"]["temp"]
            feels_like = w_data["main"]["feels_like"]
            humidity = w_data["main"]["humidity"]
            desc = w_data["weather"][0]["description"]
            icon_code = w_data["weather"][0]["icon"]

            st.markdown(f"#### 📍 {w_data['name']}, {w_data['sys']['country']}")
            
            w_col1, w_col2 = st.columns([1, 2])
            with w_col1:
                st.image(f"https://openweathermap.org/img/wn/{icon_code}@2x.png", width=90)
            with w_col2:
                st.metric("현재 기온", f"{temp:.1f} °C", delta=f"체감 {feels_like:.1f} °C")

            st.write(f"- **날씨 상태**: {desc}")
            st.write(f"- **현재 습도**: {humidity}%")
            st.write(f"- **바람 세기**: {w_data['wind']['speed']} m/s")

        elif w_res.status_code == 404:
            st.warning("입력하신 도시를 찾을 수 없습니다. 철자를 확인해 주세요.")
        else:
            st.error(f"날씨 API 오류: {w_data.get('message', '알 수 없는 에러')}")

    except Exception as e:
        st.error(f"날씨 데이터를 가져오는 중 에러 발생: {e}")

# ==================================================
# 2. 우측: 환율 정보 섹션 (ExchangeRate-API)
# ==================================================
with col_exchange:
    st.subheader("💱 실시간 주요 환율 (KRW 기준)")
    base_currency = st.selectbox("기준 통화 선택 (Base Currency):", ["USD", "EUR", "JPY", "CNY"], index=0)

    # ExchangeRate-API v6 최신 환율 엔드포인트 호출
    exchange_url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{base_currency}"

    try:
        ex_res = requests.get(exchange_url)
        ex_data = ex_res.json()

        if ex_res.status_code == 200 and ex_data.get("result") == "success":
            rates = ex_data["conversion_rates"]
            last_update = ex_data.get("time_last_update_utc", "")[:16]

            st.markdown(f"#### 💵 1 {base_currency} 당 주요 통화 가치")
            st.caption(f"기준 업데이트: {last_update} (UTC)")

            # 주요 통화 메트릭 카드 3개 표시
            m1, m2, m3 = st.columns(3)
            with m1:
                krw_rate = rates.get("KRW", 0)
                st.metric("대한민국 (KRW)", f"{krw_rate:,.2f} 원")
            with m2:
                usd_or_eur = rates.get("USD") if base_currency != "USD" else rates.get("EUR")
                label_target = "USD" if base_currency != "USD" else "EUR"
                st.metric(f"기타 ({label_target})", f"{usd_or_eur:,.4f}")
            with m3:
                jpy_rate = rates.get("JPY", 0)
                st.metric("일본 (JPY)", f"{jpy_rate:,.2f} 엔")

            st.markdown("---")
            
            # 간이 계산기 (환전 시뮬레이션)
            amount = st.number_input(f"환전할 금액 입력 ({base_currency}):", min_value=1.0, value=100.0, step=10.0)
            converted_krw = amount * krw_rate
            st.success(f"**{amount:,.0f} {base_currency}** = **{converted_krw:,.2f} KRW (원)**")

        else:
            st.error(f"환율 정보를 가져오지 못했습니다: {ex_data.get('error-type', 'API 키 또는 요청 주소 확인')}")

    except Exception as e:
        st.error(f"환율 데이터를 가져오는 중 에러 발생: {e}")