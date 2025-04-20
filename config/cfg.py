import torch
from pathlib import Path

# base LLM
ZHIPU_MODEL_NAME = "glm-4-flash"
ZHIPU_API_KEY = "a9d09b23922a4f1daccfc896ce087b80.R3uIADh7YBlDzlGq"

# pretrained model path
BASE_DIR = Path(__file__).resolve().parent.parent

PATH_DATA_DIR = BASE_DIR / 'data'
PATH_BGE_M3 = "E:/models/m3e-base"
PATH_BGE_RERANKER = r"E:\models\bge-reranker-large"

# model device config
DEVICE_EMBEDDING_MODEL = "cuda" if torch.cuda.is_available() else "cpu"
DEVICE_RERANKER_MODEL = 'cuda' if torch.cuda.is_available() else 'cpu'
