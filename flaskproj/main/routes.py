from flask import render_template, request, Blueprint
from flaskproj.models import Postagem

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
	pagina = request.args.get('page', 1, type=int)
	postagens = Postagem.query.order_by(Postagem.data_postagem.desc()).paginate(per_page=4, page=pagina)
	return render_template('home.html', posts = postagens, titulo = 'Home')

@main.route('/sobre')
def sobre():
	return render_template('sobre.html', titulo = 'Sobre')
