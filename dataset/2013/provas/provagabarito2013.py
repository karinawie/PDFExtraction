import scrapy
from scrapy.selector import Selector

class EnadeSpiderSpider(scrapy.Spider):
    name = 'provagabaritoanos_spider'
    start_urls = ['http://inep.gov.br/web/guest/educacao-superior/enade/provas-e-gabaritos']

    def parse(self,response):
        base_url = 'http://inep.gov.br/web/guest/educacao-superior/enade/provas-e-gabaritos'
        #session_urls = response.xpath('//*[@class="filter__year"]/option[6]').extract() 
        session_urls = response.xpath('//*[@class="filter__year"]/option/@value').extract()
        
        for url in session_urls:
            next_url = base_url.format(url)
            yield scrapy.Request(url=next_url, callback=self.get_pdf)

    def get_pdf(self, response):
        pdfs = response.xpath('//*[@data-nav="2013"]/div/a[@target="_blank"]/@href').extract()
        for pdf in pdfs:
            print(pdf)
            yield scrapy.Request(url=pdf, callback=self.save_pdf)

    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        print(path)
        self.logger.info("Saving PDF %s", path)
        with open(path, 'wb') as f:
            f.write(response.body)
