# import app from views
from products.views import app

#import products from models
from products.models import db,create_default_user


with app.app_context():
    db.drop_all() #drop all tables
    db.create_all() # create all tables
    create_default_user()