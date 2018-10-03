from datetime import datetime
from flaskproj import db, gerenciador_login
from flask_login import UserMixin

@gerenciador_login.user_loader
def carrega_usuario(usuario_id):
	return Usuario.query.get(int(usuario_id))

class Usuario(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	imagem_file = db.Column(db.String(20), nullable=False, default='s.jpg')
	senha = db.Column(db.String(60), nullable=False)
	postagens = db.relationship('Postagem', backref='autor', lazy=True) 

	def __repr__(self):
		return f"Usuario('{self.nome}', '{self.email}','{self.imagem_file}')"

class Postagem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	titulo = db.Column(db.String(100), nullable=False)
	data_postagem = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	conteudo = db.Column(db.Text, nullable=False)
	usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

	def __repr__(self):
		return f"Postagem('{self.titulo}', '{self.data_postagem}')"