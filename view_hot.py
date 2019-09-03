import logging
import time
from sqlalchemy import create_engine
import pandas
import datetime
import jieba
import heapq


def get_oneday_toutiao_df(date, engine):
    toutiao_df = pandas.read_sql('tb_toutiao_hot', con=engine, index_col='index')
    today_toutiao_df = toutiao_df[toutiao_df.spider_time >= date - datetime.timedelta(days=1)]

    return today_toutiao_df


def get_oneday_df(timestamp, table, engine):
    all_df = pandas.read_sql(table, con=engine, index_col='index')
    today_df = all_df[all_df.start_time >= timestamp - 24 * 3600]

    return today_df


def get_vector_sum(target, corpus):
    vector = list()
    for word in corpus:
        vector.append(1 if word in target else 0)

    return sum(vector)


def select_hot(toutiao_df, weibo_resou_df, bilibili_hotword_df, corpus, max_len):
    # 选取最大的20个，所以选用最小堆
    h = list()

    # 筛选今日头条里的内容
    for i, row in toutiao_df.iterrows():
        item_sum_of_vector = get_vector_sum(list(jieba.cut(row.abstract)), corpus) * 0.65
        if len(h) < max_len:
            heapq.heappush(h, (item_sum_of_vector, row.abstract, '今日头条'))
        elif item_sum_of_vector > h[0][0]:
            heapq.heapreplace(h, (item_sum_of_vector, row.abstract, '今日头条'))

    # 筛选微博热搜的内容
    for i, row in weibo_resou_df.iterrows():
        item_sum_of_vector = get_vector_sum(list(jieba.cut(row.title)), corpus)
        if len(h) < max_len:
            heapq.heappush(h, (item_sum_of_vector, row.title, '微博热搜'))
        elif item_sum_of_vector > h[0][0]:
            heapq.heapreplace(h, (item_sum_of_vector, row.title, '微博热搜'))

    # 筛选哔哩哔哩的内容
    for i, row in bilibili_hotword_df.iterrows():
        item_sum_of_vector = get_vector_sum(list(jieba.cut(row.hot_word)), corpus) * 1.3
        if len(h) < max_len:
            heapq.heappush(h, (item_sum_of_vector, row.hot_word, '哔哩哔哩'))
        elif item_sum_of_vector > h[0][0]:
            heapq.heapreplace(h, (item_sum_of_vector, row.hot_word, '哔哩哔哩'))

    return h


def main():
    logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s - %(message)s')

    engine = create_engine('sqlite:////Users/lawyzheng/Desktop/Code/spider.db')
    now = int(time.time())
    today = datetime.datetime.today()

    # 获取今日头条、微博热搜、哔哩哔哩 最近一天的数据
    toutiao_df = get_oneday_toutiao_df(today, engine)
    weibo_resou_df = get_oneday_df(now, 'tb_weibo_resou', engine)
    bilibili_hotword_df = get_oneday_df(now, 'tb_bilibili_hotword', engine)

    # 将所有数据转化成字符串，用jieba进行切割，建立语料库
    text_toutiao = ''.join(toutiao_df.abstract.to_numpy()) + ''.join(toutiao_df.article_tags.to_numpy())
    text_weibo = ''.join(weibo_resou_df.title.to_numpy())
    text_bilibili_hotword = ''.join(bilibili_hotword_df.hot_word.to_numpy())

    jieba.load_userdict('wordsdict.txt')
    corpus = list(jieba.cut(text_toutiao + text_weibo + text_bilibili_hotword))
    corpus = [word for word in corpus if word.isalnum() and word != '中国']

    # 筛选出最热门的前30条数据
    selected_hot_list = select_hot(toutiao_df, weibo_resou_df, bilibili_hotword_df, corpus, 30)
    rank = 0
    result = ''

    while(selected_hot_list):
        item = heapq.heappop(selected_hot_list)
        result = '%2d  %s  来自:%s\n' % (30-rank, item[1], item[2]) + result
        rank += 1

    print(result)


if __name__ == '__main__':
    main()
