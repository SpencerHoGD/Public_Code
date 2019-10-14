# -*- coding: utf-8 -*-
from urllib.parse import urlencode
import json
import scrapy
from tuchong_spider.items import TuchongSpiderItem


class TuchongSpider(scrapy.Spider):
    name = 'tuchong'

    def start_requests(self):
        url = 'https://tuchong.com/rest/search/posts'

        for page in range(1, 2):
            params = {
                    "query": "私房",
                    "count": 20,
                    "page": page
                 }

            new_url = url + '?' + urlencode(params)
            yield scrapy.Request(new_url, self.parse)

    def parse(self, response):
        json_data = json.loads(response.text)

        # 遍历每个图集
        for each_images in json_data['data']['post_list']:
            # 提取出图集里每张图片的尺寸
            image_urls = list()
            for each_image in each_images['images']:
                url = each_image['source']['ft640']
                url = url.replace('ft640', 'f')
                image_urls.append(url)

            item = TuchongSpiderItem()
            item['image_urls'] = image_urls

            yield item
