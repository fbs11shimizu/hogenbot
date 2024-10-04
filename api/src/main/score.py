import os
import json
import torch
import logging 
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel, PeftConfig

def init():
    global tuned_model
    global tokenizer

    # モデルとトークナイザーのロード
    base_path = "/var/azureml-app/azureml-models/ELYZA/1/hogenbot_model"  
    base_model_path = base_path + "/base_model"

    tokenizer = AutoTokenizer.from_pretrained(base_model_path)

    # LoRAアダプターのロード
    adapter_config_path = base_path
    peft_config = PeftConfig.from_pretrained(adapter_config_path)

    # 基本モデルのロード (LoRAのベースモデルを読み込む)
    base_model = AutoModelForCausalLM.from_pretrained(
        peft_config.base_model_name_or_path,
        torch_dtype="auto",  # 自動的に最適なデータ型を選択
        device_map="auto",   # デバイス（GPU/CPU）の自動マッピング
    )

    tuned_model = PeftModel.from_pretrained(base_model, adapter_config_path)
    tuned_model.eval()

def run(data) -> dict:
    try:  
        data = json.loads(data) if isinstance(data, str) else data  
        message = data.get("massage")  
  
        if not message is None:  
            raise ValueError("Data is missing required fields: 'message', 'repeat_penalty', 'temperature'")  
  
        response = tuned_model(
            create_prompt(message),
            max_tokens=50,
            echo=False,
            do_sample=True,
            top_p=0.95,
            repeat_penalty=1.15,
            temperature=0.2
            ) 
        logging.info(response)
        logging.info("Inference done.")  
        return response
    except Exception as e:  
        logging.error(f"Inference failed: {e}")  
        raise e

def create_prompt(message):
    # システムメッセージを定義
    sys_msg = "以下の「指示」に対して、適切な「応答」となる内容の文章を出力してください。"

    prompt = f"""
    {sys_msg}

    指示:
    {message}

    応答：
    """
    logging.info(prompt)
    return prompt
