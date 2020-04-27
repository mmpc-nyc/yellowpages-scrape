import os
# Flask
DEBUG = True

# SQL Alchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///yp_scrape/yp_scrape.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'tempkey'

# Scrape
BASE_URL = 'https://www.yellowpages.com'
SEARCH_URL = 'https://www.yellowpages.com/search'
SEARCH_TERMS = 'nursing home'
GEO_LOCATION_TERMS = 'Jersey City, NJ'