from flask_sqlalchemy import SQLAlchemy
from app.database import db
import re


class Aluno(db.Model):
    __tablename__ = 'aluno'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    fullname = db.Column(db.String(80), nullable=False)
    idade = db.Column(db.Integer)
    _contato = db.Column("contato",db.String(20)) # Coluna interna pra contato
    _cpf = db.Column("cpf",db.String(14), nullable=False) # Coluna interna pra cpf
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    
    treinos = db.relationship('Treino', backref='aluno', lazy=True, cascade="all, delete") # cascade=all delete

    # informar o estado do objeto
    def __repr__(self):
        return f'<Aluno {self.username}>' # objeto aluno e inclui o username

    # tranformar a instancia da classe em um dicionario
    def to_dict(self):
        return {
            "id": self.id, 
            "username": self.username,
            "fullname": self.fullname, 
            "email": self.email,
            "cpf": self.cpf,
            "contato": self.contato,
            "idade": self.idade
        }

    @property
    def cpf(self):
        return re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', self._cpf)

    @property
    def contato(self):
        return re.sub(r'(\d{2})(\d{4})(\d{4})', r'(\1) \2-\3', self._contato)
    
    @contato.setter
    def contato(self, contato):
        self._contato = contato

class Exercicio(db.Model):
    __tablename__ = 'exercicios'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(200), nullable=True)

    # Relacionamento  muitos-pra-muitos entre Exercicio e Treino, com a tabela intermediaria
    treinos = db.relationship('Treino', secondary='treino_exercicio', back_populates='exercicios')

    def __repr__(self):
        return f'<Exercicio {self.name}>'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "descricao": self.descricao
        }

class Treino(db.Model):
    __tablename__ = 'treino'
    
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    nome_treino = db.Column(db.String(50), nullable=False)
    objetivo = db.Column(db.String(50))  # Ex.: Hipertrofia, emagrecimento
    data_inicio = db.Column(db.Date)
    intensidade = db.Column(db.String(50), nullable=False)  

    # Relacionamento  muitos-pra-muitos entre Treino e Exercicio, com a tabela intermediaria
    # Aluno--> Treino (um-pra-muitos), treino term varios exercicios e vice-versa
    # Um aluno tem varios treinos, quando exclui o aluno, todos os treino que tão vinculado tambem vao ser removidos
    exercicios = db.relationship('Exercicio', secondary='treino_exercicio', back_populates='treinos')

    def __repr__(self):
        return f'<Treino {self.nome_treino} do Aluno {self.aluno_id}>'

    def to_dict(self):
        return {
            "id": self.id,
            "nome_treino": self.nome_treino,
            "aluno_id": self.aluno_id,
            "intensidade": self.intensidade,
            "exercicios": [exercicio.to_dict() for exercicio in self.exercicios]
        }


# Treino --> Exercicio (muitos-pra-muitos)
# Um treino tem varios exercicios, e um exercicio tambem pode pertencer a varios treinos

# criar tabela sem associação a um modelo de classe, definido em treino e exercicio relação de muitos-pra-muitos
treino_exercicio = db.Table('treino_exercicio', # tabela intermediaria
    db.Column('treino_id', db.Integer, db.ForeignKey('treino.id'), primary_key=True),
    db.Column('exercicio_id', db.Integer, db.ForeignKey('exercicio.id'), primary_key=True)
)

# Um Aluno pode ter vários Treinos, mas cada Treino pertence só a um Aluno
# Um Treino pode ter vários Exercícios, e cada Exercício pode pertencer a vários Treinos