# dockerhubよりpythonのベースイメージを作成(名称を"base"とする)
FROM python:3.12-slim AS base

# 作業ディレクトリを指定
WORKDIR /app

# 現在のホストのディレクトリ内のフォルダ/ファイルをコンテナのWORKDIR指定のディレクトリにコピー
COPY . .

# ホストからコピーしたrequirements.txtに従ってpipでライブラリをインストール
RUN pip install -r requirements.txt

# コンテナがlistenするポートを明示（※マッピングは必要）
EXPOSE 8501

# コンテナ起動後にbashを起動
CMD ["bash"]
# CMD ["streamlit", "run", "/src/main/app.py"]