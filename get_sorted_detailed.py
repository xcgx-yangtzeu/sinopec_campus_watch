import csv
import requests
import os.path
from datetime import datetime
import pandas as pd

# 读取CSV文件
filename = 'sorted_id.csv'
post_ids = []

with open(filename, 'r') as file:
    reader = csv.reader(file)
    header = ['id', 'job_position', 'number', 'work_addr', 'education_norm', 'specialty_norm', 'post_num', 'dept_name',
              'timestamp']
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

filename = "result.csv"
file_exists = os.path.isfile(filename)
existing_jobs = []  # 存储已存在的职位数据

if file_exists:
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            existing_jobs.append(row)  # 将已存在的职位数据添加到列表中

with open(filename, "a", newline="") as file:
    writer = csv.writer(file)

    if not file_exists:
        writer.writerow(header)  # 写入表头

    for post_id in post_ids:
        url = f"{base_url}?postId={post_id}"
        response = requests.get(url, headers=headers).json()

        # 处理响应数据
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
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前日期和时间

                # 刷新已存在的职位数据
                updated = False
                for i, job in enumerate(existing_jobs):
                    if job[0] == id_value:  # 根据职位ID匹配
                        existing_jobs[i] = [id_value, job_position, number, work_addr,
                                            education_norm, specialty_norm, post_num, dept_name, current_datetime]
                        updated = True
                        print(f"职位ID {post_id} 的数据已刷新")
                        break

                # 如果不存在，则将新数据添加到列表中
                if not updated:
                    existing_jobs.append([id_value, job_position, number, work_addr,
                                          education_norm, specialty_norm, post_num, dept_name, current_datetime])
                    print(f"职位ID {post_id} 的数据已添加")

        except:
            print(f"请求失败或无数据，职位ID {post_id}")

    # 将所有数据写入CSV文件
    writer.writerows(existing_jobs)

# 将结果文件排序
df = pd.read_csv(filename)
df['post_num'] = pd.to_numeric(df['post_num'])
df['number'] = pd.to_numeric(df['number'])
df['post_num_num_ratio'] = df['post_num'] / df['number']
df_sorted = df.sort_values(by='post_num_num_ratio', ascending=True)
df_sorted.to_csv(filename, index=False)

print(f"已将排序后的结果保存到文件: {filename}")