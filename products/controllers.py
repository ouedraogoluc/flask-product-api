from flask import make_response, jsonify
from products.models import Product , db
from products.utils import *
import json, os
from products.views import app
from werkzeug.datastructures import ImmutableMultiDict

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
        
    def delete_all_product():
        # get all products
        products = Product.query.all()
        # delete all produit
        for product in products:
            db.session.delete(product)
            db.session.commit()
        
        return make_response(jsonify(message="All products successfully deleted", status="success")),200
       

        

        
