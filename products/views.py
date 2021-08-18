from flask import Flask, jsonify , request , make_response
from flask_cors import cross_origin

# create app
app = Flask(__name__)

# configuration de la base de donnee
app.config.from_object('config')

#importer le controller
from products.controllers import ProductContoller

# route principale
@app.route('/')
@cross_origin()
def index():
   return make_response(jsonify(message = 'Bienvenue sur notre api de produit')),200

#route pour lister les produits

@app.route('/products')
@cross_origin()
def get_all_products():
   return ProductContoller.index()

#route pour ajouter un produit
@app.route('/products/create', methods=['POST'])
@cross_origin()
def create_product():
    return ProductContoller.store(request)

@app.route('/products/<int:id>', methods=['GET','PUT','DELETE'])
@cross_origin()
def handle_product(id):
    if request.method == 'GET':
       print(request.method)
       return ProductContoller.show(id)

    elif request.method == 'PUT':
       return ProductContoller.update(id, request)
   
    elif request.method == 'DELETE':
        return ProductContoller.delete(id)


@app.route('/products/price/<int:price>', methods=['GET'])
@cross_origin()
def get_prodcut_price(price):
    return ProductContoller.get_prodcut_by_price(price)

