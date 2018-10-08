from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskproj import db
from flaskproj.models import Post
from flaskproj.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route('/post/novo', methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(titulo=form.title.data, conteudo=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Seu post foi criado!', 'success')
		return redirect(url_for('main.home'))
	return render_template('new_post.html', titulo='Novo Post',
		form = form, legend='Novo Post')

@posts.route('/posts/<int:post_id>')
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', titulo=post.title, post=post)

@posts.route('/posts/<int:post_id>/editar', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Seu post foi atualizado!', 'success')
		return redirect(url_for('posts.post', post_id=post.id))
	elif request.method == 'GET' :	
		form.title.data = post.titulo
		form.content.data = post.content
	return render_template('new_post.html', titulo="Editar Post",
		form=form, legend='Editar Post')

@posts.route('/posts/<int:post_id>/apagar', methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Seu post foi apagado :(', 'success')
	return redirect(url_for('main.home'))
