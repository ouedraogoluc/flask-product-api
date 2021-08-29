# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from products.views import app
from werkzeug.security import generate_password_hash
from datetime import datetime

# create database connexion
db = SQLAlchemy(app)

#create user classe
class User(db.Model):

    """Model for user accounts."""
    __tablename__ = 'users'

    #create field
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    profil = db.Column(db.String(40), nullable=False)
    photo = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)   

    # relationship with product table
    products = db.relationship('Product', backref='owner')
    
    #formate affichage
    def __repr__(self):
        return '<User {}>'.format(self.id)
    
     #json object 
    def json(self):
        return { "id":self.id,"firstname":self.firstname, "lastname":self.lastname,  "email":self.email, "profil":self.profil, "photo" :self.photo}


#create classe
class Product(db.Model):

    """Model for product."""

    #rename table
    __tablename__ = 'products'

    #create field
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(8,2), nullable=False)
    content = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)   
    
    # ajout de la cle etranger 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # formatte l'affichage
    def __repr__(self):
        return '<Product {} {} {}>'.format(self.id, self.name, self.price)

    #json object 
    def json(self):
        return { 
            "id":self.id,
            "name":self.name, 
            "price":int(self.price), "content":self.content, "quantity":self.quantity,
            "image_url":self.image_url
            }


def create_default_user():
    new_user = User(profil="admin",firstname="luc",lastname="ouedraogo", email="luc@gmail.com", password=generate_password_hash("admin"))
    # ajouter en base 
    db.session.add(new_user)
    db.session.commit()


