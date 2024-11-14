from app.models.tables import Aluno, Treino
from flask import Flask, Blueprint ,request, jsonify, render_template, url_for, session, redirect
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import re
import datetime
from app.controllers.restapi import token_required
from app.controllers.restapi import restapi

routes = Blueprint('routes', __name__)

@routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Recebe os dados do frontend

    # Validações
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Preencha todos os campos!'}), 400
    
    # Verifica se o usuário já existe
    if Aluno.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Nome de usuário já existe'}), 400
    
    # Cria o novo usuário
    hashed_password = generate_password_hash(data['password'])
    new_user = Aluno(username=data['username'], email=data['email'], senha=hashed_password, contato=data['contact'])

    # Adiciona no banco de dados
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuário registrado com sucesso!'}), 201


@routes.route('/', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')
    
    if not email or not senha:
        return jsonify({'message': 'Preencha todos os campos!'}), 400
    
    user = Aluno.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.senha, senha):
        return jsonify({'message': 'Credenciais inválidas!'}), 401

    token = user.gerar_token(user.id)
    return jsonify({'message': 'Usuário logado com sucesso!', 'token': token}), 200
  

# Verificar se o user ta logado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('routes.index'))
        return f(*args, **kwargs)
    return decorated_function

# Rota pra Pagina inicial
@routes.route ('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Se é pra Registro ou Login
        if 'email' in request.form: # email só está presente no registro
            fullname = request.form.get('fullname')
            username = request.form.get('username')
            cpf = request.form.get('cpf')
            email = request.form.get('email')
            senha = request.form.get('senha')
            confirm_senha = request.form.get('confirm_senha')
            contato = request.form.get('contato')

            if senha != confirm_senha:
                return jsonify({'error':'As senhas nao conferem'}), 400                      

            # Verifica se o username ou email ja existe no banco de dados
            existing_email = Aluno.query.filter_by(email=email).first()
            if existing_email:
                return jsonify({'error': 'Esse e-mail já está sendo utilizado'}), 400

            existing_user = Aluno.query.filter_by(username=username).first()
            if existing_user:
                return jsonify({'error': 'Nome de usuário já existe'}), 400
            
            # Criar novo user se as validações passarem
            hashed_password = generate_password_hash(senha)
            new_user = Aluno(username=username, fullname=fullname, cpf=cpf, email=email, senha=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id
            session['username'] = new_user.username
            return jsonify({'message': 'Usuário registrado com sucesso!'}), 201

        else:  # Se é pra Login
            username = request.form.get['username']
            senha = request.form.get['senha']
            user = Aluno.query.filter_by(username=username).first()

            # Se a senha ta correta
            if user and check_password_hash(user.senha, senha):
                session['user_id'] = user.id
                session['username'] = user.username
                return jsonify({'message': 'Login bem-sucedido!'}), 200
            else:
                return jsonify({'error': 'Usuário ou senha inválidos'}), 401
    
    else: # Se o método for GET
        return render_template('index.html')


# Rota para a página do usuário 
@routes.route('/aluno/<username>', methods=['GET', 'POST', 'PUT']) # Exige que o usuário esteja logado
def aluno(username):
    user = Aluno.query.filter_by(username=username).first_or_404()
    return render_template('aluno.html', username=username) # buscando aluno pelo username
#    return jsonify(user.to_dict()) # pra retornar um JSON


# Rota para adicionar um novo aluno via JSON (POST)
@routes.route('/user/add_alunos', methods=['POST'])
def adicionar_aluno():
    data = request.get_json()
    required_fields = ['username', 'fullname', 'cpf', 'email', 'senha']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Falta o campo {field}"}), 400

    novo_aluno = Aluno(
        username=data['username'],
        fullname=data['fullname'],
        idade=data.get('idade'), # opcional
        contato=data.get('contato', None), # opcional
        cpf=data['cpf'],
        email=data['email'],
        senha=generate_password_hash(data['senha']))
    db.session.add(novo_aluno)
    db.session.commit()
    return jsonify({"message": "Aluno adicionado com sucesso!"}), 201

#criando novo treino e associando ao aluno (current_user)
@restapi.route('/treino', methods=['POST'])
@token_required
def criar_treino(current_user):
    data = request.get_json()

    # Verificar se todos os campos necessários foram enviados
    required_fields = ['nome_treino', 'objetivo', 'intensidade']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Falta o campo {field}"}), 400

    novo_treino = Treino(
        aluno_id=current_user.id,  # Associa o treino ao usuário atual
        nome_treino=data['nome_treino'],
        objetivo=data['objetivo'],
        intensidade=data['intensidade'],
        data_inicio=datetime.now()  #usar a data atual ou enviar pelo frontend
    )
    db.session.add(novo_treino)
    db.session.commit()
    return jsonify({"message": "Treino criado com sucesso!"}), 201

# buscar todos os treinos associados ao aluno logado
@restapi.route('/treinos', methods=['GET'])
@token_required
def listar_treinos(current_user):
    treinos = Treino.query.filter_by(aluno_id=current_user.id).all()
    return jsonify([treino.to_dict() for treino in treinos])


@routes.route('/api/check-login', methods=['GET'])
def check_login():
    if 'user_id' in session:  # Verifica se o usuário está logado
        return jsonify({'loggedIn': True}), 200
    return jsonify({'loggedIn': False}), 200

@routes.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  # Remove o usuário da sessão
    return jsonify({'message': 'Logout bem-sucedido'}), 200

# Rota pra deletar um aluno DELETE
@routes.route('/alunos/<int:id>', methods=['DELETE'])
@login_required
def deletar_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    return jsonify({"message": "Aluno deletado com sucesso"}), 200




