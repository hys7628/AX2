import streamlit as st
import requests
import os
import base64

# ----------------------------------------------------------------------
# 1. 기종 무관 폰트 완벽 로드: 로컬 파일 직접 Base64 인코딩
# ----------------------------------------------------------------------
# 지정해주신 폰트 절대 경로 및 상대 경로 자동 탐색
FONT_PATHS = [
    r"C:\Users\user\AX2\DAY_06_0910\OK_Mallang_Font\ttf\Ok Mallang B.ttf",
    os.path.join(os.path.dirname(__file__), "Ok Mallang B.ttf") if "__file__" in locals() else "Ok Mallang B.ttf",
    "Ok Mallang B.ttf"
]

font_base64 = ""
for path in FONT_PATHS:
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                font_base64 = base64.b64encode(f.read()).decode("utf-8")
            break
        except Exception:
            continue

# 모바일 기종(iOS/Android)에 상관없이 폰트를 강제 적용하는 CSS 구성
font_face_css = ""
if font_base64:
    font_face_css = f"""
    @font-face {{
        font-family: 'OkMallangB';
        src: url("data:font/ttf;charset=utf-8;base64,{font_base64}") format("truetype");
        font-weight: normal;
        font-style: normal;
        font-display: block; /* 모바일 브라우저 폰트 대체 방지 */
    }}
    """

st.set_page_config(page_title="머니머니 계산기", page_icon="💵", layout="centered")

st.markdown(f"""
<style>
    {font_face_css}

    /* 전역 글꼴 강제 적용 (아이폰/안드로이드 모든 태그 적용) */
    html, body, [class*="css"], .stApp, button, input, select, textarea, span, p, div {{
        font-family: 'OkMallangB', -apple-system, BlinkMacSystemFont, sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }}

    /* 1. 바깥 웹 배경: 순백색 */
    .stApp, html, body {{
        background-color: #FFFFFF !important;
    }}

    header, footer {{ visibility: hidden !important; height: 0 !important; }}

    /* 2. 한 화면 맞춤 스마트폰 외곽 테두리 (모바일 화면에 맞춰 유동 크기) */
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

    /* 3. 상단 다이내믹 아일랜드 노치 */
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

    /* 4. 모바일에서도 1열로 떨어지지 않고 반드시 3열 유지 */
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 6px !important;
        margin-bottom: 5px !important;
    }}

    div[data-testid="stColumn"] {{
        flex: 1 1 0px !important;
        min-width: 0 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }}

    /* 5. 국가 선택 셀렉트박스 */
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

    /* 6. 동그라미 버튼 규격 */
    div[data-testid="stButton"] {{
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    div[data-testid="stButton"] > button {{
        width: clamp(52px, 14vw, 62px) !important;
        height: clamp(52px, 14vw, 62px) !important;
        min-width: clamp(52px, 14vw, 62px) !important;
        min-height: clamp(52px, 14vw, 62px) !important;
        max-width: clamp(52px, 14vw, 62px) !important;
        max-height: clamp(52px, 14vw, 62px) !important;
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

    /* 숫자 버튼: 주황색 배경 + Ok Mallang B 폰트 강제 상속 */
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

    /* 기능 버튼 (C, ⌫): 회색 버튼 */
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
# 3. 상단 다이내믹 아일랜드 및 컴팩트 디스플레이
# ----------------------------------------------------------------------
st.markdown("""
<div class="dynamic-island">
    <div class="camera-lens"></div>
</div>
<div style="text-align: center; margin-bottom: 4px;">
    <span style="font-size: 13px; font-weight: 800; color: #FFFFFF; letter-spacing: 0.5px;">💵 머니머니 계산기 💵</span>
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
<div style="padding: 4px 10px; margin-bottom: 6px; text-align: right;">
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
# 4. 3열 키패드 (기종 무관 Ok Mallang B 적용)
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