import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app, Blueprint
from app.models.tables import Aluno
from app import app


restapi = Blueprint('restapi', __name__)

@restapi.route('/gerar_token/<int:usuario_id>', methods=['GET'])
def gerar_token(usuario_id):
    payload = {
        'id': usuario_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token}), 200 #retorna o token no formato json

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token nao fornecido!'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            #token = token.split(" ")[1]  # Remove "Bearer " se estiver presente
            #decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = data['id'] # acessar o id do user que foi codificado
            current_user = Aluno.query.get(user_id)
            if not current_user is None:
                return jsonify({'message': 'Usuario nao encontrado!'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'mensagem': 'Token expirado!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'mensagem': 'Token invalido!'}), 401

        return f(*args, **kwargs)

    return decorated

@restapi.route('/treino', methods=['GET'])
@token_required
def treino():
#    treino = treino.query.all()
#    return jsonify([treino.to_dict() for treino in treino])
    treino_data = {
            "nome": "Flexão",
            "repeticoes": 15,
            "series": 3
        }
    return jsonify(treino_data)
#    return jsonify({'Flexão'})

