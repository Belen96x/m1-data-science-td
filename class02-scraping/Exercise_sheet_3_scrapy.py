import scrapy
import json

class WikipediaSpider(scrapy.Spider): #Something is missing here. What exactly?
    name = "wikipedia"

    start_urls = ["https://en.wikipedia.org/wiki/List_of_French_artists"]

    def parse(self, response):
        list_els = response.css('ul li a::attr(href)').getall() 
        # Find all the elements <a> inside <li> inside <ul> and gave the values with the attribute <href>
        list_see_also = response.css('span#See_also ~ ul li a::attr(href)').getall()
        res_list = list(set(list_els) - set(list_see_also))
        for link in res_list:
            #check that the link actually exists and is not red
                yield response.follow(link, callback=self.parse_artist)
        
    def parse_artist(self, response):
        url = response.url
        name = response.css('h1#firstHeading > span.mw-page-title-main::text').get()
        paragraph = ''.join(response.css('p *::text').getall())
        yield {'url': url,
               'name': name,
               'paragraph': paragraph}
        
        
if __name__=='__main__':
    import scrapy.crawler
    
    process = scrapy.crawler.CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0',
        'FEEDS': {
            "artists.json": {"format": "json"},
        },
    })
    process.crawl(WikipediaSpider)
    process.start()
    process.stop()
