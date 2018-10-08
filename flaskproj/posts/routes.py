from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskproj import db
from flaskproj.models import Postagem
from flaskproj.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route('/post/novo', methods=['GET', 'POST'])
@login_required
def novo_post():
	form = PostForm()
	if form.validate_on_submit():
		postagem = Postagem(titulo=form.titulo.data, conteudo=form.conteudo.data, autor=current_user)
		db.session.add(postagem)
		db.session.commit()
		flash('Sua postagem foi criada!', 'success')
		return redirect(url_for('main.home'))
	return render_template('criar_post.html', titulo='Nova Postagem',
		form = form, legend='Nova Postagem')

@posts.route('/posts/<int:post_id>')
def post(post_id):
	post = Postagem.query.get_or_404(post_id)
	return render_template('postagem.html', titulo=post.titulo, post=post)

@posts.route('/posts/<int:post_id>/editar', methods=['GET', 'POST'])
@login_required
def post_editar(post_id):
	post = Postagem.query.get_or_404(post_id)
	if post.autor != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.titulo = form.titulo.data
		post.conteudo = form.conteudo.data
		db.session.commit()
		flash('Sua postagem foi atualizada!', 'success')
		return redirect(url_for('posts.post', post_id=post.id))
	elif request.method == 'GET' :	
		form.titulo.data = post.titulo
		form.conteudo.data = post.conteudo
	return render_template('criar_post.html', titulo="Editar Postagem",
		form=form, legend='Editar Postagem')

@posts.route('/posts/<int:post_id>/apagar', methods=['POST'])
@login_required
def post_apagar(post_id):
	post = Postagem.query.get_or_404(post_id)
	if post.autor != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Sua postagem foi apagada :(', 'success')
	return redirect(url_for('main.home'))
