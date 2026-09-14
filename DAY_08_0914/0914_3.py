import os
import streamlit as st
import pandas as pd
import pydeck as pdk
import requests
from dotenv import load_dotenv

# 1. 페이지 레이아웃 설정 (최상단)[cite: 1, 5]
st.set_page_config(
    page_title="여행갈래? 환율볼래? 카페갈래?",
    page_icon="☕",
    layout="wide"
)

# 2. 상위 폴더의 .env 읽기 (abspath 미사용 지침 준수)
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

# REST API 키 불러오기
REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")

# 3. 환경변수 체크 및 에러 핸들링
if not REST_API_KEY:
    st.error(f"❌ .env 파일을 찾지 못했거나 키가 비어 있습니다.\n확인한 경로: {env_path}")
    st.info("AX2/.env 파일 안에 아래 내용이 적혀 있는지 확인하세요:\nKAKAO_REST_API_KEY=발급받은_REST_API_키")
    st.stop()

# 4. 카카오 REST API 좌표 검색 함수
def get_coordinates_from_kakao(address: str, rest_key: str):
    """카카오 로컬 REST API를 호출하여 주소를 위도, 경도로 변환합니다."""
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {rest_key}"}
    params = {"query": address}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=3.0)
        if response.status_code == 200:
            documents = response.json().get("documents", [])
            if documents:
                # y: 위도(lat), x: 경도(lon)
                return float(documents[0]["y"]), float(documents[0]["x"])
    except Exception as e:
        st.warning(f"REST API 호출 실패 ({address}): {e}")
    return None, None

# 5. 대상 카페 목록 (주소 기반)[cite: 2]
cafe_targets = [
    {"name": "더피아노", "address": "서울 종로구 평창6길 71"},
    {"name": "카페 산아래", "address": "서울 강북구 삼양로181길 56"},
    {"name": "1인1잔", "address": "서울 은평구 연서로 534"},
    {"name": "스태픽스", "address": "서울 종로구 사직로9길 22"},
]

# 6. 화면 전환 상태(session_state) 관리[cite: 4, 5]
if "page" not in st.session_state:
    st.session_state.page = "home"

# =====================================================================
# 화면 1: 홈 화면 (가운데 정렬된 큼직한 'Seoul Cafe' 버튼)[cite: 5, 8]
# =====================================================================
if st.session_state.page == "home":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'> ✈️여행갈래? 💵환율볼래? 🧋카페갈래?</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; font-size: 1.15rem;'>👉원하는 정보를 골라주세요👈</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # 3개 컬럼의 가운데 컬럼을 사용해 버튼을 정중앙에 배치[cite: 4, 5]
    col_left, col_center, col_right = st.columns([1, 1.2, 1])
    with col_center:
        if st.button("🧋서울 카페 가볼래?", use_container_width=True, type="primary"):
            st.session_state.page = "map"
            st.rerun()

# =====================================================================
# 화면 2: 서울 카페 지도 화면 (버튼 클릭 시 전환되는 화면)[cite: 1, 5]
# =====================================================================
elif st.session_state.page == "map":
    # 상단 헤더 및 홈 복귀 버튼[cite: 5]
    header_col, btn_col = st.columns([4, 1])
    with header_col:
        st.title("📍 서울 카페 지도")
        st.caption("카카오 REST API로 조회한 위·경도 좌표 기반 지도입니다.")
    with btn_col:
        st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
        if st.button("🏠HOME🏠", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # REST API로 위/경도 좌표 변환
    places_data = []
    with st.spinner("카카오 REST API로 카페 위치 좌표를 조회하는 중..."):
        for cafe in cafe_targets:
            lat, lon = get_coordinates_from_kakao(cafe["address"], REST_API_KEY)
            if lat and lon:
                places_data.append({
                    "name": cafe["name"],
                    "address": cafe["address"],
                    "latitude": lat,
                    "longitude": lon
                })

    df_places = pd.DataFrame(places_data)

    if df_places.empty:
        st.warning("주소 변환 결과가 없습니다. REST API 키 유효성을 확인해 주세요.")
    else:
        # 좌측: PyDeck 지도 / 우측: 카페 상세 정보 카드
        col_map, col_list = st.columns([2.5, 1], gap="large")

        with col_map:
            view_state = pdk.ViewState(
                latitude=df_places["latitude"].mean(),
                longitude=df_places["longitude"].mean(),
                zoom=11,
                pitch=0
            )

            layer = pdk.Layer(
                "ScatterplotLayer",
                data=df_places,
                get_position="[longitude, latitude]",
                get_color="[255, 75, 75, 200]",
                get_radius=300,
                pickable=True
            )

            tooltip = {
                "html": "<b>{name}</b><br>{address}",
                "style": {"color": "white"}
            }

            deck = pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip=tooltip,
                map_style="road"
            )

            st.pydeck_chart(deck, use_container_width=True)

        with col_list:
            st.subheader("📋 카페 리스트")
            for _, row in df_places.iterrows():
                with st.container():
                    st.markdown(f"**☕ {row['name']}**")
                    st.caption(f"📍 {row['address']}")
                    st.caption(f"위도: `{row['latitude']:.4f}` | 경도: `{row['longitude']:.4f}`")
                    st.markdown("---")