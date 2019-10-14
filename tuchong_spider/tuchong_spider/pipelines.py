# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import ImagesPipeline
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# class TuchongSpiderPipeline(ImagesPipeline):

#     def get_media_requests(self, item, info):
#         for image_url in item['image_urls']:
#             yield scrapy.Request(image_url)

#     def item_completed(self, results, item, info):
#         file_paths = [x['path'] for ok, x in results if ok]
#         if not file_paths:
#             raise DropItem("Item contains no files")
#         item['file_paths'] = file_paths
#         return item
