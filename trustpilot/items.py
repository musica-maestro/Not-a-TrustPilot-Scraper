from scrapy.item import Item, Field
from itemloaders.processors import MapCompose, TakeFirst
import re

def remove_query_url(text):
    return text.replace('?utm_medium=company_profile&utm_source=trustpilot&utm_campaign=domain_click', '')

def extract_votes_number(text):
    try:
        return text.split()[0]
    except:
        return 'no available'

class CompanyItem(Item):
    name  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    website  = Field(
        input_processor = MapCompose(remove_query_url),
        output_processor = TakeFirst()
    )
    info  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    mail  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    phone  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    address  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    reviews_count  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    overall_rating  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    excellent  = Field(
        input_processor = MapCompose(extract_votes_number),
        output_processor = TakeFirst()
    )
    great  = Field(
        input_processor = MapCompose(extract_votes_number),
        output_processor = TakeFirst()
    )
    average  = Field(
        input_processor = MapCompose(extract_votes_number),
        output_processor = TakeFirst()
    )
    poor  = Field(
        input_processor = MapCompose(extract_votes_number),
        output_processor = TakeFirst()
    )
    bad  = Field(
        input_processor = MapCompose(extract_votes_number),
        output_processor = TakeFirst()
    )
