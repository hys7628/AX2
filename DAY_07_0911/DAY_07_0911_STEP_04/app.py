import streamlit as st

st.set_page_config(page_title="🌍 세계 여행 포털 🌍", layout="wide")


home_page = st.pag("view/home.py", title="홈", icons="", default=True)
usa_page = st.pag("view/usa.py", title="미국", icons="", default=True)
china_page = st.pag("view/china.py", title="중국", icons="", default=True)
japan_page = st.pag("view/japan.py", title="일본", icons="", default=True)
switzerland_page = st.pag("view/switzerland.py", title="스위스", icons="", default=True)

pg = st.navigation([home_page, usa_page, china_page, japan_page, switzerland_page])
pg.run()