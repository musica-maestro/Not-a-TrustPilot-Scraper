from scrapy.item import Item, Field
from itemloaders.processors import MapCompose, TakeFirst

from datetime import datetime

def remove_quotes(text):
    text = text.strip(u'\u201c'u'\u201d')
    return text

def convert_date(text):
    return datetime.strptime(text, '%B %d, %Y')

def parse_location(text):
    return text [3:]

class CompanyItem(Item):
    name  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    website  = Field(
        input_processor = MapCompose(str.strip),
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
