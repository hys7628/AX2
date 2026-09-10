import streamlit as st
import requests

# ----------------------------------------------------------------------
# 1. 페이지 설정 및 완전 반응형(Responsive) 스마트폰 CSS
# ----------------------------------------------------------------------
st.set_page_config(page_title="머니머니 계산기", page_icon="💵", layout="centered")

st.markdown("""
<style>
    /* 1. 바깥 배경: 깨끗한 흰색 유지 */
    .stApp, html, body {
        background-color: #FFFFFF !important;
    }

    header, footer { visibility: hidden !important; }

    /* 2. 반응형 스마트폰 프레임: clamp() 및 vw로 모바일/PC 유동 대응 */
    .block-container {
        width: 94vw !important;
        max-width: 420px !important;
        background-color: #000000 !important;
        border: clamp(8px, 2.8vw, 14px) solid #1f1f21 !important;
        border-radius: clamp(36px, 12vw, 54px) !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.35), 0 0 0 2px #444448 !important;
        padding: clamp(14px, 4vw, 24px) clamp(12px, 3.5vw, 18px) clamp(16px, 4.5vw, 26px) clamp(12px, 3.5vw, 18px) !important;
        margin: clamp(10px, 2.5vh, 25px) auto !important;
        box-sizing: border-box !important;
    }

    /* 3. 반응형 상단 다이내믹 아일랜드 */
    .dynamic-island {
        width: clamp(85px, 25vw, 110px);
        height: clamp(20px, 5.8vw, 26px);
        background-color: #000000;
        border-radius: 20px;
        margin: 0 auto clamp(8px, 2.2vw, 12px) auto;
        border: 2px solid #222224;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 10px;
    }
    .camera-lens {
        width: 8px;
        height: 8px;
        background-color: #0a1128;
        border-radius: 50%;
        border: 1px solid #1b263b;
    }

    /* 4. 라벨 흰색 및 반응형 글자 크기 */
    div[data-testid="stSelectbox"] label,
    div[data-testid="stSelectbox"] label p {
        color: #FFFFFF !important;
        font-size: clamp(12px, 3.2vw, 14px) !important;
        font-weight: 700 !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #1C1C1E !important;
        border-radius: 12px !important;
        border: 1px solid #333333 !important;
        min-height: clamp(36px, 8vw, 42px) !important;
    }
    div[data-baseweb="select"] span {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: clamp(12px, 3vw, 14px) !important;
    }

    /* 5. 동그라미 버튼 반응형 크기 (화면 폭에 맞춰 자동 스케일링) */
    div[data-testid="stButton"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin-bottom: clamp(6px, 1.8vw, 12px) !important;
    }

    div[data-testid="stButton"] > button {
        width: clamp(58px, 18vw, 80px) !important;
        height: clamp(58px, 18vw, 80px) !important;
        min-width: clamp(58px, 18vw, 80px) !important;
        min-height: clamp(58px, 18vw, 80px) !important;
        max-width: clamp(58px, 18vw, 80px) !important;
        max-height: clamp(58px, 18vw, 80px) !important;
        border-radius: 50% !important;
        border: none !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 auto !important;
        padding: 0 !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.35) !important;
        transition: transform 0.08s ease, opacity 0.1s ease !important;
    }

    div[data-testid="stButton"] > button:active {
        transform: scale(0.92) !important;
        opacity: 0.7 !important;
    }

    /* [반응형 숫자 버튼]: 주황색 배경 + 화면 크기별 볼드 텍스트 */
    .btn-num div[data-testid="stButton"] > button {
        background-color: #FF9F0A !important;
    }
    .btn-num div[data-testid="stButton"] > button p,
    .btn-num div[data-testid="stButton"] > button span,
    .btn-num div[data-testid="stButton"] > button div,
    .btn-num div[data-testid="stButton"] > button * {
        color: #FFFFFF !important;
        font-size: clamp(26px, 8.5vw, 40px) !important;
        font-weight: 900 !important;
        line-height: 1 !important;
        margin: 0 !important;
        padding: 0 !important;
        text-align: center !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif !important;
    }

    /* 기능 버튼 (C, ⌫) */
    .btn-fn div[data-testid="stButton"] > button {
        background-color: #A5A5A5 !important;
    }
    .btn-fn div[data-testid="stButton"] > button p,
    .btn-fn div[data-testid="stButton"] > button span,
    .btn-fn div[data-testid="stButton"] > button div,
    .btn-fn div[data-testid="stButton"] > button * {
        color: #000000 !important;
        font-size: clamp(18px, 5.5vw, 26px) !important;
        font-weight: 900 !important;
        line-height: 1 !important;
        margin: 0 !important;
        padding: 0 !important;
        text-align: center !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif !important;
    }

    /* 하단 홈 바 */
    .home-bar {
        width: clamp(90px, 28vw, 130px);
        height: clamp(3.5px, 1vw, 5px);
        background-color: #FFFFFF;
        border-radius: 10px;
        margin: clamp(14px, 4vw, 22px) auto 0 auto;
        opacity: 0.75;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 2. 세션 상태 관리 및 환율 계산 로직
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
# 3. 반응형 상단 헤더 및 디스플레이 액정
# ----------------------------------------------------------------------
st.markdown("""
<div class="dynamic-island">
    <div class="camera-lens"></div>
</div>
<div style="text-align: center; margin-bottom: clamp(6px, 2vw, 12px);">
    <span style="font-size: clamp(13px, 3.8vw, 15px); font-weight: 800; color: #FFFFFF; letter-spacing: 0.5px;">💵 머니머니 계산기 💵</span>
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
<div style="padding: clamp(6px, 2vw, 10px) clamp(8px, 2.5vw, 14px); margin-bottom: clamp(8px, 2.5vw, 14px); text-align: right;">
    <div style="display: flex; justify-content: flex-end; align-items: baseline; gap: 6px;">
        <span style="font-size: clamp(28px, 9vw, 42px); font-weight: 300; color: #FFFFFF; line-height: 1;">{formatted_input}</span>
        <span style="font-size: clamp(11px, 3vw, 14px); color: #8E8E93; font-weight: 700;">{from_code}</span>
    </div>
    <div style="height: 1px; background-color: #272729; margin: clamp(6px, 2vw, 10px) 0;"></div>
    <div style="display: flex; justify-content: flex-end; align-items: baseline; gap: 6px;">
        <span style="font-size: clamp(22px, 7.5vw, 34px); font-weight: 600; color: #FF9F0A; line-height: 1;">{st.session_state.converted_amount}</span>
        <span style="font-size: clamp(11px, 3vw, 14px); color: #8E8E93; font-weight: 700;">{to_code}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 4. 반응형 키패드 (연속 입력 지원 네이티브 버튼)
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