__author__ = 'LanChorY'
from scrapy.http import Request,FormRequest
from scrapy.spider import Spider
from scrapy.selector import Selector


from scrapy.item import Item, Field

class zhaopinItem(Item):
    times = Field()

class zhaopinSpider(Spider):
    name = "zhaopin"
    allowed_domains = ["zhaopin.com"]
    start_urls = [
        "http://my.zhaopin.com/myzhaopin/resume_index.asp"
    ]


    def __init__(self, username='填入用户名', password='填入密码', *args, **kwargs):
        super(zhaopinSpider, self).__init__(*args, **kwargs)
        self.http_user = username
        self.http_pass = password
        #login form
        self.formdata = {'loginname':self.http_user,
                        'password':self.http_pass,
                        }
        self.headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Encoding':'gzip,deflate,sdch',
                        'Accept-Language':'zh-CN,zh;q=0.8',
                        'Cache-Control':'max-age=0',
                        'Connection':'keep-alive',
                        'Content-Type':'application/x-www-form-urlencoded'
                        }


    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield FormRequest(url, meta = {'cookiejar': i},
                                headers = self.headers,
                                callback = self.login)#jump to login page

    def _log_page(self, response, filename):
        with open(filename, 'w') as f:
            f.write("%s\n%s\n%s\n" % (response.url, response.headers, response.body))
    def login(self, response):
        self._log_page(response, 'zhaopin_login.html')
        return [FormRequest.from_response(response,
                            formdata = self.formdata,
                            headers = self.headers,
                            meta = {'cookiejar':response.meta['cookiejar']},
                            callback = self.parse_item,
                            dont_filter=True)]#success login

    def parse_item(self, response):
        self._log_page(response, 'after_login.html')
        sel = Selector(response)
        sites = sel.xpath('//div[@class="intro"]')
        items=[]
        for site in sites:
            item= zhaopinItem()
            item['times'] = site.xpath('a/em/text()').extract()
            return item
