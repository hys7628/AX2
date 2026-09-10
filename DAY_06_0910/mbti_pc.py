"""
프로젝트: 무역 직무 적합도 MBTI 대시보드 (Trade Job Fit Test)
수정사항: 
1. 인트로 화면 텍스트 전체 완벽한 가운데 정렬 (text-align: center)
2. 코식이 / 무식이 볼드체 및 모바일 3줄 줄바꿈 유지
3. 적합 매칭도 -> 6대 직무 차트 -> 실무 가이드 순 세로 정렬
4. 다운로드 & 처음으로 돌아가기 버튼 중앙 정렬 및 1:1 동일 크기
5. 💾 진단 리포트 저장 및 안내 헤더 왼쪽 정렬
실행 명령어: streamlit run app.py
"""
import platform
import io
import os
import base64
import streamlit as st
import pandas as pd
import numpy as np

# --------------------------------------------------
# 1. Streamlit 페이지 설정 및 커스텀 CSS
# --------------------------------------------------
st.set_page_config(
    page_title="무역 직무 MBTI 진단소",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
/* 뷰포트 맞춤 컨테이너 */
.main .block-container {
    max-width: 820px !important;
    padding-left: clamp(1rem, 3.5vw, 2.5rem) !important;
    padding-right: clamp(1rem, 3.5vw, 2.5rem) !important;
    padding-top: clamp(1.2rem, 3vw, 2.2rem) !important;
    font-family: -apple-system, BlinkMacSystemFont, "Malgun Gothic", "맑은 고딕", "Apple SD Gothic Neo", sans-serif !important;
}

/* 유동적 헤딩 글자 크기 */
.main-title {
    font-size: clamp(1.35rem, 4.2vw, 2.1rem) !important;
    font-weight: 800 !important;
    text-align: center;
    line-height: 1.35;
    margin-bottom: 0.8rem;
    word-break: keep-all;
}

/* 카드 UI */
.responsive-card {
    padding: clamp(15px, 3.2vw, 24px) !important;
    border-radius: 14px !important;
    margin-bottom: 18px !important;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06) !important;
    background: rgba(255, 255, 255, 0.03);
    word-break: keep-all;
}

/* 중앙 집중형 질문 상자 */
.quiz-question-container {
    text-align: center;
    margin-top: 5px;
    margin-bottom: 25px;
    padding: 10px;
}
.quiz-badge {
    display: inline-block;
    background-color: #EBF5FB;
    color: #2980B9;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 0.88rem;
    font-weight: 700;
    margin-bottom: 12px;
}
.quiz-question-title {
    font-size: clamp(1.25rem, 3.8vw, 1.65rem);
    font-weight: 800;
    color: #1A252F;
    line-height: 1.45;
    word-break: keep-all;
    max-width: 680px;
    margin: 0 auto;
}

/* 선택지 버튼 상자 스타일링 */
div[data-testid="stButton"] > button {
    width: 100%;
    min-height: 52px;
    background-color: #FFFFFF !important;
    color: #2C3E50 !important;
    border: 1.8px solid #E2E8F0 !important;
    border-radius: 12px !important;
    font-size: clamp(0.95rem, 2.6vw, 1.05rem) !important;
    font-weight: 600 !important;
    padding: 10px 16px !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.03) !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    margin-bottom: 10px !important;
}

div[data-testid="stButton"] > button:hover {
    border-color: #38BDF8 !important;
    color: #0284C7 !important;
    background-color: #F0F9FF !important;
    box-shadow: 0 4px 12px rgba(56, 189, 248, 0.15) !important;
    transform: translateY(-1.5px);
}

/* 이전 버튼 스타일 */
.nav-btn div[data-testid="stButton"] > button {
    background-color: #F8FAFC !important;
    border: 1px solid #CBD5E1 !important;
    color: #64748B !important;
    min-height: 42px !important;
}

/* 한글 깨짐 방지 네이티브 바 차트 스타일 */
.native-chart-container {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 18px 20px;
    margin: 12px 0 16px 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.03);
}
.chart-row {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
}
.chart-row:last-child {
    margin-bottom: 0;
}
.chart-label {
    width: 140px;
    min-width: 140px;
    font-size: clamp(0.85rem, 2.6vw, 0.95rem);
    font-weight: 700;
    color: #334155;
    text-align: right;
    padding-right: 14px;
    white-space: nowrap;
}
.chart-bar-bg {
    flex-grow: 1;
    background-color: #F1F5F9;
    border-radius: 8px;
    height: 22px;
    overflow: hidden;
}
.chart-bar-fill {
    height: 100%;
    border-radius: 8px;
    transition: width 0.8s ease-out;
}
.chart-value {
    width: 60px;
    min-width: 60px;
    padding-left: 12px;
    font-size: clamp(0.85rem, 2.6vw, 0.95rem);
    font-weight: 800;
    color: #1E293B;
}

/* 다운로드 및 다시하기 버튼 동일 높이 맞춤 */
div[data-testid="stDownloadButton"] > button {
    width: 100%;
    min-height: 52px !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 2. 직무 정의 및 상세 정보
# --------------------------------------------------
TRADE_JOBS = {
    "해외영업": {
        "english": "Overseas Sales & Business Development",
        "icon": "🌍",
        "summary": "글로벌 시장을 무대로 신규 바이어를 발굴하고 수주를 이끌어내는 무역의 프론트 플레이어",
        "core_skills": ["바이어 발굴 및 협상력", "비즈니스 외국어 회화", "시장 개척 의지 및 회복탄력성", "전시회 참가 및 세일즈 피칭"],
        "recommended_certs": ["국제무역사 1급", "무역영어 1급", "비즈니스 어학(TOEIC Speaking, OPIc)"],
        "color": "#FF4B4B"
    },
    "무역사무/수출입관리": {
        "english": "Trade Operations & Compliance Support",
        "icon": "📑",
        "summary": "계약 체결부터 대금 회수까지 서류의 무결성을 유지하며 수출입 전 과정을 조율하는 프로세스 마스터",
        "core_skills": ["L/C(신용장) 서류 심사 능력", "인코텀즈(Incoterms 2020) 이해", "수출입 선적서류(C/I, P/L) 작성의 꼼꼼함", "수금 일정 관리"],
        "recommended_certs": ["국제무역사", "무역영어 1/2급", "전산회계운용사"],
        "color": "#3498DB"
    },
    "포워딩/국제물류": {
        "english": "Freight Forwarding & Supply Chain Logistics",
        "icon": "🚢",
        "summary": "화물이 공장에서 바이어 창고에 도착할 때까지 최적의 운송 경로와 운임을 설계하는 물류 코디네이터",
        "core_skills": ["선사/항공사 부킹 및 스케줄링", "B/L(선하증권) 실무", "물류 클레임 및 긴급 상황 대처력", "복합운송 운임 견적 비교"],
        "recommended_certs": ["물류관리사", "유통관리사 2급", "국제물류사"],
        "color": "#2ECC71"
    },
    "글로벌 소싱/구매": {
        "english": "Global Procurement & Sourcing",
        "icon": "🔍",
        "summary": "경쟁력 있는 글로벌 서플라이어를 발굴해 최적의 단가와 품질로 원자재 및 완제품을 조달하는 가치 창출자",
        "core_skills": ["원가 분석(Cost Breakdown)", "공급업체 품질 감사(Audit)", "단가 인하 협상력", "공급망 단절(Supply Chain) 리스크 관리"],
        "recommended_certs": ["CPIM/CSCP (APICS)", "국제무역사", "구매자재관리사(KPM)"],
        "color": "#F39C12"
    },
    "통관/무역규제": {
        "english": "Customs Brokerage & Trade Compliance",
        "icon": "⚖️",
        "summary": "수출입 통관 요건, HS Code 분류, FTA 원산지 관리를 통해 법적 리스크와 관세를 최적화하는 관세 전문가",
        "core_skills": ["HS Code 6단위/10단위 품목 분류", "FTA 원산지 증명서(C/O) 발급", "외환거래법 및 대외무역법 숙지", "관세 환급 실무"],
        "recommended_certs": ["관세사(전문자격)", "원산지관리사", "보세사"],
        "color": "#9B59B6"
    },
    "무역금융/외환관리": {
        "english": "Trade Finance & FX Risk Management",
        "icon": "💳",
        "summary": "수출환어음 매입, 결제 조건 협의, 환율 변동 위험을 헷지하여 무역 거래의 재무적 안전을 책임지는 금융 스페셜리스트",
        "core_skills": ["수출입 금융(Usance, D/A, D/P, L/C Nego)", "선물환/외환 포지션 관리", "무역보험(K-SURE) 활용", "대금 미회수 채권 리스크 방어"],
        "recommended_certs": ["외환전문역 1/2종", "CDCS(신용장전문가)", "투자자산운용사"],
        "color": "#1ABC9C"
    }
}

# --------------------------------------------------
# 3. 20개 진단 문항 정의
# --------------------------------------------------
QUESTIONS = [
    {"id": 1, "cat": "대인관계 및 영업", "q": "모르는 외국인 바이어에게 먼저 다가가 스몰토크를 건네고 관계를 맺는 것이 즐겁다.", "job": "해외영업", "weight": 2.5},
    {"id": 2, "cat": "대인관계 및 영업", "q": "목표 매출과 수주 실적이 숫자로 명확히 보상받을 때 가장 큰 동기부여를 느낀다.", "job": "해외영업", "weight": 2.5},
    {"id": 3, "cat": "대인관계 및 영업", "q": "해외 박람회 부스에 서서 하루 종일 고객 상담과 제품 피칭을 할 수 있는 에너지가 있다.", "job": "해외영업", "weight": 2.0},
    {"id": 4, "cat": "대인관계 및 영업", "q": "공급선과의 팽팽한 가격 협상에서 양보하지 않고 최적의 단가를 이끌어내는 데 자신 있다.", "job": "글로벌 소싱/구매", "weight": 2.0},
    {"id": 5, "cat": "서류 및 프로세스", "q": "계약서, 인보이스의 오탈자나 단어 하나의 오역도 절대 그냥 넘어가지 않고 잡아낸다.", "job": "무역사무/수출입관리", "weight": 2.5},
    {"id": 6, "cat": "서류 및 프로세스", "q": "신용장(L/C) 상의 까다로운 선적 조건과 유효기일을 캘린더에 맞춰 체계적으로 통제하는 게 적성에 맞는다.", "job": "무역사무/수출입관리", "weight": 2.5},
    {"id": 7, "cat": "서류 및 프로세스", "q": "예측 불가능한 돌발 영업보다는 명확한 매뉴얼과 정해진 절차대로 업무를 완결하는 것을 선호한다.", "job": "무역사무/수출입관리", "weight": 2.0},
    {"id": 8, "cat": "서류 및 프로세스", "q": "법조문이나 관세율표를 찾아보며 규정에 부합하는지 팩트체크하는 과정이 흥미롭다.", "job": "통관/무역규제", "weight": 2.0},
    {"id": 9, "cat": "물류 및 스케줄링", "q": "컨테이너 선박, 항공기, 내륙 트럭이 연결되는 복잡한 운송망 지도를 보면 가슴이 뛴다.", "job": "포워딩/국제물류", "weight": 2.5},
    {"id": 10, "cat": "물류 및 스케줄링", "q": "태풍이나 항만 파업으로 선적 지연이 발생해도 빠르게 대체 선박을 찾아내는 순발력이 있다.", "job": "포워딩/국제물류", "weight": 2.5},
    {"id": 11, "cat": "물류 및 스케줄링", "q": "여러 선사와 포워더의 운임 견적서를 비교해 최저 운임과 최단 리드타임을 도출하는 계산이 재밌다.", "job": "포워딩/국제물류", "weight": 2.0},
    {"id": 12, "cat": "물류 및 스케줄링", "q": "실제 창고나 보세구역에 화물이 입출고되는 현장 동선과 패킹 상태를 확인하는 것을 좋아한다.", "job": "포워딩/국제물류", "weight": 2.0},
    {"id": 13, "cat": "글로벌 소싱 및 시장조사", "q": "동일한 원자재라도 해외 사이트(알리바바 등)를 이 잡듯 뒤져 더 저렴한 제조사를 찾아낸다.", "job": "글로벌 소싱/구매", "weight": 2.5},
    {"id": 14, "cat": "글로벌 소싱 및 시장조사", "q": "해외 제조 공장의 생산 공정과 불량률, 품질 인증을 분석하고 평가하는 일에 흥미가 있다.", "job": "글로벌 소싱/구매", "weight": 2.5},
    {"id": 15, "cat": "글로벌 소싱 및 시장조사", "q": "환율, 유가, 글로벌 원자재 가격 변동 추이를 주기적으로 챙겨보고 향후 가격을 예측해 본다.", "job": "무역금융/외환관리", "weight": 2.0},
    {"id": 16, "cat": "글로벌 소싱 및 시장조사", "q": "공급업체의 일방적인 납기 지연을 방지하기 위해 엄격한 지체상금 조항을 계약서에 넣는 편이다.", "job": "글로벌 소싱/구매", "weight": 2.0},
    {"id": 17, "cat": "법률/관세 및 금융", "q": "복잡한 기계 부품의 재질과 기능을 따져 10단위 HS 품목분류 코드를 확정 짓는 퍼즐 같은 일이 매력적이다.", "job": "통관/무역규제", "weight": 2.5},
    {"id": 18, "cat": "법률/관세 및 금융", "q": "각국 FTA 특혜관세 기준을 충족시켜 관세를 절감해 줄 때 보람을 느낀다.", "job": "통관/무역규제", "weight": 2.5},
    {"id": 19, "cat": "법률/관세 및 금융", "q": "바이어의 부도나 대금 미지급 리스크를 사전에 차단하기 위해 신용조사와 무역보험을 철저히 챙긴다.", "job": "무역금융/외환관리", "weight": 2.5},
    {"id": 20, "cat": "법률/관세 및 금융", "q": "수출환어음 매입(네고) 시 은행의 하자 지적을 받지 않도록 금융 서류를 빈틈없이 검토한다.", "job": "무역금융/외환관리", "weight": 2.5}
]

CARD_OPTIONS = [
    (1, "🙅‍♂️ 전혀 아니다"),
    (2, "🙁 아닌 편이다"),
    (3, "😐 보통이다"),
    (4, "🙂 그런 편이다"),
    (5, "🙆‍♂️ 매우 그렇다")
]

# --------------------------------------------------
# 4. 세션 상태 초기화
# --------------------------------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "intro"
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "answers" not in st.session_state:
    st.session_state.answers = {q["id"]: 3 for q in QUESTIONS}

# --------------------------------------------------
# 화면 1: 초기 인트로 화면 (텍스트 전체 가운데 정렬 반영)
# --------------------------------------------------
if st.session_state.stage == "intro":
    st.markdown("<div class='main-title'>🌐 무역 직무 MBTI 센터 🌐</div>", unsafe_allow_html=True)

    intro_path = os.path.join(os.path.dirname(__file__), "intro.jpg")
    
    if os.path.exists(intro_path):
        with open(intro_path, "rb") as img_file:
            b64_data = base64.b64encode(img_file.read()).decode()
        img_tag_src = f"data:image/jpeg;base64,{b64_data}"
    else:
        img_tag_src = "https://images.unsplash.com/photo-1578575437130-527eed3abbec?w=1000&auto=format&fit=crop&q=80"

    st.markdown(
        f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 10px auto 16px auto;">
            <div style="
                width: 100%;
                max-width: clamp(230px, 68vw, 330px);
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 14px rgba(0,0,0,0.12);
            ">
                <img src="{img_tag_src}" style="width: 100%; height: auto; display: block;" alt="직무 준비">
            </div>
            <p style="font-size: clamp(0.75rem, 2.3vw, 0.85rem); color: #888; margin-top: 6px; text-align: center;">직무...준비되셨습니까?</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("""
    <div class='responsive-card' style='border: 1px solid #e0e0e0; text-align: center;'>
        <p style='font-size: clamp(1rem, 3.5vw, 1.15rem); font-weight: bold; margin-bottom: 6px; text-align: center;'>
            &ldquo;무역학과 나와서 뭐 하지?&rdquo;
        </p>
        <p style='font-size: clamp(1rem, 3.5vw, 1.15rem); font-weight: bold; margin-bottom: 14px; text-align: center;'>
            &ldquo;비전공자인데 어떤 무역 포지션이 맞을까?&rdquo;
        </p>
        <div style='line-height: 1.75; color: #475569; font-size: clamp(0.85rem, 2.9vw, 1.0rem); margin-bottom: 0; text-align: center;'>
            <p style='margin: 0; text-align: center;'>10년 차 UI 전문가 <b>코식이</b>와</p>
            <p style='margin: 0; text-align: center;'>20년 차 무역 전문가 <b>무식이</b>가 함께 설계한</p>
            <p style='margin: 0; text-align: center;'>20문항 초정밀 직무 적합도 진단입니다.</p>
        </div>
        <hr style='margin: 14px 0;'>
        <p style='font-size: clamp(0.8rem, 2.5vw, 0.9rem); color: #888; margin-bottom: 0; text-align: center;'>
            ⏱️ 진단 소요 시간: 약 2 ~ 3분 | 척도: 1점 ~ 5점
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 진단 시작", use_container_width=True, type="primary"):
        st.session_state.stage = "test"
        st.session_state.q_index = 0
        st.rerun()

# --------------------------------------------------
# 화면 2: 질문 상자 및 컨테이너선 진행 바 (🚢 항해 트랙)
# --------------------------------------------------
elif st.session_state.stage == "test":
    curr_idx = st.session_state.q_index
    total_q = len(QUESTIONS)
    curr_q = QUESTIONS[curr_idx]

    progress_pct = round(((curr_idx + 1) / total_q) * 100, 1)

    st.markdown(
        f"""
        <div style="width: 100%; margin: 12px 0 25px 0;">
            <div style="position: relative; width: 100%; height: 28px;">
                <span style="
                    position: absolute;
                    left: calc({progress_pct}% - 14px);
                    font-size: 24px;
                    transition: left 0.35s cubic-bezier(0.4, 0, 0.2, 1);
                    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.18));
                    user-select: none;
                ">🚢</span>
            </div>
            <div style="
                width: 100%; 
                height: 8px; 
                background-color: #E2E8F0; 
                border-radius: 6px; 
                overflow: hidden;
            ">
                <div style="
                    width: {progress_pct}%; 
                    height: 100%; 
                    background: linear-gradient(90deg, #38BDF8 0%, #0284C7 100%);
                    border-radius: 6px; 
                    transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1);
                "></div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px;">
                <span style="font-size: 0.8rem; color: #0284C7; font-weight: 700;">🌊 {progress_pct}% 순항 중</span>
                <span style="font-size: 0.85rem; color: #64748B; font-weight: 700;">{curr_idx + 1} / {total_q}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="quiz-question-container">
            <span class="quiz-badge">{curr_q['cat']}</span>
            <div class="quiz-question-title">{curr_q['q']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    pad_left, center_col, pad_right = st.columns([1, 4, 1])

    with center_col:
        for score, label_text in CARD_OPTIONS:
            if st.button(label_text, key=f"btn_opt_{score}_{curr_q['id']}", use_container_width=True):
                st.session_state.answers[curr_q["id"]] = score
                if curr_idx < total_q - 1:
                    st.session_state.q_index += 1
                    st.rerun()
                else:
                    st.session_state.stage = "result"
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if curr_idx > 0:
            st.markdown("<div class='nav-btn'>", unsafe_allow_html=True)
            if st.button("⬅️ 이전 질문으로 돌아가기", use_container_width=True):
                st.session_state.q_index -= 1
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# 화면 3: 최종 진단 결과 화면
# --------------------------------------------------
elif st.session_state.stage == "result":
    job_scores = {job: 0.0 for job in TRADE_JOBS.keys()}
    job_max_possible = {job: 0.0 for job in TRADE_JOBS.keys()}

    for item in QUESTIONS:
        q_id = item["id"]
        target_job = item["job"]
        weight = item["weight"]
        user_val = st.session_state.answers[q_id]

        job_scores[target_job] += user_val * weight
        job_max_possible[target_job] += 5.0 * weight

    job_percentages = {}
    for job in TRADE_JOBS.keys():
        job_percentages[job] = round((job_scores[job] / job_max_possible[job]) * 100, 1)

    sorted_jobs = sorted(job_percentages.items(), key=lambda x: x[1], reverse=True)
    top_job, top_pct = sorted_jobs[0]
    top_info = TRADE_JOBS[top_job]

    ocean_wave_animation_html = """
    <style>
    .wave-transition-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 999999;
        pointer-events: none;
        overflow: hidden;
        animation: fadeOutContainer 2.2s forwards ease-in-out;
    }
    .wave-layer {
        position: absolute;
        left: -50%;
        width: 200%;
        height: 140vh;
        border-radius: 43% 47% 44% 46%;
        bottom: -150vh;
    }
    .wave1 {
        background: linear-gradient(180deg, rgba(56, 189, 248, 0.85) 0%, rgba(2, 132, 199, 0.95) 100%);
        animation: waveRoll 2.1s forwards cubic-bezier(0.4, 0, 0.2, 1);
        z-index: 1;
    }
    .wave2 {
        background: linear-gradient(180deg, rgba(14, 165, 233, 0.75) 0%, rgba(3, 105, 161, 0.9) 100%);
        animation: waveRoll 2.1s forwards cubic-bezier(0.4, 0, 0.2, 1) 0.12s;
        border-radius: 46% 44% 47% 43%;
        z-index: 2;
    }
    .wave3 {
        background: linear-gradient(180deg, rgba(224, 242, 254, 0.9) 0%, rgba(56, 189, 248, 0.8) 100%);
        animation: waveRoll 2.1s forwards cubic-bezier(0.4, 0, 0.2, 1) 0.22s;
        border-radius: 42% 48% 43% 47%;
        z-index: 3;
    }
    @keyframes waveRoll {
        0% { bottom: -140vh; transform: rotate(0deg); }
        48% { bottom: -15vh; transform: rotate(180deg); }
        100% { bottom: 120vh; transform: rotate(360deg); }
    }
    @keyframes fadeOutContainer {
        0% { opacity: 1; }
        85% { opacity: 0.95; }
        100% { opacity: 0; visibility: hidden; }
    }
    </style>
    <div class="wave-transition-overlay">
        <div class="wave-layer wave1"></div>
        <div class="wave-layer wave2"></div>
        <div class="wave-layer wave3"></div>
    </div>
    """
    st.markdown(ocean_wave_animation_html, unsafe_allow_html=True)

    # 1. '당신에게 가장 추천하는 무역 직무' (적합 매칭도)
    st.markdown(
        "<h3 style='font-size: clamp(1.2rem, 3.8vw, 1.6rem); margin-bottom: 12px; word-break: keep-all;'>🎯 당신에게 가장 추천하는 무역 직무</h3>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"""
        <div class='responsive-card' style="border: 2.5px solid {top_info['color']}; text-align: center;">
            <div style="font-size: clamp(40px, 10vw, 55px); margin-bottom: 8px;">{top_info['icon']}</div>
            <h2 style="color: {top_info['color']}; font-size: clamp(1.5rem, 5vw, 2.2rem); margin-bottom: 4px;">{top_job}</h2>
            <p style="font-size: clamp(0.85rem, 2.5vw, 0.95rem); color: #888; font-weight: 500;">{top_info['english']}</p>
            <hr style="border: 0.5px solid #eee; margin: 14px 0;">
            <p style="font-size: clamp(1.1rem, 3.5vw, 1.35rem); font-weight: bold; margin-bottom: 8px;">적합 매칭도: <span style="color: {top_info['color']};">{top_pct}%</span></p>
            <p style="font-size: clamp(0.92rem, 2.8vw, 1.05rem); line-height: 1.6; text-align: center; margin-top: 10px;">
                {top_info['summary']}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # 2. '6대 직무 적합도 비교 차트'
    st.markdown("<h3 style='font-size: clamp(1.2rem, 3.8vw, 1.6rem); margin-bottom: 12px;'>📊 6대 직무 적합도 비교 차트</h3>", unsafe_allow_html=True)
    
    chart_rows_list = []
    for rank, (j_name, j_pct) in enumerate(sorted_jobs):
        alpha = max(0.28, 1.0 - (rank * 0.14))
        bar_color_style = f"background-color: {top_info['color']}; opacity: {alpha:.2f};"
        row_html = (
            f'<div class="chart-row">'
            f'<div class="chart-label">{j_name}</div>'
            f'<div class="chart-bar-bg">'
            f'<div class="chart-bar-fill" style="width: {j_pct}%; {bar_color_style}"></div>'
            f'</div>'
            f'<div class="chart-value">{j_pct:.1f}%</div>'
            f'</div>'
        )
        chart_rows_list.append(row_html)

    all_chart_rows_html = "".join(chart_rows_list)
    st.markdown(
        f"""
        <div class="native-chart-container">
            {all_chart_rows_html}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # 3. '무식이 교수의 실무 가이드'
    st.markdown(
        f"""
        <h3 style='font-size: clamp(1.2rem, 3.8vw, 1.6rem); line-height: 1.45; margin-bottom: 16px;'>
            🎓 무식이 교수의 실무 가이드:<br>'{top_job} 취업 전략'
        </h3>
        """, 
        unsafe_allow_html=True
    )
    
    g_col1, g_col2 = st.columns(2)

    with g_col1:
        st.markdown("#### 🛠️ 현업 요구 실무 역량")
        for skill in top_info["core_skills"]:
            st.markdown(f"- ✅ **{skill}**")

    with g_col2:
        st.markdown("#### 📜 추천 자격증 & 로드맵")
        for cert in top_info["recommended_certs"]:
            st.markdown(f"- 🏅 **{cert}**")

    # 4. 진단 리포트 CSV 다운로드 및 다시하기 버튼
    st.markdown("---")
    # 📌 왼쪽 정렬 적용 (text-align: left)
    st.markdown("<h3 style='font-size: clamp(1.2rem, 3.8vw, 1.6rem); margin-bottom: 16px; text-align: left;'>💾 진단 리포트 저장 및 안내</h3>", unsafe_allow_html=True)

    report_df = pd.DataFrame([
        {"순위": i+1, "무역직무": j[0], "영문명": TRADE_JOBS[j[0]]["english"], "적합도(%)": j[1]}
        for i, j in enumerate(sorted_jobs)
    ])
    csv_data = report_df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")

    pad_l, btn_c1, btn_c2, pad_r = st.columns([1, 2, 2, 1])

    with btn_c1:
        st.download_button(
            label="📥 무역 직무 다운로드 (CSV)",
            data=csv_data,
            file_name="trade_job_mbti_result.csv",
            mime="text/csv",
            use_container_width=True
        )

    with btn_c2:
        if st.button("🔄 처음으로 돌아가기", use_container_width=True):
            st.session_state.stage = "intro"
            st.session_state.q_index = 0
            st.session_state.answers = {q["id"]: 3 for q in QUESTIONS}
            st.rerun()