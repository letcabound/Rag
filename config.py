import torch


# base LLM
ZHIPU_MODEL_NAME = "your_model_name"
ZHIPU_API_KEY = "your_model_api_key"

# pretrained model path
PATH_BGE_M3 = "E:/models/m3e-base"
PATH_BGE_RERANKER = r"E:\models\bge-reranker-large"
PATH_FILE_KN = r'C:\Users\zhang\Desktop\地理学常识科普.pdf'

# model device config
EMBEDDING_MODEL_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
RERANKER_MODEL_DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

