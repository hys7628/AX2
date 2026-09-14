import streamlit as st

# 브라우저 탭 설정 (최상단)
st.set_page_config(page_title="🌍 세계 여행 포털 🌍", layout="wide")

# 1. 개별 페이지 정의 (st.Page 사용)
home_page = st.Page("view/home.py", title="홈", icon="🏠", default=True)
usa = st.Page("view/usa.py", title="미국", icon="🗽")
china = st.Page("view/china.py", title="중국", icon="🐼")
japan = st.Page("view/japan.py", title="일본", icon="🌸")
switzerland = st.Page("view/switzerland.py", title="스위스", icon="🏔️")

# 2. 네비게이션 메뉴 구성 (사이드바 자동 생성)
pg = st.navigation([home_page, usa, china, japan, switzerland])

# 3. 페이지 실행
pg.run()