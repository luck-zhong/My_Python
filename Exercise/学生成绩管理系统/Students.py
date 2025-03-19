#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Exercise 
@File    ：Students.py
@IDE     ：PyCharm 
@Author  ：努力赚钱的小钟！
@Date    ：2025/3/17 下午9:24 
"""
import json


class Student:
    # 初始化学生对象
    def __init__(self, student_id, name, score=None):
        self.student_id = student_id
        self.name = name
        self.score = score if score is not None else {}

    def add_score(self, subject, score):
        if 0 < score < 100:
            self.score[subject] = score
        else:
            raise ValueError('成绩必须在0-100之间!')

    def to_dict(self):
        return {
            "学号": self.student_id,
            "姓名": self.name,
            "成绩": self.score
        }


class StudentManager:
    def __init__(self, filename):
        self.filename = filename
        self.students = self._load_student_info()

    # 从文件读取学生信息
    def _load_student_info(self):
        try:
            with open(self.filename, 'r', encoding='UTF-8') as file:
                data = json.load(file)
                return [self._creat_student(item) for item in data]

        except FileNotFoundError as e:
            raise FileNotFoundError(f"文件 {self.filename} 未找到")
        except json.JSONDecodeError as e:
            raise ValueError("无效的JSON格式")

    # 保存学生信息到文件
    def save_student_info(self):
        try:
            with open(self.filename, 'w', encoding='UTF-8') as file:
                student_info = []
                for s in self.students:
                    student_info.append(s.to_dict())
                json.dump(student_info,
                          file,
                          indent=2,
                          ensure_ascii=False)

        except FileNotFoundError as e:
            raise FileNotFoundError(f"文件 {self.filename} 未找到")

    def _creat_student(self, item):
        return Student(
            item['学号'],
            item['姓名'],
            item.get('成绩', {})
        )

    # 查找学生信息
    def find_student(self, student_id):
        for s in self.students:
            if s.student_id == student_id:
                print(f"{'学号':<12} {'姓名':<10}{''.join(map(str, s.score.keys())):<8}")
                print(f"{s.student_id:<12} {s.name:<10}{''.join(map(str, s.score.values())):<8}")
                break
        else:
            print('查无此人!')

    # 删除学生信息
    def delete_student(self, student_id):
        for s in self.students:
            if s.student_id == student_id:
                self.students.remove(s)
                self.save_student_info()

    # 添加学生信息
    def add_student(self, student_id, name):
        for s in self.students:
            if student_id == s.student_id:
                print('此学生信息已存在!')
                break
        else:
            new_student = Student(student_id, name)
            self.students.append(new_student)
            self.save_student_info()


if __name__ == '__main__':
    Manage = StudentManager('student.json')
    Manage.find_student(2020)
    Manage.add_student(2022, '王五')
