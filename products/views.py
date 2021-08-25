from flask import Flask,send_file, jsonify , request , make_response , send_from_directory, url_for
from flask_cors import cross_origin
from flask_jwt_extended import JWTManager,jwt_required
from datetime import timedelta
# upload files dir
UPLOAD_FOLDER = 'static/uploads'

# create app
app = Flask(__name__)

jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "product-flask-api" 

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)
# configuration de la base de donnee
app.config.from_object('config')


# secret_key for app
app.secret_key = "product_app_key"

# put upload folder to config app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# put max size of file
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

#importer le controller
from products.controllers  import ProductContoller,UserContoller
#importer le controller user

# route principale
@app.route('/')
@cross_origin()
def index():
   return make_response(jsonify(message = 'Bienvenue sur notre api de produit')),200

#route pour lister les produits

@app.route('/products')
@cross_origin()
@jwt_required()
def get_all_products():
   return ProductContoller.index()

#route pour ajouter un produit
@app.route('/products/create', methods=['POST'])
@cross_origin()
@jwt_required()
def create_product():
    return ProductContoller.store(request)

@app.route('/products/<int:id>', methods=['GET','PUT','DELETE'])
@cross_origin()
@jwt_required()
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
@jwt_required()
def get_prodcut_price(price):
    return ProductContoller.get_prodcut_by_price(price)


@app.route('/products/upload/image', methods=['POST'])
@cross_origin()
@jwt_required()
def upload_product_img():
    return ProductContoller.upload_product_image(request)

# get product image
@app.route('/products/image/<string:filename>')
def get_product_image(filename):
    # split filename
    print(request.url_root + url_for('get_product_image', filename=filename))
    extension = filename.split('.')[1]
    # get full path
    file_path = '../static/upload'+ filename
    return send_file(file_path, mimetype='image/'+ extension)

#--------------------------------user view------------------------------------------------------

@app.route('/users')
@cross_origin()
@jwt_required()
def get_all_users():
   return UserContoller.index()

#route pour ajouter un user
@app.route('/users/create', methods=['POST'])
@cross_origin()
@jwt_required()
def create_user():
    return UserContoller.store(request)

@app.route('/users/<int:id>', methods=['GET','PUT','DELETE'])
@cross_origin()
@jwt_required()
def handle_user(id):
    if request.method == 'GET':
       print(request.method)
       return UserContoller.show(id)
    elif request.method == 'PUT':
       return UserContoller.update(id, request)
   
    elif request.method == 'DELETE':
        return UserContoller.delete(id)

@app.route('/users/email/<int:email>', methods=['GET'])
@cross_origin()
@jwt_required()
def get_user_email(email):
    return UserContoller.get_user_by_email(email)


@app.route('/users/upload/image', methods=['POST'])
@cross_origin()
@jwt_required()
def upload_user_img():
    return UserContoller.upload_user_image(request)

# get product image
@app.route('/users/image/<string:filename>')
@cross_origin()
@jwt_required()
def get_user_image(filename):
    # split filename
    print(request.url_root + url_for('get_user_image', filename=filename))
    extension = filename.split('.')[1]
    # get full path
    file_path = '../static/upload'+ filename
    return send_file(file_path, mimetype='image/'+ extension)

@app.route('/users/login', methods=['POST'])
def get_user_authenticate():
    return UserContoller.authenticate(request)
    