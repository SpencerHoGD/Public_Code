'''
通过sqlite引擎，读取数据库数据
'''

import pandas
import wordcloud
import json
from sqlalchemy import create_engine

path = '/Users/lawyzheng/Desktop/greedyai_learning/'

#连接数据库
engine = create_engine('sqlite:///' + path + 'toutiao_hot.db')
df = pandas.read_sql('tb_toutiao_hot', con=engine, index_col='index')

#将json数据转化成Python数据
for col in df.columns:
	if df[col].dtype == 'object':
		df[col] = list(map(json.loads, df[col]))

# 获取文章abstract数据
abstract_list = df.abstract.to_list()
for index, each in enumerate(abstract_list):
	if not each:
		print(index)
abstract = "\n".join(abstract_list)

# 获取文章的tags数据
tags_list = df.article_tags.to_list()
tags = '\n'.join([' '.join(l) for l in tags_list])

#清洗数据
stopwords = {'人生第一份工作', '胜利退出演艺圈', '我的第一部5G手机', '澎湃新闻', '4月吃什么', 
             '广州恒大淘宝足球俱乐部', '跳槽那些事儿', '越投入越精彩', '不完美妈妈', '原汁原味的德系SUV', '新闻',
             '头号大赢家', '理财大赛第二季','我在宫里做厨师'}
wc = wordcloud.WordCloud(width=800, height=600, font_path='msyh.ttf', stopwords=stopwords)

wc.generate(abstract + tags)
image = wc.to_image()
image.show()