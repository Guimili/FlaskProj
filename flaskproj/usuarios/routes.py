from flask import render_template, redirect, request, url_for, flash, Blueprint
from flask_login import current_user
from flaskproj import db, bcrypt
from flaskproj.usuarios.forms import RegistForm, LoginForm, UpdateForm
from flaskproj.usuarios.utils import salvar_imagem
from flaskproj.models import Usuario, Postagem
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', __name__)

@users.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistForm()
	if form.validate_on_submit():
		senha_hash = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
		usuario = Usuario(nome=form.usuario.data, email=form.email.data, senha=senha_hash)
		db.session.add(usuario)
		db.session.commit()
		flash('Sua conta foi criada com sucesso! Você já pode realizar um login =)', 'success')
		return redirect(url_for("main.home"))
	return render_template("cadastro.html", titulo = "Cadastro", form = form)

@users.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		usuario = Usuario.query.filter_by(email=form.email.data).first()
		if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
			login_user(usuario, remember=form.lembrar.data)
			proxima_pagina = request.args.get('next')
			return redirect(proxima_pagina) if proxima_pagina else redirect(url_for('main.home'))
		else:
			flash('Falha ao logar. Confirme suas informações!', 'danger')
	return render_template('login.html', titulo = 'Login', form = form)

@users.route('/logout')
def	logout():
	logout_user()
	return redirect(url_for('main.home'))


@users.route('/conta', methods=['GET', 'POST'])
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
		return redirect(url_for('users.conta'))
	elif request.method == 'GET':
		form.usuario.data = current_user.nome
		form.email.data = current_user.email
	imagem_file = url_for('static', filename='imagens_perfil/' + current_user.imagem_file)
	return render_template('conta.html', titulo = 'Minha Conta', imagem_file = imagem_file, form=form)

@users.route('/user/<string:username>')
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	usuario = Usuario.query.filter_by(nome=username).first_or_404()
	posts = Postagem.query.filter_by(autor=usuario)\
		.order_by(Postagem.data_postagem.desc())\
		.paginate(page=page, per_page=4)
	return render_template('user_posts.html', posts=posts, user=usuario)

