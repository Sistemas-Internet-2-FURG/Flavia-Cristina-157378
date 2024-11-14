from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Importando e registrando os Blueprints
from app.controllers.routes import routes
from app.controllers.restapi import restapi

app.register_blueprint(routes)
app.register_blueprint(restapi, url_prefix='/restapi')

# Importando modelos
from app.models.tables import Aluno

# Criando tabelas
with app.app_context():
    db.create_all()
