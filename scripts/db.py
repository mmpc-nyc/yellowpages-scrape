from app import Listing
from app import db


def merge_listing(listing: dict) -> bool:
    listing = Listing(**listing)
    db.session.merge(listing)
    db.session.commit()
    return True
