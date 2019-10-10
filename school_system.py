import sqlite3
import collections
import re
import random


# 用于连接 grade 表
class Grade():
    '''
    年级编号 grade_no
    年级名称 grade_name
    '''
    def __init__(self, con):
        self.con = con
        self.cursor = con.cursor()
        self.__create_table()

    # 创建表
    def __create_table(self):
        sql = 'CREATE TABLE IF NOT EXISTS grade (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                grade_no INT, grade_name TEXT)'
        self.cursor.execute(sql)

    # 插入数据
    def insert_grade(self, grade_no):
        sql = 'INSERT INTO grade(grade_no, grade_name) VALUES (?, ?)'
        self.cursor.execute(sql, (grade_no, str(grade_no)+'年级'))
        self.con.commit()


# 用于连接 class 表
class Class_():
    '''
    班级编号 class_no
    年级编号 grade_no
    班级名称 class_name
    '''
    def __init__(self, con):
        self.con = con
        self.cursor = con.cursor()
        self.__create_table()

    # 创建表
    def __create_table(self):
        sql = 'CREATE TABLE IF NOT EXISTS class (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                class_no INT, grade_no INT, class_name TEXT)'
        self.cursor.execute(sql)

    # 插入数据
    def insert_class(self, class_no, grade_no):
        sql = 'INSERT INTO class(class_no, grade_no, class_name) VALUES (?, ?, ?)'
        self.cursor.execute(sql, (class_no, grade_no, str(grade_no)+'年级'+str(class_no)+'班'))
        self.con.commit()


# 用于连接 student 表
class Student():
    '''
    学生编号 student_no
    学生名字 student_name
    学生性别 student_sex
    班级编号 class_no
    年级编号 grade_no
    '''
    def __init__(self, con):
        self.con = con
        self.cursor = con.cursor()
        self.__create_table()

    # 创建表
    def __create_table(self):
        sql = 'CREATE TABLE IF NOT EXISTS student (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                student_no INT, student_name TEXT, student_sex TEXT, class_no INT, grade_no INT)'
        self.cursor.execute(sql)

    # 插入数据
    def insert_student(self, student_no, student_name, student_sex, class_no, grade_no):
        sql = 'INSERT INTO student(student_no, student_name, student_sex, class_no, grade_no) VALUES (?, ?, ?, ?, ?)'
        self.cursor.execute(sql, (student_no, student_name, student_sex, class_no, grade_no))
        self.con.commit()


# 用于连接 course 表
class Course():
    '''
    课程编号 course_no
    课程名称 course_name
    '''
    def __init__(self, con):
        self.con = con
        self.cursor = con.cursor()
        self.__create_table()

    # 创建表
    def __create_table(self):
        sql = 'CREATE TABLE IF NOT EXISTS course (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                course_no INT, course_name TEXT)'
        self.cursor.execute(sql)

    # 插入数据
    def insert_course(self, course_no, course_name):
        sql = 'INSERT INTO course(course_no, course_name) VALUES (?, ?)'
        self.cursor.execute(sql, (course_no, course_name))
        self.con.commit()


# 用于连接 student_course 表
class StudentCourse():
    '''
    学生编号 student_no
    所选课程编号 course_no
    考试得分 score
    '''
    def __init__(self, con):
        self.con = con
        self.cursor = con.cursor()
        self.__create_table()

    # 创建表
    def __create_table(self):
        sql = 'CREATE TABLE IF NOT EXISTS student_course (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                student_no INT, course_no INT, score INT)'
        self.cursor.execute(sql)

    # 插入数据
    def insert_student(self, student_no, course_no, score):
        sql = 'INSERT INTO student_course (student_no, course_no, score) VALUES (?, ?, ?)'
        self.cursor.execute(sql, (student_no, course_no, score))
        self.con.commit()


# 从txt文件中读取数据
def get_students_and_courses_data():
    with open('学校的组织结构项目描述.txt', 'r') as f:
        # 先将开头两行描述除去
        f.readline()
        f.readline()
        # 读取剩余的数据
        text = f.read()

    # 初始化变量
    reg = '(.年级.班)'
    students = collections.defaultdict(list)

    # 获取数据列表
    raw_data = text.split()

    # 清洗出学生数据
    for i, each_line in enumerate(raw_data):
        # 获取课程列表
        if '学校的课程' in each_line:
            courses = raw_data[i + 1].split('、')
            break

        # 获取班级数据
        re_result = re.findall(reg, each_line)
        if re_result:
            class_name = re_result[0]
            continue

        # 添加学生数据到该班级
        students[class_name].append(each_line)

    return students, courses


def main():
    # 获取数据
    class_students, courses = get_students_and_courses_data()

    # 连接数据库
    con = sqlite3.connect('school.db')

    # 初始化变量
    grade_table = Grade(con)
    class_table = Class_(con)
    student_table = Student(con)
    course_table = Course(con)
    student_course_table = StudentCourse(con)

    grade_no = 1
    class_no = 1
    student_no = 1

    # 创建课程表
    for i, course in enumerate(courses):
        course_table.insert_course(i, course)

    # 遍历 students，依次创建数据
    for class_name, student_list in class_students.items():
        # 如果class_no 的值要大于6的话，说明一个年级已经遍历完了
        if class_no == 6:
            class_no = 1
            grade_no += 1

        # class_no == 1的话，说明一个年级刚开始，则需要插入年级表中
        if class_no == 1:
            grade_table.insert_grade(grade_no)

        # 将新的班级插入数据库中
        class_table.insert_class(class_no, grade_no)

        # 遍历班级里的每个学生
        for each_student in student_list:
            # 将每个班级的学生数据录入学生表中
            student_table.insert_student(student_no, each_student, random.choice(['男', '女']), class_no, grade_no)

            # 给学生随机选课，给出分数，并录入数据库中
            chosen_courses = random.sample(range(len(courses)), 4)
            # 将选中的课插入数据库中
            for course_no in chosen_courses:
                student_course_table.insert_student(student_no, course_no, random.randint(0, 100))

            student_no += 1

        class_no += 1
        # print(class_name)
        # print(student_list)


if __name__ == '__main__':
    main()
