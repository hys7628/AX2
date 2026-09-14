import streamlit as st
import pandas as pd
from openai import OpenAI

# --------------------------------------------------
# 1. 페이지 기본 설정 및 제목
# --------------------------------------------------
st.set_page_config(page_title="Paper Summary", page_icon="💬", layout="centered")
st.title("💬 Paper Summary")
st.caption("텍스트 파일을 업로드하면 OpenAI API가 원하는 스타일로 요약해 드립니다.")

# --------------------------------------------------
# 2. 세션 상태(st.session_state) 초기화
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------------------------
# 3. 사이드바 설정 (API Key, 모델, 페르소나, 요약 옵션)
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
    st.subheader("요약 옵션")
    summary_length = st.selectbox(
        "요약 길이",
        ["짧게(3줄)", "보통(5-7줄)", "자세히(500자 이상)"],
        index=0,
        help="요약 옵션을 선택하세요.",
    )
    
    # 대화 기록 초기화 버튼
    if st.button("🗑️ 대화 기록 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("[OpenAI API 키 발급받기](https://platform.openai.com/home)")

# --------------------------------------------------
# 4. 파일 업로드 + [수정 1] 미리보기 상자 + [수정 2] 요약하기 버튼
# --------------------------------------------------
uploaded_file = st.file_uploader("요약할 파일을 업로드하세요", type=["txt", "csv"])

file_content = ""

if uploaded_file is not None:
    # 1) 파일 내용 읽기
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            file_content = df.to_string()
            
            # [수정 1] CSV 미리보기 상자
            st.markdown("#### 📄 업로드한 문서 미리보기")
            st.dataframe(df.head(10), use_container_width=True)
            st.caption(f"전체 {len(df)}행 중 상위 10행을 미리 보여줍니다.")
        else:
            raw_bytes = uploaded_file.read()
            try:
                file_content = raw_bytes.decode("utf-8")
            except UnicodeDecodeError:
                file_content = raw_bytes.decode("cp949", errors="ignore")
                
            # [수정 1] TXT 문서 미리보기 상자
            st.markdown("#### 📄 업로드한 문서 미리보기")
            st.text_area(
                label="문서 원문",
                value=file_content,
                height=220,
                disabled=True,
                label_visibility="collapsed"
            )
    except Exception as e:
        st.error(f"파일을 읽는 도중 오류가 발생했습니다: {e}")

    # [수정 2] 미리보기 상자 바로 아래 '요약하기' 실행 버튼
    if st.button("📝 요약하기", type="primary", use_container_width=True):
        if not api_key:
            st.error("⚠️ 사이드바에서 OpenAI API Key를 먼저 입력해주세요.")
        elif not file_content.strip():
            st.warning("⚠️ 업로드된 파일 내용이 비어 있습니다.")
        else:
            # 요약 요청 프롬프트 생성
            summary_request_prompt = (
                f"다음 업로드된 문서 내용을 요약 길이 기준([{summary_length}])에 맞추어 네 페르소나(말투)대로 요약해라.\n\n"
                f"[문서 내용]\n{file_content[:7000]}"  # 토큰 초과 방지
            )

            # 사용자 요청 기록 추가
            st.session_state.messages.append({
                "role": "user", 
                "content": f"📄 '{uploaded_file.name}' 문서 요약을 요청했습니다. (옵션: {summary_length})"
            })

            # 스트리밍 요약 실행 및 출력
            with st.chat_message("assistant"):
                try:
                    client = OpenAI(api_key=api_key)
                    api_messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": summary_request_prompt}
                    ]

                    response_stream = client.chat.completions.create(
                        model=model,
                        messages=api_messages,
                        stream=True,
                    )
                    full_response = st.write_stream(response_stream)
                    
                    # 요약 완료 결과 세션에 저장
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": full_response
                    })
                    st.rerun()

                except Exception as e:
                    st.error(f"요약 처리 중 오류가 발생했습니다: {e}")

st.markdown("---")

# --------------------------------------------------
# 5. 요약 결과 및 이전 대화 내역 출력
# --------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------------------------------
# 6. 추가 질문 채팅 입력창
# --------------------------------------------------
user_input = st.chat_input("요약본에 대해 추가로 질문할 내용을 입력하세요...")

if user_input:
    if not api_key:
        st.error("⚠️ 사이드바에서 OpenAI API Key를 먼저 입력해주세요.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            try:
                client = OpenAI(api_key=api_key)
                api_messages = [{"role": "system", "content": system_prompt}] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]

                response_stream = client.chat.completions.create(
                    model=model,
                    messages=api_messages,
                    stream=True,
                )
                full_response = st.write_stream(response_stream)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": full_response
                })

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")