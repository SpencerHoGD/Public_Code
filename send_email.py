'''
先进行计算获得工资列表
再将每个人各自的工资发到各自的邮箱里
'''
import pandas
import datetime
import collections
import smtplib
from email.mime.text import MIMEText
from email.header import Header


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


# 计算每个人的工资
def calc_salary():
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

        # 获取每个人的邮箱
        salary_data['邮箱'].append(row['邮箱'])

    salary_df = pandas.DataFrame(salary_data)
    # salary_df.to_excel('salary.xlsx')

    return salary_df


def send_email(salary_df):
    # 设置user信息
    user_email = '594440572@qq.com'
    user_password = ''
    user_host = 'smtp.qq.com'
    user_port = 465

    # 设置寄件人、邮件主题、邮件内容格式
    sender = '594440572@qq.com'
    subject = '1997-04 工资'
    email_fmt = '''
    <p>1997年4月份工资表<p>
    <table>
        <tr>
            <th>姓名</th>
            <th>当前月薪</th>
            <th>工作日天数</th>
            <th>应出勤天数</th>
            <th>实际出勤天数</th>
            <th>年假天数</th>
            <th>事假天数</th>
            <th>病假天数</th>
            <th>税前工资</th>
        </tr>
        <tr>
            <td>{name}</td>
            <td>{cur_salary}</td>
            <td>{whole_days}</td>
            <td>{should_days}</td>
            <td>{work_days}</td>
            <td>{vac_days}</td>
            <td>{things_days}</td>
            <td>{ill_days}</td>
            <td>{salary}</td>
        </tr>
    </table>
    '''

    # 获取邮箱的server,并登录
    qqmail_server = smtplib.SMTP_SSL(user_host, user_port)
    qqmail_server.login(user_email, user_password)

    # 遍历给每个人各自发邮件
    for i, row in salary_df.iterrows():
        # 获取邮箱
        receiver = row['邮箱']
        # 格式化邮件内容
        email_text = email_fmt.format(name=row['姓名'], cur_salary=row['当前月薪'], whole_days=row['工作日天数'],
                                      should_days=row['应出勤天数'], work_days=row['实际出勤天数'], vac_days=row['年假天数'],
                                      things_days=row['事假天数'], ill_days=row['病假天数'], salary=row['应发税前工资'])
        message = MIMEText(email_text, 'html', 'utf-8')
        message['From'] = Header('LawyZheng')
        message['To'] = Header(row['姓名'])
        message['Subject'] = Header(subject, 'utf-8')

        # 发送邮件内容
        qqmail_server.sendmail(sender, receiver, message.as_string())
        print('邮件发送成功')

    # 退出邮箱服务
    qqmail_server.quit()


def main():
    # 计算工资,获取结果
    salary_df = calc_salary()

    # 发送邮件
    try:
        send_email(salary_df)
    except smtplib.SMTPException as e:
        print(e)
        print('邮件发送失败')


if __name__ == '__main__':
    main()
