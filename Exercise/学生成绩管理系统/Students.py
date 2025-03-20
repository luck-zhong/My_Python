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
                student_info = [s.to_dict() for s in self.students]
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
    def find_student(self, name):
        for s in self.students:
            if s.name == name or s.student_id == name:
                print("\n学号 | 姓名 | 科目 | 成绩")
                print("-" * 30)
                for subject, score in s.score.items():
                    print(f"{s.student_id} | {s.name} | {subject} | {score}")
                return s
        else:
            print('查无此人!')

    # 删除学生信息
    def delete_student(self, name):
        for s in self.students:
            if s.name == name:
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

    # 修改学生信息
    def revise_student(self, name, student_id, score=None):
        for s in self.students:
            if name == s.name:
                s.student_id = student_id
                s.score = score
                self.save_student_info()
                break
        else:
            print('查无此人!')

    # 显示所有学生信息
    def show_all(self):
        print("\n学号 | 姓名 | 科目 | 成绩")
        print("-" * 30)
        for s in self.students:
            if s.score:
                for subject, score in s.score.items():
                    print(f"{s.student_id} | {s.name} | {subject:} | {score:}")
            else:
                print(f"{s.student_id} | {s.name} |{'':<5}|{'':<5}")

    @staticmethod
    def confirm_action(prompt):
        """操作确认对话框"""
        while True:
            choice = input(f"{prompt} (y/n): ").lower()
            if choice == 'y':
                return True
            elif choice == 'n':
                return False
            print("请输入 y 或 n")

    @staticmethod
    def input_student_info():
        """学生信息输入流程"""
        while True:
            student_id = input("请输入学号：").strip()
            name = input("请输入姓名：").strip()
            if student_id and name:
                return student_id, name
            print("学号和姓名不能为空")


# ======================
# 用户交互模块
# ======================
def input_score():
    """安全的成绩输入流程"""
    while True:
        try:
            subject = input("请输入科目名称：").strip()
            if not subject:
                raise ValueError("科目不能为空")

            score = float(input("请输入分数（0-100）："))
            if 0 <= score <= 100:
                return subject, score
            print("分数必须在0-100之间")
        except ValueError as e:
            print(f"输入错误: {str(e)}")


def add_score_flow(managerment):
    """成绩添加流程"""
    student_id = input("请输入学号或姓名：").strip()
    student = managerment.find_student(student_id)

    if not student:
        print("学生不存在")
        return

    subject, score = input_score()
    for subject, score in student.score:
        if subject in student.score:
            if not StudentManager.confirm_action(f"科目 {subject} 已有成绩 {student.score[subject]}，是否覆盖？"):
                return

    student.add_score(subject, score)
    managerment.save_student_info()
    print("成绩更新成功！")


if __name__ == '__main__':
    manager = StudentManager('student.json')
    menu_options = {
        "1": ("添加学生", lambda: manager.add_student(*StudentManager.input_student_info())),
        "2": ("删除学生", lambda: manager.delete_student(input("请输入要删除的学生姓名：").strip())),
        "3": ("查找学生", lambda: manager.find_student(input("请输入学号或姓名：").strip())),
        "4": ("显示全部", lambda: manager.show_all()),
        "5": ("添加成绩", lambda: add_score_flow(manager)),
        "6": ("退出系统", lambda: exit())
    }
    while True:
        print("\n=== 学生成绩管理系统 ===")
        for key, (desc, _) in menu_options.items():
            print(f"{key}. {desc}")

        try:
            choice = input("请输入选项：").strip()

            if choice == "7":
                if StudentManager.confirm_action("确定要退出吗？"):
                    print("感谢使用！")
                    break
                continue

            if choice not in menu_options:
                print("无效选项")
                continue

            _, action = menu_options[choice]
            result = action()

        except Exception as e:
            print(f"操作失败: {str(e)}")
            if StudentManager.confirm_action("是否重试？"):
                continue
            break
