import streamlit as st
import numpy as np
import random
from datetime import datetime

#dfasdfsdf
#d;ferjsffaf

# random 모듈을 이용해서 1~45 사이의 중복 없는 번호 6개를 뽑고
# 자료 구조 : set, 버튼을 누르면 5세트를 한 번에 생성
# datetime로 생성 시간도 함께
# Lotto_generator_v1

st.title("🎱로또 번호 자동 생성시🎱")
st.caption("버튼을 누르면 1~45 사이의 중복 없는 번호 6개짜리 세트를 5개 만들어줍니다.")





def lotto_generator() -> list :
    """1~45에서 중복 없이 번호 6개를 뽑아 정렬된 리스트로 반환"""

    number = set[int]()
    while len(number) < 6:
            number.add(random.randint(1,45))
    return sorted(number)

st.markdown("---")
button = st.button("💰5개 번호 생성하기💰", key="widget_button")
now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.write(f"생성 시간 : {now_str}")

for i in range(1,6):
    lotto_num = lotto_generator()
    st.write(f"{i}세트: {lotto_num}")
#return sorted(number)
# 