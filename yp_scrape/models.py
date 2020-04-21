from yp_scrape.run import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    @property
    def __repr__(self):
        return f'<{self.username}>'


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100))
    business_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zipcode = db.Column(db.Integer, nullable=False)
    website = db.Column(db.String(100))
    phone = db.Column(db.String(20))
