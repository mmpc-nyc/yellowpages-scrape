import pandas as pd
import os
import sqlite3
from urllib.parse import urlparse
from app import db

from app import Listing

DB_FILE = '../yp_scrape.db'


def data_export(filename: str):
    columns = ['Email address', 'Domain name', 'Organization', 'Confidence score', 'Type', 'First name', 'Last name',
               'Department', 'Position', 'Phone number']
    data = pd.read_csv(os.path.join('parsed', filename), usecols=columns)
    personal_emails = data[data['Type'] == 'personal']
    personal_emails.head()
    grouped_personal_emails = personal_emails.groupby('Domain name')
    grouped_personal_emails.head(5).to_excel(os.path.join('parsed', '.'.join([filename.split('.')[0], 'xlsx'])),
                                             index=False)


def export_domains(keyword: str):
    connection = sqlite3.connect(DB_FILE)
    query = f"""
    SELECT 
       listing.id, business_name, address, city, state, zipcode, phone, keyword.name
    FROM keyword
    left join keywords on keyword.id = keywords.keyword_id
    left join listing on listing.id = keywords.listing_id
    where 
        website is not null and website != '' and lower(keyword.name) = {keyword.lower()}
    """
    data = pd.read_sql(con=connection, sql=query)
    data['domain'] = data['website'].apply(lambda x: urlparse(x).netloc)
    data.to_excel(os.path.join(keyword, 'xls'), index=False)


def update_domains():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    domains = db.session.query(Listing).all()
    for domain in domains:
        updated_domain = urlparse(domain.website).netloc
        print(updated_domain)
        cursor.execute('UPDATE listing SET domain = ? WHERE id = ?', (updated_domain, domain.id))
    connection.commit()