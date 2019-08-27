import pandas
import wordcloud
import os

path = '/Users/lawyzheng/Desktop/greedyai_learning'
json_list = [path + '/' + f for f in os.listdir(path) if f.endswith('.json')]
df_list = list(map(pandas.read_json, json_list))

df = pandas.concat(df_list, ignore_index=True)
df.drop_duplicates('item_id', keep='first', inplace=True)

# 获取文章abstract数据
abstract_list = df.abstract.to_list()
abstract = "\n".join(abstract_list)

# 获取文章的tags数据
tags_list = df.article_tags.to_list()
tags = '\n'.join([' '.join(l) for l in tags_list])

#清洗数据
stopwords = {'人生第一份工作', '胜利退出演艺圈', '我的第一部5G手机',
             '广州恒大淘宝足球俱乐部', '跳槽那些事儿', '越投入越精彩', '不完美妈妈', '原汁原味的德系SUV', '新闻'}
wc = wordcloud.WordCloud(width=800, height=600, font_path='msyh.ttf', stopwords=stopwords)

wc.generate(abstract + tags)
image = wc.to_image()
image.show()