from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flaskproj.models import Usuario
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegistForm(FlaskForm):
    usuario = StringField("Usuario", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    confirm = PasswordField("Confirme sua senha", validators=[DataRequired(), EqualTo("senha")])
    registrar = SubmitField("Resgistrar-se")

    def validate_usuario(self, usuario):
        usuario = Usuario.query.filter_by(nome=usuario.data).first()
        if usuario:
            raise ValidationError('Usuário já existente! Por favor, escolha outro =)')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já utilizado! Por favor, escolha outro =)')


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    lembrar = BooleanField("Lembrar senha")
    login = SubmitField("Login")


class UpdateForm(FlaskForm):
    usuario = StringField("Usuario", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    imagem = FileField('Atualizar Imagem de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    atualizar = SubmitField("Atualizar")

    def validate_usuario(self, usuario):
        if usuario.data != current_user.nome:
            usuario = Usuario.query.filter_by(nome=usuario.data).first()
            if usuario:
                raise ValidationError('Usuário já existente! Por favor, escolha outro =)')

    def validate_email(self, email):
        if email.data != current_user.email:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Email já utilizado! Por favor, escolha outro =)')

class PostForm(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired()])
    conteudo = TextAreaField('Conteudo', validators=[DataRequired()])
    enviar = SubmitField('Enviar')

