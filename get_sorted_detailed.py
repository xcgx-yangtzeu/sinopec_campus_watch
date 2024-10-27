import csv
import requests
import os.path
from datetime import datetime
import pandas as pd

def read_post_ids(filename):
    post_ids = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # 跳过表头
            for row in reader:
                post_ids.append(row[0])
    except Exception as e:
        print(f"读取文件出错: {e}")
    return post_ids

def get_job_details(post_id, headers):
    url = f"http://job.sinopec.com/api/upgrade/homepage/selectPositionDetail?postId={post_id}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.json()
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def main():
    # 配置
    input_filename = 'sorted_id.csv'
    output_filename = 'result.csv'
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "referrer": "http://job.sinopec.com/",
    }
    header = ['id', 'job_position', 'number', 'work_addr', 'education_norm',
              'specialty_norm', 'post_num', 'dept_name', 'timestamp']

    # 读取职位ID
    post_ids = read_post_ids(input_filename)
    if not post_ids:
        print("没有找到职位ID")
        return

    # 读取现有数据
    existing_jobs = {}
    if os.path.isfile(output_filename):
        try:
            df = pd.read_csv(output_filename)
            existing_jobs = df.set_index('id').to_dict('index')
        except Exception as e:
            print(f"读取现有数据出错: {e}")

    # 获取和更新数据
    updated_jobs = []
    for post_id in post_ids:
        response = get_job_details(post_id, headers)
        if not response or response.get("message") != "请求成功":
            print(f"获取职位ID {post_id} 的数据失败")
            continue

        data = response.get("data")
        if not data:
            continue

        job_data = {
            'id': data.get("id"),
            'job_position': data.get("jobPosition"),
            'number': data.get("number"),
            'work_addr': data.get("workAddr"),
            'education_norm': data.get("educationNorm"),
            'specialty_norm': data.get("specialtyNorm"),
            'post_num': data.get("postNum"),
            'dept_name': data.get("deptName"),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        updated_jobs.append(job_data)
        print(f"职位ID {post_id} 的数据已{'更新' if post_id in existing_jobs else '添加'}")

    # 保存数据
    try:
        df = pd.DataFrame(updated_jobs)
        df['post_num'] = pd.to_numeric(df['post_num'], errors='coerce')
        df['number'] = pd.to_numeric(df['number'], errors='coerce')
        df['post_num_num_ratio'] = df['post_num'] / df['number']
        df_sorted = df.sort_values(by='post_num_num_ratio', ascending=True)
        df_sorted.to_csv(output_filename, index=False)
        print(f"已将排序后的结果保存到文件: {output_filename}")
    except Exception as e:
        print(f"保存数据时出错: {e}")

if __name__ == "__main__":
    main()
