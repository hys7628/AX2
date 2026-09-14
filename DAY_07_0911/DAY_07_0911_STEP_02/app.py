import streamlit as st

# 1. 페이지 브라우저 탭 설정 (최상단 배치)
st.set_page_config(
    page_title="세계 여행",
    page_icon="✈️",
    layout="wide"
)

# 2. 사이드바 라디오 메뉴
menu = st.sidebar.radio(
    "메뉴",
    options=["홈", "미국", "중국", "일본", "스위스"]
)

# 3. 메뉴 선택에 따른 화면 분기
if menu == "홈":
    st.title("🇰🇷 대한민국 (Korea)")
    st.write("세계 여행 안내 앱의 홈 화면입니다.")
    st.markdown("""
    - **수도**: 서울
    - **특징**: 유구한 역사와 현대적인 K-컬처, 뛰어난 치안과 대중교통을 자랑하는 나라입니다.
    - **안내**: 왼쪽 사이드바에서 여행하고 싶은 다른 국가(미국, 중국, 일본, 스위스)를 선택해 보세요!
    """)

elif menu == "미국":
    st.title("🇺🇸 미국 (USA)")
    st.write("광활한 대륙에 걸친 화려한 대도시와 웅장한 국립공원을 만날 수 있는 나라입니다.")
    st.markdown("- **추천 여행지**: 뉴욕, 그랜드 캐니언, 샌프란시스코, 라스베이거스")
    # 공식 방문 사이트 링크 버튼 (새 탭 열림)
    st.link_button("🇺🇸 미국 공식 관광청 방문하기", "https://www.gousa.or.kr")

elif menu == "중국":
    st.title("🇨🇳 중국 (China)")
    st.write("수천 년의 역사를 품은 웅장한 문화유산과 현대적 메가시티가 공존하는 여행지입니다.")
    st.markdown("- **추천 여행지**: 베이징(자금성, 만리장성), 상하이, 청두, 시안")
    st.link_button("🇨🇳 중국 여행 공식 가이드 방문하기", "https://www.travelchinaguide.com")

elif menu == "일본":
    st.title("🇯🇵 일본 (Japan)")
    st.write("가까운 거리에서 미식, 쇼핑, 온천 및 다양한 전통문화를 즐길 수 있는 인기 여행지입니다.")
    st.markdown("- **추천 여행지**: 도쿄, 오사카, 교토, 삿포로, 후쿠오카")
    st.link_button("🇯🇵 일본 정부 관광국(JNTO) 공식 방문하기", "https://www.japan.travel/ko/kr/")

elif menu == "스위스":
    st.title("🇨🇭 스위스 (Switzerland)")
    st.write("알프스의 만년설과 맑은 호수가 어우러진 동화 같은 자연경관을 선사하는 곳입니다.")
    st.markdown("- **추천 여행지**: 인터라켄, 융프라우요흐, 루체른, 체르마트(마터호른)")
    st.link_button("🇨🇭 스위스 정부 관광청 공식 방문하기", "https://www.myswitzerland.com/ko/")