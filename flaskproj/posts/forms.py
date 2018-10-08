from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired 


class PostForm(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired()])
    conteudo = TextAreaField('Conteudo', validators=[DataRequired()])
    enviar = SubmitField('Enviar')
    