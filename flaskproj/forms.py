from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistForm(FlaskForm):
    usuario = StringField("Usuario", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    confirm = PasswordField("Confirme sua senha", validators=[DataRequired(), EqualTo("senha")])
    registrar = SubmitField("Resgistrar-se")


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    lembrar = BooleanField("Lembrar senha")
    login = SubmitField("Login")


