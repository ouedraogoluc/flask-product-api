from flask import make_response, jsonify
from products.models import Product, User , db
from products.utils import *
import json, os
from products.views import app
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token
#create product controller class
class ProductContoller:

    # get all products
    def index():
        # query
        products = Product.query.order_by(Product.id.desc()).all()
        # retourne la response
        return make_response(jsonify(products= [p.json() for p in products],count=len(products))),200  

    # show detail of product
    def show(id):
        # query
        product = Product.query.get(id)
        if product:
            return make_response(jsonify(product= product.json())),200 
        else:
            return make_response(jsonify(status = 'error',message='No found product')),404
        
    # save products
    def store(request):
        #recuperer les donnees json
        data = request.get_json()

        #creer un produit
        name = data['name'],
        price = data['price'],
        content = data['content'],
        quantity = data['quantity']

        new_product = Product(name=name, price=price, content=content, quantity=quantity)
        # ajouter en base 
        db.session.add(new_product)
        db.session.commit()
        return make_response(jsonify(status= 'success', message='Product successfully created', product=new_product.json())),201
 
    # update products
    def update(id,request):
        #recuperer les donnees json
        data = request.get_json()
        #chercher le produit
        updated_product = Product.query.get(id)

        if updated_product:
            updated_product.name = data['name']
            updated_product.price = data['price']
            updated_product.content = data['content']
            updated_product.quantity = data['quantity']
            db.session.commit()
            return make_response(jsonify(message="Product successfully updated", status="success", product=updated_product.json())),200
        else:
            return make_response(jsonify(status = 'error',message='No found product')),404

    # delete product
    def delete(id):
        # recuperer le produit
        deleted_product =  Product.query.get(id)
        if deleted_product:
            #supprimer en base
            db.session.delete(deleted_product)
            db.session.commit()
            return make_response(jsonify(message="Product successfully deleted", status="success")),200
        else:
            return make_response(jsonify(status = 'error',message='No found product')),404
    
    # get all product with same price
    def get_prodcut_by_price(_price):
        # query
        products= Product.query.filter(Product.price == _price).all()
        if len(products) == 0:
              return make_response(jsonify(message='Aucun produit trouvé pour {} '.format(_price),count=len(products))),200
        else:
              return make_response(jsonify(products= [p.json() for p in products],count=len(products))),200

    # add image to product
    def upload_product_image(request):
        
        # check if the post request has the file part
        if 'image' not in request.files:
            return make_response(jsonify(message='No file part in the request',status='failed')),400
        
        # get file    
        file = request.files['image']
   
        # check filename
        if file.filename == '':
            return make_response(jsonify(message='No file selected for uploading',status='failed')),400
        
        # file and allow
        if file and allowed_file(file.filename):
            # secure filename
            filename = secure_filename(file.filename)
            # save file
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # generate image_url
            image_url = request.url_root + url_for('get_product_image', filename=filename)

            # get json data
            data = request.form.get('product_id')
            
            print(data)
            # retrieve data
            product_update = Product.query.get(data)

            if product_update:
                # update
                product_update.image_url = image_url
                db.session.commit()
                return make_response(jsonify(message="Image successfully uploaded", status="success", image_uri=image_url)),200
            else:
                return make_response(jsonify(message='Product no found',  status='failed')),400
        else:
            return make_response(jsonify(message='Allowed file types are png, jpg, jpeg',status='failed')),400
        
#create product controller class
class UserContoller:

    # get all users
    def index():
        # query
        users = User.query.order_by(User.id.desc()).all()
        # retourne la response
        return make_response(jsonify(users= [u.json() for u in users ],count=len(users))),200  

    # show detail of user
    def show(id):
        # query
        user = User.query.get(id)
        if user:
            return make_response(jsonify(user= user.json())),200 
        else:
            return make_response(jsonify(status = 'error',message='No found user')),404
        
    # save user
    def store(request):
        #recuperer les donnees json
        data = request.get_json()

        #creer un produit
       
        type = data['type'],
        first_name = data['first_name'],
        last_name = data['last_name'],
        email = data['email'],
        password = generate_password_hash(data['password']),
        #reperer l'existant
        user_exist= User.query.filter(User.email ==email).first()
        if user_exist == None:
            new_user = User(type=type,first_name=first_name,last_name=last_name, email=email, password=password)
            # ajouter en base 
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify(status= 'success', message='User successfully created', user=new_user.json())),201
        else:
            return make_response(jsonify(status = 'error',message='email exist deja')),401

       
    # update products
    def update(id,request):
        #recuperer les donnees json
        data = request.get_json()
        #chercher le produit
        updated_user = User.query.get(id)

        if updated_user:
            updated_user.first_name = data['first_name']
            updated_user.last_name = data['last_name']
            updated_user.type = data['type']
            updated_user.email = data['email']
            updated_user.password =['password']
          
            db.session.commit()
            return make_response(jsonify(message="User successfully updated", status="success", user=updated_user.json())),200
        else:
            return make_response(jsonify(status = 'error',message='No found user')),404

    # delete product
    def delete(id):
        # recuperer le produit
        deleted_user =  User.query.get(id)
        if deleted_user:
            #supprimer en base
            db.session.delete(deleted_user)
            db.session.commit()
            return make_response(jsonify(message="user successfully deleted", status="success")),200
        else:
            return make_response(jsonify(status = 'error',message='No found product')),404
    
    # get all product with same price
    def get_user_by_email(_email):
        # query
        users= User.query.filter(User.email == _email).all()
        if len(users) == 0:
              return make_response(jsonify(message='Aucun produit trouvé pour {} '.format(_email),count=len(users))),200
        else:
              return make_response(jsonify(users= [u.json() for u in users],count=len(users))),200

    # add image to product
    def upload_user_image(request):
        
        # check if the post request has the file part
        if 'imageUser' not in request.files:
            return make_response(jsonify(message='No file part in the request',status='failed')),400
        
        # get file    
        file = request.files['imageUser']
   
        # check filename
        if file.filename == '':
            return make_response(jsonify(message='No file selected for uploading',status='failed')),400
        
        # file and allow
        if file and allowed_file(file.filename):
            # secure filename
            filename = secure_filename(file.filename)
            # save file
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # generate image_url
            userImage_url = request.url_root + url_for('get_user_image', filename=filename)

            # get json data
            data = request.form.get('user_id')
            
            print(data)
            # retrieve data
            user_update = User.query.get(data)

            if user_update:
                # update
                user_update.userImage_url = userImage_url
                db.session.commit()
                return make_response(jsonify(message="Image successfully uploaded", status="success", image_uri=userImage_url)),200
            else:
                return make_response(jsonify(message='Product no found',  status='failed')),400
        else:
            return make_response(jsonify(message='Allowed file types are png, jpg, jpeg',status='failed')),400
  
    def authenticate(request):
        #recuperer les information de la requete sous format json
        data=request.get_json()
        login=data["login"]
        password=data["password"]
        user=User.query.filter(User.email==login).first()
        
        if user:
            if check_password_hash(user.password,password=password):
                #generate token
                access_token = create_access_token(identity=user.id)
                return make_response(jsonify(message='vous etes connecté',token=access_token,status='success')),200
            else:
                return make_response(jsonify(message='les informations sont incorrect',status='failed')),401
        else:
            return make_response(jsonify(message="user n'exist pas",status="failed")),404

