import requests
from sqlalchemy import create_engine
import pandas
import time
import logging


def set_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    log_path = '/Users/lawyzheng/Library/LOgs/bilibili_hotwords.log'
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.INFO)

    fmt = '%(asctime)s - %(levelname)s - %(message)s'
    datefmt = '%Y/%m/%d %H:%M:%S'
    formatter = logging.Formatter(fmt, datefmt)
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger


def get_hot_words_list(url):
    hot_words = list()

    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; '
                      'Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/76.0.3809.132 '
                      'Mobile Safari/537.36'
    }

    resp = requests.get(url, headers=headers)
    hot_words_dict = resp.json()
    for each in hot_words_dict.get('list'):
        hot_words.append(each.get('keyword'))

    return hot_words


def update_new_dataframe(words_list, all_df):
    now = int(time.time())
    today_on_hot_df = all_df[all_df.start_time >= now - 24 * 3600]
    all_df['on_hot'] = False

    for each_word in words_list:
        # 如果不在榜单上
        if today_on_hot_df[today_on_hot_df.hot_word == each_word].index.empty:
            data = {
                'hot_word': [each_word],
                'start_time': [now],
                'end_time': [now],
                'lasting_time': [0],
                'on_hot': [True]
            }

            new_item = pandas.DataFrame(data)
            all_df = pandas.concat([all_df, new_item], ignore_index=True)

        # 如果正在榜单上
        else:
            index = today_on_hot_df[today_on_hot_df.hot_word == each_word].index[0]
            all_df.at[index, 'end_time'] = now
            all_df.at[index, 'lasting_time'] = now - all_df.at[index, 'start_time']
            all_df.at[index, 'on_hot'] = True

    return all_df


def main(logger):
    pandas.set_option('display.max_rows', None)
    url = 'https://s.search.bilibili.com/main/hotword'

    logger.info('开始启动程序，正在获取数据。')
    hot_words = get_hot_words_list(url)

    engine = create_engine('sqlite:////Users/lawyzheng/Desktop/Code/spider.db')
    all_df = pandas.read_sql('tb_bilibili_hotword', con=engine, index_col='index')

    logger.info('数据获取成功，正在进行整合。')
    new_df = update_new_dataframe(hot_words, all_df)

    logger.info('正在把数据录入数据库中。')
    new_df.to_sql('tb_bilibili_hotword', con=engine, index=True, if_exists='replace')


if __name__ == '__main__':
    logger = set_logger()
    try:
        main(logger)
        logger.info('数据输入成功，程序退出。')
    except Exception as e:
        logger.error('发生错误。错误原因如下:', exc_info=True)