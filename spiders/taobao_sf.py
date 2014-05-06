__author__ = 'LanChorY'
# -*- coding: < utf-8 > -*-
from scrapy.http import Request  
from scrapy.spider import Spider 
from scrapy.selector import Selector 
 
from scrapy.item import Item, Field  
 
class TaobaoItem(Item):
    title = Field()
    link = Field()
    price = Field()
 
class TaobaoSpider(Spider):
    name = "tb-sf"
    allowed_domains = ["taobao.com"]
    start_urls = [
        "http://s.paimai.taobao.com/list.htm?stype=4&ist=1&city=%BA%BC%D6%DD&_pc_client=1&sorder=1"
    ]
 
    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//li[@class="pics-li"]')
        for site in sites:
            item= TaobaoItem()
            item['title'] = site.xpath('div/p[@class="p-info-title"]/a/text()').extract()
            item['link'] = site.xpath('div/p[@class="p-info-title"]/a/@href').extract()
            item['price'] = site.xpath('div/p[@class="p-info-attr"]/strong/text()').extract()
            yield item
        try:
            next_url=sel.xpath('//li[@class="next-page"]/a/@href').extract()[0]
        except:
               raise StopIteration
        seq = Request(next_url,callback=self.parse)
        yield seq

