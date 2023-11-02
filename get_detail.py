import csv
import requests
import os.path

# 读取CSV文件
filename = 'ids.csv'
post_ids = []

with open(filename, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过表头
    for row in reader:
        post_id = row[0]
        post_ids.append(post_id)

# 发送请求并获取数据
base_url = "http://job.sinopec.com/api/upgrade/homepage/selectPositionDetail"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "referrer": "http://job.sinopec.com/",
}

filename = "job_details.csv"
file_exists = os.path.isfile(filename)
existing_ids = set()  # 用于存储已存在的职位ID

if file_exists:
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过表头
        for row in reader:
            existing_ids.add(row[0])  # 将已存在的职位ID添加到集合中

with open(filename, "a", newline="") as file:
    writer = csv.writer(file)
    if not file_exists:  # 如果文件为空，写入表头
        writer.writerow(["id", "jobPosition", "number", "workAddr", "educationNorm",
                         "specialtyNorm", "postNum", "deptName"])

    for post_id in post_ids:
        if post_id in existing_ids:
            print(f"职位ID {post_id} 已存在，跳过")
            continue

        url = f"{base_url}?postId={post_id}"
        response = requests.get(url, headers=headers).json()

        # 处理响应数据
        print(post_id + ":")
        try:
            data = response.get("data")
            message = response.get("message")
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
        except:
            print(f"请求失败或无数据，职位ID {post_id}")