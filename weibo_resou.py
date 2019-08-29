import requests
import time
import datetime
import pandas
import random
import logging
from sqlalchemy import create_engine

def set_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    #文件输出
    log_path = '/Users/lawyzheng/Desktop/Code/Public_Code/weibo_resou.log'
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.WARNING)

    #Stream输出
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)

    #设置format
    fmt = '%(asctime)s - %(levelname)s - %(message)s'
    datefmt = '%Y/%m/%d %H:%M:%S'
    formatter = logging.Formatter(fmt, datefmt)

    fh.setFormatter(formatter)
    sh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(sh)

    return logger


def get_browsers():
    url = 'https://fake-useragent.herokuapp.com/browsers/0.1.11'
    resp = requests.get(url)
    browsers = resp.json()['browsers']
    return browsers


def get_one_browser(browsers_dict):
    browsers_types = ['chrome', 'opera',
                      'firefox', 'internetexplorer', 'safari']
    browser_name = random.choice(browsers_types)
    return browsers_dict[browser_name][random.randint(0, len(browsers_dict[browser_name])-1)]


def get_json_data(timestamp):
    url = 'https://m.weibo.cn/api/container/getIndex'

    headers = {
                'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
                'Accept' : 'application/json, text/plain, */*',
                'MWeibo-Pwa' : '1',
                'Sec-Fetch-Mode' : 'cors',
                'X-Requested-With' : 'XMLHttpRequest',
                'Referer' : 'https://m.weibo.cn/p/index?'\
                        'containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&'\
                        'title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C&'\
                        'extparam=pos%3D0_0%26mi_cid%3D100103%26cate%3D10103%26filter_type%3Drealtimehot%26c_type%3D30%26display_time%3D{}&'\
                        'luicode=10000011&lfid=231583'.format(timestamp)
    }

    params = {
            'containerid' : '106003type=25&t=3&disable_hot=1&filter_type=realtimehot',
            'title' : '微博热搜',
            'extparam' : 'pos=0_0&mi_cid=100103&cate=10103&filter_type=realtimehot&c_type=30&display_time=%d' % timestamp,
            'luicode' : '10000011',
            'lfid' : '231583'
    }

    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()

    return data['data']['cards'][0]['card_group']


def format_data(dataframe, targets, timestamp):
    for target  in targets:
        #不属于热搜榜
        if not target.get('desc_extr'):
            continue

        #如果dataframe为空，直接添加数据
        if dataframe.empty:
            data = {
                "title" : target['desc'],
                "hot_index" : int(target['desc_extr']),
                "showed_times" : 1,
                "start_time" : timestamp,
                "end_time" : timestamp
            }

            item = pandas.DataFrame(data, index=[0])
            dataframe = pandas.concat([dataframe, item], ignore_index=True)

        else:
            item = dataframe[dataframe.title == target['desc']]
            #如果不在dataframe中，则添加该数据
            if item.empty:
                data = {
                    "title" : target['desc'],
                    "hot_index" : int(target['desc_extr']),
                    "showed_times" : 1,
                    "start_time" : timestamp,
                    "end_time" : timestamp
                }

                item = pandas.DataFrame(data, index=[0])
                dataframe = pandas.concat([dataframe, item], ignore_index=True)

            #如果在dataframe中
            else:
                index = item.index[0]
                #更新hot_index
                dataframe.at[index, 'hot_index'] = int(target['desc_extr']) if dataframe.at[index, 'hot_index'] < int(target['desc_extr']) else dataframe.at[index, 'hot_index']
                #更新end_time
                dataframe.at[index, 'end_time'] = timestamp
                #更新showed_time
                dataframe.at[index, 'showed_times'] += 1

    return dataframe


def main(logger):
    #创建数据库连接，读取数据库
    engine = create_engine('sqlite:////Users/lawyzheng/Desktop/Code/Public_Code/weibo_resou.db')
    df = pandas.read_sql('tb_weibo_resou', con=engine, index_col='index')
    logger.debug('连接数据库成功。')

    #获取时间和时间戳
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=3)

    today_timestamp = int(time.mktime(today.timetuple()))
    yesterday_timestamp = int(time.mktime(yesterday.timetuple()))


    #获取热搜
    logger.debug('正在获取热搜榜。')
    targets = get_json_data(int(time.time()))

    #整理数据
    logger.debug('获取完成，正在进行数据整合。')
    df = format_data(df, targets, yesterday_timestamp)
    #print(df)

    #获取每分钟的热搜
    # for timestamp in range(yesterday_timestamp, today_timestamp, 60):
    #     targets = get_json_data(timestamp)
    #     df = format_data(df, targets, timestamp)

    #     print(df)
    #     finished = (timestamp - yesterday_timestamp + 60) / (today_timestamp - yesterday_timestamp)
    #     print('已完成 %.2f %% 。' % (finished * 100))

    #录入数据库
    logger.debug('数据整合完成，正在录入数据库。')
    df.to_sql('tb_weibo_resou', con=engine, index=True, if_exists='replace')
    logger.debug('录入数据库成功，退出程序。')


if __name__ == '__main__':
    logger = set_logger()
    try:
        main(logger)
    except Exception as e:
        logger.error('发生错误。错误信息如下:', exc_info=True)