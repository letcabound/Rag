import requests

url = r'http://127.0.0.1:8000/api/v1/rags/geology'
query = '现代地理学的检测手段有哪些'
response = requests.post(url=url, params={'query': query})
print(response.json())