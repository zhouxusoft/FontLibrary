import requests

# 定义请求的 URL
url = "https://www.fonts.net.cn/font-download.html"

# 定义请求的数据
data = {
    'id': '42183327657',
    'type': 'font'
}

# 发送 POST 请求
response = requests.post(url, data=data)

# 获取响应结果
if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print("POST request failed with status code:", response.status_code)