from contextlib import nullcontext
from warnings import catch_warnings
import scrapy
from scrapy.loader import ItemLoader

from trustpilot.items import CompanyItem

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TrustpilotSpider(scrapy.Spider):
    name = "trustpilot"
    allowed_domains = ["trustpilot.com"]
    start_urls = ['https://www.it.trustpilot.com/categories/electronics_technology?page1']

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
        for a in response.css('a.link_internal__YpiJI.button_button__3sN8k.button_large__3HOoE.button_primary__2eJ8_.link_button__13BH6.pagination-link_next__1ld6a.pagination-link_rel__3ZMei'):
            yield response.follow(a, self.parse)

    def parse_company(self, response):

        path = 'trustpilot\driver\chromedriver.exe'
        options = webdriver.ChromeOptions()
        options.add_argument("-headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        driver = webdriver.Chrome(executable_path=path, options=options)

        driver.get(response.request.url)

        # Implicit wait
        driver.implicitly_wait(1)
        # Explicit wait
        wait = WebDriverWait(driver, 1)

        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "styles_container__2lPJ7")))
            info = driver.find_elements_by_class_name("styles_container__2lPJ7")
            info = info[0].get_attribute('outerText')
        except:
            info = ''
        
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "address > ul > li:nth-child(1) > a")))
            mail = driver.find_elements_by_css_selector("address > ul > li:nth-child(1) > a")
            mail = mail[0].get_attribute('outerText')
        except:
            mail = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "address > ul > li:nth-child(2) > a")))
            phone = driver.find_elements_by_css_selector("address > ul > li:nth-child(2) > a")
            phone = phone[0].get_attribute('outerText')
        except:
            phone = ''
        
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "address > ul > li:nth-child(3) > ul")))
            address = driver.find_elements_by_css_selector("address > ul > li:nth-child(3) > ul")
            address = address[0].get_attribute('outerText')
        except:
            address = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.paper_paper__29o4A.card_card__2F_07.styles_reviewsOverview__3aD-n > div.styles_container__1h0Ze > label:nth-child(1)")))
            excellent = driver.find_elements_by_css_selector("div.paper_paper__29o4A.card_card__2F_07.styles_reviewsOverview__3aD-n > div.styles_container__1h0Ze > label:nth-child(1)")
            excellent = excellent[0].get_attribute('title')
        except:
            excellent = '0'

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.paper_paper__29o4A.card_card__2F_07.styles_reviewsOverview__3aD-n > div.styles_container__1h0Ze > label:nth-child(2)")))
            great = driver.find_elements_by_css_selector("div.paper_paper__29o4A.card_card__2F_07.styles_reviewsOverview__3aD-n > div.styles_container__1h0Ze > label:nth-child(2)")
            great = great[0].get_attribute('title')
        except:
            great = '0'

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.paper_paper__29o4A.card_card__2F_07.styles_reviewsOverview__3aD-n > div.styles_container__1h0Ze > label:nth-child(3)")))
            average = driver.find_elements_by_css_selector("div.paper_paper__29o4A.card_card__2F_07.styles_reviewsOverview__3aD-n > div.styles_container__1h0Ze > label:nth-child(3)")
            average = average[0].get_attribute('title')
        except:
            average = '0'

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.paper_paper__29o4A.card_card__2F_07.styles_reviewsOverview__3aD-n > div.styles_container__1h0Ze > label:nth-child(4)")))
            poor = driver.find_elements_by_css_selector("div.paper_paper__29o4A.card_card__2F_07.styles_reviewsOverview__3aD-n > div.styles_container__1h0Ze > label:nth-child(4)")
            poor = poor[0].get_attribute('title')
        except:
            poor = '0'

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.paper_paper__29o4A.card_card__2F_07.styles_reviewsOverview__3aD-n > div.styles_container__1h0Ze > label:nth-child(5)")))
            bad = driver.find_elements_by_css_selector("div.paper_paper__29o4A.card_card__2F_07.styles_reviewsOverview__3aD-n > div.styles_container__1h0Ze > label:nth-child(5)")
            bad = bad[0].get_attribute('title')
        except:
            bad = '0'
        
        

        loader = ItemLoader(item=CompanyItem(), response=response)
        loader.add_css('name', 'span.typography_typography__23IQz.typography_h1__3CI-9.typography_weight-heavy__36UHe.typography_fontstyle-normal__1_HQI.styles_displayName__1ocKa::text')
        loader.add_css('website', 'section.styles_businessInformation__36EuU > div.styles_badgesWrapper__3A6EU > div > div > a::attr(href)')
        loader.add_value('info', info)
        loader.add_value('mail', mail)
        loader.add_value('phone', phone)
        loader.add_value('address', address)
        loader.add_css('reviews_count', 'div.styles_header__TbVq- > h2 > span::text')
        loader.add_xpath('overall_rating', '//*[@id="__next"]/div/main/div/div[2]/div[2]/div/div/section[1]/div[1]/div[2]/span/text()[5]')
        loader.add_value('excellent', excellent)
        loader.add_value('great', great)
        loader.add_value('average', average)
        loader.add_value('poor', poor)
        loader.add_value('bad', bad)
        yield loader.load_item()