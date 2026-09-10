# 설문조사 앱
# 전송 버튼, 체크박스, 라디오 단추, 셀렉트 박스, 멀티 셀렉트 박스, 슬라이더, 텍스트 입력
# 위젯 
import streamlit as st

st.title("📚호날두 선호도 조사")
st.caption("좋아하는 축구 선수를 조사하기 위한 설문 조사입니다.")
st.markdown("---")

# 1) 텍스트 입력 위젯 : key 값을 넣어서 다른 위젯과 이름이 겹치지 않게 한다. 
name = st.text_input("1) 이름을 입력하세요", value="Ronaldo", key="widget_name")
# age = st.text_input("1) 나이를 입력하세요", value="40", key="widget_age")

# 2) 슬라이드 위젯 : 최소/최대/기본값
age = st.slider("2) 나이를 선택하세요", min_value=10, max_value=80, value=25, key="widget_age")

# 3) 라디오 버튼 : 여러 선택지 중에서 하나만 고를 때 사용
job = st.radio(
    "3) 직군을 선택하세요", 
    options=["학생","축구선수","직장인","주부","취업준비생","프리랜서","기타"],
    key="widget_job"
    # index=3 '주부'가 기본 값일 때
)

# 4) 셀렉트 박스(드롭 다운) : 라디오와 비슷하지만 목록이 길 때 공간을 절약할 수 있다. 
country = st.selectbox(
    "4) 호날두의 소속팀은?", 
    options=["Real Madrid", "Al Nasr", "Juventus", "Manchester United"], 
    key="widget_country"
)

# 5) 멀티 셀렉트 박스 : 여러 개를 동시에 선택할 수 있다. 
team = st.multiselect(
    "5) 관심 있는 축구팀을 모두 골라주세요", 
    options=["Barcelona", "Chelsea", "Machester City", "LA FC"], 
    key="widget_team",
    default=["Barcelona"]
)

# 6 체크 박스 : 참/거짓값 하나를 받을 때
check = st.checkbox("6) 본인이 선택한 축구팀에 만족하시나요? 어?",
            key="widget_check")

score = st.slider("7) 본 조사 만족도 점수(1~5점)", 
                         1,5,5, 
                         key="widget_score")

# 9 텍스트 영역 : 여러 줄의 입력 필요할 때 자유 의견 입력
feedback = st.text_area("8) 자유롭게 의견을 남겨주세요", 
                        key="widget_feedback")


# 10 전송 버튼 : 클릭 여부 (True / False)
submit = st.button("제출하기", key="widget_submit_btn")

st.markdown("---")
st.subheader("실시간 응답 요약")

# 위젯 값들을 버튼을 누르지 않아도 조작하는 즉시 바로 갱신된다. 
if submit:
    st.write(f'- 이름 : **{name}** / 나이 : **{age}**')
    st.write(f'- 직군 : **{job}** / 관심 팀 : **{country}**')
    st.write(f'- 관심 축구팀 : **{", ".join(team) if team else "선택없음"}**')
    st.write(f"- 조사 만족 여부 : {'만족' if check else '미체크' } / 만족도 점수 : **{score}점**")
    # ',' -> 일반문자열로 바꿈
    st.write(f'- 자유 의견 : **{feedback if feedback else "작성 안 함"}**')
else:
    st.write("위에 항목을 입력한 뒤 제출하기 버튼을 눌러주세요")




