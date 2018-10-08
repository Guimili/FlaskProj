from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskproj.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
gerenciador_login = LoginManager()
gerenciador_login.login_view = 'users.login'
gerenciador_login.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    gerenciador_login.init_app(app)
    
    from flaskproj.usuarios.routes import users
    from flaskproj.posts.routes import posts
    from flaskproj.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app