from flask import Flask , jsonify, make_response
from products.views import app

@app.errorhandler(404)
def not_found(error):
    print(error)
    return make_response(jsonify(message="Ressource not found")), 404


@app.errorhandler(500)
def error_server(error):
    print(error)
    return make_response(jsonify(message="Error du serveur")), 404


@app.errorhandler(401)
def not_authorize(error):
    print(error)
    return make_response(jsonify(message="Forbidden Authorization required")), 401


@app.errorhandler(405)
def not_allow(error):
    print(error)
    return make_response(jsonify(message="Method not allowed")), 405

    
