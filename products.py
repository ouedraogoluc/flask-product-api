from flask import Flask, jsonify , request , make_response

app = Flask(__name__)

from data import products

#route principale
@app.route('/')
def index():
   return make_response(jsonify(message = 'Bienvenue sur notre api de produit')),200

#route pour lister les produits
@app.route('/products')
def get_all_products():
   return make_response(jsonify(products = products,total = len(products)))

#route pour ajouter un produit
@app.route('/products/create', methods=['POST'])
def create_product():
    #recuperer les donnees json
    data = request.get_json()
    #creer un produit
    product = {
        'name' : data['name'],
        'price' : data['price'],
        'content' : data['content'],
        'quantity' : data['quantity'],
    }
    #ajouter le produits dans le tableau
    products.append(product)
    #retourne la response
    return make_response(jsonify(status= 'success', message='Product successfully created', product=product)),201

@app.route('/products/<int:id>', methods=['GET','PUT','DELETE'])
def handle_product(id):
   if request.method == 'GET':
       print(request.method)
       try:
           #recuperer le produit correspond
           product = products[id - 1]
           return make_response(jsonify(product= product)),200
       except IndexError:
           return make_response(jsonify(status = 'error',message='No found product')),404
   
   elif request.method == 'PUT':
        #recuperer le element correspondant
        try:
            data = request.get_json()
            product = products[int(data['id'])]
            product['name'] = data['name']
            product['price'] = data['price']
            product['content'] = data['content']
            product['quantity'] = data['quantity']
            return make_response(jsonify(status= 'success', message='Product successfully updated', product=product)),200
        except IndexError:
           return make_response(jsonify(status = 'error',message='No found product')),404
   
   elif request.method == 'DELETE':
        #recuperer le element correspondant
        try:
            data = request.get_json()
            products.pop(int(data['id']) -1 )
            return make_response(jsonify(status= 'success', message='Product successfully deleted', products=products)),200
        except IndexError:
           return make_response(jsonify(status = 'error',message='No found product')),404

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(debug=True)
