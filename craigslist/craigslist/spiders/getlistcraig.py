import scrapy
from scrapy import Request

class GetlistcraigSpider(scrapy.Spider):
    name = 'getlistcraig'
    allowed_domains = ['seattle.craigslist.org/search/est/cta']
    start_urls = ['http://seattle.craigslist.org/search/est/cta/']

    def parse(self, response):
        lists = response.xpath('//div[@class="content"]/ul/li')

        for l in lists:
            #title = l.xpath('/li[@class="result-row"]/div[@class="result-info"]/h3[@class="result-heading"]/a/text()').extract_first()
            title = l.xpath('div/h3/a[@class="result-title hdrlnk"]/text()').extract_first()
            price = l.xpath('div/span/span[@class="result-price"]/text()').extract_first()
            hood = l.xpath('div/span/span[@class="result-hood"]/text()').extract_first("")[2:-1]
            rel_url =l.xpath('div/h3/a/@href').extract_first()
            abs_url = response.urljoin(rel_url)
            yield Request(abs_url, callback = self.parse_page, dont_filter = True,
                          meta = {'title': title,'price': price,'hood':hood,'URL':abs_url})
            
        rel_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        if rel_next_url!= '':
            abs_next_url = response.urljoin('?'+rel_next_url.split('?')[-1])
        else:
            print(rel_next_url)
            return                                
            
        yield Request(abs_next_url, callback=self.parse, dont_filter=True)
        
    
    def parse_page(self, response):
        ad_descrption = response.xpath('//*[@id="postingbody"]/text()').extract()
        title = response.meta['title'] 
        price = response.meta.get('price') #different syntax using get function
        hood = response.meta['hood']
        URL = response.meta['URL']
        
        yield {'title':title,'price':price, 'hood': hood,'URL':URL, 'Description': ad_descrption}