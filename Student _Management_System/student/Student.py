from typing import List, Dict, Optional
from dataclasses import dataclass
import json


@dataclass
class Grade:
    """成绩类 - 封装单科成绩信息"""
    course_name: str
    score: float
    credit: float

    def to_dict(self) -> Dict:
        """将成绩对象转换为字典"""
        return {
            'course_name': self.course_name,
            'score': self.score,
            'credit': self.credit
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Grade':
        """从字典创建成绩对象"""
        return cls(
            course_name=data['course_name'],
            score=data['score'],
            credit=data['credit']
        )


class Student:
    """学生类 - 封装学生信息和行为"""

    def __init__(self, student_id: str, name: str, major: str):
        self.student_id = student_id
        self.name = name
        self.major = major
        self.grades: List[Grade] = []  # 组合关系：学生包含多个成绩

    def add_grade(self, course_name: str, score: float, credit: float) -> None:
        """添加成绩"""
        grade = Grade(course_name, score, credit)
        self.grades.append(grade)

    def calculate_gpa(self) -> float:
        """计算GPA"""
        if not self.grades:
            return 0.0

        total_credits = sum(grade.credit for grade in self.grades)
        weighted_sum = sum(grade.score * grade.credit for grade in self.grades)

        return weighted_sum / total_credits if total_credits > 0 else 0.0

    def get_course_grade(self, course_name: str) -> Optional[Grade]:
        """获取指定课程成绩"""
        for grade in self.grades:
            if grade.course_name == course_name:
                return grade
        return None

    def to_dict(self) -> Dict:
        """将学生对象转换为字典"""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'major': self.major,
            'grades': [grade.to_dict() for grade in self.grades]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Student':
        """从字典创建学生对象"""
        student = cls(data['student_id'], data['name'], data['major'])
        student.grades = [Grade.from_dict(grade_data) for grade_data in data['grades']]
        return student


class GradeManager:
    """成绩管理类 - 单例模式，管理所有学生成绩"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.students: Dict[str, Student] = {}
        return cls._instance

    def add_student(self, student_id: str, name: str, major: str) -> bool:
        """添加学生"""
        if student_id in self.students:
            return False
        self.students[student_id] = Student(student_id, name, major)
        return True

    def get_student(self, student_id: str) -> Optional[Student]:
        """获取学生"""
        return self.students.get(student_id)

    def add_grade(self, student_id: str, course_name: str, score: float, credit: float) -> bool:
        """为学生添加成绩"""
        student = self.get_student(student_id)
        if not student:
            return False
        student.add_grade(course_name, score, credit)
        return True

    def get_student_gpa(self, student_id: str) -> Optional[float]:
        """获取学生GPA"""
        student = self.get_student(student_id)
        return student.calculate_gpa() if student else None

    def get_course_statistics(self, course_name: str) -> Dict:
        """获取课程统计信息"""
        scores = []
        for student in self.students.values():
            grade = student.get_course_grade(course_name)
            if grade:
                scores.append(grade.score)

        if not scores:
            return {}

        return {
            'average': sum(scores) / len(scores),
            'max': max(scores),
            'min': min(scores),
            'count': len(scores)
        }

    def save_to_file(self, filename: str) -> bool:
        """保存数据到文件"""
        try:
            data = {
                'students': {sid: student.to_dict() for sid, student in self.students.items()}
            }
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False

    def load_from_file(self, filename: str) -> bool:
        """从文件加载数据"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.students = {}
            for sid, student_data in data['students'].items():
                self.students[sid] = Student.from_dict(student_data)
            return True
        except:
            return False


# 示例使用
def main():
    # 创建成绩管理器
    manager = GradeManager()

    # 添加学生
    manager.add_student("2023001", "张三", "计算机科学")
    manager.add_student("2023002", "李四", "软件工程")

    # 添加成绩
    manager.add_grade("2023001", "高等数学", 85.5, 4.0)
    manager.add_grade("2023001", "程序设计", 92.0, 3.0)
    manager.add_grade("2023002", "高等数学", 78.0, 4.0)
    manager.add_grade("2023002", "英语", 88.5, 2.0)

    # 查询信息
    print(f"张三的GPA: {manager.get_student_gpa('2023001'):.2f}")
    print(f"高等数学统计: {manager.get_course_statistics('高等数学')}")

    # 保存数据
    manager.save_to_file("grades.json")


if __name__ == "__main__":
    main()