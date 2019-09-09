import requests
from bs4 import BeautifulSoup
import time
import pandas
import re
from sqlalchemy import create_engine
import logging
import xlsxwriter
import sys


def set_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    log_path = '/Users/lawyzheng/Library/Logs/today_hot.log'
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.INFO)

    fmt = '%(asctime)s - %(levelname)s - %(message)s'
    datefmt = '%Y/%m/%d %H:%M:%S'
    formatter = logging.Formatter(fmt, datefmt)
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger


def get_html(url):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko)'}
    resp = requests.get(url, headers=headers)
    return resp.text


def get_nodes(html):
    soup = BeautifulSoup(html, 'html.parser')
    nodes = soup.find_all('div', class_='cc-cd')
    return nodes


def get_each_node_data(df, nodes):
    now = int(time.time())

    # 遍历每个榜
    for node in nodes:
        # 获得榜单的来源
        source = node.find('div', class_='cc-cd-lb').text.strip()
        # 若是不需要的榜单，则跳过
        if source in ['什么值得买', '淘宝', '拼多多', '武大珞珈山水', '复旦大学日月光华', '北大未名']:
            continue

        messages = node.find('div', class_='cc-cd-cb-l nano-content').find_all('a')
        for message in messages:
            content = message.find('span', class_='t').text.strip()
            # 如果是来自微信的消息，就去掉 「」里面的内容
            if source == '微信':
                reg = '「.+?」(.+)'
                content = re.findall(reg, content)[0]

            # 如果不在数据库中，就添加新的数据
            if df.empty or df[df.content == content].empty:

                data = {
                    'content': [content],
                    'url': [message['href']],
                    'source': [source],
                    'start_time': [now],
                    'end_time': [now]
                }

                item = pandas.DataFrame(data)
                df = pandas.concat([df, item], ignore_index=True)

            # 如果已经在数据库中，则更新相关信息
            else:
                index = df[df.content == content].index[0]
                df.at[index, 'end_time'] = now

    return df


def main(logger):
    url = 'https://tophub.today'
    engine = create_engine('sqlite:////Users/lawyzheng/Desktop/Code/spider.db')

    logger.info('开始运行程序，正在获取数据。')
    try:
        html = get_html(url)
    except Exception as e:
        logger.info('网络请求失败，失败原因: %s' % e)
        sys.exit(0)

    logger.info('数据获取成功，正在进行数据清洗整合。')
    nodes = get_nodes(html)
    df = pandas.read_sql('tb_today_hot', con=engine, index_col='index')
    old_length = len(df)
    df = get_each_node_data(df, nodes)
    new_length = len(df)
    logger.info('增加数据 %d 条。' % (new_length - old_length))

    logger.info('数据整合完毕，正在录入数据库。')
    df.to_sql('tb_today_hot', con=engine, index=True, if_exists='replace')

    xlsx_content = pandas.ExcelWriter('/Users/lawyzheng/Desktop/Code/today_hot.xlsx', engine='xlsxwriter')
    df.to_excel(xlsx_content, sheet_name='Sheet1')
    logger.info('数据录入成功。程序退出。')


if __name__ == '__main__':
    try:
        logger = set_logger()
        main(logger)
    except Exception as e:
        logger.error('发生错误。错误原因如下:', exc_info=True)
