import streamlit as st
import requests

# ----------------------------------------------------------------------
# 1. 페이지 설정 및 완벽한 원형 키패드 복원 CSS
# ----------------------------------------------------------------------
st.set_page_config(page_title="환율 계산기", page_icon="✦", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Montserrat:wght@300;400;600&display=swap');

    /* 바깥 배경: 샴페인 베이지 */
    .stApp, html, body {
        background-color: #ECE5DE !important;
        font-family: 'Montserrat', sans-serif !important;
    }

    header, footer { visibility: hidden !important; height: 0 !important; }

    /* 스마트폰 기기 프레임 (한 화면 쏙 맞춤) */
    .block-container {
        width: 94vw !important;
        max-width: 380px !important;
        background: #09090b !important;
        border: clamp(6px, 2vw, 9px) solid #c9a598 !important; /* 로즈골드 메탈 베젤 */
        border-radius: clamp(32px, 9vw, 46px) !important;
        box-shadow: 
            0 0 0 2px #5a453f,
            0 20px 50px rgba(0, 0, 0, 0.45) !important;
        padding: 10px 14px 16px 14px !important;
        margin: 4px auto !important;
        box-sizing: border-box !important;
    }

    /* 상단 다이내믹 아일랜드 */
    .dynamic-island {
        width: 72px;
        height: 18px;
        background-color: #000000;
        border-radius: 12px;
        margin: 0 auto 4px auto;
        border: 1.5px solid #1c1c1e;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 8px;
    }
    .camera-lens {
        width: 6px;
        height: 6px;
        background-color: #0d1322;
        border-radius: 50%;
        border: 1px solid #1e293b;
    }

    /* 제목 '환율 계산기' 중앙 정렬 */
    .header-area {
        width: 100% !important;
        text-align: center !important;
        margin: 2px 0 6px 0 !important;
    }
    .top-star {
        color: #d8b2a7;
        font-size: 11px;
        margin-bottom: 1px;
    }
    .main-title {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: clamp(21px, 6vw, 25px) !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #FFF1EE 0%, #E8BCB0 50%, #C99E90 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 2px;
        margin: 0 !important;
        text-align: center !important;
        display: block !important;
        width: 100% !important;
    }
    .sub-title {
        font-size: 8px;
        letter-spacing: 3px;
        color: #aa8d84;
        margin-top: 1px;
        text-transform: uppercase;
        text-align: center;
    }

    /* 국가 선택 셀렉트박스 */
    div[data-testid="stSelectbox"] label {
        color: #d9bfb7 !important;
        font-size: 10px !important;
        font-weight: 600 !important;
        margin-bottom: 1px !important;
    }
    div[data-baseweb="select"] > div {
        background: linear-gradient(180deg, #181517 0%, #100e10 100%) !important;
        border-radius: 16px !important;
        border: 1px solid #735952 !important;
        min-height: 32px !important;
        height: 32px !important;
    }
    div[data-baseweb="select"] span {
        color: #f5eae7 !important;
        font-size: 11px !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="select"] svg {
        fill: #c99e90 !important;
    }

    /* 디스플레이 화면 */
    .display-box {
        text-align: right;
        padding: 2px 8px 6px 8px;
        margin-bottom: 4px;
    }
    .amount-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(26px, 7.5vw, 34px);
        font-weight: 600;
        color: #ffffff;
        line-height: 1;
    }
    .currency-tag {
        font-size: 11px;
        font-weight: 600;
        color: #b09187;
        margin-left: 4px;
    }
    .divider-star {
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        height: 1px;
        background: linear-gradient(90deg, transparent, #84675e, transparent);
        margin: 6px 0;
    }
    .divider-star::after {
        content: "✦";
        position: absolute;
        color: #e5b9ad;
        font-size: 9px;
        background: #09090b;
        padding: 0 4px;
    }

    /* 3열 수평 블록 정렬 */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: space-around !important;
        gap: 6px !important;
        margin-bottom: 8px !important;
        width: 100% !important;
    }
    div[data-testid="stColumn"] {
        flex: 1 1 0px !important;
        min-width: 0 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }

    /* [핵심] 완벽한 원형 버튼 고정 (aspect-ratio + border-radius 50%) */
    div[data-testid="stButton"] {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 auto !important;
        padding: 0 !important;
    }
    div[data-testid="stButton"] > button {
        width: clamp(54px, 15vw, 68px) !important;
        height: clamp(54px, 15vw, 68px) !important;
        min-width: clamp(54px, 15vw, 68px) !important;
        min-height: clamp(54px, 15vw, 68px) !important;
        max-width: clamp(54px, 15vw, 68px) !important;
        max-height: clamp(54px, 15vw, 68px) !important;
        aspect-ratio: 1 / 1 !important; /* 👈 절대 찌그러지지 않는 1:1 정원형 */
        border-radius: 50% !important;   /* 👈 완벽한 동그라미 */
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 auto !important;
        padding: 0 !important;
        transition: transform 0.08s ease, opacity 0.1s ease !important;
    }
    div[data-testid="stButton"] > button:active {
        transform: scale(0.92) !important;
        opacity: 0.75 !important;
    }

    /* 숫자 원형 버튼: 블랙 펄 3D 구체 */
    .btn-num div[data-testid="stButton"] > button {
        background: radial-gradient(circle at 35% 30%, #2f2a29 0%, #151314 65%, #0d0c0d 100%) !important;
        border: 1px solid rgba(220, 180, 170, 0.45) !important;
        box-shadow: 
            inset 0 2px 4px rgba(255, 240, 235, 0.25),
            inset 0 -2px 6px rgba(0, 0, 0, 0.9),
            0 4px 12px rgba(0, 0, 0, 0.6) !important;
    }
    .btn-num div[data-testid="stButton"] > button p,
    .btn-num div[data-testid="stButton"] > button span,
    .btn-num div[data-testid="stButton"] > button div,
    .btn-num div[data-testid="stButton"] > button * {
        color: #F8ECE8 !important;
        font-family: 'Cormorant Garamond', serif !important;
        font-size: clamp(26px, 7vw, 32px) !important;
        font-weight: 600 !important;
        line-height: 1 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* 기능 원형 버튼 (C, ⌫): 메탈릭 로즈골드 3D 구체 */
    .btn-fn div[data-testid="stButton"] > button {
        background: radial-gradient(circle at 35% 30%, #F5D7CE 0%, #D4A99D 55%, #A87A6E 100%) !important;
        border: 1px solid #FFE4DC !important;
        box-shadow: 
            inset 0 2px 5px rgba(255, 255, 255, 0.7),
            inset 0 -3px 6px rgba(110, 60, 50, 0.4),
            0 4px 14px rgba(190, 130, 120, 0.3) !important;
    }
    .btn-fn div[data-testid="stButton"] > button p,
    .btn-fn div[data-testid="stButton"] > button span,
    .btn-fn div[data-testid="stButton"] > button div,
    .btn-fn div[data-testid="stButton"] > button * {
        color: #261613 !important;
        font-family: 'Cormorant Garamond', serif !important;
        font-size: clamp(20px, 5.5vw, 25px) !important;
        font-weight: 700 !important;
        line-height: 1 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* 하단 홈 바 */
    .home-bar {
        width: 80px;
        height: 3.5px;
        background: linear-gradient(90deg, #99786f, #d8b2a7, #99786f);
        border-radius: 10px;
        margin: 10px auto 0 auto;
        opacity: 0.8;
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
    "🇺🇸 미국 (USD)": "USD",
    "🇰🇷 대한민국 (KRW)": "KRW",
    "🇪🇺 유럽연합 (EUR)": "EUR",
    "🇯🇵 일본 (JPY)": "JPY",
    "🇨🇳 중국 (CNY)": "CNY",
    "🇬🇧 영국 (GBP)": "GBP"
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
# 3. 상단 헤더 (중앙 정렬)
# ----------------------------------------------------------------------
st.markdown("""
<div class="dynamic-island">
    <div class="camera-lens"></div>
</div>
<div class="header-area">
    <div class="top-star">✦</div>
    <div class="main-title">✦ 환율 계산기 ✦</div>
    <div class="sub-title">CURRENCY CONVERTER</div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 4. 국가 선택
# ----------------------------------------------------------------------
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

# ----------------------------------------------------------------------
# 5. 디스플레이 화면
# ----------------------------------------------------------------------
st.markdown(f"""
<div class="display-box">
    <div style="display: flex; justify-content: flex-end; align-items: baseline;">
        <span class="amount-text">{formatted_input}</span>
        <span class="currency-tag">{from_code}</span>
    </div>
    <div class="divider-star"></div>
    <div style="display: flex; justify-content: flex-end; align-items: baseline;">
        <span class="amount-text" style="color: #f7d5cc;">{st.session_state.converted_amount}</span>
        <span class="currency-tag" style="color: #d1ada3;">{to_code}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 6. 완벽한 원형 3D 키패드 배치 (1~9, C, 0, ⌫)
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

# 4행: C (로즈골드 원형), 0 (블랙펄 원형), ⌫ (로즈골드 원형)
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