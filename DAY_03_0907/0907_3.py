# 인코딩 자동 감지 + 한글 폰트 막대그래프
# 여러 인코딩("utf-8-sig", "cp949", "euc-kr") 순서대로 시도
# 내가 쓸 폰트 같은 경로에 있어야 함
# 객실 등급 별 막대 그래프 생성 후 그림으로 저장 chart.png
# 실행 streamlit run 0907_3.py


import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib import font_manager
# CSV_PATH = os.path.join(os.path.dirname(__file__), )"..", "common", "파일명"
# 상위 폴더로 할 때의 작동법 -> streamlit run .\ㅁ\a.py
# CSV_PATH = "..\common\Titanic.csv" #실행하는 폴더 안에 반드시 들어가있어야 함

st.title("📊인코딩 자동 감지 + 한글 폰트 막대 그래프(Titanic 연습)📊")
st.caption("여러 인코딩을 순서대로 시도해서 파일을 읽고, 객실등급별 생존율을 그래프로 그립니다.")

csv_path = "titanic_cleaned.csv"
font_path = "GriunXHangeul_OCHUNGI.KIM-Rg.ttf"


def read_csv_with_auto_encoding(csv_path):
    """
    utf-8-sig -> cp949 -> euc-kr 순서대로 읽기를 시도하는 자동 인코딩 함수
    """
    # 1. 시도해 볼 인코딩 안경 목록을 순서대로 적어둡니다.
    encodings = ["utf-8-sig", "cp949", "euc-kr"]
    
    # 2. 목록에 있는 안경을 하나씩 차례대로 꺼내서 써봅니다.
    for encoding in encodings:
        try:
            # 해당 인코딩 안경을 쓰고 파일을 읽어봅니다!
            df = pd.read_csv(csv_path, encoding=encoding)
            st.write(f"✅ 성공! '{encoding}' 인코딩으로 파일을 잘 읽었습니다.")
            return df  # 성공했으니 읽은 표(DataFrame)를 들고 돌아갑니다.
            
        except UnicodeDecodeError:
            # 글자가 깨져서 읽기 실패하면 투덜대지 않고 다음 안경을 준비합니다.
            continue
            
    # 3. 3가지 안경을 다 써봤는데도 전부 실패했을 때
    raise ValueError("❌ utf-8-sig, cp949, euc-kr 인코딩으로 모두 읽기에 실패했습니다.")

# 인코딩 자동 감지로 csv 읽기
st.subheader("1) 인코딩 자동 감지")
df = read_csv_with_auto_encoding(csv_path)

st.markdown('---')
# 객실등급(Pclass) 별 생존율 집계
# Survived : 사망(0) / 생존(1) 등급별 평균을 내면
# 그대로가 등급의 생존 비율이 된다. 

pclass_survival_rate = df.groupby("Pclass")['Survived'].mean().sort_index()
st.subheader("2) 객실 등급별 생존율")
st.dataframe((pclass_survival_rate * 100).round(1).rename("생존율(%)"))
st.markdown("---")

# 차트 그리기
st.subheader("3) 객실 등급별 생존율 막대그래프")
try:
    font_prop = font_manager.FontProperties(fname=font_path)
    # matplotlib font_manager에 폰트를 등록하고 전역 폰트로 설정
    font_manager.fontManager.addfont(font_path)
    st.write("GriunXHangeul_OCHUNGI.KIM-Rg를 적용했습니다")
   
except FileNotFoundError: # 폰트 파일이 없으면 FileNotFoundError 발생
    st.warning("너희들 지금 뭐하는거니? 폰트 파일을 찾을 수가 없습니다.")

# fig = 차트 영역, ax = 그림 영역
fig, ax = plt.subplots(figsize=(8,5))
(pclass_survival_rate * 100).plot(kind="bar", color="#0000ff", ax=ax)
ax.set_title("객실 등급별 생존율", fontproperties=font_prop, fontsize=15)
ax.set_xlabel("객실 등급", fontproperties=font_prop, fontsize=12)
ax.set_ylabel("생존율", fontproperties=font_prop, fontsize=12)

st.pyplot(fig)

output_png = os.path.join(os.path.dirname(__file__),  "chart.png")
fig.savefig(output_png)