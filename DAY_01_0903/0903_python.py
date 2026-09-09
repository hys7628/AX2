import streamlit as st

# st.title("내용")은 페이지에서 가장 크고 굵은 제목을 만든다.(h1 태그 느낌)

st.title("무역데이터 부트캠프에서 호날두 친구의 자기소개")

# st.header("내용")은 title보다 한 단계 작은 큰 제목(2 느낌)
st.header("안녕하세요❤️ Streamlit으로 만든 Cristiano Ronaldo입니다.")

# st.subheader("내용") header보다 한 단계 작은 큰 제목(h3 느낌)
st.subheader("🙊오늘 배운 것🙊 : 텍스트를 화면에 예쁘게 보여주는 방법")

# st.text("내용") 꾸밈이 전혀 없는, 순수 텍스트를 그대로 출력
st.text("st.text로 출력한 문장입니다. 줄을 바꾸거나 ")

# st.caption("내용") 아주 작은 글씨로 보조 설명을 넣을 때
st.caption("이 문장은 st.caption이다")

# st.markdown("") 마크다운 문법 : 굵게, 기울임, 링크, 목록
# st.markdown("---") 마크다운 문법

st.markdown(
    """
    ### 마크다운으로 작성한 자기소개
    - **이름** : 홍길동
    - **관심분야** : *데이터 분석*, 무역데이터 시각화
    - **목표** : 나만의 대시보드 만들기
    - 참고 링크 : [네이버]("https://www.naver.com")
"""
)

st.markdown("---")

st.subheader("오늘 배운 한 줄 코드")
st.code(
    """
    st.title("안녕하세요. streamlit을 배우고 있는 Lionel Messie입니다.")
"""
)
