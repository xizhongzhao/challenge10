# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import RepositoryItem


class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'
    allowed_domains = ['https://github.com']
    
    @property
    def start_urls(self):
        return ('https://github.com/shiyanlou?page={}&tab=repositories'.format(i) for i in range(1,5))

    def parse(self, response):
        for repos in response.css('li.public'):
            item = RepositoryItem()
            item['name'] = repos.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first('^\s*(\S*)'),
            item['update_time'] = repos.xpath('.//relative-time/@datetime').extract_first()
            repos_url = response.urljoin(repos.xpath('.//h3/a[@itemprop="name codeRepository"]/@href').extract_first())
            request = scrapy.Request(repos_url,callback=self.parse_repos)
            request.meta['item'] = item
            yield request
    
    def parse_repos(self,response):
        item = response.meta['item']
        for num in response.css('ul.numbers-summary li'):
            type_text = num.xpath('.//a/text()').re_first('\s*(.*)\s*')
            num_text = num.xpath('.//span[@class="num text-emphasized"]/text()').re_first('\s*(.*)\s*')
            if type_text and num_text:
                if type_text in ('commit','commits'):
                    item['commits'] = num_text
                elif type_text in ('branch','branches'):
                    item['brances'] = num_text
                elif type_text in ('release','releases'):
                    item['releases'] = num_text
        yield item

