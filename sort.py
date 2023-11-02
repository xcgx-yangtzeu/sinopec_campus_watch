import csv

input_filename = "job_details.csv"
output_filename = "sorted_id.csv"

selected_ids = []

with open(input_filename, 'r') as input_file:
    reader = csv.reader(input_file)
    header = next(reader)  # 读取表头

    id_index = header.index("id")
    position_index = header.index("jobPosition")
    education_index = header.index("educationNorm")
    specialty_index = header.index("specialtyNorm")

    for row in reader:
        id_value = row[id_index]
        job_position = row[position_index]
        education_norm = row[education_index]
        specialty_norm = row[specialty_index]

        if "本科" in education_norm and ("计算机类" in specialty_norm or "软件工程" in specialty_norm) and "三地" not in job_position:
            selected_ids.append(id_value)

if len(selected_ids) > 0:
    with open(output_filename, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["id"])

        for id_value in selected_ids:
            writer.writerow([id_value])

    print(f"符合条件的ID已保存到文件: {output_filename}")
else:
    print("未找到符合条件的ID.")