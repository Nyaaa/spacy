from scrapy.http import HtmlResponse, Request


def load_sample(sample='sample.htm'):
    url = 'http://www.example.com'
    request = Request(url=url)
    with open(sample, 'rb') as f:
        response = HtmlResponse(url=url, request=request, body=f.read(), encoding='utf-8')

    text_block = response.xpath("//div[@class='et_pb_text_inner']")
    yield from text_block.xpath("./*[self::p or self::ul or starts-with(name(),'h')]")
