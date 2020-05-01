from app import Listing
from app import Domain
from app import db


def merge_listing(listing: dict):
    listing = Listing(**listing)
    db.session.merge(listing)
    db.session.commit()


def merge_domain(domain_id: str):
    domain = Domain(id=domain_id)
    db.session.merge(domain)
    db.session.commit()
