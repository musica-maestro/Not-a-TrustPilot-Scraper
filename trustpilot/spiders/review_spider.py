import scrapy
from scrapy.loader import ItemLoader
from trustpilot.items import CompanyItem

class TrustpilotSpider(scrapy.Spider):
    name = "trustpilot"
    allowed_domains = ["it.trustpilot.com"]
    start_urls = ['https://it.trustpilot.com/categories/electronics_technology']


    def parse(self, response):
        self.logger.info('Parse function called on {}'.format(response.url))
        
        # getting all the companies on the page
        companies = response.css('div.styles_categoryBusinessListWrapper__2H2X5 > a')

        self.logger.info('CYCLING COMPANIES ON THE PAGE')

        for company in companies:

            # get company url
            company_trustpilot_url = company.css('a::attr(href)').get()

            # go to the company page
            yield response.follow(company_trustpilot_url, self.parse_company)

        # go to Next page with companies
        for a in response.css('a.link_internal__YpiJI.button_button__3sN8k.button_large__3HOoE.button_primary__2eJ8_.link_button__13BH6.pagination-link_next__1ld6a.pagination-link_rel__3ZMeia'):
            yield response.follow(a, self.parse)

    def parse_company(self, response):
        loader = ItemLoader(item=CompanyItem(), response=response)
        loader.add_css('name', 'span.typography_typography__23IQz.typography_h1__3CI-9.typography_weight-heavy__36UHe.typography_fontstyle-normal__1_HQI.styles_displayName__1ocKa::text')
        loader.add_css('website', 'section.styles_businessInformation__36EuU > div.styles_badgesWrapper__3A6EU > div > div > a::attr(href)')
        loader.add_css('info', 'p.styles_container__2lPJ7::text')
        #loader.add_css('mail', '')
        #loader.add_css('phone', '')
        #loader.add_css('address', '')
        loader.add_css('reviews_count', 'div.styles_header__TbVq- > h2 > span::text')
        loader.add_xpath('overall_rating', '//*[@id="__next"]/div/main/div/div[2]/div[2]/div/div/section[1]/div[1]/div[2]/span/text()[5]')
        yield loader.load_item()