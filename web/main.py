from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistForm, LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "2aa24047ca929ad7d69e91b1da76ad40"

posts = [
	{
		'autor': 'IsQuilo',
		'titulo': 'Quem vê, pensa',
		'conteudo': 'Quando 1 Xuqnimirrain, 2 não Kipsy my baby.',
		'data': '16/07/2018'
	},
	{
		'autor': 'MeuZovo',
		'titulo': 'Que eu sei oq to fazendo',
		'conteudo': 'Entenda por que Python > Java',
		'data': '17/07/2018'
	},
	{
		'autor': 'Boiiii',
		'titulo': 'Mal sabe, coitado.',
		'conteudo': 'Hotel Babilôbnia está em construção!',
		'data': '18/07/2099'
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
	form = RegistForm()
	if form.validate_on_submit():
		flash(f'Conta criada com sucesso para {form.usuario.data}!', 'success')
		return redirect(url_for("homePage"))
	return render_template("cadastro.html", titulo = "Cadastro", form = form)

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'admin@blog.com' and form.senha.data == 'senha':
			flash(f'Você entrou em sua conta!', 'success')
			return redirect(url_for('homePage'))
		else:
			flash('Falha ao logar. Confirme suas informações!', 'danger')
	return render_template('login.html', titulo = 'Login', form = form)

if __name__ == "__main__":
	app.run(debug = True)
