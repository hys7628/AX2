import os
import streamlit as st

# 1. 브라우저 탭 설정 (반드시 최상단 배치)
st.set_page_config(
    page_title="글로벌 여행 가이드 포털",
    page_icon="✈️",
    layout="wide"
)

# 2. 이미지 폴더 기본 경로 (src/images)
import os
import streamlit as st

# 1. 윈도우 실제 절대 경로를 최우선으로 고정
FIXED_IMAGE_DIR = r"C:\Users\user\AX2\DAY_07_0911\my_travel_app\src\images"

def display_country_image(filename: str, caption: str):
    # 파일 확장자가 붙어 있든 안 붙어 있든 순수 파일명 추출
    base_name = os.path.splitext(filename)[0]
    
    # 1순위: 탐색기에서 확인된 실제 절대 경로
    # 2순위: 현재 실행 파일 기준 상대 경로
    search_dirs = [
        FIXED_IMAGE_DIR,
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "images"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
    ]
    
    target_path = None
    for folder in search_dirs:
        for ext in [".jpg", ".jpeg", ".png", ".JPG"]:
            candidate = os.path.join(folder, base_name + ext)
            if os.path.exists(candidate):
                target_path = candidate
                break
        if target_path:
            break

    # 이미지 출력 또는 실패 시 실제 탐색한 경로 화면 출력
    if target_path:
        st.image(target_path, caption=caption, use_container_width=True)
    else:
        st.error(f"❌ 파일을 찾지 못했습니다. 확인한 폴더: {FIXED_IMAGE_DIR} / 대상 파일: {base_name}.jpg")

# 3. 사이드바 메뉴 네비게이션
with st.sidebar:
    st.title("🌏 여행 포털")
    st.write("떠나고 싶은 국가를 선택하세요.")
    menu = st.radio(
        "이동할 페이지",
        options=["홈 (대한민국)", "중국", "일본", "미국", "스위스"],
        index=0
    )

# 4. 메뉴 분기 처리
if menu == "홈 (대한민국)":
    st.title("🇰🇷 대한민국 (Republic of Korea)")
    st.caption("전통의 미와 역동적인 현대 문화가 공존하는 여행지")
    
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.subheader("📌 주요 안내")
        st.markdown("""
        - **수도**: 서울 (Seoul)
        - **주요 명소**: 경복궁, 남산서울타워, 제주도 성산일출봉, 해운대
        - **특징**: K-컬처(K-POP, K-Food), 24시간 편리한 대중교통 및 우수한 치안
        - **이용 팁**: 사이드바를 통해 중국, 일본, 미국, 스위스 여행 정보를 탐색할 수 있습니다.
        """)
        st.link_button("🌐 대한민국 관광공사(Visit Korea) 바로가기", "https://korean.visitkorea.or.kr")
    with col2:
        display_country_image("korea.jpg", "아름다운 대한민국 풍경")

elif menu == "중국":
    st.title("🇨🇳 중국 (China)")
    st.caption("수천 년 역사의 숨결과 장대한 자연을 만나는 대륙")
    
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.subheader("📌 여행 정보")
        st.markdown("""
        - **추천 도시**: 베이징, 상하이, 시안, 청두
        - **주요 명소**: 만리장성, 자금성, 상하이 와이탄, 병마용갱
        - **여행 팁**: 넓은 국토로 인해 고속철도망 이용이 편리하며, 모바일 간편결제가 보편화되어 있습니다.
        """)
        st.link_button("🇨🇳 중국 공식 여행 가이드 바로가기", "https://www.travelchinaguide.com/")
    with col2:
        display_country_image("china.jpg", "웅장한 중국의 명소")

elif menu == "일본":
    st.title("🇯🇵 일본 (Japan)")
    st.caption("가까운 거리에서 미식, 쇼핑, 온천 힐링을 즐길 수 있는 여행지")
    
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.subheader("📌 여행 정보")
        st.markdown("""
        - **추천 도시**: 도쿄, 오사카, 교토, 후쿠오카, 삿포로
        - **주요 명소**: 후지산, 센소지, 도톤보리, 유후인 온천
        - **여행 팁**: 각 지역별 패스(JR Pass, 지하철 패스)를 활용하면 교통비를 절약할 수 있습니다.
        """)
        st.link_button("🇯🇵 일본 정부 관광국(JNTO) 바로가기", "https://www.japan.travel/ko/kr/")
    with col2:
        display_country_image("japan.jpg", "일본의 다채로운 풍경")

elif menu == "미국":
    st.title("🇺🇸 미국 (USA)")
    st.caption("광활한 대자연 국립공원과 세계적인 대도시들의 향연")
    
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.subheader("📌 여행 정보")
        st.markdown("""
        - **추천 도시**: 뉴욕, 로스앤젤레스, 샌프란시스코, 라스베이거스
        - **주요 명소**: 그랜드 캐니언, 타임스퀘어, 금문교, 옐로스톤 국립공원
        - **여행 팁**: 입국 전 전자여행허가제(ESTA) 신청이 필수입니다.
        """)
        st.link_button("🇺🇸 미국 관광청 공식 사이트 바로가기", "https://www.gousa.or.kr/")
    with col2:
        display_country_image("usa.jpg", "미국의 화려한 도시와 자연")

elif menu == "스위스":
    st.title("🇨🇭 스위스 (Switzerland)")
    st.caption("알프스의 만년설과 맑은 호수가 펼쳐진 대자연의 파라다이스")
    
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.subheader("📌 여행 정보")
        st.markdown("""
        - **추천 도시**: 인터라켄, 취리히, 루체른, 체르마트
        - **주요 명소**: 융프라우요흐, 마터호른, 리기산, 피르스트
        - **여행 팁**: 스위스 트래블 패스를 이용하면 기차, 유람선, 산악열차 혜택을 폭넓게 누릴 수 있습니다.
        """)
        st.link_button("🇨🇭 스위스 정부 관광청 바로가기", "https://www.myswitzerland.com/ko/")
    with col2:
        display_country_image("switzerland.jpg", "알프스 설경과 호수")