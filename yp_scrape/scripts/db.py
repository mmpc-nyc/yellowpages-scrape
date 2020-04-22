from app import Listing
from app import db


def merge_listing(listing: dict) -> bool:
    listing = Listing(**listing)
    db.session.merge(listing)
    db.session.commit()
    return True


def merge_category(category, listing_id):
    pass


def merge_keyword(keyword, listing_id):
    pass


def merge_category_listing(category_id, listing_id):
    pass
