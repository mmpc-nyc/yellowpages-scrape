import os
from dotenv import load_dotenv

load_dotenv()

# Flask
DEBUG = True

# SQL Alchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///yp_scrape.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv('SECRET_KEY')

# Scrape
BASE_URL = 'https://www.yellowpages.com'
SEARCH_URL = 'https://www.yellowpages.com/search'

#Hunter IO
HUNTERIO_API_KEY = os.getenv('HUNTERIO_API_KEY')