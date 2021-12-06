import bs4.element
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass()
class Website:
    """ Class containing the specifics about a website

    Instance Attribtue:
        - url: the url of the main website
        - element: element used to find the href
        - class_type: the class type used to find the href
        - href_element: the element in the href used to find the information
        = href_class_type: the class type in the href used to find the information
    """
    url: str
    element: str
    class_type: str
    href_element: str
    href_class_type: str


@dataclass()
class WebInfo:
    """ Class containing the information taken from a website

    """

    source: str
    keywords: dict
    total_words: int


def get_information(url: str) -> bs4.BeautifulSoup:
    """ Take a string url and convert it into a Beautiful Soup data type.

    """

    request_website = requests.get(url)
    home_page = request_website.content
    soup_website = BeautifulSoup(home_page, 'html.parser')

    return soup_website


def get_href(soup: bs4.BeautifulSoup, element: str, class_type: str) -> list[str]:
    """ From a bs4.BeautifulSoup, soup, return the href values as a list of strings.

    """
    href_list = []
    information = soup.find_all(element, class_=class_type)
    for i in range(0, min(15, len(information))):
        href_list.append(information[i]['href'])

    return href_list


def href_sites_information(domain: str, href_list: list[str], element: str, class_type: str) -> list[str]:
    """

    """
    all_text = []
    for href in href_list:
        web_article = get_information(domain + href)
        body = web_article.find_all(element, class_=class_type)
        href_information = ''
        for sentence in body:
            lowercase = str(sentence).lower()
            all_words = str.split(lowercase)
            for word in all_words:
                href_information += (word + ' ')

        all_text.append(href_information)

    return all_text


def site_information(web: Website, keywords: list[str]):
    """ Check for keywords on the top articles for the BBC website.

    """
    info = get_information(web.url)
    hrefs = get_href(info, web.element, class_type=web.class_type)
    text = href_sites_information(web.url, hrefs, web.href_element, class_type=web.href_class_type)

    for i in range(0, len(hrefs)):
        keyword_frequency = {}
        list_of_words = str.split(text[i])
        total_words = len(list_of_words)
        source = web.url + hrefs[i]
        for word in list_of_words:
            for keyword in keywords:
                if keyword in word:
                    if keyword not in keyword_frequency:
                        keyword_frequency[keyword] = 1
                    else:
                        keyword_frequency[keyword] += 1

        all_webinfo.append(WebInfo(source, keyword_frequency, total_words))


# Website data classes
bbc = Website('https://www.bbc.com', 'a', 'block-link__overlay-link', 'p', 'ssrcss-1q0x1qg-Paragraph')
tor_sun = Website('https://torontosun.com', 'a', 'article-card__image-link', 'section', 'article-content__content-group')
tor_star = Website('https://www.thestar.com', 'a', 'c-mediacard', 'p', 'text-block-container')
national = Website('https://nationalpost.com', 'a', 'article-card__link', 'section', 'article-content__content-group')
yahoo = Website('https://ca.news.yahoo.com', 'a', 'js-content-viewer', 'div', 'caas-body')
ctv = Website('https://www.ctvnews.ca', 'a', 'c-list__item__link', 'div',
              'articleBody election-col-11 election-col-s-12 election-col-m-12 '
              'election-col-l-10 election-col-xl-11 offset-right-col-l-1 offset-left-col-l-1 '
              'offset-left-col-xl-1 offset-left-col-1')

all_webinfo = []
keywords = ['covid', 'vaccine', 'pandemic']




