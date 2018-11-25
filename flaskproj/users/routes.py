from flask import render_template, redirect, request, url_for, flash, Blueprint
from flask_login import current_user
from flaskproj import db, bcrypt
from flaskproj.users.forms import RegistForm, LoginForm, UpdateForm
from flaskproj.users.utils import save_image
from flaskproj.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', __name__)

@users.route('/cadastro', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistForm()
	if form.validate_on_submit():
		hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.user.data, email=form.email.data, password=hash_password)
		db.session.add(user)
		db.session.commit()
		flash('Sua conta foi criada com sucesso! Você já pode realizar um login =)', 'success')
		return redirect(url_for("main.home"))
	return render_template("register.html", titulo = "Cadastro", form = form)

@users.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash('Falha ao logar. Confirme suas informações!', 'danger')
	return render_template('login.html', titulo = 'Login', form = form)

@users.route('/logout')
def	logout():
	logout_user()
	return redirect(url_for('main.home'))


@users.route('/conta', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateForm()
	if form.validate_on_submit():
		if form.image.data:
			image_file = save_image(form.imagem.data)
			current_user.image_file = image_file
		current_user.username = form.user.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Suas informações foram atualizadas com sucesso!', 'success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.user.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='perfil_images/' + current_user.image_file)
	return render_template('account.html', titulo = 'Minha Conta', image_file = image_file, form=form)

@users.route('/user/<string:username>')
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user)\
		.order_by(Post.date_posted.desc())\
		.paginate(page=page, per_page=4)
	return render_template('user_posts.html', posts=posts, user=user)

