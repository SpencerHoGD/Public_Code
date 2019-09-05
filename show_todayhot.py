from sqlalchemy import create_engine
import pandas
import jieba
import heapq
import time


def get_vector_sum(target, corpus):
    vector_sum = 0
    for each_word in corpus:
        if each_word in target:
            vector_sum += corpus[each_word]

    return vector_sum


def get_top_30(df, corpus, max_len=30):
    h = list()

    for i, row in df.iterrows():
        vector_sum = get_vector_sum(row['content'], corpus)
        # vector_sum /= len(row['content'])
        if row['source'] in ['微博', '百度']:
            vector_sum *= 2
        if len(h) < max_len:
            heapq.heappush(h, (vector_sum, i))
        elif vector_sum > h[0][0]:
            heapq.heapreplace(h, (vector_sum, i))

    return h


def main():
    now = int(time.time())
    engine = create_engine('sqlite:////Users/lawyzheng/Desktop/Code/spider.db')
    df = pandas.read_sql('tb_today_hot', con=engine, index_col='index')
    df = df[df.end_time >= (now - 24 * 3600)]

    corpus = list(jieba.cut(''.join(df.content.to_numpy())))
    # ignore_list= list()
    ignore_list = ['的', '你', '我', '了', '又', '个', '什么', '吗', '为什么']
    corpus = [word for word in corpus if word.isalpha() and word not in ignore_list]

    word_count = dict()
    for each_word in corpus:
        word_count[each_word] = word_count.get(each_word, 0) + 1

    clean_corpus = dict()
    for each_word in word_count:
        if 1 < word_count[each_word] < 30:
            clean_corpus[each_word] = word_count[each_word]

    # print(clean_d)

    num = 40
    top = get_top_30(df, clean_corpus, max_len=num)
    result = ''
    i = 0
    while top:
        each = heapq.heappop(top)
        result = "%2d %s \t来自:%s\n" % (num - i, df.at[each[1], 'content'], df.at[each[1], 'source']) + result
        i += 1

    print(result)


if __name__ == '__main__':
    main()
