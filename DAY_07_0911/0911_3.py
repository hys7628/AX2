# 대화 기록을 기억하는 멀티턴 챗봇 (스트리밍 응답)
# st.session_state에 대화 기록을 저장해 이전 맥락을 기억
# st.chat_message / st.chat_input 전용 위젯 활용
# stream=True 옵션과 st.write_stream으로 실시간 타이핑 효과 구현
# 실행 명령어: streamlit run 0911_3.py

import streamlit as st
from openai import OpenAI

# --------------------------------------------------
# 1. 페이지 기본 설정
# --------------------------------------------------
st.set_page_config(page_title="I'M YOUR CHATBOT", page_icon="💬", layout="centered")
st.title("💬 THIS IS MY CHATBOT")
st.caption("대화 맥락을 기억하고 실시간 스트리밍으로 타이핑하듯 답변하는 멀티턴 챗봇")

# --------------------------------------------------
# 2. 세션 상태(st.session_state) 초기화
# --------------------------------------------------
# messages 리스트에는 {"role": "user"|"assistant", "content": "..."} 형태로 대화 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------------------------
# 3. 사이드바 설정 (API Key, 모델, 커스텀 시스템 프롬프트, 초기화)
# --------------------------------------------------
with st.sidebar:
    st.header("⚙️ 설정")
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="sk-로 시작하는 OpenAI API key를 입력하세요.",
    )
    model = st.selectbox(
        "모델 선택",
        ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"],
        index=0,
        help="사용할 OpenAI 모델을 선택하세요.",
    )

    st.markdown("---")
    st.subheader("🎭 시스템 역할 (페르소나) 설정")
    
    # 기본값으로 기존 야쿠자 두목 콘셉트 제공 및 사용자가 자유롭게 수정 가능
    default_system_prompt = (
        "너는 거칠고 위압감 넘치지만 묘하게 의리 있는 일본 야쿠자 조직의 오야붕(두목)이다. "
        "반말과 거친 어조('~냐?', '~해라, 알아들었냐?', '이 몸이 친히 말해주마')를 사용해 한국어로 답변하라."
    )
    system_prompt = st.text_area(
        "시스템 메시지 입력",
        value=default_system_prompt,
        height=140,
        help="AI의 성격, 말투, 역할 규칙을 지정할 수 있습니다.",
    )

    st.markdown("---")
    # 대화 기록 초기화 버튼
    if st.button("🗑️ 대화 기록 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("[OpenAI API 키 발급받기](https://platform.openai.com/home)")

# --------------------------------------------------
# 4. 이전 대화 기록 화면 렌더링
# --------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------------------------------
# 5. 채팅 입력창 및 스트리밍 응답 처리
# --------------------------------------------------
user_input = st.chat_input("메시지를 입력하세요...")

if user_input:
    # API 키 누락 검증
    if not api_key:
        st.error("⚠️ 사이드바에서 OpenAI API Key를 먼저 입력해주세요.")
    else:
        # 1. 사용자 질문을 세션 상태에 추가하고 화면에 출력
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # 2. 어시스턴트(챗봇) 답변 스트리밍 생성
        with st.chat_message("assistant"):
            try:
                client = OpenAI(api_key=api_key)

                # OpenAI API에 전달할 메시지 조합 (System Prompt + 이전 대화 기록 전체)
                api_messages = [{"role": "system", "content": system_prompt}] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]

                # stream=True 옵션 설정
                response_stream = client.chat.completions.create(
                    model=model,
                    messages=api_messages,
                    stream=True,
                )

                # st.write_stream은 제너레이터를 받아 화면에 실시간 타이핑하고 최종 문자열을 반환
                full_response = st.write_stream(response_stream)

                # 3. 스트리밍이 완료된 최종 답변을 세션 상태에 저장하여 다음 턴에 반영
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")