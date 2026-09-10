import pandas as pd
import numpy as np
import os 
import io
import streamlit as st
import matplotlib.pyplot as plt


# raw_trade_data.csv 파일 활용
# HS 코드가 85로 시작하는(반도체류) + 국가명 미국 또는 베트남 + 수출금액이 0보다 큰 수(실제 수출실적이 있는)
# 다중 조건으로 필터링 한 뒤, 수출 금액 상위 10건 화면에 보여주고 report.csv로 저장
# streamlit 사용 streamlit run 0908_2.py

import io
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# 1. 페이지 레이아웃을 넓게 설정 (반드시 최상단에 위치)
st.set_page_config(page_title="무역 원본 데이터 분석", layout="wide")

st.title("🚢 무역 원본 데이터(raw_trade_data) 분석 대시보드")
st.caption("CSV 데이터를 불러와 기초 탐색 및 결측치, 요약 통계를 확인합니다.")

# 2. 파일 경로 설정
# 현재 폴더(DAY_04_0908)에서 상위(..)로 나간 뒤 CSV 폴더 안의 raw_trade_data.csv 지정
current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "..", "CSV", "raw_trade_data.csv")


# 3. 인코딩 안전 감지 함수 (utf-8, cp949, euc-kr 순차 시도)
def load_trade_data(file_path):
    encodings = ["utf-8", "utf-8-sig", "cp949", "euc-kr"]
    for enc in encodings:
        try:
            return pd.read_csv(file_path, encoding=enc)
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue
    return None


# 4. 데이터 로드 및 확인
df = None
if os.path.exists(csv_path):
    df = load_trade_data(csv_path)
    if df is not None:
        st.success(f"✅ 파일을 성공적으로 불러왔습니다: {os.path.abspath(csv_path)}")
    else:
        st.error("❌ 지원하는 인코딩으로 파일을 읽을 수 없습니다.")
else:
    # 절대 경로로 한 번 더 확인
    alt_path = r"C:\Users\user\AX2\CSV\raw_trade_data.csv"
    if os.path.exists(alt_path):
        df = load_trade_data(alt_path)
        st.success(f"✅ 파일을 성공적으로 불러왔습니다: {alt_path}")
    else:
        st.error(f"❌ 파일을 찾을 수 없습니다. 경로를 확인해 주세요:\n- {csv_path}")

st.markdown("---")

# 5. 데이터가 정상적으로 읽혔을 때 분석 화면 표시
if df is not None:
    # 1) 기본 크기 카드 (Metric)
    st.subheader("1) 데이터 크기 요약")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("총 행 개수", f"{df.shape[0]:,}개")
    with col2:
        st.metric("총 열 개수", f"{df.shape[1]}개")
    with col3:
        st.metric("전체 결측치 수", f"{df.isna().sum().sum():,}개")

    # 2) 상위 / 하위 데이터 미리보기
    st.subheader("2) 데이터 미리보기")
    tab1, tab2 = st.tabs(["상위 5행 (head)", "하위 5행 (tail)"])
    with tab1:
        st.dataframe(df.head(5), use_container_width=True)
    with tab2:
        st.dataframe(df.tail(5), use_container_width=True)

    # 3) 컬럼 목록 및 데이터 요약(info)
    st.subheader("3) 컬럼 목록 및 데이터 구조 (Info)")
    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.write("**컬럼 목록**")
        st.write(list(df.columns))

    with col_right:
        st.write("**데이터 구조 요약**")
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())

    # 4) 숫자형 데이터 통계 요약 (describe)
    st.subheader("4) 숫자형 데이터 요약 통계 (Describe)")
    st.dataframe(df.describe(), use_container_width=True)

    # 5) 결측치 현황
    st.subheader("5) 열별 결측치(NaN) 현황")
    missing_df = df.isna().sum().rename("결측치 개수").to_frame()
    missing_df["결측치 비율(%)"] = (missing_df["결측치 개수"] / len(df) * 100).round(
        2
    )
    st.dataframe(missing_df, use_container_width=True)

