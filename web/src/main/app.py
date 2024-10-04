import os
import sys
import streamlit as st 
import numpy as np 
import json
import requests
from openai import AzureOpenAI
from dotenv import load_dotenv

st.title('方言Chat Bot')

# 3つのカラムを作成
col1, col2, col3 = st.columns([2, 2, 1])
# 右上にボタンを配置
with col3:
    if st.button("クリア"):
        st.session_state.messages = [{"role": "assistant", "content":"なんでも質問してや"}]

def generate_answer_elyza(question):
  load_dotenv()

  import urllib.request
  import json
  import os
  import ssl

  def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

  allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

  # Request data goes here
  # The example below assumes JSON formatting which may be updated
  # depending on the format your endpoint expects.
  # More information can be found here:
  # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
  data = {
     "message":question
  }

  body = str.encode(json.dumps(data))

  url = 'https://hogen-chatbot-team2-qzkfn.japaneast.inference.ml.azure.com/score'
  # Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint
  api_key = os.getenv("AZURE_ML_API_KEY_ELYZA")
  if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")


  headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

  req = urllib.request.Request(url, body, headers)

  try:
    response = urllib.request.urlopen(req)

    result = response.read()
    result_json = json.loads(result.decode('utf-8'))
    print(result_json)
  except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))
  return result_json

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content":"なんでも質問してや"}]

# アプリの再実行の際に履歴のチャットメッセージを表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザー入力に対する反応
if prompt := st.chat_input("質問をどうぞ"):
    # チャットメッセージコンテナにユーザーメッセージを表示
    st.chat_message("user").markdown(prompt)
    # チャット履歴にユーザーメッセージを追加
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner('回答を生成中...'):
      bot_response = generate_answer_elyza(prompt)
      answer = bot_response['choices'][0]['text']
      response = f"""{answer}"""

    # チャットメッセージコンテナにアシスタントのレスポンスを表示
    with st.chat_message("assistant"):
      st.markdown(response)

    # チャット履歴にアシスタントのレスポンスを追加
    st.session_state.messages.append({"role": "assistant", "content": response})