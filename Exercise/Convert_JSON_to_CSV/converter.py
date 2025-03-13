import json
import csv
import os
import chardet


def input_json(filename):
    """读取JSON文件并返回解析后的数据"""
    try:
        # 检测文件编码
        with open(filename, 'rb') as f:
            raw_data = f.read()
            encoding = chardet.detect(raw_data)['encoding']

        # 使用检测到的编码读取文件
        with open(filename, 'r', encoding=encoding) as file:
            data = json.load(file)  # 直接使用 json.load 简化代码
            if not data:
                raise ValueError("JSON文件内容为空")
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"文件 {filename} 未找到")
    except json.JSONDecodeError:
        raise ValueError("JSON文件格式错误")


def output_csv(data, output_filename='output.csv'):
    """将数据写入CSV文件"""
    try:
        with open(output_filename, 'w', encoding='utf-8-sig', newline='') as file:
            if not data:
                raise ValueError("无有效数据可写入CSV")
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"CSV文件已生成: {output_filename}")
    except (IOError, PermissionError) as e:
        raise RuntimeError(f"写入文件失败: {e}")


if __name__ == '__main__':
    try:
        # 直接使用相对路径（假设JSON与脚本同目录）
        json_filename = 'input.json'
        data = input_json(json_filename)
        output_csv(data)
    except Exception as e:
        print(f"错误: {e}")
