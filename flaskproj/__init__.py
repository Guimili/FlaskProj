from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "2aa24047ca929ad7d69e91b1da76ad40"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt()
gerenciador_login = LoginManager(app)
gerenciador_login.login_view = 'login'
gerenciador_login.login_message_category = 'info'

from flaskproj import routes