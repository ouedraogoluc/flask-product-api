# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from products.views import app
from werkzeug.security import generate_password_hash
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
    image_url = db.Column(db.Text, nullable=True)
    
    # formatte l'affichage
    def __repr__(self):
        return '<Product {} {} {}>'.format(self.id, self.name, self.price)

    #json object 
    def json(self):
        return {
            "id":self.id,
            "name":self.name, 
            "price":int(self.price), 
            "content":self.content, 
            "quantity":self.quantity,
            "image_url":self.image_url 
            }
#create user classe
class User(db.Model):
    """Model for user accounts."""
    __tablename__ = 'users'
#create field
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String,nullable=False)
    last_name = db.Column(db.String,nullable=False)
    email = db.Column(db.String(40),unique=True, nullable=False)
    password = db.Column(db.String(200),nullable=False)
    type = db.Column(db.String,nullable=False)
    #formate affichage
    def __repr__(self):
        return '<User {}>'.format(self.username)
     #json object 
    def json(self):
        return {
            "id":self.id,
            
            "first_name":self.first_name,  
            "last_name":self.last_name,  
            "email":self.email, 
            "password":self.password, 
            "type":self.type,
            }

def create_default_user():
    new_user = User(type="admin",first_name="luc",last_name="ouedraogo", email="luc@gmail.com", password=generate_password_hash("admin"))
    # ajouter en base 
    db.session.add(new_user)
    db.session.commit()


