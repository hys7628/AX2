import streamlit as st
import pandas as pd
import os 


csv_path = os.path.join(os.path.dirname(__file__), "..","CSV","raw_trade_data.csv" ) # 경로가 다를 때(다른 폴더에 있을 때)
# csv_path = os.path.join(os.path.dirname(__file__), "raw_trade_data.csv" ) # 경로가 같을 때(같은 폴더 안에 있을 때)

# 환율 샘플 데이터
# 딕셔너리로 표 만들기
exchange_data = {
    "통화":["USD", "EUR", "JPY(100엔)", "CNY"], 
    "환율(KRW)":[1390.5000,1503.2000,930.8000,191.3000],
    "전일대비":[5.2000,3.1000,1.0000,0.4000]
 }



df_exchange = pd.DataFrame(exchange_data)
df_trade = pd.read_csv(csv_path, encoding='utf-8')

st.title("💱오늘의 환율 대시보드💱")
st.caption("아래 데이터는 실제 환율이 아닌 실습용 샘플 데이터입니다.")
st.header("1)환율 표 보기")
st.write("▶ st.dataframe (상호작용 가능한 표)")

st.dataframe(df_exchange, use_container_width=True)

st.write("▶ st.datatable (정적인 표)")
st.table(df_exchange)

st.markdown("---")

st.subheader("2) 주요 환율 카드 (st.metric)")
col1, col2, col3 = st.columns(3) # 3개의 컬럼 사용할거야

# st.metric(라벨, 현재값, 증감값)
with col1 :
    st.metric(label='USD/KRW', value=1450.5, delta="+5.2")

with col2 :
    st.metric(label='EUR/KRW', value=1503.2, delta="-3.1")

with col3 :
    st.metric(label='JPY(100엔)/KRW', value=930.8, delta="+1.0")

st.header("3)보너스: 무역 원본 데이터 미리보기")
st.text("공용 데이터 파일 raw_trade_data.csv를 읽어온 상위 5행입니다.")

st.dataframe(df_trade.head(5), use_container_width=True)


