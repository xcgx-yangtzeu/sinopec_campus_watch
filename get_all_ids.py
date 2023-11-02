import requests
import json
import csv

url = "http://job.sinopec.com/api/upgrade/homepage/selectPositionList"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/json;charset=UTF-8",
    "proxy-connection": "keep-alive"
}

payload = {
    "page": 1,
    "limit": 2000,
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

# 获取响应内容
data = response.json()

# 处理响应数据
records = data['data']['records']
ids = [record['id'] for record in records]

# 保存到CSV文件
filename = 'ids.csv'
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id'])  # 写入表头
    writer.writerows([[id] for id in ids])  # 逐行写入数据

print(f"IDs已保存到文件: {filename}")