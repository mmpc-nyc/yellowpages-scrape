from bs4 import BeautifulSoup
import requests
from slugify import slugify
from time import sleep

from settings import BASE_URL
from settings import SEARCH_URL
from settings import SEARCH_TERMS
from settings import GEO_LOCATION_TERMS

from yp_scrape.scripts.db import merge_listing
from app import Category
from app import Keyword


def get_page(search_terms: str, geo_location_terms: str):
    params = {'search_terms': search_terms, 'geo_location_terms': geo_location_terms}
    return requests.get(SEARCH_URL, params=params)


def get_listings(_page_soup):
    return _page_soup.find_all('div', {'class': 'info'})


def parse_listing(_listing):
    _parsed_listing = {}
    business_name = _listing.find('a', {'class': 'business-name'})
    website = _listing.find('a', {'class': 'track-visit-website'})
    street_address = _listing.find('div', {'class': 'street-address'})
    locality = _listing.find('div', {'class': 'locality'})

    categories = []
    for category in _listing.find('div',{'class': 'categories'}):
        categories.append(Category(id=slugify(category.text),name=category.text))

    phones = _listing.find('div', {'class': 'phones'})
    _parsed_listing['keywords'] = [Keyword(name=SEARCH_TERMS)]
    _parsed_listing['url'] = business_name['href'].split('?')[0]
    _parsed_listing['id'] = _parsed_listing['url'].split('-')[-1]
    _parsed_listing['categories'] = categories
    _parsed_listing['business_name'] = business_name.text
    _parsed_listing['address'] = street_address.text if street_address else ''
    if not locality:
        print(_listing)
        return None
    _parsed_listing['locality'] = locality.text
    *city, _parsed_listing['state'], _parsed_listing['zipcode'] = _parsed_listing['locality'].split(' ')
    _parsed_listing['city'] = ' '.join(city).strip(',')
    _parsed_listing['zipcode'] = _parsed_listing['locality'].split()[-1] if locality else ''
    _parsed_listing['website'] = website['href'] if website else ''
    _parsed_listing['phone'] = phones.text if phones else ''
    return _parsed_listing


def page_to_soup(page):
    return BeautifulSoup(page.text, 'html.parser')


def get_next(_page_soup):
    _url = _page_soup.find('a', {'class': 'next ajax-page'})
    if _url:
        return requests.get(BASE_URL + _url['href'])
    return None


def main():
    page = get_page(SEARCH_TERMS, GEO_LOCATION_TERMS)
    page_soup = page_to_soup(page)

    while page:
        listings = get_listings(page_soup)
        for listing in listings:
            parsed_listing = parse_listing(listing)
            merge_listing(parsed_listing)
            print(parsed_listing['business_name'])
        page = get_next(page_soup)
        break


if __name__ == '__main__':
    page = get_page(SEARCH_TERMS, GEO_LOCATION_TERMS)
    page_number = 1
    listing_number = 1
    while page:
        page_soup = page_to_soup(page)
        print(f'Page {page_number}\t {page.url}')
        listings = get_listings(page_soup)
        for listing in listings:
            parsed_listing = parse_listing(listing)
            if parsed_listing:
                merge_listing(parsed_listing)
                print(f"{listing_number}\t {parsed_listing['business_name']}")
            listing_number += 1
        sleep(1)
        page_number += 1
        page = get_next(page_soup)