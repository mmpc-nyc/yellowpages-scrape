from bs4 import BeautifulSoup
import requests

from yp_scrape.settings import BASE_URL
from yp_scrape.settings import SEARCH_URL
from yp_scrape.settings import SEARCH_TERMS
from yp_scrape.settings import GEO_LOCATION_TERMS



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
    phones = _listing.find('div', {'class': 'phones'})
    _parsed_listing['url'] = business_name['href'].split('?')[0]
    _parsed_listing['id'] = _parsed_listing['url'].split('-')[-1]
    _parsed_listing['business_name'] = business_name.text
    _parsed_listing['street_address'] = street_address.text if street_address else ''
    _parsed_listing['locality'] = locality.text if locality else ''
    *city , _parsed_listing['state'], _parsed_listing['zipcode'] = _parsed_listing['locality'].split(' ')
    _parsed_listing['city'] = ' '.join(city).strip(',')
    _parsed_listing['zipcode'] = _parsed_listing['locality'].split()[-1] if locality else ''
    _parsed_listing['website'] = website['href'] if website else ''
    _parsed_listing['phones'] = phones.text if phones else ''
    return _parsed_listing


def page_to_soup(page):
    return BeautifulSoup(page.text, 'html.parser')


def scrape(url: str):
    # TODO Implement scrape function
    return


def get_next(_page_soup):
    _url = _page_soup.find('a', {'class': 'next ajax-page'})
    if _url:
        return requests.get(BASE_URL + _url['href'])
    return None


def write_data(data: dict) -> bool:
    #  TODO Implement write_data function that writes data to csv line by line
    return


if __name__ == '__main__':

    page = get_page(SEARCH_TERMS, GEO_LOCATION_TERMS)
    page_soup = page_to_soup(page)

    while page:
        listings = get_listings(page_soup)
        for listing in listings:
            parsed_listing = parse_listing(listing)
            break
        page = get_next(page_soup)
        break
