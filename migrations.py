# import app from views
from products.views import app

#import products from models
from products.models import db


with app.app_context():
    db.drop_all() #drop all tables
    db.create_all() # create all tables