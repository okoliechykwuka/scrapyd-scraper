import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime
from scrapy.crawler import CrawlerProcess
import re
import os
import pandas as pd


class GreyhoundSpider(CrawlSpider):
    name = 'greyhound'
    path = os.getcwd() + '\\' + 'results.json'

    custom_settings = {
        'FEEDS': {
        path : {'format':'json'

        }}}
   
    allowed_domains = ['thegreyhoundrecorder.com.au']
    start_urls = ['http://thegreyhoundrecorder.com.au/form-guides/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//tbody/tr/td[2]/a"), callback='parse_item', follow=True), #//tbody/tr/td[2]/a 
    )

    def clean_date(dm):
        year = pd.to_datetime('now').year     # Get current year
        race_date =  pd.to_datetime(dm + ' ' + str(year)).strftime('%d/%m/%Y')
        return race_date


    def parse_item(self, response):
        #Field =  response.xpath ("//ul/li[1][@class='nav-item']/a/text()").extract_first() #all fileds
        for race in response.xpath("//div[@class= 'fieldsSingleRace']"):
            my_list = []
            title = str(race.xpath("//div/h1[@class='title']/text()").extract_first())
            clean_track = title.split('-')[0].strip()
            Track = clean_track.split(' ')[0].strip()
            date = str(title.split('-')[1].strip())
            year = pd.to_datetime('now').year 
            race_date =  pd.to_datetime(date + ' ' + str(year)).strftime('%d/%m/%Y')
            race_number = race.xpath("//tr[@id = 'tableHeader']/td[1]/text()").extract()

            for i in race_number:
                m = re.split(' |a',i)
                new_str = "".join(m[::len(m)-1]).strip()
                my_list.append(new_str)
            final_race = ",".join(my_list)

            Distance = race.xpath("//tr[@id = 'tableHeader']/td[3]/text()").extract()
            TGR_Grade = race.xpath("//tr[@id = 'tableHeader']/td[4]/text()").extract()
            TGR1 = race.xpath("//tbody/tr[@class='fieldsTableRow raceTipsRow']//div/span[1]/text()").extract()
            TGR2 = race.xpath("//tbody/tr[@class='fieldsTableRow raceTipsRow']//div/span[2]/text()").extract()
            TGR3 = race.xpath("//tbody/tr[@class='fieldsTableRow raceTipsRow']//div/span[3]/text()").extract()
            TGR4 = race.xpath("//tbody/tr[@class='fieldsTableRow raceTipsRow']//div/span[4]/text()").extract()
            
        yield {  
                'Date': race_date,
                'Track': Track,
                '#': final_race,
                'Distance': Distance,
                'TGR Grade': TGR_Grade,
                'TGR1': TGR1,
                'TGR2': TGR2,
                'TGR3': TGR3,
                'TGR4': TGR4,
                
           }

# if __name__ == "__main__":
#   process = CrawlerProcess()
#   process.crawl(GreyhoundSpider)
#   process.start()
