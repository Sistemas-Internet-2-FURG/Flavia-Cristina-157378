import os

class Config:
    SECRET_KEY = '896f373670c515c39717dafb80a4bd5d'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URL') or 'postgresql://postgres:senha@localhost/meubanco'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# ALTER USER postgres PASSWORD 'senha';
