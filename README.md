# RAG for DIY

## 1. 接口文档
POST
url: http://127.0.0.1:8000/api/v1/rags/geology  
params:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;query: 从 "地理知识科普.pdf" 文件中提问的问题。
```angular2html
import requests

url = r'http://127.0.0.1:8000/api/v1/rags/geology'
query = '现代地理学的检测手段有哪些'
response = requests.post(url=url, params={'query': query})
print(response.json())
```

## 2. 项目启动【python==3.11】
2.1 pip install -r requirements.txt  
2.2 python run.py  
2.3
在config.cfg.py文件中修改 PATH_BGE_MM3 为embedding模型本地存储目录
在config.cfg.py文件中修改 PATH_BGE_RERANKER 为rerank模型本地存储目录
在config.cfg.py文件中修改 ZHIPU_MODEL_NAME 为选用的智谱大模型名称
在config.cfg.py文件中修改 ZHIPU_MODEL_APIKEY 为选用的智谱大模型APIKEY
2.4 访问服务：http://127.0.0.1:8000


## 3. other
... ...
