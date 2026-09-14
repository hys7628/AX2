# Open AI + streamlit 앱
# 질문 하나 입력하면 OpenAI chat Completions API 한 번 호출
# 답변을 받아오는 가장 단순한 방법
# 대화 기록을 기억하지 않는 단발성 질문-답변
# streamlit run 0911_2.py

# 챗봇 만든가? -> rag, langchain 필요!!

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="I'M YOUR CHATBOT")
st.title("THIS IS MY CHATBOT")
st.caption(
    "질문 하나 입력하면 OpenAI chat Completions API 한 번 호출, 답변을 받아오는 가장 단순한 방법"
)

# ---------- 사이드바 API 모델 ---------------
with st.sidebar:
    st.header("설정")
    api_key = st.text_input(
        "OpenAI API key",
        type="password",
        help="sk-로 시작하는 OpenAI API key를 입력하세요.",
    )
    model = st.selectbox(
        "모델 선택",
        ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"],
        index=0,
        help="사용할 모델을 선택하세요",
    )
    st.markdown("[api 발급 받기](https://platform.openai.com/home)")

# -------------- 메인 화면 --------------------

question = st.text_input(
    "질문을 입력하세요", placeholder="욘두는 스타로드의 아버지니?"
)

if st.button("질문하기", type = "primary"):
    if not api_key:
        st.error("OpenAI API Key를 입력하세요.")
    elif not question:
        st.error("질문을 입력하세요.")
    else:
        try:
            # 1. OpenAI 클라이언트 초기화
            client = OpenAI(api_key=api_key)

            # 2. 로딩 상태 스피너 표시
            with st.spinner("두목이 담배 한 대 피우며 생각 중이다..."):
                # 3. 야쿠자 두목 시스템 프롬프트 설정 및 API 호출
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "너는 거칠고 위압감 넘치지만 묘하게 의리 있는 일본 야쿠자 조직의 오야붕(두목)이다. "
                                "반말과 거친 어조('~냐?', '~해라, 알아들었냐?', '이 몸이 친히 말해주마')를 사용해 한국어로 답변하라."
                            ),
                        },
                        {"role": "user", "content": question},
                    ],
                )

            # 4. 답변 출력
            answer = response.choices[0].message.content
            st.subheader("🕶️ 두목의 답변")
            st.write(answer)

            # 5. 사용한 토큰 수 표시 (입력 토큰, 출력 토큰, 총 토큰 수)
            if response.usage:
                st.markdown("---")
                st.caption("📊 토큰 소비 내역")
                col1, col2, col3 = st.columns(3)
                col1.metric("입력(질문) 토큰", f"{response.usage.prompt_tokens}개")
                col2.metric(
                    "출력(답변) 토큰", f"{response.usage.completion_tokens}개"
                )
                col3.metric("총 사용 토큰", f"{response.usage.total_tokens}개")

        except Exception as e:
            # 6. 오류 발생 시 에러 메시지 출력
            st.error(f"오류가 발생했습니다: {e}")
