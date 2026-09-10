import streamlit as st
import random
from datetime import datetime

st.title("🎱 로또 번호 자동 생성기 🎱")
st.caption("버튼을 누르면 1~45 사이의 중복 없는 번호 5개짜리 세트를 5개 만들어줍니다.")

def lotto_generator() -> list[int]:
    """1~45에서 중복 없이 번호 5개를 뽑아 정렬된 리스트로 반환"""
    numbers = set()
    while len(numbers) < 5:
        numbers.add(random.randint(1, 45))
    return sorted(numbers)

def get_circle(num: int) -> str:
    """번호 범위에 맞는 색깔 동그라미 이모지 반환"""
    # 1-10: 빨간색, 11-20: 노란색, 21-30: 파란색, 31-40: 초록색, 41-45: 흰색
    if 1 <= num <= 10:
        return "🔴"
    elif 11 <= num <= 20:
        return "🟡"
    elif 21 <= num <= 30:
        return "🔵"
    elif 31 <= num <= 40:
        return "🟢"
    else:
        return "⚪"

st.markdown("---")
button = st.button("💰 5개 번호 세트 생성하기 💰", key="widget_button", use_container_width=True)

if button:
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"🕒 생성 시간 : {now_str}")
    st.write("")

    for i in range(1, 6):
        lotto_nums = lotto_generator()
        # 각 번호 앞에 해당 색깔 동그라미를 붙여 결합 (예: 🔴 3  🟡 15  🔵 27 ...)
        result_text = "  ".join(f"{get_circle(num)} {num}" for num in lotto_nums)
        st.write(f"**{i}세트:** {result_text}")