import secrets, os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskproj import app, db, bcrypt
from flaskproj.forms import RegistForm, LoginForm, PostForm, UpdateForm
from flaskproj.models import Usuario, Postagem
from flask_login import login_user, current_user, logout_user, login_required


# posts = [
# 	{
# 		'autor': 'IsQuilo',
# 		'titulo': 'Só uns',
# 		'conteudo': 'Quando 1 Xuqnimirrain, 2 não Kipsy my baby.',
# 		'data': '16/07/2018'
# 	},
# 	{
# 		'autor': 'Berg',
# 		'titulo': 'Post estatico',
# 		'conteudo': 'Entenda por que Python > All',
# 		'data': '17/07/2018'
# 	},
# 	{
# 		'autor': 'Boiiii',
# 		'titulo': 'Pra testar',
# 		'conteudo': 'Hotel Babilôbnia está em construção!',
# 		'data': 'Ném é data kkk'
# 	}
# ]


@app.route('/')
@app.route('/home')
def home():
	postagens = Postagem.query.all()
	return render_template('home.html', posts = postagens, titulo = 'Home')

@app.route('/sobre')
def sobre():
	return render_template('sobre.html', titulo = 'Sobre')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistForm()
	if form.validate_on_submit():
		senha_hash = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
		usuario = Usuario(nome=form.usuario.data, email=form.email.data, senha=senha_hash)
		db.session.add(usuario)
		db.session.commit()
		flash('Sua conta foi criada com sucesso! Você já pode realizar um login =)', 'success')
		return redirect(url_for("home"))
	return render_template("cadastro.html", titulo = "Cadastro", form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		usuario = Usuario.query.filter_by(email=form.email.data).first()
		if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
			login_user(usuario, remember=form.lembrar.data)
			proxima_pagina = request.args.get('next')
			return redirect(proxima_pagina) if proxima_pagina else redirect(url_for('home'))
		else:
			flash('Falha ao logar. Confirme suas informações!', 'danger')
	return render_template('login.html', titulo = 'Login', form = form)

@app.route('/logout')
def	logout():
	logout_user()
	return redirect(url_for('home'))

def salvar_imagem(form_imagem):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_imagem.filename)
	imagem_nome = random_hex + f_ext
	imagem_path = os.path.join(app.root_path, 'static/imagens_perfil', imagem_nome)
	
	dimensao = (125, 125)
	i = Image.open(form_imagem)
	i.thumbnail(dimensao)
	i.save(imagem_path)
	
	return imagem_nome

@app.route('/conta', methods=['GET', 'POST'])
@login_required
def conta():
	form = UpdateForm()
	if form.validate_on_submit():
		if form.imagem.data:
			imagem_arquivo = salvar_imagem(form.imagem.data)
			current_user.imagem_file = imagem_arquivo
		current_user.nome = form.usuario.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Suas informações foram atualizadas com sucesso!', 'success')
		return redirect(url_for('conta'))
	elif request.method == 'GET':
		form.usuario.data = current_user.nome
		form.email.data = current_user.email
	imagem_file = url_for('static', filename='imagens_perfil/' + current_user.imagem_file)
	return render_template('conta.html', titulo = 'Minha Conta', imagem_file = imagem_file, form=form)

@app.route('/post/novo', methods=['GET', 'POST'])
@login_required
def novo_post():
	form = PostForm()
	if form.validate_on_submit():
		postagem = Postagem(titulo=form.titulo.data, conteudo=form.conteudo.data, autor=current_user)
		db.session.add(postagem)
		db.session.commit()
		flash('Sua postagem foi criada!', 'success')
		return redirect(url_for('home'))
	return render_template('criar_post.html', titulo='Nova Postagem', form = form)
