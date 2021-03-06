""" Webscraper Module

This module contains data classes and functions to store and compute data
from websites and articles scraped by the Beautiful Soup library

This file is Copyright (c) 2021 Amelia, Henry, Darlyn, Nyko. """

from dataclasses import dataclass
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
import bs4.element
import pandas
import python_ta
import requests

pytrends = TrendReq(hl='en-US', tz=360)


@dataclass()
class Website:
    """ Class containing the specifics about a website
    Instance Attributes:
        - url: the url of the main website
        - element: element used to find the href
        - class_type: the class type used to find the href
        - href_element: the element in the href used to find the information
        - href_class_type: the class type in the href used to find the information

    Representation Invariants:
        - url != ''
        - element != ''
        - class_type != ''
        - href_element != ''
        - href_class_type != ''
    """
    url: str
    element: str
    class_type: str
    href_element: str
    href_class_type: str


# Website Data Class Constant Instances
TOR_SUN = Website('https://torontosun.com', 'a', 'article-card__image-link', 'section',
                  'article-content__content-group')

TOR_STAR = Website('https://www.thestar.com', 'a',
                   'c-mediacard', 'p', 'text-block-container')

NATIONAL = Website('https://nationalpost.com', 'a',
                   'article-card__link', 'section', 'article-content__content-group')

YAHOO = Website('https://ca.news.yahoo.com', 'a',
                'js-content-viewer', 'div', 'caas-body')

WEBSITES = [TOR_SUN, TOR_STAR, NATIONAL, YAHOO]


@dataclass()
class Article:
    """ Class containing the information taken from an article
    Instance Attributes:
        - source: the article url
        - keywords: a list of keywords and its frequency on the article
        - total_words: the amount of words on a article

    Representation Invariants:
        - source != ''
        - all(x < total_words for x in keywords.values())
        - total_words >= 0
    """

    source: str
    keywords: dict
    total_words: int


def trends_data(keywords: list[str]) -> pandas.DataFrame:
    """ Takes all keys in keywords and finds the historical search trends over
    the past year for those keywords

    """
    pytrends.build_payload(keywords, cat=0, timeframe='today 12-m', geo='', gprop='')
    interest = pytrends.interest_over_time()

    return interest


def get_information(url: str) -> bs4.BeautifulSoup:
    """ Take a string url and convert it into a Beautiful Soup data type.

    Note: We will not use any doctests for this function as websites are not static and
    can be changed over time.
    Therefore, if we provide a docstring, it may not always work.

    """

    request_website = requests.get(url)
    home_page = request_website.content
    soup_website = BeautifulSoup(home_page, 'html.parser')

    return soup_website


def get_href(soup: bs4.BeautifulSoup, element: str, class_type: str) -> list[str]:
    """ From a bs4.BeautifulSoup, soup, return the href values as a list of strings.

    Note: We will not use any doctests for this function as websites are not static and
    can be changed over time.
    Therefore, if we provide a docstring, it may not always work.

    """
    href_list = []
    information = soup.find_all(element, class_=class_type)
    for i in range(0, min(20, len(information))):
        href_list.append(information[i]['href'])

    return href_list


def href_sites_information(domain: str, href_list: list[str],
                           element: str, class_type: str) -> list[str]:
    """ Takes the href information and scans the data from each reference site.

    Note: We will not use any doctests for this function as websites are not static and
    can be changed over time.
    Therefore, if we provide a docstring, it may not always work.

    """
    all_text = []
    for href in href_list:
        # If connection issues occur, skip that article.
        try:
            web_article = get_information(domain + href)
            body = web_article.find_all(element, class_=class_type)
            href_information = ''
            # Converts all paragraphs and bodies of text to
            # lowercase and converts them into a single string
            for sentence in body:
                lowercase = str(sentence).lower()
                all_words = str.split(lowercase)
                for word in all_words:
                    href_information += (word + ' ')

        except requests.exceptions.ConnectionError:
            continue
        # Remove article if skipped.
        if not href_information:
            href_list.remove(href)
            continue
        else:
            all_text.append(href_information)

    return all_text


def site_information(web: Website, keywords: list[str]) -> list[Article]:
    """ Check for keywords on the top articles for the BBC website.

    Note: We will not use any doctests for this function as websites are not static and
    can be changed over time.
    Therefore, if we provide a docstring, it may not always work.

    """
    info = get_information(web.url)
    hrefs = get_href(info, web.element, class_type=web.class_type)
    text = href_sites_information(web.url, hrefs, web.href_element, class_type=web.href_class_type)

    article_info = []

    for i in range(0, len(text)):
        keyword_frequency = {}
        list_of_words = str.split(text[i])
        total_words = len(list_of_words)
        source = web.url + hrefs[i]
        for word in list_of_words:
            for keyword in keywords:
                # Checking if the keyword is within each word in list_of_words
                if keyword in word:
                    if keyword not in keyword_frequency:
                        keyword_frequency[keyword] = 1
                    else:
                        keyword_frequency[keyword] += 1

        article_info.append(Article(source, keyword_frequency, total_words))
    return article_info


def find_related(webs: list[Article], keywords: list[str]) -> tuple[dict[str, int], int]:
    """ Find the percentage of articles with keywords to total articles and return a list of the
    percentages as a float

    >>> keywords = ['covid']
    >>> web = [Article('https://www.thestar.com/news/gta/2021/12/13/omicron-is-poised-to-overtake-delta-in-ontario-what-you-need-to-know.html', {'covid': 7}, 940)]
    >>> find_related(web, keywords)
    ({'covid': 1}, 1)

    """
    total = 0
    related = {}

    for keyword in keywords:
        related[keyword] = 0
        for website in webs:
            # Checking if each Webinfo contains any keywords
            if not website.keywords:
                total += 1
            elif keyword in website.keywords:
                total += 1
                related[keyword] += 1

    return related, total


def find_percentage(keywords: list[str]) -> dict[str, float]:
    """ Find the percentage of articles with keywords to total articles and return a dictionary
     mapping the keyword to a float representing the percentage

    >>> keywords = ['covid']
    >>> data = ({'covid': 8}, 20)
    >>> find_percentage(data, keywords)
    {'covid': 40.0}
    """
    article_info = []
    for website in WEBSITES:
        article_info.extend(site_information(website, keywords))

    percentages = {}

    related, total = find_related(article_info, keywords)
    for i in range(0, len(related)):
        percent = (related[keywords[i]] / total) * 100
        percentages[keywords[i]] = percent

    return percentages


if __name__ == '__main__':
    python_ta.check_all(config={
        'extra-imports': ['bs4.element', 'pandas', 'requests',
                          'bs4', 'pytrends.request'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'E9997']
    })

    import doctest

    doctest.testmod()
