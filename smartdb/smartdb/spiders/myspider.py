import scrapy
from smartdb.items import SmartdbItem
import sys


class MySpider(scrapy.Spider):
    """
    name:scrapy唯一定位实例的属性，必须唯一
    allowed_domains：允许爬取的域名列表，不设置表示允许爬取所有
    start_urls：起始爬取列表
    start_requests：它就是从start_urls中读取链接，然后使用make_requests_from_url生成Request，
                    这就意味我们可以在start_requests方法中根据我们自己的需求往start_urls中写入
                    我们自定义的规律的链接
    parse：回调函数，处理response并返回处理后的数据和需要跟进的url
    log：打印日志信息
    closed：关闭spider
    """
    # 设置name
    name = "spidersmartdb"
    # 设定域名
    allowed_domains = ["smartdb.bioinf.med.uni-goettingen.de","www.baidu.com"]
    # http://smartdb.bioinf.med.uni-goettingen.de/cgi-bin/SMARtDB/smar.cgi
    # 填写爬取地址
    start_urls = [
        "http://smartdb.bioinf.med.uni-goettingen.de/cgi-bin/SMARtDB/smar.cgi",
        "http://smartdb.bioinf.med.uni-goettingen.de/cgi-bin/SMARtDB/",
    ]

    # 编写爬取方法
    def parse(self, response):
        i = 0
        for line in response.xpath('/html/body/table/tr'):
            i += 1
            # print('line:',type(line))
            if i >=2:
                # 初始化item对象保存爬取的信息
                item = SmartdbItem()
                # 这部分是爬取部分，使用xpath的方式选择信息，具体方法根据网页结构而定
                item['accession_number'] = line.xpath(
                    './td[1]/font/a/text()').extract()
                item['name'] = line.xpath(
                    './td[2]/font/text()').extract()
                item['species'] = line.xpath(
                    './td[3]/font/text()').extract()
                item['url'] = line.xpath(
                    './td[1]/font/a/@href').extract()
                request = scrapy.Request(self.start_urls[1]  + item['url'][0], callback=self.parse_page2)
                request.meta['item'] = item
                # yield item
                yield request


    def parse_page2(self, response):
        item = response.meta['item']
        result = response.xpath('//pre')
        item_1 = SmartdbItem()
        sq_data = ''
        na_data = ''
        tmp_sq = ''
        for i in range(1,100):
            tmp_sq = result.xpath("./a[%s]/text()"%(i)).extract()

            tmp_na = result.xpath("./text()[%s]" % (i)).extract()
            tmp_na_next = result.xpath("./text()[%s]" % (i+1)).extract()
            if tmp_sq:
                # print('tmp_sq:', tmp_sq[0])
                # print('tmp_na:', tmp_na[0])
                # print('i:', i)
                if tmp_sq[0] == 'SQ':
                    sq_data += str(tmp_na_next[0]).strip().split('\n')[0]
                if tmp_sq[0] == 'NA':
                    na_data = tmp_na_next[0]

        # print('sq_data:',sq_data)
        # print('na_data:',na_data)
        item_1['accession_number'] = str(item['accession_number'][0])
        item_1['name'] = str(item['name'][0])
        item_1['species'] = str(item['species'][0])
        item_1['url']= str(self.start_urls[1] + item['url'][0])
        item_1['SQ'] = sq_data
        item_1['NA'] = na_data.split('\nXX\n')[0].strip()
        yield item_1