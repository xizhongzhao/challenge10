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
            item = RepositoryItem()
            item['name'] = repos.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first('^\s*(\S*)'),
            item['update_time'] = repos.xpath('.//relative-time/@datetime').extract_first()
            repos_url = response.urljoin(repos.xpath('.//a[@itemprop="name codeRepository"]/@href').extract_first())
            request = scrapy.Request(repos_url,callback=self.parse_repos)
            request.meta['item'] = item
            yield request
    
    def parse_repos(self,response):
        item = response.meta['item']
        _span_list = response.xpath('//span[@class="num text-emphasized"]/text()').re('^\s*(\S*)\s*')
        item['commits'] = _span_list[0]
        item['branches'] = _span_list[1]
        item['releases'] = _span_list[2]
        yield item

