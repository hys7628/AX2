from openai import OpenAI 

client = OpenAI(api_key="")
# response = client.chat.completions.create(
#     model = "gpt-4o-mini",
#     messages = [
#         {"role": "system", "content": "친절한 도우미."},
#          ]    
# )
# print(response.choices[0].message.content)


# 함수로 만들어서 다용도로 만들기

def ask_llm(api_key, model, question):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model = model,
        messages = [{"role": "system", "content": "친절한 도우미."},
        {"role": "user", "content":question} ]
    )
    return response.choices[0].message.content, response.usage

my_api_key = ""
answer, usage = ask_llm(my_api_key, "gpt-4o-mini", "안녕하세요. 오늘 환율 얼마인가요?")
print("Answer:", answer)
