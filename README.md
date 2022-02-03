# scrapy
Practice on scrapy

## Project Quotes
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
