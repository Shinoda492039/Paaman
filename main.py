import streamlit as st
import openai

# デプロイ環境用 API キー
openai.api_key = st.secrets.OpenAIAPI.OPENAI_API_KEY

# フロント構成コード
input_text = st.text_input('質問を具体的に入力してください')
if len(input_text) > 0:
    completion = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [{'role': 'user', 'content': input_text}],
        stream = True
)

    result_area = st.empty()
    text = ''
    for chunk in completion:
        next = chunk['choices'][0]['delta'].get('content', '')
        text += next
        result_area.write(text)
