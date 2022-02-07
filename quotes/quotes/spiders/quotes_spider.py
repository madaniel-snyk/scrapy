import scrapy
from ..items import QuotesItem, QuoteItemLoader


class QuoteSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['https://quotes.toscrape.com/']

    def parse(self, response, **kwargs):

        # Extract main page quotes
        for quote in response.css('div.quote'):
            quote_info = {
                'quote': quote.css('span.text ::text').get(),
                'author': quote.css('small.author ::text').get(),
                'tags': quote.css('a.tag ::text').getall(),
            }

            # Extract more details from 'about' url
            relative_details_url = quote.css('a ::attr(href)').get()
            details_url = response.urljoin(relative_details_url)

            yield scrapy.Request(url=details_url, callback=self.parse_details, cb_kwargs=quote_info)

        # Checking if there's another page
        next_page = response.css('li.next ::attr(href)').get()

        if next_page:
            # Continue scrapping the next page
            yield response.follow(next_page, callback=self.parse)

    @staticmethod
    def parse_details(response, **kwargs):
        quote_info = kwargs

        details = {
            'born_date': response.css('span.author-born-date ::text').get(),
            'born_location': response.css('span.author-born-location ::text').get(),
            'description': response.css('div.author-description ::text').get()
        }

        quote_info.update(details)

        yield quote_info


class QuoteSpiderItem(scrapy.Spider):
    name = "quotes_item"
    start_urls = ['https://quotes.toscrape.com/']

    def parse(self, response, **kwargs):
        quote_item = QuotesItem()

        # Extract main page quotes
        for quote in response.css('div.quote'):
            quote_item['quote'] = quote.css('span.text ::text').get()
            quote_item['author'] = quote.css('small.author ::text').get()
            quote_item['tags'] = quote.css('a.tag ::text').getall()

            # Extract more details from 'about' url
            relative_details_url = quote.css('a ::attr(href)').get()
            details_url = response.urljoin(relative_details_url)

            yield scrapy.Request(url=details_url, callback=self.parse_details, cb_kwargs=quote_item)

        # Checking if there's another page
        next_page = response.css('li.next ::attr(href)').get()

        if next_page:
            # Continue scrapping the next page
            yield response.follow(next_page, callback=self.parse)

    @staticmethod
    def parse_details(response, **kwargs):
        quote_item = kwargs

        quote_item['born_date'] = response.css('span.author-born-date ::text').get()
        quote_item['born_location'] = response.css('span.author-born-location ::text').get()
        quote_item['description'] = response.css('div.author-description ::text').get()

        yield quote_item


class QuoteSpiderItemEnhanced(scrapy.Spider):
    name = "quotes_item_enhanced"
    start_urls = ['https://quotes.toscrape.com/']

    def parse(self, response, **kwargs):
        # Extract main page quotes
        for quote in response.css('div.quote'):
            loader = QuoteItemLoader(item=QuotesItem(), selector=quote)

            loader.add_css('quote', css='span.text ::text')
            loader.add_css('author', css='small.author ::text')
            loader.add_css('tags', css='a.tag ::text')
            loader.add_css('about_link', css='a ::attr(href)')

            # Build a full link for 'about' link
            details_url = response.urljoin(loader.get_output_value('about_link'))

            yield scrapy.Request(url=details_url, callback=self.parse_details, meta={'loader': loader})

            # Checking if there's another page
            next_page = response.css('li.next ::attr(href)').get()

            if next_page:
                # Continue scrapping the next page
                yield response.follow(next_page, callback=self.parse)

    @staticmethod
    def parse_details(response, **kwargs):
        loader = QuoteItemLoader(selector=response.css('div.author-details'), parent=response.meta['loader'])

        loader.add_css('born_date', 'span.author-born-date ::text')
        loader.add_css('born_location', 'span.author-born-location ::text')
        loader.add_css('description', 'div.author-description ::text')

        yield loader.load_item()
