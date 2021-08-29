from re import I
from flask import url_for
from werkzeug.utils import secure_filename

# les extensions autorisés
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_image_url(uploaded_image):
    return url_for('send_uploaded_file', filename=uploaded_image)

def check_user_type(type):
    if type=='developper':
        return type

    elif type=='seller' or type=='admin':
        return None

def generate_image(identifiant: str) -> str:    
    return 'https://i.pravatar.cc/150?u='+identifiant[0]


        