import os
import streamlit as st
import pandas as pd
import pydeck as pdk
import requests
from dotenv import load_dotenv

# ======================================================================
# 1. 페이지 공통 기본 설정 (최상단)
# ======================================================================
st.set_page_config(
    page_title="여행갈래? 환율볼래? 카페갈래?",
    page_icon="✨",
    layout="wide"
)

# 화면 상태 관리 (home / exchange / cafe)
if "page" not in st.session_state:
    st.session_state.page = "home"

# ----------------------------------------------------------------------
# [공통 데이터 & 세션 상태]
# ----------------------------------------------------------------------
# 1) 카페 관련: 상위 폴더의 .env 읽기
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)
REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")

cafe_targets = [
    {"name": "더피아노", "address": "서울 종로구 평창6길 71"},
    {"name": "카페 산아래", "address": "서울 강북구 삼양로181길 56"},
    {"name": "1인1잔", "address": "서울 은평구 연서로 534"},
    {"name": "스태픽스", "address": "서울 종로구 사직로9길 22"},
]

def get_coordinates_from_kakao(address: str, rest_key: str):
    """카카오 로컬 REST API를 호출하여 주소를 위도, 경도로 변환합니다."""
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {rest_key}"}
    params = {"query": address}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=3.0)
        if response.status_code == 200:
            documents = response.json().get("documents", [])
            if documents:
                return float(documents[0]["y"]), float(documents[0]["x"])
    except Exception as e:
        st.warning(f"REST API 호출 실패 ({address}): {e}")
    return None, None

# 2) 환율 계산기 관련 설정
if "input_amount" not in st.session_state:
    st.session_state.input_amount = "0"
if "converted_amount" not in st.session_state:
    st.session_state.converted_amount = "0"

CURRENCIES = {
    "미국 (USD)": "USD",
    "대한민국 (KRW)": "KRW",
    "유럽연합 (EUR)": "EUR",
    "일본 (JPY)": "JPY",
    "중국 (CNY)": "CNY",
    "영국 (GBP)": "GBP"
}

FALLBACK_RATES = {
    "USD": {"USD": 1.0, "KRW": 1390.0, "EUR": 0.92, "JPY": 155.0, "CNY": 7.23, "GBP": 0.78},
    "KRW": {"KRW": 1.0, "USD": 0.00072, "EUR": 0.00066, "JPY": 0.11, "CNY": 0.0052, "GBP": 0.00056},
    "EUR": {"EUR": 1.0, "USD": 1.08, "KRW": 1510.0, "JPY": 168.0, "CNY": 7.85, "GBP": 0.85},
    "JPY": {"JPY": 1.0, "KRW": 8.96, "USD": 0.0064, "EUR": 0.0059, "CNY": 0.046, "GBP": 0.005},
    "CNY": {"CNY": 1.0, "KRW": 192.0, "USD": 0.138, "EUR": 0.127, "JPY": 21.4, "GBP": 0.108},
    "GBP": {"GBP": 1.0, "KRW": 1780.0, "USD": 1.28, "EUR": 1.17, "JPY": 198.0, "CNY": 9.25}
}

def calculate_exchange(amt_str, from_c, to_c):
    try:
        val = float(amt_str)
        if val == 0:
            return "0"
        if from_c == to_c:
            calc = val
        else:
            try:
                url = f"https://api.frankfurter.dev/v1/latest?base={from_c}&symbols={to_c}"
                res = requests.get(url, timeout=1.0)
                calc = val * res.json()["rates"][to_c]
            except Exception:
                calc = val * FALLBACK_RATES.get(from_c, {}).get(to_c, 1.0)
        
        if to_c in ["KRW", "JPY"]:
            return f"{calc:,.0f}"
        else:
            return f"{calc:,.2f}"
    except ValueError:
        return "0"

def press_action(key, from_c, to_c):
    cur = str(st.session_state.input_amount)
    if key == "C":
        st.session_state.input_amount = "0"
        st.session_state.converted_amount = "0"
    elif key == "back":
        st.session_state.input_amount = cur[:-1] if len(cur) > 1 else "0"
        st.session_state.converted_amount = calculate_exchange(st.session_state.input_amount, from_c, to_c)
    else:
        if cur == "0":
            st.session_state.input_amount = str(key)
        else:
            st.session_state.input_amount = cur + str(key)
        st.session_state.converted_amount = calculate_exchange(st.session_state.input_amount, from_c, to_c)


# ======================================================================
# 화면 1: 홈 화면 (두 개의 전환 버튼 배치)
# ======================================================================
if st.session_state.page == "home":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>✈️ 여행갈래? 💵 환율볼래? ☕ 카페갈래?</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; font-size: 1.2rem;'>👉 원하시는 서비스를 선택해 주세요 👈</p>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)

    # 4분할 컬럼을 활용해 중앙에 두 버튼 나란히 배치
    col_pad1, col_btn1, col_btn2, col_pad2 = st.columns([1, 1.2, 1.2, 1])

    with col_btn1:
        if st.button("💵 환율 볼래?", use_container_width=True, type="primary"):
            st.session_state.page = "exchange"
            st.rerun()

    with col_btn2:
        if st.button("☕ 서울 카페", use_container_width=True, type="primary"):
            st.session_state.page = "cafe"
            st.rerun()


# ======================================================================
# 화면 2: 환율 계산기 화면 (스마트폰 디자인 유지)
# ======================================================================
elif st.session_state.page == "exchange":
    # 상단 홈 복귀 버튼
    top_col1, top_col2 = st.columns([5, 1])
    with top_col2:
        if st.button("🏠 HOME", key="back_from_exchange", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    # 계산기 전용 스타일 CSS 주입
    st.markdown("""
    <style>
        .block-container {
            max-width: 420px !important;
            background-color: #000000 !important;
            border: 14px solid #1f1f21 !important;
            border-radius: 54px !important;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.4), 0 0 0 2px #444448 !important;
            padding: 24px 18px 28px 18px !important;
            margin: 10px auto 30px auto !important;
        }
        .dynamic-island {
            width: 110px;
            height: 26px;
            background-color: #000000;
            border-radius: 20px;
            margin: 0 auto 12px auto;
            border: 2px solid #222224;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 12px;
        }
        .camera-lens {
            width: 9px;
            height: 9px;
            background-color: #0a1128;
            border-radius: 50%;
            border: 1px solid #1b263b;
        }
        div[data-testid="stSelectbox"] label,
        div[data-testid="stSelectbox"] label p {
            color: #FFFFFF !important;
            font-size: 14px !important;
            font-weight: 700 !important;
        }
        div[data-baseweb="select"] > div {
            background-color: #1C1C1E !important;
            border-radius: 14px !important;
            border: 1px solid #333333 !important;
        }
        div[data-baseweb="select"] span {
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }
        div[data-testid="stButton"] {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            margin-bottom: 12px !important;
        }
        div[data-testid="stButton"] > button {
            width: 82px !important;
            height: 82px !important;
            min-width: 82px !important;
            min-height: 82px !important;
            max-width: 82px !important;
            max-height: 82px !important;
            border-radius: 50% !important;
            border: none !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            margin: 0 auto !important;
            padding: 0 !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.4) !important;
            transition: transform 0.08s ease, opacity 0.1s ease !important;
        }
        div[data-testid="stButton"] > button:active {
            transform: scale(0.92) !important;
            opacity: 0.7 !important;
        }
        .btn-num div[data-testid="stButton"] > button {
            background-color: #FF9F0A !important;
        }
        .btn-num div[data-testid="stButton"] > button p,
        .btn-num div[data-testid="stButton"] > button span,
        .btn-num div[data-testid="stButton"] > button div,
        .btn-num div[data-testid="stButton"] > button * {
            color: #FFFFFF !important;
            font-size: 42px !important;
            font-weight: 900 !important;
            line-height: 1 !important;
            margin: 0 !important;
            padding: 0 !important;
            text-align: center !important;
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif !important;
        }
        .btn-fn div[data-testid="stButton"] > button {
            background-color: #A5A5A5 !important;
        }
        .btn-fn div[data-testid="stButton"] > button p,
        .btn-fn div[data-testid="stButton"] > button span,
        .btn-fn div[data-testid="stButton"] > button div,
        .btn-fn div[data-testid="stButton"] > button * {
            color: #000000 !important;
            font-size: 28px !important;
            font-weight: 900 !important;
            line-height: 1 !important;
            margin: 0 !important;
            padding: 0 !important;
            text-align: center !important;
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif !important;
        }
        .home-bar {
            width: 130px;
            height: 5px;
            background-color: #FFFFFF;
            border-radius: 10px;
            margin: 20px auto 0 auto;
            opacity: 0.75;
        }
    </style>
    """, unsafe_allow_html=True)

    # 디스플레이 영역
    st.markdown("""
    <div class="dynamic-island">
        <div class="camera-lens"></div>
    </div>
    <div style="text-align: center; margin-bottom: 12px;">
        <span style="font-size: 15px; font-weight: 800; color: #FFFFFF; letter-spacing: 0.5px;">💵 환율 계산기 💵</span>
    </div>
    """, unsafe_allow_html=True)

    c_box1, c_box2 = st.columns(2)
    with c_box1:
        from_name = st.selectbox("보내는 국가", list(CURRENCIES.keys()), index=0)
    with c_box2:
        to_name = st.selectbox("받는 국가", list(CURRENCIES.keys()), index=1)

    from_code = CURRENCIES[from_name]
    to_code = CURRENCIES[to_name]

    if st.session_state.input_amount != "0" and st.session_state.converted_amount == "0":
        st.session_state.converted_amount = calculate_exchange(st.session_state.input_amount, from_code, to_code)

    try:
        formatted_input = f"{int(st.session_state.input_amount):,}"
    except ValueError:
        formatted_input = st.session_state.input_amount

    st.markdown(f"""
    <div style="padding: 10px 14px; margin-bottom: 14px; text-align: right;">
        <div style="display: flex; justify-content: flex-end; align-items: baseline; gap: 6px;">
            <span style="font-size: 42px; font-weight: 300; color: #FFFFFF; line-height: 1;">{formatted_input}</span>
            <span style="font-size: 14px; color: #8E8E93; font-weight: 700;">{from_code}</span>
        </div>
        <div style="height: 1px; background-color: #272729; margin: 12px 0;"></div>
        <div style="display: flex; justify-content: flex-end; align-items: baseline; gap: 6px;">
            <span style="font-size: 34px; font-weight: 600; color: #FF9F0A; line-height: 1;">{st.session_state.converted_amount}</span>
            <span style="font-size: 14px; color: #8E8E93; font-weight: 700;">{to_code}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4x3 키패드
    r1 = st.columns(3)
    for idx, num in enumerate([1, 2, 3]):
        with r1[idx]:
            st.markdown('<div class="btn-num">', unsafe_allow_html=True)
            st.button(str(num), key=f"k_{num}", on_click=press_action, args=(num, from_code, to_code))
            st.markdown('</div>', unsafe_allow_html=True)

    r2 = st.columns(3)
    for idx, num in enumerate([4, 5, 6]):
        with r2[idx]:
            st.markdown('<div class="btn-num">', unsafe_allow_html=True)
            st.button(str(num), key=f"k_{num}", on_click=press_action, args=(num, from_code, to_code))
            st.markdown('</div>', unsafe_allow_html=True)

    r3 = st.columns(3)
    for idx, num in enumerate([7, 8, 9]):
        with r3[idx]:
            st.markdown('<div class="btn-num">', unsafe_allow_html=True)
            st.button(str(num), key=f"k_{num}", on_click=press_action, args=(num, from_code, to_code))
            st.markdown('</div>', unsafe_allow_html=True)

    r4 = st.columns(3)
    with r4[0]:
        st.markdown('<div class="btn-fn">', unsafe_allow_html=True)
        st.button("C", key="k_c", on_click=press_action, args=("C", from_code, to_code))
        st.markdown('</div>', unsafe_allow_html=True)
    with r4[1]:
        st.markdown('<div class="btn-num">', unsafe_allow_html=True)
        st.button("0", key="k_0", on_click=press_action, args=(0, from_code, to_code))
        st.markdown('</div>', unsafe_allow_html=True)
    with r4[2]:
        st.markdown('<div class="btn-fn">', unsafe_allow_html=True)
        st.button("⌫", key="k_back", on_click=press_action, args=("back", from_code, to_code))
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="home-bar"></div>', unsafe_allow_html=True)


# ======================================================================
# 화면 3: 서울 카페 지도 화면
# ======================================================================
elif st.session_state.page == "cafe":
    # API 키 체크
    if not REST_API_KEY:
        st.error(f"❌ .env 파일을 찾지 못했거나 키가 비어 있습니다.\n확인한 경로: {env_path}")
        st.info("AX2/.env 파일 안에 아래 내용이 적혀 있는지 확인하세요:\nKAKAO_REST_API_KEY=발급받은_REST_API_키")
        if st.button("🏠 HOME으로 돌아가기"):
            st.session_state.page = "home"
            st.rerun()
        st.stop()

    header_col, btn_col = st.columns([4, 1])
    with header_col:
        st.title("📍 서울 카페 지도")
        st.caption("카카오 REST API로 조회한 위·경도 좌표 기반 지도입니다.")
    with btn_col:
        st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
        if st.button("🏠 HOME", key="back_from_cafe", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    places_data = []
    with st.spinner("카카오 REST API로 카페 위치 좌표를 조회하는 중..."):
        for cafe in cafe_targets:
            lat, lon = get_coordinates_from_kakao(cafe["address"], REST_API_KEY)
            if lat and lon:
                places_data.append({
                    "name": cafe["name"],
                    "address": cafe["address"],
                    "latitude": lat,
                    "longitude": lon
                })

    df_places = pd.DataFrame(places_data)

    if df_places.empty:
        st.warning("주소 변환 결과가 없습니다. REST API 키 유효성을 확인해 주세요.")
    else:
        col_map, col_list = st.columns([2.5, 1], gap="large")

        with col_map:
            view_state = pdk.ViewState(
                latitude=df_places["latitude"].mean(),
                longitude=df_places["longitude"].mean(),
                zoom=11,
                pitch=0
            )

            layer = pdk.Layer(
                "ScatterplotLayer",
                data=df_places,
                get_position="[longitude, latitude]",
                get_color="[255, 75, 75, 200]",
                get_radius=300,
                pickable=True
            )

            tooltip = {
                "html": "<b>{name}</b><br>{address}",
                "style": {"color": "white"}
            }

            deck = pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip=tooltip,
                map_style="road"
            )

            st.pydeck_chart(deck, use_container_width=True)

        with col_list:
            st.subheader("📋 카페 리스트")
            for _, row in df_places.iterrows():
                with st.container():
                    st.markdown(f"**☕ {row['name']}**")
                    st.caption(f"📍 {row['address']}")
                    st.caption(f"위도: `{row['latitude']:.4f}` | 경도: `{row['longitude']:.4f}`")
                    st.markdown("---")