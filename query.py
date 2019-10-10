import sqlite3


def get_students_course(cursor, course):
    '''
    联合course和student_course表筛选出选了该课程学生的学生号。
    并且联合student和student_course筛选出选了该课程学生的名字。
    '''
    sql = ("SELECT a.student_name, c.course_name FROM \
       student AS a JOIN student_course AS b JOIN course AS c \
       ON a.student_no = b.student_no AND b.course_no = c.course_no \
       WHERE c.course_name = '{}'".format(course))

    return cursor.execute(sql).fetchall()


def get_students_course_class_grade(cursor, course, grade_no, class_no):
    '''
    联合course和student_course表筛选出选了该课程学生的学生号。
    联合student和student_course表筛选出选了该课程学生的名字。
    联合student和class表筛选出班级年级名称。
    '''
    sql = ("SELECT stu.student_name, cou.course_name, cls.class_name FROM \
            student AS stu JOIN student_course AS stuCou JOIN course AS cou JOIN class AS cls \
            ON stu.student_no = stuCou.student_no AND stuCou.course_no = cou.course_no \
            AND (stu.class_no = cls.class_no AND stu.grade_no = cls.grade_no) \
            WHERE cou.course_name = '{}' AND stu.grade_no = '{}' AND stu.class_no = '{}'".format(course, grade_no, class_no))

    return cursor.execute(sql).fetchall()


def course1_and_course2(cursor, course_1, course_2):
    '''
    先在student_student_course表中选出选了course_1的学生号。
    再用同样的方法筛选出选了course_2，并且在course_1筛选结果中的学生号。
    最后根据student表，确定名字。
    '''
    sql = ("SELECT student_name from student WHERE student_no IN (SELECT student_no FROM student_course \
            WHERE (course_no = (SELECT course_no FROM course WHERE course_name = '{}')) AND (student_no IN \
            (SELECT student_no FROM student_course WHERE course_no = \
            (SELECT course_no FROM course WHERE course_name = '{}'))))".format(course_1, course_2))

    return cursor.execute(sql).fetchall()


def get_name_by_score(cursor, course, score):
    '''
    方法一
    联合student, student_course, course三张表一起查询两个条件
    '''
    sql1 = ("SELECT stu.student_name FROM student AS stu JOIN course AS cou JOIN student_course AS stuCou \
            ON stu.student_no = stuCou.student_no AND cou.course_no = stuCou.course_no \
            WHERE cou.course_name = '{}' AND stuCou.score >= '{}'".format(course, score))

    '''
    方法二
    1 在course表中查出课程编号。
    2 在student_no表中根据课程编号和分数查出学生编号
    3 在student表中根据学生编号查出学生姓名
    '''
    sql2 = ("SELECT student_name FROM student WHERE student_no \
             IN (SELECT student_no FROM student_course WHERE score >= '{}' \
             AND course_no = (SELECT course_no FROM course WHERE course_name = '{}'))".format(score, course))

    return cursor.execute(sql1).fetchall()


def get_failed(cursor, grade_no):
    sql = ("SELECT stu.student_name FROM student AS stu JOIN student_course AS stuCou \
            ON stu.student_no = stuCou.student_no \
            WHERE stuCou.score < 60 AND stu.grade_no = '{}'".format(grade_no))

    # 用set给数据去重
    return set(cursor.execute(sql).fetchall())


def main():
    db = sqlite3.connect('school.db')
    cursor = db.cursor()

    # 查询出都有哪些同学学习了Python课程，要求查询出同学的姓名、课程名称
    res = get_students_course(cursor, 'Python')
    print('问题1: 查询出都有哪些同学学习了Python课程，要求查询出同学的姓名、课程名称')
    for name, course in res:
        print(name, course)
    print('--'*20)

    # 查询出1年1班，都有哪些同学学习了机器学习课程，要求查询出同学的姓名、课程名称、班级名称、年级名称
    res = get_students_course_class_grade(cursor, '机器学习', 1, 1)
    print('问题2: 查询出1年1班，都有哪些同学学习了机器学习课程，要求查询出同学的姓名、课程名称、班级名称、年级名称')
    for name, course, class_name in res:
        print(name, course, class_name)
    print('--'*20)

    # 哪些同学同时报了Python课程和数据分析课程
    res = course1_and_course2(cursor, 'Python', '数据分析')
    print('问题3: 哪些同学同时报了Python课程和数据分析课程')
    for name in res:
        print(name[0])
    print('--'*20)

    # 查询出数据分析课程，考试分数在60分以上的同学的姓名  分数的筛选支持 >大于  >=大于等于这些符号运算
    res = get_name_by_score(cursor, "数据分析", 60)
    print('问题4: 查询出数据分析课程，考试分数在60分以上的同学的姓名  分数的筛选支持 >大于  >=大于等于这些符号运算')
    for name in res:
        print(name[0])
    print('--'*20)

    # 查询出2年级，所有考试未及格的同学
    res = get_failed(cursor, 2)
    print('问题5: 查询出2年级，所有考试未及格的同学')
    for name in res:
        print(name[0])
    print('--'*20)


if __name__ == '__main__':
    main()
