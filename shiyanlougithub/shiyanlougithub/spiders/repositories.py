# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import RepositoryItem


class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'
    
    @property
    def start_urls(self):
        return ('https://github.com/shiyanlou?page={}&tab=repositories'.format(i) for i in range(1,5))

    def parse(self, response):
        for repos in response.css('li.public'):
            item = RepositoryItem()
            item['name'] = repos.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first('^\s*(\S*)'),
            item['update_time'] = repos.xpath('.//relative-time/@datetime').extract_first()
            repos_url = response.urljoin(repos.xpath('.//a[@itemprop="name codeRepository"]/@href').extract_first())
            request = scrapy.Request(repos_url,callback=self.parse_repos)
            request.meta['item'] = item
            yield request
    
    def parse_repos(self,response):
        item = response.meta['item']
        for num in response.css('ul.numbers-summary li'):
            type_text = num.xpath('.//a/text()').re_first('\n\s*(.*)\n')
            num_text = num.xpath('.//span[@class="num text-emphasized"]/text()').re_first('\n\s*(.*)\n')
            if type_text and num_text:
                num_text = num_text.replace(',','')
                if type_text in ('commit','commits'):
                    item['commits'] = int(num_text)
                elif type_text in ('branch','branches'):
                    item['branches'] = int(num_text)
                elif type_text in ('release','releases'):
                    item['releases'] = int(num_text)
        yield item

