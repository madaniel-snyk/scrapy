
import scrapy

"""
This Spider is scrapping 'quotes' site.

Each quote element has:
1. The quote
2. The author
3. Tags for the quote
4. Link with further details about the author

For each item - 
We iterate over it and scrap the item fields and also the 'more info' details behind the link.
We yield a dictionary in json with all the relevant details

After we complete to scrap the page - we search for a 'Next' button and continue the process for the next page. 
"""


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
