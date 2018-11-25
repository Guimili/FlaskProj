from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Length
from flaskproj.models import User


class RegistForm(FlaskForm):
    user = StringField("Usuario", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    confirm = PasswordField("Confirme sua senha", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Resgistrar-se")

    def validate_user(self, user):
        user = User.query.filter_by(username=user.data).first()
        if user:
            raise ValidationError('Usuário já existente! Por favor, escolha outro =)')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email já utilizado! Por favor, escolha outro =)')


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    remember = BooleanField("Lembrar senha")
    submit = SubmitField("Login")


class UpdateForm(FlaskForm):
    user = StringField("Usuario", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    image = FileField('Atualizar Imagem de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Atualizar")

    def validate_user(self, user):
        if user.data != current_user.username:
            user = User.query.filter_by(username=user.data).first()
            if user:
                raise ValidationError('Usuário já existente! Por favor, escolha outro =)')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email já utilizado! Por favor, escolha outro =)')
