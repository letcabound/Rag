import torch
from pathlib import Path

# base LLM
ZHIPU_MODEL_NAME = "glm-4-flash"
ZHIPU_API_KEY = "YOUR_API_KEY"

# pretrained model path
BASE_DIR = Path(__file__).resolve().parent.parent

PATH_DATA_DIR = BASE_DIR / 'data'

PATH_BGE_M3 = r"E:\models\m3e-base"
RERANK_BY_MODEL = True
PATH_BGE_RERANKER = r"E:\models\bge-reranker-large"

# model device config
DEVICE_EMBEDDING_MODEL = "cuda" if torch.cuda.is_available() else "cpu"
DEVICE_RERANKER_MODEL = 'cuda' if torch.cuda.is_available() else 'cpu'
