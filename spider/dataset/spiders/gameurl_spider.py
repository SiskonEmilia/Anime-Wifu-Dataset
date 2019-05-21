import scrapy
from ..items import FaceItem, GameInfo

class GameUrlSpider(scrapy.Spider):
  name = 'gameurl'

  def start_requests(self):
    url = 'file:///Users/siskon/Desktop/2013SQL.html'
    yield scrapy.Request(url=url, callback=self.parse_table)

  def parse_table(self, response):
    rows = response.css('#query_result_main tr')[1:5]
    for row in rows:
      print('Collecting game: ', row.xpath('td[2]/text()').get())
      url = row.xpath('td[4]/text()').get()
      print(url)
      if url is not None:
        yield scrapy.Request(url = 'http://' + url + '&gc=gc', 
        meta     = GameInfo(name=row.xpath('td[1]/text()').get()),
        callback = self.collect_image)
  
  def collect_image(self, response):
    srcs = response.css('table a+img::attr(src)').getall()
    srcs = [response.urljoin(src) for src in srcs]
    for src in srcs:
      print(src)
    yield FaceItem(image_urls=srcs, meta=response.meta,
      name=response.url.split('=')[-1])