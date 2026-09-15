import pandas as pd
import yfinance as yf

# 1. 삼성전자 티커 심볼 지정 (한국 코스피는 .KS)
ticker = "005930.KS"

# 2. 2026년 8월 1일부터 8월 31일까지의 기간 설정
# (end 날짜는 미포함(exclusive)이므로 2026-09-01로 지정)
start_date = "2026-08-01"
end_date = "2026-09-01"

print(f"[{ticker}] 2026년 8월 주가 데이터 다운로드 중...")

# 3. 주가 데이터 수집
df = yf.download(ticker, start=start_date, end=end_date, progress=False)

# 4. 종가(Close) 데이터 추출 및 정리
if not df.empty:
    # yfinance 버전에 따라 컬럼이 MultiIndex일 수 있으므로 단일 레벨로 정리
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # 날짜 인덱스를 일반 컬럼으로 변환하고 날짜 포맷 정리 (YYYY-MM-DD)
    df = df.reset_index()
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")

    # 일일 종가 및 주요 주가 정보 선택 (필요 시 Close만 선택 가능)
    result_df = df[["Date", "Close", "Open", "High", "Low", "Volume"]].copy()
    result_df.columns = ["날짜", "종가(Close)", "시가(Open)", "고가(High)", "저가(Low)", "거래량(Volume)"]

    # 5. 엑셀 파일로 저장
    output_filename = "samsung_stock_202608.xlsx"
    result_df.to_excel(output_filename, index=False, engine="openpyxl")
    print(f"✅ 저장이 완료되었습니다: {output_filename}")
    print(result_df.head())
else:
    print("⚠️ 해당 기간에 수집된 주가 데이터가 없습니다. (날짜 범위 확인 필요)")