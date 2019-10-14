import sqlite3
# import pandas
# from sqlalchemy import create_engine


def get_scores(cursor, course):
    sql = ("SELECT stuCou.score, stu.student_name, cls.class_name FROM \
            student_course AS stuCou JOIN student AS stu JOIN class AS cls JOIN course AS cou \
            ON stuCou.course_no = cou.course_no AND stuCou.student_no = stu.student_no AND (stu.class_no = cls.class_no AND stu.grade_no = cls.grade_no) \
            WHERE cou.course_name = '{}' ORDER BY stuCou.score DESC".format(course))

    return cursor.execute(sql)


def get_student_num(cursor):
    sql = ("SELECT cls.class_name, count(stu.student_no) FROM \
            class AS cls JOIN student AS stu ON (cls.grade_no = stu.grade_no AND cls.class_no = stu.class_no) \
            GROUP BY cls.grade_no, cls.class_no ")

    return cursor.execute(sql)


def get_max(cursor):
    sql = ("SELECT cou.course_name, stu.student_name, max(stuCou.score) FROM \
            course AS cou JOIN student AS stu JOIN student_course AS stuCou \
            ON cou.course_no = stuCou.course_no AND stu.student_no = stuCou.student_no \
            GROUP BY cou.course_no")

    return cursor.execute(sql)


def get_min(cursor):
    sql = ("SELECT cou.course_name, stu.student_name, min(stuCou.score) FROM \
            course AS cou JOIN student AS stu JOIN student_course AS stuCou \
            ON cou.course_no = stuCou.course_no AND stu.student_no = stuCou.student_no \
            GROUP BY cou.course_no")

    return cursor.execute(sql)


def get_std(cursor):
    '''
    sqlite3 没有提供内置的 std函数 和 sqrt函数，就通过方差来直接筛选了。
    筛选结果我用pandas对比了一下，虽然最终结果是一样的。但具体的数值好像还是有差异。
    不知道是我选法的问题，还是数据精度的问题。
    '''
    sql = ("SELECT min(result), course FROM \
            (SELECT avg((stuCou.score - sub.mean) * (stuCou.score - sub.mean)) AS result, cou.course_name AS course \
            FROM student_course AS stuCou JOIN course AS cou ON stuCou.course_no = cou.course_no ,\
            (SELECT avg(score) AS mean FROM student_course) AS sub GROUP BY cou.course_no)")

    return cursor.execute(sql)

    # con = create_engine('sqlite:///school.db')
    # df = pandas.read_sql('student_course', con=con, index_col='id')
    # df = df.groupby('course_no').score.var()
    # print(df)


def main():
    db =sqlite3.connect('school.db')
    cursor = db.cursor()

    # 查询出所有学习人工智能基础课程的同学分数、姓名、班级名字、年级名字，然后按照分数从大到小排列
    res = get_scores(cursor, '人工智能基础')
    print('1: 查询出所有学习人工智能基础课程的同学分数、姓名、班级名字、年级名字，然后按照分数从大到小排列')
    for score, name, class_ in res:
        print(score, name, class_)
    print("--"*20)

    # 查询出每个年级的每个班分别有多少学生
    res = get_student_num(cursor)
    print('2: 查询出每个年级的每个班分别有多少学生')
    for class_, num in res:
        print(class_, num)
    print("--"*20)

    # 查询出每一个科目最高(max)得分的学生是谁
    res = get_max(cursor)
    print('3: 查询出每一个科目最高(max)得分的学生是谁')
    for course, name, score in res:
        print(course, name, score)
    print("--"*20)

    # 查询出每一个科目最低(min)得分的学生是谁
    res = get_min(cursor)
    print('4: 查询出每一个科目最低(min)得分的学生是谁')
    for course, name, score in res:
        print(course, name, score)
    print("--"*20)

    # 计算该校学生哪一个科目的成绩最稳定，就是计算成绩的标准差最小。标准差可以数据分析中非常常用且重要的指标哦。
    res = get_std(cursor)
    print('5: 计算该校学生哪一个科目的成绩最稳定，就是计算成绩的标准差最小。标准差可以数据分析中非常常用且重要的指标哦。')
    for var, course in res:
        print(var, course)
    print("--"*20)


if __name__ == "__main__":
    main()