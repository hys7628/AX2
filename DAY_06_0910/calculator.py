import streamlit as st
import requests

# ----------------------------------------------------------------------
# 1. 페이지 설정 및 디자인 고정 CSS (디자인 100% 유지)
# ----------------------------------------------------------------------
st.set_page_config(page_title="머니머니 계산기", page_icon="💵", layout="centered")

st.markdown("""
<style>
    /* 1. 바깥 웹 배경: 완전한 흰색 */
    .stApp, html, body {
        background-color: #FFFFFF !important;
    }

    header, footer { visibility: hidden !important; }

    /* 2. 스마트폰 본체 외곽 테두리 */
    .block-container {
        max-width: 420px !important;
        background-color: #000000 !important;
        border: 14px solid #1f1f21 !important;
        border-radius: 54px !important;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.4), 0 0 0 2px #444448 !important;
        padding: 24px 18px 28px 18px !important;
        margin: 25px auto !important;
    }

    /* 3. 상단 다이내믹 아일랜드 */
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

    /* 4. 라벨 흰색 */
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

    /* 5. 동그라미 버튼 형태 및 정렬 유지 */
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

    /* [핵심] 숫자 버튼: 주황색 배경 + 42px 대왕 900 볼드 텍스트 강제 적용 */
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

    /* 기능 버튼 (C, ⌫): 연회색 배경 + 28px 볼드 텍스트 */
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

    /* 하단 홈 바 */
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

# ----------------------------------------------------------------------
# 2. 세션 상태 관리 및 실시간 환율 계산 로직
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

# ------------------------------------------------------
# 3. 스마트폰 상단 헤더 및 디스플레이
# ------------------------------------------------------
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

# 통화 선택 변경 시 자동 갱신
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

# ------------------------------------------------------
# 4. 키패드: 새로고침 없는 Streamlit 네이티브 버튼 (연속 입력 지원)
# ------------------------------------------------------
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