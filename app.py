from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = Flask(__name__)
app.config.from_pyfile('settings.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

keywords = db.Table(
    'keywords',
    db.Column('keyword_id', db.Integer, db.ForeignKey('keyword.id'), primary_key=True),
    db.Column('listing_id', db.Integer, db.ForeignKey('listing.id'), primary_key=True)
)


categories = db.Table(
    'categories',
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True),
    db.Column('listing_id', db.Integer, db.ForeignKey('listing.id'), primary_key=True)
)


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100))
    business_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100))
    locality = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zipcode = db.Column(db.Integer, nullable=False)
    website = db.Column(db.String(255))
    domain = db.Column(db.String(100))
    phone = db.Column(db.String(20))

    categories = db.relationship(
        'Category', secondary=categories, lazy='subquery',
        backref=db.backref('Listings', lazy=True)
    )
    keywords = db.relationship(
        'Keyword', secondary=keywords, lazy='subquery',
        backref=db.backref('Listings', lazy=True)
    )

    def __repr__(self):
        return f'<{self.business_name}>'


class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)


class Category(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100))


if __name__ == '__main__':
    manager.run()
