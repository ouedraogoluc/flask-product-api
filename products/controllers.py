from flask import make_response, jsonify, Request
from products.models import Product, User , db
from products.utils import *
import json, os
from products.views import app
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token


class ProductContoller:
    
    def index(self, user_id: int = None) -> "Response":
        """
           Get all products
        """
        try:
            results = []
            
            if user_id != None:
                 # get user 
                user = User.query.get(user_id)
                if user:
                    results = [ p.json () for p in user.products] 
                else:
                    return make_response(jsonify(message='User not found')),404
            
            results = [ p.json () for p in Product.query.order_by(Product.created_at.desc()).all() ]
            
            return make_response(jsonify(products = results)),200 
        except Exception as e:
            print(type(e), e) # print error in console
            return make_response(jsonify(message='Error server')), 500

    def show(self, id: int) -> "Response":
        """
           Get one product from id
        """
        try:
            product = Product.query.get(id)
            print(product)
            if product:
                return make_response(jsonify(product= product.json())),200 
            else:
                return make_response(jsonify(message='Product not found')),404
        except Exception as e:
            print(type(e), e) # print error in console
            return make_response(jsonify(message='Error server')), 500

    def store(self, request: Request) -> "Response":
        """
           Save Product in database
        """
        try:
            # get json datas
            data = request.get_json()
            # put every data json in variable
            name = data['name'],
            price = data['price'],
            content = data['content'],
            quantity = data['quantity']
            user_id = data['user_id']

            # get user for checking if user exists
            user = User.query.filter(User.id == user_id).first()

            if user:
               
                new_product = Product(name=name, price=price, content=content, quantity=quantity, owner=user)
                db.session.add(new_product) 
                db.session.commit()
                return make_response(jsonify(message='Product successfully created', product=new_product.json())),201
            else:
                return make_response(jsonify(message="User not found")),404
        except Exception as e:
            print(type(e), e) # print error in console
            return make_response(jsonify(message='Error server')), 500

    def update(self, id: int, request: Request) -> "Response":
        """
           Update Product information in database
        """
        try:
            data = request.get_json()
            updated_product = Product.query.get(id)
            if updated_product:
                updated_product.name = data['name']
                updated_product.price = data['price']
                updated_product.content = data['content']
                updated_product.quantity = data['quantity']
                db.session.commit()
                return make_response(jsonify(message="Product successfully updated", status="success", product=updated_product.json())),200
            else:
                return make_response(jsonify(message='Product No found product')),404
        except Exception as e:
            print(type(e), e) # print error in console
            return make_response(jsonify(message='Error server')), 500
    
    def delete(self, id: int) -> "Response":
        """
           Delete Product in database
        """
        try:
            deleted_product =  Product.query.get(id)
            if deleted_product:
                db.session.delete(deleted_product)
                db.session.commit()
                return make_response(jsonify(message="Product successfully deleted", status="success")),200
            else:
                return make_response(jsonify(message='No found product')),404
    
        except Exception as e:
            print(type(e), e) # print error in console
            return make_response(jsonify(message='Error server')), 500

    def get_prodcut_by_price(self, price: int) -> "Response":
        """
           Get all products filter by price
        """
        try:
            products = Product.query.filter(Product.price == price).all()
            if len(products) == 0:
                return make_response(jsonify(message='Aucun produit trouvé pour {} '.format(_price),count=len(products))),200
            else:
                return make_response(jsonify(products= [p.json() for p in products],count=len(products))),200

        except Exception as e:
            print(type(e), e) # print error in console
            return make_response(jsonify(message='Error server')), 500
       
    def upload_product_image(self, request: Request)  -> "Response":
        """
           upload product image filter by price
        """
        try:
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
        except Exception as e:
            print(type(e), e) # print error in console
            return make_response(jsonify(message='Error server')), 500
   
    def delete_all_product(self)  -> "Response":
        """
           Delete all product
        """
        try:
            # get all products
            products = Product.query.all()
            # delete all produit
            for product in products:
                db.session.delete(product)
                db.session.commit()
            
            return make_response(jsonify(message="All products successfully deleted")),200
        except Exception as e:
            print(type(e), e) # print error in console
            return make_response(jsonify(message='Error server')), 500

class UserContoller:

    # get all users
    def index(self):
        # query
        users = User.query.order_by(User.id.desc()).all()
        # retourne la response
        return make_response(jsonify(users= [u.json() for u in users ],count=len(users))),200  

    # show detail of user
    def show(self, id):
        # query
        user = User.query.get(id)
        if user:
            return make_response(jsonify(user= user.json())),200 
        else:
            return make_response(jsonify(message='No found user')),404
        
    # save user
    def store(self, request):
        #recuperer les donnees json
        data = request.get_json()

        #creer un produit
        profil = data['profil'],
        firstname = data['firstname'],
        lastname = data['lastname'],
        email = data['email'],
        password = generate_password_hash(data['password']),
        #reperer l'existant
        user_exist= User.query.filter(User.email ==email).first()
        print(profil)
        if user_exist == None:
            new_user = User(profil=profil, firstname=firstname, lastname=lastname, email=email, password=password, photo=generate_image(email))
            # ajouter en base 
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify(message='User successfully created', user=new_user.json() )),201
        else:
            return make_response(jsonify(message='email exist deja')),409
  
    # update products
    def update(self, id,request):
        #recuperer les donnees json
        data = request.get_json()
        #chercher le produit
        updated_user = User.query.get(id)

        if updated_user:
            updated_user.firstname = data['firstname']
            updated_user.lastname = data['lastname']
            updated_user.profil = data['profil']
            updated_user.email = data['email']
            updated_user.password =['password']
          
            db.session.commit()
            return make_response(jsonify(message="User successfully updated", status="success", user=updated_user.json())),200
        else:
            return make_response(jsonify(message='No found user')),404

    # delete product
    def delete(iself, id):
        # recuperer le produit
        deleted_user =  User.query.get(id)
        if deleted_user:
            #supprimer en base
            db.session.delete(deleted_user)
            db.session.commit()
            return make_response(jsonify(message="user successfully deleted", status="success")),200
        else:
            return make_response(jsonify(message='No found product')),404
    
    # add image to product
    def upload_user_image(self, request):
        
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
  
    def authenticate(self, request):
        #recuperer les information de la requete sous format json
        data=request.get_json()
        login=data["login"]
        password=data["password"]
        user=User.query.filter(User.email==login).first()
        
        if user:
            if check_password_hash(user.password,password=password):
                #generate token
                access_token = create_access_token(identity=user.id)
                return make_response(jsonify(message='vous etes connecté',token=access_token,status='success',user=user.json())),200
            else:
                return make_response(jsonify(message='les informations sont incorrect',status='failed')),401
        else:
            return make_response(jsonify(message="user n'exist pas",status="failed")),404

    def register(self, request):
        return self.store(request)

    
    def delete_all_user(self)  -> "Response":
        """
           Delete all users
        """
        try:
            # get all products
            users = User.query.all()
            # delete all produit
            for user in users:
                db.session.delete(user)
                db.session.commit()
            
            return make_response(jsonify(message="All users successfully deleted")),200
        except Exception as e:
            print(type(e), e) # print error in console
            return make_response(jsonify(message='Error server')), 500