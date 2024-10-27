import csv
import requests
import os.path

# 读取CSV文件
filename = 'ids.csv'
post_ids = []

with open(filename, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过表头
    for row in reader:
        post_id = row[0]
        post_ids.append(post_id)

# 发送请求并获取数据
base_url = "http://job.sinopec.com/api/upgrade/homepage/selectPositionDetail"

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "DNT": "1",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://job.sinopec.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

filename = "job_details.csv"
file_exists = os.path.isfile(filename)
existing_ids = set()

if file_exists:
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过表头
        for row in reader:
            if row:  # 确保行不为空
                existing_ids.add(row[0])

with open(filename, "a", newline="", encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    if not file_exists:  # 如果文件为空，写入表头
        writer.writerow(["id", "jobPosition", "number", "workAddr", "educationNorm",
                         "specialtyNorm", "postNum", "deptName"])

    for post_id in post_ids:
        if post_id in existing_ids:
            print(f"职位ID {post_id} 已存在，跳过")
            continue

        url = f"{base_url}?postId={post_id}"
        try:
            response = requests.get(url, headers=headers, verify=False)  # 添加 verify=False
            response_json = response.json()

            # 处理响应数据
            print(post_id + ":")
            data = response_json.get("data")
            message = response_json.get("message")

            if message == "请求成功" and data:
                # 提取字段数据
                id_value = data.get("id")
                job_position = data.get("jobPosition")
                number = data.get("number")
                work_addr = data.get("workAddr")
                education_norm = data.get("educationNorm")
                specialty_norm = data.get("specialtyNorm")
                post_num = data.get("postNum")
                dept_name = data.get("deptName")

                # 保存到CSV文件
                writer.writerow([id_value, job_position, number, work_addr,
                                 education_norm, specialty_norm, post_num, dept_name])

                print(f"职位ID {post_id} 的数据已保存到文件: {filename}")
            else:
                print(f"请求失败或无数据，职位ID {post_id}")
        except Exception as e:
            print(f"请求失败或无数据，职位ID {post_id}，错误信息：{str(e)}")
