from flask import jsonify, request
import os
from . import linux_user

def configure(app):
    def check_auth():
        if 'Authorization' not in request.headers:
            return jsonify(data={ 'message': 'Sem permissão para acessar.' }), 401
        token = request.headers['Authorization']
        lower = token.lower()
        
        if not lower.startswith("bearer "):
            return jsonify(data={ 'message': 'Sem permissão para acessar.' }), 401
        
        token = lower[7:]
        if token != os.environ.get("AUTHORIZATION", None):
            return jsonify(data={ 'message': 'Sem permissão para acessar.' }), 401
        
        return None

    @app.route("/verify/", methods=["POST"])
    def verify():
        auth_output = check_auth()
        if auth_output is not None:
            return auth_output
        
        if request.is_json:
            data = request.json
            if "user_name" in data:
                user_name = data["user_name"]
                if linux_user.user_already_exists(user_name):
                    return jsonify(data={'message': 'O usuário de e-mail não está disponível.'}), 400
                return jsonify(data={'message': 'O usuário de e-mail está disponível.'}), 200
                
        return jsonify(data={ 'message': 'O usuário de e-mail não foi enviado.' }), 400
    
    @app.route("/add/", methods=["POST"])
    def add():
        auth_output = check_auth()
        if auth_output is not None:
            return auth_output

        if request.is_json:
            data = request.json
            if "user_name" in data:
                user_name = data["user_name"]
                user_name = linux_user.get_unique_name(user_name)
                if not linux_user.create_mail_anonymous_user(user_name):
                    return jsonify(data={ 'message': 'Não foi possível adicionar o usuário, nosso servidor parece estar com problemas.' }), 500
                return jsonify(data={
                    'user_name': user_name
                }), 200

        return jsonify(data={'message': 'Nome de e-mail não foi enviado.'}), 400
