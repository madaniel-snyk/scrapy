import scrapy


class WorldClockSpider(scrapy.Spider):

    name = "world_clock"
    start_urls = ['https://www.timeanddate.com/worldclock']

    def parse(self, response, **kwargs):

        # Extract main page cities
        for city_element in response.css('div.tb-scroll > table > tr > td'):
            yield {
                'City': city_element.css('a ::text').get(),
                'Time': city_element.css('td::text ').get(),
            }

        urls = response.css('div.tb-scroll > table > tr > td a ::attr(href)').extract()

        # Extract city detail pages
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_details)

    @staticmethod
    def parse_details(response, **kwargs):
        yield {
            'Country': response.css('div.bk-focus__info > table > tbody > tr > td ::text').get(),
            'Weather': response.css('.four.columns > p ::text').get(),
            'Temp': response.css('.four.columns > p > span ::text').get(),
        }

# In main page

# City
# response.css('div.tb-scroll > table > tr > td a ::text').get()

# Time
# response.css('div.tb-scroll > table > tr > td::text ').get()

# Link to details
# response.css('div.tb-scroll > table > tr > td a ::attr(href)').get()

# # #In element details page:

# Country
# response.css('div.bk-focus__info > table > tbody > tr > td ::text').get()

# Weather
# response.css('.four.columns > p ::text').get()

# Min/Max Temp
# response.css('.four.columns > p > span ::text').get()


