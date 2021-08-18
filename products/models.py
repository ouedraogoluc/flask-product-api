# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from products.views import app

# create database connexion
db = SQLAlchemy(app)

#create classe
class Product(db.Model):
    #rename table
    __tablename__ = 'products'
    #create field
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(8,2), nullable=False)
    content = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    
    # formatte l'affichage
    def __repr__(self):
        return '<Product {} {} {}>'.format(self.id, self.name, self.price)

    #json object 
    def json():
        return {
            "id":self.id,
            "name":self.name, 
            "price":self.price, 
            "content":self.content, 
            "quantity":self.quantity,
            "image_url":self.image_url 
            }