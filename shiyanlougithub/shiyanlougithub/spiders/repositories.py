# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import RepositoryItem


class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'
    allowed_domains = ['https://github.com']
    start_urls = ['']
    
    @property
    def start_urls(self):
        return ('https://github.com/shiyanlou?page={}&tab=repositories'.format(i) for i in range(1,5))

    def parse(self, response):
        for repos in response.css('li.public'):
            item = RepositoryItem({
                'name':repos.xpath('.//a[@itmprop="name codeRepository"]/text()').re_first('^\s*(\S*)'),
                'update_time':repos.xpath('.//relative-time/@datetime').extract_first()
                })
            yield item

