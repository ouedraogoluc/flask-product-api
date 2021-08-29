from flask import Flask,send_file, jsonify , request , make_response , send_from_directory, url_for
from flask_cors import cross_origin
from flask_jwt_extended import JWTManager,jwt_required
from datetime import timedelta


# upload files dir
UPLOAD_FOLDER = 'static/uploads'

# create app
app = Flask(__name__)

# create jwt instance
jwt = JWTManager(app)

# add jwt secret key
app.config["JWT_SECRET_KEY"] = "product-flask-api" 

# add jwt access expired date
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)

# configuration de la base de donnee
app.config.from_object('config')

# secret_key for app
app.secret_key = "product_app_key"

# put upload folder to config app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# put max size of file
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

#importer les controllers
from products.controllers  import ProductContoller,UserContoller
from products.errors import *

# route principale
@app.route('/')
@cross_origin()
def index():
   return make_response(jsonify(message = 'Bienvenue sur notre api de produit')),200

@app.route('/api/v1/products', methods=['POST', 'GET'])
@cross_origin() # crossorigin autorize all client to fetch api
@jwt_required()  # protected route
def product():
    if request.method == 'GET':
        return ProductContoller().index()

    elif request.method == 'POST':
        return ProductContoller().store(request)

@app.route('/api/v1/products/<int:id>', methods=['GET','PUT','DELETE'])
@cross_origin() 
@jwt_required()
def handle_product(id):
    if request.method == 'GET':
       return ProductContoller().show(id)

    elif request.method == 'PUT':
       return ProductContoller().update(id, request)
   
    elif request.method == 'DELETE':
        return ProductContoller().delete(id)

@app.route('/api/v1/products/price/<int:price>', methods=['GET'])
@cross_origin() 
@jwt_required()
def get_prodcut_price(price):
    return ProductContoller().get_prodcut_by_price(price)

@app.route('/api/v1/products/upload/image', methods=['POST'])
@cross_origin() 
@jwt_required()
def upload_product_img():
    return ProductContoller().upload_product_image(request)


@app.route('/api/v1/products/image/<string:filename>')
@cross_origin() 
def get_product_image(filename):
    # split filename
    print(request.url_root + url_for('get_product_image', filename=filename))
    extension = filename.split('.')[1]
    # get full path
    file_path = '..//static//uploads//'+ filename
    return send_file(file_path, mimetype='image/'+ extension)

@app.route('/api/v1/products/delete', methods=['DELETE'])
@cross_origin() 
def delete_all_product():
    return ProductContoller().delete_all_product()

@app.route('/api/v1/users/delete', methods=['DELETE'])
@cross_origin() 
def delete_all_user():
    return UserContoller().delete_all_user()

@app.route('/api/v1/users', methods=['POST', 'GET'])
@cross_origin() # crossorigin autorize all client to fetch api
@jwt_required()  # protected route
def user():
    if request.method == 'GET':
        return UserContoller().index()

    elif request.method == 'POST':
        return UserContoller().store(request)

@app.route('/api/v1/users/<int:id>', methods=['GET','PUT','DELETE'])
@cross_origin() 
@jwt_required()
def handle_user(id):
    if request.method == 'GET':
       print(request.method)
       return UserContoller().show(id)
    elif request.method == 'PUT':
       return UserContoller().update(id, request)
   
    elif request.method == 'DELETE':
        return UserContoller().delete(id)

@app.route('/api/v1/login', methods=['POST'])
@cross_origin()
def get_user_authenticate():
    return UserContoller().authenticate(request)

@app.route('/api/v1/register', methods=['POST'])
@cross_origin() 
@jwt_required()
def signup():
    return UserContoller().register(request)

@app.route('/api/v1/users/<int:id>/products')
@cross_origin() 
@jwt_required() 
def get_user_products(id):
   return ProductContoller().index(id)

