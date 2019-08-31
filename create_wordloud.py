'''
通过sqlite引擎，读取数据库数据
'''
import jieba
import pandas
import wordcloud
import json
from sqlalchemy import create_engine

path = '/Users/lawyzheng/Desktop/Code/'

# 连接数据库
engine = create_engine('sqlite:///' + path + 'spider.db')
df = pandas.read_sql('tb_toutiao_hot', con=engine, index_col='index')

# 获取文章abstract数据
abstract_list = df.abstract.to_list()
abstract_list = list(map(jieba.cut, abstract_list))
abstract_list = list(map(list, abstract_list))
abstract = " ".join([' '.join(l) for l in abstract_list])
# abstract = "\n".join(abstract_list)

# 获取文章的tags数据
tags_list = df.article_tags.to_list()
tags = ' '.join(tags_list)

# 清洗数据
with open('/Users/lawyzheng/Desktop/Code/Public_Code/stopwords.txt', 'r') as f:
    stopwords = f.read()

stopwords = set(stopwords.split('\n'))
wc = wordcloud.WordCloud(width=800, height=600, font_path='msyh.ttf', stopwords=stopwords)

wc.generate(abstract + tags)
image = wc.to_image()
image.show()
