import os
from flask import Flask, render_template, request, send_from_directory, jsonify
from openai import OpenAI

app = Flask(__name__)


@app.route("/")
def home():
    """메인 홈 화면"""
    return render_template("index.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    """JS 없이 폼 전송할 때 사용하는 라우트"""
    country = ""
    api_key = ""
    result = None
    error_msg = None

    if request.method == "POST":
        api_key = request.form.get("apiKey", "").strip()
        country = request.form.get("country", "").strip()
        actual_key = api_key or os.getenv("OPENAI_API_KEY", "")

        if not actual_key:
            error_msg = "OpenAI API 키를 상단 입력창에 입력해주세요!"
        elif not country:
            error_msg = "조회할 국가명을 입력해주세요!"
        else:
            try:
                client = OpenAI(api_key=actual_key)
                system_prompt = (
                    "너는 글로벌 공급망 전문가 AI 'SupplyLens'야. "
                    "사용자가 요청한 국가에 대해 아래 5가지 항목을 빠짐없이 분석해 줘:\n"
                    "1. ⚠️ 공급망 리스크\n"
                    "2. 🚢 운임 동향\n"
                    "3. 💱 환율 변동성\n"
                    "4. 📋 관세 및 규제\n"
                    "5. 📰 핵심 뉴스\n"
                    "친절하고 명확한 한국어 텍스트로 작성해 줘."
                )

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"[{country}]의 현재 글로벌 공급망 상세 정보를 분석해줘."},
                    ],
                    temperature=0.3,
                )
                result = response.choices[0].message.content
            except Exception as e:
                error_msg = f"분석 중 문제가 발생했습니다: {str(e)}"

    return render_template(
        "dashboard.html",
        country=country,
        api_key=api_key,
        result=result,
        error_msg=error_msg,
    )


# 🎵 BGM 제공 라우트
@app.route('/bgm.mp3')
@app.route('/static/bgm.mp3')
def serve_bgm():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'bgm.mp3')


# 🤖 비동기 챗봇 통신 API 라우트
@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(silent=True) or {}
    country = data.get("country", "").strip()
    api_key = data.get("apiKey", "").strip() or os.getenv("OPENAI_API_KEY", "")

    if not api_key:
        return jsonify({"error": "OpenAI API 키를 상단에 입력해주세요!"}), 400
    if not country:
        return jsonify({"error": "국가명을 입력해주세요!"}), 400

    try:
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "너는 글로벌 공급망 분석 전문가다. "
                        "1.리스크 2.운임 3.환율 4.관세 5.핵심뉴스로 정리하라."
                    ),
                },
                {
                    "role": "user",
                    "content": f"[{country}]의 글로벌 공급망을 분석해줘.",
                },
            ],
            temperature=0.3,
        )
        return jsonify({"reply": resp.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": f"API 호출 오류: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)