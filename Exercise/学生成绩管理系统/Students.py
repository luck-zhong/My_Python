import json
import os
from datetime import datetime
from functools import wraps


# ======================
# 装饰器模块
# ======================
def validate_student_id(func):
    """验证学号格式的装饰器"""

    @wraps(func)
    def wrapper(manager, student_id, *args, **kwargs):
        if not student_id.isalnum():
            raise ValueError("学号必须为字母数字组合")
        return func(manager, student_id, *args, **kwargs)

    return wrapper


def validate_name(func):
    """验证姓名格式的装饰器"""

    @wraps(func)
    def wrapper(manager, student_id, name, *args, **kwargs):
        if not name.strip():
            raise ValueError("姓名不能为空")
        if any(char.isdigit() for char in name):
            raise ValueError("姓名不能包含数字")
        return func(manager, student_id, name, *args, **kwargs)

    return wrapper


# ======================
# 数据模型类
# ======================
class Student:
    """学生信息数据模型"""

    def __init__(self, student_id, name, scores=None, created_at=None):
        self.student_id = student_id
        self.name = name
        self.scores = scores if scores is not None else {}
        self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_score(self, subject, score):
        """添加/更新科目成绩"""
        if not isinstance(score, (int, float)) or not (0 <= score <= 100):
            raise ValueError("成绩必须是0-100的数字")
        self.scores[subject] = round(score, 1)

    def get_average(self):
        """计算加权平均分"""
        if not self.scores:
            return 0.0
        return round(sum(self.scores.values()) / len(self.scores), 1)

    def to_dict(self):
        """序列化为字典"""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "scores": self.scores,
            "created_at": self.created_at
        }


# ======================
# 业务逻辑类
# ======================
class StudentManager:
    """学生管理核心业务逻辑"""

    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = self._load_data()

    def _load_data(self):
        """安全加载数据"""
        if not os.path.exists(self.filename):
            return []

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [self._create_student(item) for item in data]
        except json.JSONDecodeError:
            print("数据文件格式错误，已初始化新数据")
            return []
        except PermissionError:
            print("文件访问权限不足")
            return []
        except Exception as e:
            print(f"数据加载失败: {str(e)}")
            return []

    def _create_student(self, item):
        """安全创建学生对象"""
        try:
            return Student(
                student_id=item["student_id"],
                name=item["name"],
                scores=item.get("scores", {}),
                created_at=item.get("created_at")
            )
        except KeyError as e:
            print(f"数据字段缺失: {str(e)}")
            return None

    def save_data(self):
        """自动保存数据"""
        try:
            valid_students = [s for s in self.students if s is not None]
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(
                    [s.to_dict() for s in valid_students],
                    f,
                    indent=2,
                    ensure_ascii=False
                )
        except IOError as e:
            print(f"保存失败: {str(e)}")

    @validate_student_id
    @validate_name
    def add_student(self, student_id, name):
        """添加新学生"""
        if any(s.student_id == student_id for s in self.students if s):
            raise ValueError("学号已存在")
        new_student = Student(student_id, name)
        self.students.append(new_student)
        self.save_data()

    @validate_student_id
    def delete_student(self, student_id):
        """删除学生"""
        original_count = len(self.students)
        self.students = [s for s in self.students
                         if s and s.student_id != student_id]
        if len(self.students) == original_count:
            raise ValueError("学号不存在")
        self.save_data()

    def find_student(self, keyword):
        """模糊查找学生"""
        return [s for s in self.students
                if s and (keyword.lower() in s.name.lower()
                          or keyword == s.student_id)]

    def get_class_stats(self, subject=None):
        """获取班级统计信息"""
        valid_students = [s for s in self.students if s and s.scores]

        if subject:
            scores = [s.scores[subject] for s in valid_students
                      if subject in s.scores]
        else:
            scores = [s.get_average() for s in valid_students]

        if not scores:
            return None

        return {
            "average": round(sum(scores) / len(scores), 1),
            "max": max(scores),
            "min": min(scores)
        }

    def show_all(self):
        """显示所有学生信息"""
        if not any(self.students):
            print("当前没有学生记录")
            return

        print("\n{:<12} {:<10} {:<8} {:<10}".format(
            "学号", "姓名", "平均分", "创建时间"))

        for s in self.students:
            if s:
                avg = s.get_average()
                print("{:<12} {:<10} {:<8} {:<10}".format(
                    s.student_id, s.name, avg, s.created_at))


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


def input_student_info():
    """学生信息输入流程"""
    while True:
        student_id = input("请输入学号：").strip()
        name = input("请输入姓名：").strip()
        if student_id and name:
            return student_id, name
        print("学号和姓名不能为空")


def confirm_action(prompt):
    """操作确认对话框"""
    while True:
        choice = input(f"{prompt} (y/n): ").lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        print("请输入 y 或 n")


# ======================
# 主程序
# ======================
def main():
    manager = StudentManager()

    menu_options = {
        "1": ("添加学生", lambda: manager.add_student(*input_student_info())),
        "2": ("删除学生", lambda: manager.delete_student(input("请输入要删除的学号：").strip())),
        "3": ("查找学生", lambda: manager.find_student(input("请输入学号或姓名：").strip())),
        "4": ("显示全部", manager.show_all),
        "5": ("添加成绩", lambda: add_score_flow(manager)),
        "6": ("班级统计", lambda: show_stats(manager)),
        "7": ("退出系统", lambda: exit())
    }

    while True:
        print("\n=== 学生成绩管理系统 ===")
        for key, (desc, _) in menu_options.items():
            print(f"{key}. {desc}")

        try:
            choice = input("请输入选项：").strip()

            if choice == "7":
                if confirm_action("确定要退出吗？"):
                    print("感谢使用！")
                    break
                continue

            if choice not in menu_options:
                print("无效选项")
                continue

            _, action = menu_options[choice]
            result = action()
            handle_action_result(result)

        except Exception as e:
            print(f"操作失败: {str(e)}")
            if confirm_action("是否重试？"):
                continue
            break


def add_score_flow(manager):
    """成绩添加流程"""
    student_id = input("请输入学号：").strip()
    students = manager.find_student(student_id)

    if not students:
        print("学生不存在")
        return

    student = students[0]
    subject, score = input_score()

    if subject in student.scores:
        if not confirm_action(f"科目 {subject} 已有成绩 {student.scores[subject]}，是否覆盖？"):
            return

    student.add_score(subject, score)
    manager.save_data()
    print("成绩更新成功！")


def show_stats(manager):
    """统计信息展示"""
    subject = input("请输入要统计的科目（留空统计总分）：").strip()
    stats = manager.get_class_stats(subject or None)

    if not stats:
        print("没有可用的统计数据")
        return

    print(f"\n{'科目' if subject else '班级'}统计结果：")
    print(f"平均分: {stats['average']}")
    print(f"最高分: {stats['max']}")
    print(f"最低分: {stats['min']}")


if __name__ == "__main__":
    main()