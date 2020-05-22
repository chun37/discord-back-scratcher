import re
import pytest
from verbalexpressions import VerEx

url_pettern = [
    "https://www.amazon.co.jp/%E3%82%A4%E3%83%A4%E3%83%AA%E3%83%B3%E3%82%B0-%E3%82%BB%E3%83%83%E3%83%88%E5%8D%81%E5%AD%97%E6%9E%B6-%E5%8E%B3%E9%81%B8%E3%83%94%E3%82%A2%E3%82%B9-%E3%83%AC%E3%83%87%E3%82%A3%E3%83%BC%E3%82%B9-12%E7%A8%AE%E9%A1%9E%E3%82%BB%E3%83%83%E3%83%88/dp/B07Y9QXMKL?pf_rd_r=NJH2N1K8316E24PG7QJA&pf_rd_p=d1035135-0a5f-4b82-a7a8-b7d0cf6569fb&pd_rd_r=f4ecb322-cee2-4a31-90b7-eb2f9e612916&pd_rd_w=8veu6&pd_rd_wg=VQJjg&ref_=pd_gw_hlp13n_t4im",
    "https://www.amazon.co.jp/dp/B0042J0KIW/ref=as_li_ss_tl?ie=UTF8&linkCode=sl1&tag=travelinguert-22&linkId=d9ddb98dcc5bff40a064ac68343fe1dc&language=ja_JP",
]


@pytest.mark.parametrize(
    "text", url_pettern,
)
def test_re_pattern(text):
    AMAZON_URL_PATTERN = r"https?://\S+?amazon\.co\.jp\S*?/dp/\S{10}\S*"
    match_object = re.search(AMAZON_URL_PATTERN, text)
    assert not match_object is None
    assert match_object.group() == text


@pytest.mark.parametrize("text", url_pettern)
def test_verex(text):
    verbal_expression = VerEx()
    tester = (
        verbal_expression.start_of_line()
        .find("http")
        .maybe("s")
        .find("://")
        .maybe("www.")
        .find("amazon.co.jp")
        .anything_but(" ")
        .end_of_line()
    )
    match_object = tester.match(text)
    assert not match_object is None
    assert match_object.group() == text
