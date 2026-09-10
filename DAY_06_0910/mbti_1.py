"""
프로젝트: 무역 직무 적합도 MBTI 대시보드 (Trade Job Fit Test) - 완전 반응형 모바일/웹 지원
설명: 모바일(스마트폰), 태블릿, 데스크톱 화면 크기에 따라 UI가 유동적으로 변하는 20문항 진단 대시보드
수정사항: 시작 화면 이미지를 1:2:1 비율 컬럼의 가운데(2 위치)에 width=600으로 배치
실행 명령어: streamlit run app.py
"""
import platform
import io
import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# --------------------------------------------------
# 0. 한글 폰트 설정 (OS 환경별 대응)
# --------------------------------------------------
if platform.system() == "Windows":
    plt.rcParams["font.family"] = "Malgun Gothic"
elif platform.system() == "Darwin":
    plt.rcParams["font.family"] = "AppleGothic"
else:
    plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.unicode_minus"] = False

# --------------------------------------------------
# 1. Streamlit 페이지 설정 및 반응형 글로벌 CSS 주입
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
    max-width: 950px !important;
    padding-left: clamp(1rem, 4vw, 2.5rem) !important;
    padding-right: clamp(1rem, 4vw, 2.5rem) !important;
    padding-top: clamp(1.2rem, 3vw, 2.5rem) !important;
}

/* 유동적 헤딩 글자 크기 */
.main-title {
    font-size: clamp(1.4rem, 4.5vw, 2.2rem) !important;
    font-weight: 800 !important;
    text-align: center;
    line-height: 1.35;
    margin-bottom: 0.8rem;
    word-break: keep-all;
}

/* 카드 UI 반응형 패딩 */
.responsive-card {
    padding: clamp(16px, 3.5vw, 28px) !important;
    border-radius: 14px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06) !important;
    background: rgba(255, 255, 255, 0.03);
    word-break: keep-all;
}

/* 문항 글자 반응형 */
.question-text {
    font-size: clamp(1.05rem, 3.2vw, 1.4rem) !important;
    line-height: 1.55 !important;
    font-weight: 700 !important;
    margin-top: 14px !important;
    word-break: keep-all;
}

/* 모바일 화면에서 버튼 간격 최적화 */
@media (max-width: 640px) {
    div[data-testid="column"] {
        margin-bottom: 8px !important;
    }
    .stRadio div[role="radiogroup"] {
        gap: 6px !important;
    }
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

SCALE_OPTIONS = [
    (1, "1. 전혀 아님"),
    (2, "2. 아님"),
    (3, "3. 보통"),
    (4, "4. 그렇다"),
    (5, "5. 매우 그렇다")
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

def next_question_callback(q_id):
    chosen_val = st.session_state[f"radio_step_{q_id}"]
    st.session_state.answers[q_id] = chosen_val
    if st.session_state.q_index < len(QUESTIONS) - 1:
        st.session_state.q_index += 1

# --------------------------------------------------
# 화면 1: 초기 인트로 화면 (1:2:1 컬럼의 2 위치에 width=600 배치)
# --------------------------------------------------
if st.session_state.stage == "intro":
    st.markdown("<div class='main-title'>🌐 무역 직무 MBTI 센터 🌐</div>", unsafe_allow_html=True)

    intro_path = os.path.join(os.path.dirname(__file__), "intro.jpg")
    
    # 📌 1:2:1 컬럼 생성 후 가운데 2번 컬럼(img_col2)에 width=600 사진 배치
    img_col1, img_col2, img_col3 = st.columns([1, 2, 1])
    with img_col2:
        if os.path.exists(intro_path):
            st.image(intro_path, caption="직무...준비되셨습니까?", width=600)
        else:
            st.image("https://images.unsplash.com/photo-1578575437130-527eed3abbec?w=1000&auto=format&fit=crop&q=80", caption="Global Trade Navigator", width=600)
    
    st.markdown("""
    <div class='responsive-card' style='border: 1px solid #e0e0e0;'>
        <p style='font-size: clamp(1rem, 3.5vw, 1.15rem); font-weight: bold; margin-bottom: 6px;'>&ldquo;무역학과 나와서 뭐 하지?&rdquo;</p>
        <p style='font-size: clamp(1rem, 3.5vw, 1.15rem); font-weight: bold; margin-bottom: 12px;'>&ldquo;비전공자인데 어떤 무역 포지션이 맞을까?&rdquo;</p>
        <p style='line-height: 1.65; color: #555; font-size: clamp(0.9rem, 3vw, 1.02rem); margin-bottom: 0;'>
            10년 차 UI 전문가 <b>코식이</b>와 20년 차 무역 전문가 <b>무식이</b>가 함께 설계한<br>
            <b>20문항 초정밀 직무 적합도 진단</b>입니다.
        </p>
        <hr style='margin: 14px 0;'>
        <p style='font-size: clamp(0.8rem, 2.5vw, 0.9rem); color: #888; margin-bottom: 0;'>⏱️ 진단 소요 시간: 약 2 ~ 3분 | 척도: 1점 ~ 5점</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 진단 시작", use_container_width=True, type="primary"):
        st.session_state.stage = "test"
        st.session_state.q_index = 0
        st.rerun()

# --------------------------------------------------
# 화면 2: 1문항씩 게임형 진단 화면
# --------------------------------------------------
elif st.session_state.stage == "test":
    curr_idx = st.session_state.q_index
    total_q = len(QUESTIONS)
    curr_q = QUESTIONS[curr_idx]

    progress_val = (curr_idx + 1) / total_q
    st.progress(progress_val)
    st.markdown(f"<p style='text-align: right; color: #888; font-weight: 700; font-size: clamp(0.8rem, 2.8vw, 0.95rem); margin-top: 4px;'>진행도: {curr_idx + 1} / {total_q} 문항</p>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class='responsive-card' style='border: 2px solid #3498DB;'>
            <span style="background-color: #3498DB; color: white; padding: 4px 10px; border-radius: 16px; font-size: clamp(0.75rem, 2.5vw, 0.85rem); font-weight: bold;">
                {curr_q['cat']}
            </span>
            <div class='question-text'>* {curr_q['q']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    saved_val = st.session_state.answers.get(curr_q["id"], 3)
    
    st.radio(
        label=f"문항_{curr_q['id']}_선택",
        options=[opt[0] for opt in SCALE_OPTIONS],
        format_func=lambda x: [opt[1] for opt in SCALE_OPTIONS if opt[0] == x][0],
        index=saved_val - 1,
        key=f"radio_step_{curr_q['id']}",
        on_change=next_question_callback,
        args=(curr_q["id"],),
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    btn_col1, btn_col2 = st.columns([1, 1])

    with btn_col1:
        if curr_idx > 0:
            if st.button("⬅️ 이전 문제", use_container_width=True):
                st.session_state.q_index -= 1
                st.rerun()

    with btn_col2:
        if curr_idx == total_q - 1:
            if st.button("🚀 최종 제출", use_container_width=True, type="primary"):
                st.session_state.stage = "result"
                st.rerun()

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

    door_animation_html = f"""
    <style>
    .door-portal-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 999999;
        pointer-events: none;
        perspective: 1200px;
        display: flex;
        overflow: hidden;
    }}
    .door-panel {{
        position: absolute;
        top: 0;
        width: 50vw;
        height: 100vh;
        background: linear-gradient(135deg, #1A252F 0%, #2C3E50 60%, #111827 100%);
        box-shadow: inset 0 0 60px rgba(0, 0, 0, 0.9);
        display: flex;
        align-items: center;
        transition: transform 1.6s cubic-bezier(0.77, 0, 0.175, 1);
    }}
    .door-left {{
        left: 0;
        transform-origin: left center;
        justify-content: flex-end;
        border-right: 2px solid rgba(255, 215, 0, 0.4);
        animation: openLeftDoor 1.8s forwards ease-in-out;
    }}
    .door-right {{
        right: 0;
        transform-origin: right center;
        justify-content: flex-start;
        border-left: 2px solid rgba(255, 215, 0, 0.4);
        animation: openRightDoor 1.8s forwards ease-in-out;
    }}
    @keyframes openLeftDoor {{
        0% {{ transform: rotateY(0deg); opacity: 1; }}
        65% {{ transform: rotateY(-95deg); opacity: 0.9; }}
        100% {{ transform: rotateY(-120deg); opacity: 0; visibility: hidden; }}
    }}
    @keyframes openRightDoor {{
        0% {{ transform: rotateY(0deg); opacity: 1; }}
        65% {{ transform: rotateY(95deg); opacity: 0.9; }}
        100% {{ transform: rotateY(120deg); opacity: 0; visibility: hidden; }}
    }}
    </style>
    <div class="door-portal-overlay">
        <div class="door-panel door-left"></div>
        <div class="door-panel door-right"></div>
    </div>
    """
    st.markdown(door_animation_html, unsafe_allow_html=True)

    # 1. '당신에게 가장 추천하는 무역 직무'
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
    
    plot_jobs = sorted_jobs[::-1]
    job_names = [j[0] for j in plot_jobs]
    job_values = [j[1] for j in plot_jobs]
    n_jobs = len(plot_jobs)

    alpha_levels = np.linspace(0.25, 1.0, n_jobs)
    base_color = top_info['color']
    rgb_base = mcolors.to_rgb(base_color)
    bar_colors = [(rgb_base[0], rgb_base[1], rgb_base[2], a) for a in alpha_levels]

    fig, ax = plt.subplots(figsize=(8, 4.2))
    bars = ax.barh(job_names, job_values, color=bar_colors, edgecolor=base_color, height=0.58)

    ax.set_xlim(0, 118)
    ax.set_xlabel("직무 적합도 (%)", fontsize=10, fontweight="bold")

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color("#ccc")
    ax.spines['bottom'].set_color("#ccc")
    ax.xaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)

    for bar in bars:
        width = bar.get_width()
        ax.annotate(
            f" {width:.1f}%",
            xy=(width, bar.get_y() + bar.get_height() / 2),
            xytext=(3, 0),
            textcoords="offset points",
            va="center",
            ha="left",
            fontsize=10,
            fontweight="bold",
            color="#222"
        )

    ax.tick_params(axis='y', labelsize=10.5)
    for tick in ax.get_yticklabels():
        tick.set_fontweight("bold")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

    st.markdown("---")

    # 3. '무식이 교수의 실무 가이드'
    st.markdown(f"<h3 style='font-size: clamp(1.2rem, 3.8vw, 1.6rem); margin-bottom: 12px;'>🎓 무식이 교수의 실무 가이드: '{top_job}' 취업 전략</h3>", unsafe_allow_html=True)
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
    st.markdown("<h3 style='font-size: clamp(1.2rem, 3.8vw, 1.6rem); margin-bottom: 12px;'>💾 진단 리포트 저장 및 다운로드</h3>", unsafe_allow_html=True)

    report_df = pd.DataFrame([
        {"순위": i+1, "무역직무": j[0], "영문명": TRADE_JOBS[j[0]]["english"], "적합도(%)": j[1]}
        for i, j in enumerate(sorted_jobs)
    ])

    csv_data = report_df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")

    action_col1, action_col2 = st.columns([2, 1])
    with action_col1:
        st.download_button(
            label="📥 진단서 다운로드 (CSV)",
            data=csv_data,
            file_name="trade_job_mbti_result.csv",
            mime="text/csv",
            use_container_width=True
        )
    with action_col2:
        if st.button("🔄 다시 검사하기", use_container_width=True):
            st.session_state.stage = "intro"
            st.session_state.q_index = 0
            st.session_state.answers = {q["id"]: 3 for q in QUESTIONS}
            st.rerun()