from flask import make_response, jsonify
from products.models import Product , db

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

      
        

        
