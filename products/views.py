from flask import Flask,send_file, jsonify , request , make_response , send_from_directory, url_for
from flask_cors import cross_origin

# upload files dir
UPLOAD_FOLDER = 'static/uploads'

# create app
app = Flask(__name__)

# configuration de la base de donnee
app.config.from_object('config')

# secret_key for app
app.secret_key = "product_app_key"

# put upload folder to config app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# put max size of file
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

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


@app.route('/products/upload/image', methods=['POST'])
@cross_origin()
def upload_product_img():
    return ProductContoller.upload_product_image(request)

# get product image
@app.route('/products/image/<string:filename>')
def get_product_image(filename):
    # split filename
    print(request.url_root + url_for('get_product_image', filename=filename))
    extension = filename.split('.')[1]
    # get full path
    file_path = '..\\static\\uploads\\'+ filename
    return send_file(file_path, mimetype='image/'+ extension)