from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('settings.py')

from yp_scrape.views import *

db = SQLAlchemy(app)

import yp_scrape.models

if __name__ == '__main__':
    app.run(debug=True)
