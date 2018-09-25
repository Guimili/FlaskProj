from flask import render_template, url_for, flash, redirect, request
from flaskproj import app, db, bcrypt
from flaskproj.forms import RegistForm, LoginForm
from flaskproj.models import Usuario, Postagem
from flask_login import login_user, current_user, logout_user, login_required



posts = [
	{
		'autor': 'IsQuilo',
		'titulo': 'Só uns',
		'conteudo': 'Quando 1 Xuqnimirrain, 2 não Kipsy my baby.',
		'data': '16/07/2018'
	},
	{
		'autor': 'Berg',
		'titulo': 'Post estatico',
		'conteudo': 'Entenda por que Python > All',
		'data': '17/07/2018'
	},
	{
		'autor': 'Boiiii',
		'titulo': 'Pra testar',
		'conteudo': 'Hotel Babilôbnia está em construção!',
		'data': 'Ném é data kkk'
	}
]


@app.route('/')
@app.route('/home')
def homePage():
	return render_template('home.html', posts = posts, titulo = 'Home')

@app.route('/sobre')
def sobrePage():
	return render_template('sobre.html', titulo = 'Sobre')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastroPage():
	if current_user.is_authenticated:
		return redirect(url_for('homePage'))
	form = RegistForm()
	if form.validate_on_submit():
		senha_hash = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
		usuario = Usuario(nome=form.usuario.data, email=form.email.data, senha=senha_hash)
		db.session.add(usuario)
		db.session.commit()
		flash('Sua conta foi criada com sucesso! Você já pode realizar um login =)', 'success')
		return redirect(url_for("homePage"))
	return render_template("cadastro.html", titulo = "Cadastro", form = form)

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
	if current_user.is_authenticated:
		return redirect(url_for('homePage'))
	form = LoginForm()
	if form.validate_on_submit():
		usuario = Usuario.query.filter_by(email=form.email.data).first()
		if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
			login_user(usuario, remember=form.lembrar.data)
			proxima_pagina = request.args.get('next')
			return redirect(proxima_pagina) if proxima_pagina else redirect(url_for('homePage'))
			flash('Sua conta foi acessada com sucesso! =)', 'success')
		else:
			flash('Falha ao logar. Confirme suas informações!', 'danger')
	return render_template('login.html', titulo = 'Login', form = form)

@app.route('/logout')
def	logoutPage():
	logout_user()
	return redirect(url_for('homePage'))

@app.route('/conta')
@login_required
def contaPage():
	return render_template('conta.html', titulo = 'Minha Conta')

