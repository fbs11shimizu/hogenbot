import os
import sys
import streamlit as st 
import numpy as np 
import json
import requests
from openai import AzureOpenAI
from dotenv import load_dotenv

st.title('Databricks Q&A bot')
#st.header('Databricks Q&A bot')

def generate_answer(question):
  load_dotenv()

  # クライアント設定方法
  client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key = os.getenv("AZURE_OPENAI_API_KEY"),
    api_version = os.getenv("AZURE_OPENAI_API_KEY")
    )

  # API呼出方法
  response = client.chat.completions.create(
      model="gpt-4o-mini-2024-07-18",
      messages=[
          {"role": "user", "content": prompt},
      ],
  )
  return response


if "messages" not in st.session_state:
    st.session_state.messages = []

# アプリの再実行の際に履歴のチャットメッセージを表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザー入力に対する反応
if prompt := st.chat_input("こんにちは！"):
    # チャットメッセージコンテナにユーザーメッセージを表示
    st.chat_message("user").markdown(prompt)
    # チャット履歴にユーザーメッセージを追加
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner('回答を生成中...'):
      bot_response = generate_answer(prompt)
      answer = bot_response.choices[0].message.content
      response = f"""{answer}"""

    # チャットメッセージコンテナにアシスタントのレスポンスを表示
    with st.chat_message("assistant"):
      st.markdown(response)

    # チャット履歴にアシスタントのレスポンスを追加
    st.session_state.messages.append({"role": "assistant", "content": response})


  