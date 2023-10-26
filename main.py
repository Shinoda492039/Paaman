import streamlit as st
import openai

# デプロイ環境用 Organization ID
openai.organization = st.secrets.OpenAIAPI.organization

# デプロイ環境用 API キー
openai.api_key = st.secrets.OpenAIAPI.OPENAI_API_KEY

# ファインチューニング時に得られたモデルID
finetuned_model   =  'davinci:ft-personal-2023-10-15-05-38-51'

def AskChatbot(message):

    # 応答設定
    completion = openai.Completion.create(
    model       = finetuned_model,  # ファインチューニングしたモデルを選択
    prompt      = message,          # 質問文
    max_tokens  = 1024,             # 生成する文章の最大単語数
    n           = 1,                # いくつの返答を生成するか
    stop        = None,             # 指定した単語が出現した場合、文章生成を打ち切る
    temperature = 0.5               # 出力する単語のランダム性（0から2の範囲） 0であれば毎回返答内容固定
)

    # 応答
    response = completion.choices[0]['text']

    # 出力
    return response

# フロント構成コード
input_text = st.text_input('質問を具体的に入力してください')
if len(input_text) > 0:
    completion = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo', # finetuned_model を指定すると「openai.error.InvalidRequestError: This is not a chat model and thus not supported in the v1/chat/completions endpoint. Did you mean to use v1/completions?」というエラーが返ってくる
        messages = [{'role': 'user', 'content': input_text}], # content に「AskChatbot(input_text)」を入れるとエラーは出ないが動かない
        stream = True
)

    result_area = st.empty()
    text = ''
    for chunk in completion:
        next = chunk['choices'][0]['delta'].get('content', '')
        text += next
        result_area.write(text)
