from flask import render_template, request, Blueprint
from flaskproj.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=4, page=page)
	return render_template('home.html', posts = posts, titulo = 'Home')

@main.route('/sobre')
def about():
	return render_template('about.html', titulo = 'Sobre')
