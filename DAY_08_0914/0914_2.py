import os
from dotenv import load_dotenv
import pandas as pd
import pydeck as pdk
import requests
import streamlit as st

# 1. 페이지 레이아웃 설정 (최상단)[cite: 2, 3]
st.set_page_config(
    page_title="서울 카페 지도 (REST API)", page_icon="🗺️", layout="wide"
)

# 2. 요청하신 방식 그대로 상위 폴더의 .env 지정 (abspath 미사용)
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

# REST API 키 불러오기
REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")

st.title("🗺️ 서울 카페 위치 지도 (카카오 REST API 연동)")
st.caption(
    "카카오 REST API로 주소의 위·경도 좌표를 조회하고 Streamlit 네이티브 지도로 시각화합니다."
)

# 3. 환경변수 체크 및 에러 안내
if not REST_API_KEY:
  st.error(
      f"❌ .env 파일을 찾지 못했거나 키가 비어 있습니다.\n확인한 경로: {env_path}"
  )
  st.info(
      "AX2/.env 파일 안에 아래 내용이 적혀 있는지 확인하세요:\n"
      "KAKAO_REST_API_KEY=발급받은_REST_API_키"
  )
  st.stop()


# 4. 카카오 REST API 주소 검색 함수[cite: 1]
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

# 위/경도 좌표 변환
places_data = []
with st.spinner("카카오 REST API로 주소 좌표 변환 중..."):
  for cafe in cafe_targets:
    lat, lon = get_coordinates_from_kakao(cafe["address"], REST_API_KEY)
    if lat and lon:
      places_data.append({
          "name": cafe["name"],
          "address": cafe["address"],
          "latitude": lat,
          "longitude": lon,
      })

df_places = pd.DataFrame(places_data)

if df_places.empty:
  st.warning(
      "주소 변환 결과가 없습니다. REST API 키 유효성 또는 인터넷 연결을 확인해 주세요."
  )
  st.stop()

# 6. 화면 분할 (좌측: 지도 / 우측: 카페 목록 카드)
col_map, col_list = st.columns([2.5, 1], gap="large")

with col_map:
  view_state = pdk.ViewState(
      latitude=df_places["latitude"].mean(),
      longitude=df_places["longitude"].mean(),
      zoom=11,
      pitch=0,
  )

  layer = pdk.Layer(
      "ScatterplotLayer",
      data=df_places,
      get_position="[longitude, latitude]",
      get_color="[255, 75, 75, 200]",
      get_radius=300,
      pickable=True,
  )

  tooltip = {"html": "<b>{name}</b><br>{address}", "style": {"color": "white"}}

  deck = pdk.Deck(
      layers=[layer],
      initial_view_state=view_state,
      tooltip=tooltip,
      map_style="road",
  )

  st.pydeck_chart(deck, use_container_width=True)

with col_list:
  st.subheader("📋 변환된 카페 정보")
  for _, row in df_places.iterrows():
    with st.container():
      st.markdown(f"**☕ {row['name']}**")
      st.caption(f"📍 {row['address']}")
      st.caption(
          f"위도: `{row['latitude']:.4f}` | 경도: `{row['longitude']:.4f}`"
      )
      st.markdown("---")