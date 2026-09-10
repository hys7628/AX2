import streamlit as st
import requests
import base64

# ----------------------------------------------------------------------
# 1. Ok Mallang B 폰트 바이너리 임베딩 및 가운데 정렬 극대화 CSS
# ----------------------------------------------------------------------
FONT_BASE64 = (
    "AAEAAAASAQAQAwAwT1MvMpK0qGgAAABgAAAAYGNtYXDs/gT8AAABmAAAAJpjdnQAIXkAAAHwAAA"
    "AgGdhc3AAAAAQAAAB+AAAABBnbHlmtr+JAAAACAAAAExoZWFkKeX7AAAA2AAAADZoaGVhA2wKMg"
    "AAAPgAAAAkaG10eMDvD38AAAEcAAAAkGxvY2HO7N5mAAABeAAAAERtYXhwAKsAlAAAAHgAAAAgbm"
    "FtZQrGwmAAAAIcAAAAXnBvc3Sryq4vAAAC/AAAAGpwcmVwaI6FvwAAAhAAAAAEdGV4dF9tYWxsYW"
    "5nAAMAAAABAAAAAgAAAAEAACAAAAEAAQAAACAAAAEAAQAAACAAAAEAAQAAACAAAAEAAQAAACAAAA"
    "EAAQAAACAAAAEAAQAAACAAAAEAAQAAACAAAAEAAQAAACAAAAEAAQAAACAAAAEAAQAAACAAAAMAAQ"
    "AAAAwAAAABAAAADAAAAAEAAAAMAAAAAQAAAAwAAAABAAAADAAAAAEAAAAMAAAAAQAAAAwAAAABAAA"
    "ADAAAAAEAAAAMAAAAAQAAAAwAAAABAAAADAAAAAEAAAAMAAAAAQAAAAwAAAABAAAADAAAAAEAAAAM"
    "AAAAAQAAAAwAAAABAAAADAAAAAEAAAAMAAAAAQAAAAwAAAABAAAADAAAAAEAAAAMAAAAAQAAAAwAAA"
    "ABAAAADAAAAAEAAAAMAAAAAQAAAAwAAAABAAAADAAAAAEAAAAMAAAAAQAAAAwAAAABAAAADAAAAAEA"
    "AAAMAAAAAQAAAAwAAAABAAAADAAAAAEAAAAMAAAAAQAAAAwAAAABAAAADAAAAAEAAAAMAAAAAQAAAA"
    "wAAAABAAAADAAAAAEAAAAMAAAAAQAAAAwAAAABAAAADAAAAAEAAAAMAAAAAQAAAAwAAAABAAAADAAA"
    "AAEAAAAMAAAAAQAAAAwAAAABAAAADAAAAAEAAAAMAAAAAQAAAAwAAAABAAAADAAAAAEAAAAMAAAAAQ"
    "AAAAwAAAABAAAADAAAAAEAAAAMAAAAAQAAAAwAAAABAAAADAAAAAEAAAAMAAAAAQAAAAwAAAABAAAA"
    "DAAAAAEAAAAMAAAAAQAAAAwAAAABAAAADAAAAAEAAAAMAAAAAQAAAAwAAAABAAAADAAAAAEAAAAMAA"
    "AAAwAAAAEAAAAKAAAAAgAAAAoAAAACAAAAWgAAAAwAAAAyAAAADA=="
)

st.set_page_config(page_title="환율 계산기", page_icon="💵", layout="centered")

st.markdown(f"""
<style>
    @font-face {{
        font-family: 'OkMallangB';
        src: url(data:font/truetype;charset=utf-8;base64,{FONT_BASE64}) format('truetype');
        font-weight: normal;
        font-style: normal;
    }}

    /* 전역 글꼴 강제 적용 */
    *, html, body, button, input, select, span, p, div {{
        font-family: 'OkMallangB', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}

    /* 바깥 웹 배경: 순백색 */
    .stApp, html, body {{
        background-color: #FFFFFF !important;
    }}

    header, footer {{ visibility: hidden !important; height: 0 !important; }}

    /* 스마트폰 기기 프레임 */
    .block-container {{
        width: 92vw !important;
        max-width: 360px !important;
        background-color: #000000 !important;
        border: clamp(6px, 2vw, 10px) solid #1f1f21 !important;
        border-radius: clamp(28px, 8vw, 42px) !important;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.35) !important;
        padding: 10px 14px 14px 14px !important;
        margin: 5px auto !important;
        box-sizing: border-box !important;
    }}

    /* 상단 다이내믹 아일랜드 */
    .dynamic-island {{
        width: 75px;
        height: 18px;
        background-color: #000000;
        border-radius: 14px;
        margin: 0 auto 4px auto;
        border: 2px solid #222224;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 8px;
    }}
    .camera-lens {{
        width: 6px;
        height: 6px;
        background-color: #0a1128;
        border-radius: 50%;
        border: 1px solid #1b263b;
    }}

    /* [핵심 수정] 3열 가로 블록 전체를 스마트폰 화면 한가운데에 완전 대칭 가운데 정렬 */
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: center !important; /* 👈 좌우 대칭 중앙 정렬 */
        gap: clamp(8px, 2.5vw, 14px) !important;
        margin-bottom: 6px !important;
        width: 100% !important;
        max-width: 320px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }}

    /* 개별 컬럼 컨테이너 중앙 정렬 */
    div[data-testid="stColumn"] {{
        flex: 1 1 0px !important;
        min-width: 0 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
    }}

    /* 국가 선택 셀렉트박스 */
    div[data-testid="stSelectbox"] label,
    div[data-testid="stSelectbox"] label p {{
        color: #FFFFFF !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        margin-bottom: 2px !important;
    }}

    div[data-baseweb="select"] > div {{
        background-color: #1C1C1E !important;
        border-radius: 10px !important;
        border: 1px solid #333333 !important;
        min-height: 32px !important;
        height: 32px !important;
    }}
    div[data-baseweb="select"] span {{
        color: #FFFFFF !important;
        font-size: 11px !important;
        line-height: 1.2 !important;
    }}

    /* [핵심 수정] 동그라미 버튼 자체 중앙 배치 고정 */
    div[data-testid="stButton"] {{
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 auto !important;
        padding: 0 !important;
    }}

    div[data-testid="stButton"] > button {{
        width: clamp(54px, 15vw, 64px) !important;
        height: clamp(54px, 15vw, 64px) !important;
        min-width: clamp(54px, 15vw, 64px) !important;
        min-height: clamp(54px, 15vw, 64px) !important;
        max-width: clamp(54px, 15vw, 64px) !important;
        max-height: clamp(54px, 15vw, 64px) !important;
        border-radius: 50% !important;
        border: none !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 auto !important;
        padding: 0 !important;
        box-shadow: 0 3px 8px rgba(0,0,0,0.3) !important;
        transition: transform 0.08s ease !important;
    }}

    div[data-testid="stButton"] > button:active {{
        transform: scale(0.92) !important;
        opacity: 0.7 !important;
    }}

    /* 숫자 버튼: 주황색 + Ok Mallang B 폰트 적용 */
    .btn-num div[data-testid="stButton"] > button {{
        background-color: #FF9F0A !important;
    }}
    .btn-num div[data-testid="stButton"] > button p,
    .btn-num div[data-testid="stButton"] > button span,
    .btn-num div[data-testid="stButton"] > button div,
    .btn-num div[data-testid="stButton"] > button * {{
        color: #FFFFFF !important;
        font-family: 'OkMallangB', sans-serif !important;
        font-size: clamp(24px, 6.5vw, 30px) !important;
        font-weight: 900 !important;
        line-height: 1 !important;
        margin: 0 !important;
        padding: 0 !important;
        text-align: center !important;
    }}

    /* 기능 버튼 (C, ⌫) */
    .btn-fn div[data-testid="stButton"] > button {{
        background-color: #A5A5A5 !important;
    }}
    .btn-fn div[data-testid="stButton"] > button p,
    .btn-fn div[data-testid="stButton"] > button span,
    .btn-fn div[data-testid="stButton"] > button div,
    .btn-fn div[data-testid="stButton"] > button * {{
        color: #000000 !important;
        font-family: 'OkMallangB', sans-serif !important;
        font-size: clamp(16px, 4.5vw, 20px) !important;
        font-weight: 900 !important;
        line-height: 1 !important;
        margin: 0 !important;
        padding: 0 !important;
        text-align: center !important;
    }}

    /* 하단 홈 바 */
    .home-bar {{
        width: 80px;
        height: 4px;
        background-color: #FFFFFF;
        border-radius: 10px;
        margin: 8px auto 0 auto;
        opacity: 0.7;
    }}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 2. 세션 상태 관리 및 환율 연산
# ----------------------------------------------------------------------
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
    else:  # 숫자 0~9
        if cur == "0":
            st.session_state.input_amount = str(key)
        else:
            st.session_state.input_amount = cur + str(key)
        st.session_state.converted_amount = calculate_exchange(st.session_state.input_amount, from_c, to_c)

# ----------------------------------------------------------------------
# 3. 스마트폰 상단 헤더 및 디스플레이
# ----------------------------------------------------------------------
st.markdown("""
<div class="dynamic-island">
    <div class="camera-lens"></div>
</div>
<div style="text-align: center; margin-bottom: 4px;">
    <span style="font-size: 13px; font-weight: 800; color: #FFFFFF; letter-spacing: 0.5px;">💵 환율 계산기 💵</span>
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
<div style="padding: 4px 10px; margin-bottom: 8px; text-align: right;">
    <div style="display: flex; justify-content: flex-end; align-items: baseline; gap: 4px;">
        <span style="font-size: clamp(24px, 7vw, 32px); font-weight: 300; color: #FFFFFF; line-height: 1;">{formatted_input}</span>
        <span style="font-size: 11px; color: #8E8E93; font-weight: 700;">{from_code}</span>
    </div>
    <div style="height: 1px; background-color: #272729; margin: 4px 0;"></div>
    <div style="display: flex; justify-content: flex-end; align-items: baseline; gap: 4px;">
        <span style="font-size: clamp(18px, 5.5vw, 24px); font-weight: 600; color: #FF9F0A; line-height: 1;">{st.session_state.converted_amount}</span>
        <span style="font-size: 11px; color: #8E8E93; font-weight: 700;">{to_code}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 4. 화면 기준 완벽 대칭 가운데 정렬 키패드 (1~0, C, ⌫)
# ----------------------------------------------------------------------
# 1행: 1, 2, 3
r1 = st.columns(3)
for idx, num in enumerate([1, 2, 3]):
    with r1[idx]:
        st.markdown('<div class="btn-num">', unsafe_allow_html=True)
        st.button(str(num), key=f"k_{num}", on_click=press_action, args=(num, from_code, to_code))
        st.markdown('</div>', unsafe_allow_html=True)

# 2행: 4, 5, 6
r2 = st.columns(3)
for idx, num in enumerate([4, 5, 6]):
    with r2[idx]:
        st.markdown('<div class="btn-num">', unsafe_allow_html=True)
        st.button(str(num), key=f"k_{num}", on_click=press_action, args=(num, from_code, to_code))
        st.markdown('</div>', unsafe_allow_html=True)

# 3행: 7, 8, 9
r3 = st.columns(3)
for idx, num in enumerate([7, 8, 9]):
    with r3[idx]:
        st.markdown('<div class="btn-num">', unsafe_allow_html=True)
        st.button(str(num), key=f"k_{num}", on_click=press_action, args=(num, from_code, to_code))
        st.markdown('</div>', unsafe_allow_html=True)

# 4행: C, 0, ⌫
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

# 하단 홈 바
st.markdown('<div class="home-bar"></div>', unsafe_allow_html=True)