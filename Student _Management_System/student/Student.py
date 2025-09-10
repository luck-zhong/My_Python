#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Student _Management_System 
@File    ：Student.py
@IDE     ：PyCharm 
@Author  ：努力赚钱的小钟！
@Date    ：2025/9/10 下午8:31 
"""
import json


class Student(object):
    def __init__(self, name, student_id):
        self.file_name = 'student_info.json'
        self.name = name
        self.student_id = student_id
        self.stu_info = self._find_student_info()

    def _find_student_info(self):
        """从JSON文件中找到当前学生的信息"""
        try:
            with open(self.file_name, 'r', encoding='utf-8') as rf:
                data = json.load(rf)
                # 在学生列表中查找当前学生
                for student in data.get('students', []):
                    if (student.get('name') == self.name and
                            student.get('student_id') == self.student_id):
                        return student
                # 如果没找到，创建一个新的学生信息
                return self._create_new_student()
        except FileNotFoundError:
            # 如果文件不存在，创建新的学生信息
            return self._create_new_student()

    def _create_new_student(self):
        """创建新的学生信息结构"""
        return {
            "name": self.name,
            "student_id": self.student_id,
            "score": {}
        }

    def add_score(self, subject, score):
        """添加或更新科目成绩"""
        if subject in self.stu_info['score']:
            print(f"更新 {subject} 成绩: {self.stu_info['score'][subject]} -> {score}")
        else:
            print(f"添加 {subject} 成绩: {score}")

        self.stu_info['score'][subject] = score
        self._save_to_file()

    def _save_to_file(self):
        """将学生信息保存到文件"""
        try:
            # 读取现有数据
            with open(self.file_name, 'r', encoding='utf-8') as rf:
                data = json.load(rf)
        except FileNotFoundError:
            # 如果文件不存在，创建新的数据结构
            data = {"students": []}

        # 查找是否已存在该学生
        found = False
        for i, student in enumerate(data['students']):
            if (student.get('name') == self.name and
                    student.get('student_id') == self.student_id):
                # 更新现有学生信息
                data['students'][i] = self.stu_info
                found = True
                break

        # 如果没找到，添加新学生
        if not found:
            data['students'].append(self.stu_info)

        # 写回文件
        with open(self.file_name, 'w', encoding='utf-8') as wf:
            json.dump(data, wf, ensure_ascii=False, indent=2)

    def show_info(self):
        """显示学生信息"""
        print(f"学生: {self.name} (学号: {self.student_id})")
        print("成绩:")
        for subject, score in self.stu_info['score'].items():
            print(f"  {subject}: {score}")


if __name__ == '__main__':
    # 初始化学生（会自动创建或加载信息）
    stu = Student("zhangsan", 20)

    # 添加成绩
    stu.add_score('Math', 95)
    stu.add_score('Chinese', 88)
    stu.add_score('English', 92)

    # 显示信息
    stu.show_info()

    # 更新成绩
    stu.add_score('Math', 98)
    stu.show_info()
