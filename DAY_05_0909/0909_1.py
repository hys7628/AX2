# raw_trade_data.csv 파일 활용
# HS 코드가 85로 시작하는(반도체류) + 국가명 미국 또는 베트남 + 수출금액이 0보다 큰 수(실제 수출실적이 있는)
# 다중 조건으로 필터링 한 뒤, 수출 금액 상위 10건 화면에 보여주고 report.csv로 저장
# streamlit 사용 streamlit run 0909_1.py


import os
import streamlit as st
import pandas as pd

# 1. 페이지 레이아웃 설정
st.set_page_config(page_title="수출 실적 분석 리포트", layout="wide")
st.title("📊 반도체류(HS 85) 대미·대베트남 수출 실적 TOP 10")
st.caption("HS코드(85*), 국가(미국/베트남), 수출금액(>0) 조건 필터링 및 report.csv 저장")

# 2. 파일 경로 설정
data_dir = r"C:\Users\user\AX2\CSV"
input_file = os.path.join(data_dir, "raw_trade_data.csv")
output_file = os.path.join(data_dir, "report.csv")

# 파일이 없을 경우 상위 폴더 경로 보조 확인
if not os.path.exists(input_file):
    alt_file = os.path.join(os.path.dirname(__file__), "..", "CSV", "raw_trade_data.csv")
    if os.path.exists(alt_file):
        input_file = alt_file

# 3. 데이터 불러오기
if not os.path.exists(input_file):
    st.error(f"❌ 파일을 찾을 수 없습니다: `{input_file}`")
else:
    # 인코딩 순차 시도
    encodings = ["utf-8-sig", "utf-8", "cp949", "euc-kr"]
    df = None
    for enc in encodings:
        try:
            df = pd.read_csv(input_file, encoding=enc)
            break
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue

    if df is None:
        st.error("❌ 파일 인코딩을 읽지 못했습니다.")
    else:
        # 컬럼 양끝 공백 제거
        df.columns = df.columns.str.strip()

        # 4. 컬럼 매핑 확인 ('hs_code' 고정 반영)
        # 국가명 및 수출금액 컬럼 자동 감지 (한글/영문 대응)
        def get_col(candidates, default):
            for cand in candidates:
                for col in df.columns:
                    if cand.lower() == col.lower() or cand.lower() in col.lower():
                        return col
            return default

        hs_col = "hs_code" if "hs_code" in df.columns else get_col(["hs", "품목"], df.columns[0])
        country_col = get_col(["국가명", "국가", "country"], "국가명")
        amount_col = get_col(["수출금액", "수출액", "export_amount", "amount"], "수출금액")

        st.write("### 📌 원본 데이터 미리보기 (상위 5건)")
        st.dataframe(df.head(5), use_container_width=True)

        # 5. 다중 조건 필터링
        # 조건 1: HS 코드가 85로 시작 (문자열 변환 후 접두어 확인)
        cond_hs = df[hs_col].astype(str).str.strip().str.startswith("85")

        # 조건 2: 국가명이 미국 또는 베트남 (한글 및 영문 대응)
        target_countries = ["미국", "베트남", "USA", "VIETNAM", "Vietnam", "U.S.A"]
        cond_country = df[country_col].astype(str).str.strip().isin(target_countries)

        # 조건 3: 수출금액이 0보다 큰 수 (쉼표 제거 후 숫자 변환)
        clean_amount = (
            df[amount_col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df["_amount_calc"] = pd.to_numeric(clean_amount, errors="coerce").fillna(0)
        cond_amount = df["_amount_calc"] > 0

        # 다중 조건 결합 후 정렬
        filtered_df = df[cond_hs & cond_country & cond_amount].copy()
        top10_df = filtered_df.sort_values(by="_amount_calc", ascending=False).head(10)

        # 계산용 임시 컬럼 삭제
        top10_df = top10_df.drop(columns=["_amount_calc"])

        # 6. 결과 출력 및 report.csv 저장
        st.markdown("---")
        st.subheader("🎯 필터링 결과: 수출금액 상위 10건")

        if len(top10_df) == 0:
            st.warning("⚠️ 일치하는 조건의 데이터가 없습니다.")
        else:
            st.dataframe(top10_df, use_container_width=True)

            # CSV 파일 저장 (한글 깨짐 방지 utf-8-sig)
            top10_df.to_csv(output_file, index=False, encoding="utf-8-sig")
            st.success(f"✅ `report.csv` 저장이 완료되었습니다: `{output_file}`")

            # 웹 화면 다운로드 버튼
            csv_data = top10_df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
            st.download_button(
                label="📥 report.csv 직접 다운로드",
                data=csv_data,
                file_name="report.csv",
                mime="text/csv"
            )
