'''
有人貌似好像周末也来上班了，造成了实际出勤天数大于应出勤天数。
但我没给他周末加班额外加工资，毕竟本来就是带薪的假期！
新建了一个dataframe，之前用 dataframe.at 来修改值似乎效率很低
'''
import pandas
import datetime
import collections


# 计算应该出勤天数
def calc_workdays(start_working_date, end_working_date):
    # 含双休日天数
    whole_days = (end_working_date - start_working_date).days
    # 完整的双休日的天数
    weekend = whole_days // 7 * 2
    # 获取开始那天的星期，并检验剩下的日子里是否含有双休日
    start_weekday = start_working_date.weekday() + 1
    weekend += min(max(whole_days % 7 + start_weekday - 1 - 5, 0), 2)  # 先取最大查看是否有周末，再取最小防止超过2天

    return whole_days - weekend, whole_days


def main():
    # 读取excel
    data = pandas.read_excel('data.xlsx')
    salary_data = collections.defaultdict(list)

    # 获取开始和结束日期
    today = datetime.datetime.strptime('1997-05-01', '%Y-%m-%d')
    previous_month_day = datetime.datetime.strptime('1997-04-01', '%Y-%m-%d')

    # 计算应出勤天数和总天数
    should_work_days, whole_days = calc_workdays(previous_month_day, today)

    # 遍历每个人的情况
    for i, row in data.iterrows():
        # 获取姓名信息
        salary_data['姓名'].append(row['姓名'])

        # 获取入职时间
        # print(row['入职时间'].strftime('%Y/%m/%d'))
        salary_data['入职时间'].append(row['入职时间'].strftime('%Y/%m/%d'))

        # 获取当前月薪
        salary_data['当前月薪'].append(row['当前月薪'])

        # 计算日新
        wage = row['当前月薪'] / whole_days
        salary_data['日薪'].append(wage)

        # 计算出勤天数
        if row['入职时间'] > previous_month_day:
            should_work_days_i, whole_days_i = calc_workdays(row['入职时间'], today)
        else:
            should_work_days_i, whole_days_i = should_work_days, whole_days

        # 计算工资天数
        salary_data['工作日天数'].append(whole_days_i)

        # 应出勤天数
        salary_data['应出勤天数'].append(should_work_days_i)

        # 获取实际出勤天数
        salary_data['实际出勤天数'].append(row['实际出勤天数'])

        # 获取年假天数
        salary_data['年假天数'].append(row['年假天数'])

        # 计算事假天数 : 应出勤天数 - 实际出勤天数 - 年假天数 - 病假天数
        no_salary_days = should_work_days_i - row['实际出勤天数'] - row['年假天数'] - row['病假天数']
        salary_data['事假天数'].append(max(0, no_salary_days))

        # 获取病假天数
        salary_data['病假天数'].append(row['病假天数'])

        # 计算税前应发工资 : 工作日天数 / 该月总天数 * 总工资 -（ 事假天数 + 病假天数 * 1.5 ）* 日薪
        salary_data['应发税前工资'].append((whole_days_i / whole_days * row['当前月薪'] -
                                          (no_salary_days + 1.5 * row['病假天数']) * wage))

    salary_df = pandas.DataFrame(salary_data)
    salary_df.to_excel('salary.xlsx')


if __name__ == '__main__':
    main()
